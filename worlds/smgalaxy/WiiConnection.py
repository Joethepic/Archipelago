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


    def open(self, host: str, port: str) -> None:
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((host, port))
        self.server.listen(1)
        
        self.status = Status.LISTENING


    async def connect(self) -> bool:
        if self.status != Status.LISTENING or self.status == Status.CONNECTING:
            return False

        if self.status == Status.CONNECTED:
            return True
        
        self.status = Status.CONNECTING

        self.connection, _ = self.server.accept()

        self.status = Status.CONNECTED

        return True


    async def receive(self) -> list[APPacket] | None:
        if self.status != Status.CONNECTED:
            return None

        self.status = Status.RECEIVING

        data = self.connection.recv(PACKET_SIZE * PACKET_BUFFER)

        self.status = Status.CONNECTED

        if (remainder := data % PACKET_SIZE) != 0:
            raise ValueError(f"Encountered an issue while receiving packets. Received {int(100 * remainder / PACKET_SIZE)}% of a packet.")
        
        stream = BinaryIO(data)

        packets: list[APPacket] = []
        for i in range(int(data / PACKET_SIZE)):
            packets[i] = APPacket.unpack(stream)

        return packets
        
    async def send(self, packets: APPacket) -> None:
        self.send_buffer.append(packets)

        if self.status != Status.CONNECTED:
            return

        self.status = Status.SENDING

        while not self.send_buffer is None:
            self.connection.send(self.send_buffer[0].pack())

        self.status = Status.CONNECTED


    def is_connected(self) -> bool:
        return self.status == Status.CONNECTED
    

    def close(self):
        self.connection.close()
        self.server.close()

        self.status = Status.DISCONNECTED
