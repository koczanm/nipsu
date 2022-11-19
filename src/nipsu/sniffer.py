import datetime
import itertools
import logging
from typing import Iterator, Optional, Tuple, Type

import pcap

import nipsu.protocols
from nipsu.packet import Packet
from nipsu.protocols import is_supported_protocol
from nipsu.protocols.base import Protocol

logger = logging.getLogger(__name__)


class FrameInfo:
    id_iter: Iterator = itertools.count()

    def __init__(self, ts: float, packet: Packet):
        self.id = next(FrameInfo.id_iter)
        self.ts = datetime.datetime.fromtimestamp(ts)
        self.packet = packet


class Decoder:
    @staticmethod
    def decode_packet(data: Tuple[float, bytes]) -> FrameInfo:
        ts, raw_packet = data
        idx = 0
        protocols = []
        next_proto: Optional[str] = "Ethernet"
        while next_proto:
            if not is_supported_protocol(next_proto):
                logger.warning("Unsupported protocol: %s", next_proto)
                break
            proto_cls: Type[Protocol] = getattr(nipsu.protocols, next_proto)
            proto = proto_cls.decode(raw_packet[idx:])
            protocols.append(proto)
            next_proto = proto.encap_proto
            idx += proto.header_len
        return FrameInfo(ts, Packet(*protocols))


class Sniffer:
    def __init__(self, interface: str) -> None:
        self.interface = interface

    def listen(self) -> Iterator[FrameInfo]:
        for data in pcap.pcap(name=self.interface, immediate=True):
            try:
                yield Decoder.decode_packet(data)
            except Exception:
                continue
