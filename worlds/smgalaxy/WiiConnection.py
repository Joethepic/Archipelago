import asyncio
from enum import IntEnum
from io import BytesIO
from typing import BinaryIO, ClassVar

from wiithon import BinaryReader, BinaryWriter


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


    def __init__(self, packet_type: PacketType, data: bytes = b''):
        self.packet_type = packet_type
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
                size = StarPacket.size
            case _:
                size = APPacket.size + len(self.data)
                writer.raw(self.data)

        packet_end = writer.tell()

        writer.seek(packet_start)
        writer.u16(size)

        writer.seek(packet_end)



class StarPacket(APPacket):
    size: ClassVar[int] = APPacket.size + 4 + 1 + 1
    star_type: StarType
    galaxy_id: int
    scenario_id: int


    def __init__(self, star_type: StarType, galaxy_id: int = 0, scenario_id: int = 0):
        super().__init__(PacketType.Star)

        self.star_type = star_type
        self.galaxy_id = galaxy_id
        self.scenario_id = scenario_id


    @classmethod
    def read(cls, stream: BinaryIO) -> "StarPacket":
        reader = BinaryReader(stream)

        star_type = reader.u32()
        galaxy_id = reader.u8()
        scenario_id = reader.u8()

        return StarPacket(StarType(star_type), galaxy_id, scenario_id)


    def write(self, stream: BinaryIO) -> None:
        super().write(stream)

        writer = BinaryWriter(stream)

        writer.u32(self.star_type)
        writer.u8(self.galaxy_id)
        writer.u8(self.scenario_id)


class WiiConnection:
    is_connected: bool
    server: asyncio.Server
    recv_buffer: list[APPacket]
    send_buffer: list[APPacket]


    def __init__(self):
        self.is_connected = False
        self.server = None
        self.recv_buffer = []
        self.send_buffer = []


    async def open(self, host: str, port: str) -> None:
        self.server = await asyncio.start_server(self.update, host, port)


    async def update(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        self.is_connected = True

        while self.is_connected:
            async def recv(reader: asyncio.StreamReader) -> APPacket:
                data = await reader.readexactly(2)
                size = int.from_bytes(data, "big") - 2
                data += await reader.readexactly(size)

                stream = BytesIO(data)
                packet = APPacket.read(stream)
                return packet
            
            async def send(writer: asyncio.StreamWriter, packet: APPacket) -> None:
                stream = BytesIO()
                packet.write(stream)

                writer.write(stream.getvalue())
                await writer.drain()

            try:
                packet = await asyncio.wait_for(recv(reader), 1.0)

                if packet:
                    print(f"Received: {packet}")
                    self.recv_buffer.append(packet)
            except asyncio.IncompleteReadError as error:
                if error.expected != 2:
                    raise ValueError(f"Something went wrong when reading a data packet. Expected to read {error.expected} bytes, got {error.partial} instead.")
            except TimeoutError:
                pass
            except Exception as error:
                print(f"Receive error ({type(error).__name__}): {error}")

            try:
                if self.send_buffer:
                    packet = self.send_buffer[0]
                    await send(writer, packet)
                    
                    print(f"Sent: {packet}")

                    self.send_buffer.pop(0)
            except Exception as error:
                print(f"Send error ({type(error).__name__}): {error}")

            await asyncio.sleep(1.0)


    def receive(self) -> APPacket | None:
        if self.recv_buffer:
            return self.recv_buffer.pop(0)
        return None


    def send(self, packet: APPacket) -> None:
        self.send_buffer.append(packet)


    async def close(self):
        if self.server:
            await self.server.wait_closed()

        self.is_connected = False
