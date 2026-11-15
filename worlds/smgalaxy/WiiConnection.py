import asyncio
from enum import IntEnum
import socket
from typing import BinaryIO

from attr import dataclass
from wiithon import BinaryReader

PACKET_SIZE = 4
PACKET_BUFFER = 32

class Status(IntEnum):
    DISCONNECTED = 1
    LISTENING = 2
    CONNECTING = 3
    CONNECTED = 4
    RECEIVING = 5
    SENDING = 6


class PacketType(IntEnum):
    NULL = 0
    PowerStar = 1
    GrandStar = 2
    GreenStar = 3
    Deathlink = 4
    Lives = 5


@dataclass
class APPacket:
    packet_type: PacketType
    data: int

    @classmethod
    def unpack(cls, stream: BinaryIO) -> "APPacket":
        reader = BinaryReader(stream)

        packet_type = PacketType(reader.u8())
        reader.skip(1)
        data = reader.u16()

        return cls(packet_type, data)


    def pack(self) -> bytes:
        out = b''

        out += self.packet_type.to_bytes()
        out += b'\x00'
        out += self.data.to_bytes(2)

        return out


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
        self.connection.settimeout(0.0)

        self.status = Status.CONNECTED
        
        return True


    async def receive(self) -> list[APPacket]:
        if self.status != Status.CONNECTED:
            return []

        self.status = Status.RECEIVING

        data = self.connection.recv(PACKET_SIZE * PACKET_BUFFER)

        self.status = Status.CONNECTED
        
        if not data:
            return []

        if (remainder := len(data) % PACKET_SIZE) != 0:
            raise ValueError(f"Encountered an issue while receiving packets. Received {int(100 * remainder / PACKET_SIZE)}% of a packet.")
        
        stream = BinaryIO(data)

        packet_count = int(len(data) / PACKET_SIZE)
        packets: list[APPacket] = [APPacket.unpack(stream) for i in range(packet_count)]

        return packets
        
    async def send(self, packets: APPacket) -> None:
        self.send_buffer.append(packets)

        if self.status != Status.CONNECTED:
            return

        self.status = Status.SENDING

        self.send_buffer.append(APPacket(PacketType.NULL), 0)

        packed_packets = b''.join([packet.pack() for packet in self.send_buffer])
        self.connection.send(packed_packets)

        self.status = Status.CONNECTED


    def is_connected(self) -> bool:
        return self.status == Status.CONNECTED
    

    def close(self):
        self.connection.close()
        self.server.close()

        self.status = Status.DISCONNECTED
