import asyncio
from enum import IntEnum
from io import BytesIO
import socket
from typing import BinaryIO, ClassVar, Optional

from attr import dataclass
from wiithon import BinaryReader, BinaryWriter
from wiithon.binary.align import align

PACKET_ALIGNMENT = 4
BASE_PACKET_SIZE = 8
PACKET_BUFFER = BASE_PACKET_SIZE * 2 * 32

class Status(IntEnum):
    DISCONNECTED = 1
    LISTENING = 2
    CONNECTING = 3
    CONNECTED = 4
    RECEIVING = 5
    SENDING = 6


class PacketType(IntEnum):
    NULL = 0
    Sync = 1
    Star = 2
    Deathlink = 3
    Lives = 4


class StarType(IntEnum):
    PowerStar = 0
    GrandStar = 1
    GreenStar = 2


class APPacket:
    size: ClassVar[int] = 2 + 2 + 4
    packet_type: PacketType
    data: bytes


    def __init__(self, packet_type: PacketType, data: bytes = None):
        self.packet_type = packet_type

        if data is None:
            self.data = b''
        else:
            self.data = data


    @classmethod
    def read(cls, stream: BinaryIO) -> "APPacket":
        reader = BinaryReader(stream)

        size = reader.u16()
        reader.skip(2)
        packet_type = PacketType(reader.u32())

        match packet_type:
            case PacketType.Star:
                return StarPacket.read(stream)
            case _:
                data = reader.raw(size - APPacket.size)
                return APPacket(packet_type, data)

    
    def write(self, stream: BinaryIO) -> None:
        writer = BinaryWriter(stream)

        packet_start = writer.tell()

        writer.u16(0) # write the size later
        writer.pad(2)
        writer.u32(self.packet_type)

        match self.packet_type:
            case PacketType.Star:
                size = align(StarPacket.size, PACKET_ALIGNMENT)
                StarPacket.write(writer.stream)
            case _:
                size = align(APPacket.size + len(self.data), PACKET_ALIGNMENT)
                writer.raw(self.data)

        packet_end = writer.tell()

        writer.seek(packet_start)
        writer.u16(size)

        writer.seek(packet_end)



@dataclass
class StarPacket:
    size: ClassVar[int] = APPacket.size + 4 + 1 + 1
    star_type: StarType
    galaxy_id: Optional[int]
    scenario_id: Optional[int]


    @classmethod
    def read(cls, stream: BinaryIO) -> "StarPacket":
        reader = BinaryReader(stream)

        star_type = reader.u32()
        galaxy_id = reader.u8()
        scenario_id = reader.u8()

        return StarPacket(PacketType.Star, b'', StarType(star_type), galaxy_id, scenario_id)


    def write(self, stream: BinaryIO) -> None:
        writer = BinaryWriter(stream)

        writer.u32(self.star_type)

        if self.galaxy_id is None:
            writer.pad(1)
        else:
            writer.u8(self.galaxy_id)
        
        if self.scenario_id is None:
            writer.pad(1)
        else:
            writer.u8(self.scenario_id)


class WiiConnection:
    status: Status
    server: socket.socket
    connection: socket.socket
    send_buffer: list[APPacket]


    def __init__(self):
        self.status = Status.DISCONNECTED
        self.server = None
        self.connection = None
        self.send_buffer = []


    def open(self, host: str, port: str) -> None:
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((host, port))
        self.server.listen(1)
        
        self.status = Status.LISTENING


    async def connect(self) -> bool:
        self.status = Status.CONNECTING

        self.connection, _ = await asyncio.to_thread(self.server.accept)

        self.status = Status.CONNECTED
        
        return True


    async def receive(self) -> list[APPacket]:
        if self.status != Status.CONNECTED:
            return []

        self.status = Status.RECEIVING

        data = await asyncio.to_thread(self.connection.recv, PACKET_BUFFER)

        self.status = Status.CONNECTED
        
        if not data:
            return []

        stream = BytesIO(data)

        packets: list[APPacket] = []
        while stream.tell() != len(data):
            packet = APPacket.read(stream)
            packets.append(packet)
        return packets

        
    async def send(self, packet: APPacket) -> None:
        self.send_buffer.append(packet)

        if self.status != Status.CONNECTED or self.status != Status.RECEIVING:
            return

        self.status = Status.SENDING

        stream = BytesIO()
        for packet in self.send_buffer:
            packet.write(stream)

        self.connection.send(stream.getvalue())

        self.status = Status.CONNECTED


    def is_connected(self) -> bool:
        return self.status == Status.CONNECTED
    

    def close(self):
        self.connection.close()
        self.server.close()

        self.status = Status.DISCONNECTED
