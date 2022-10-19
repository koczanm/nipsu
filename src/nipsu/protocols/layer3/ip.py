import socket
from ctypes import c_ubyte, c_uint8, c_uint16, c_uint32
from typing import TYPE_CHECKING, Dict, Optional, Sequence, Tuple, Type, Union

from nipsu.protocols.base import JSONType, Protocol

if TYPE_CHECKING:
    from ctypes import _CData


class IP:
    proto_nums: Dict[int, str] = {
        1: "ICMP",
        6: "TCP",
        17: "UDP",
        44: "IPv6-Frag",
        137: "MPLS-in-IP",
    }
    service_classes: Dict[int, str] = {
        0: "Standard",
        8: "Low-priority data",
        10: "High-throughput data",
        12: "High-throughput data",
        14: "High-throughput data",
        16: "Network operations, administration and management",
        18: "Low-latency data",
        20: "Low-latency data",
        22: "Low-latency data",
        24: "Broadcast video",
        26: "Multimedia streaming",
        28: "Multimedia streaming",
        30: "Multimedia streaming",
        32: "Real-time interactive",
        34: "Multimedia conferencing",
        36: "Multimedia conferencing",
        38: "Multimedia conferencing",
        40: "Signaling",
        46: "Telephony",
        48: "Network control",
        56: "Reserved for future use",
    }
    ecn_codes: Dict[int, str] = {
        0b00: "Non ECN-Capable Transport",
        0b10: "ECN Capable Transport",
        0b01: "ECN Capable Transport",
        0b11: "Congestion Encountered",
    }


class IPv4(IP, Protocol):
    _fields_: Sequence[Union[Tuple[str, Type["_CData"]], Tuple[str, Type["_CData"], int]]] = [
        ("version", c_uint8, 4),
        ("ihl", c_uint8, 4),  # TODO: support the options field if ihl > 5
        ("dscp", c_uint8, 6),
        ("ecn", c_uint8, 2),
        ("length", c_uint16),
        ("id", c_uint16),
        ("flags", c_uint16, 3),
        ("offset", c_uint16, 13),
        ("ttl", c_uint8),
        ("proto", c_uint8),
        ("checksum", c_uint16),
        ("src_addr", c_ubyte * 4),
        ("dst_addr", c_ubyte * 4),
    ]
    header_len: int = 20
    flag_codes: Dict[int, str] = {
        0b000: "Not set",
        0b010: "Don't fragment",
        0b001: "More fragments",
    }

    @property
    def encap_proto(self) -> str:
        return self.proto_nums.get(self.proto, f"Unsupported: {self.proto}")

    @property
    def service_class(self) -> Optional[str]:
        return self.service_classes.get(self.dscp)

    @property
    def ecn_str(self) -> str:
        return self.ecn_codes.get(self.ecn, "Invalid")

    @property
    def flags_str(self) -> str:
        return self.flag_codes.get(self.flags, "Invalid")

    def describe(self) -> JSONType:
        return {
            "Version": self.version,
            "IHL": self.ihl,
            "DCSP": f"{self.dscp}: {self.service_class}",
            "ECN": self.ecn_str,
            "Total length": self.length,
            "Identifications": self.id,
            "Flags": self.flags_str,
            "Fragment offset": self.offset,
            "TTL": self.ttl,
            "Protocol": self.encap_proto,
            "Header checksum": self.cdata_to_hex_str(self.checksum),
            "Source address": self.array_to_proto_addr(self.src_addr, socket.AF_INET),
            "Destination address": self.array_to_proto_addr(self.dst_addr, socket.AF_INET),
        }


class IPv6(IP, Protocol):
    _fields_: Sequence[Union[Tuple[str, Type["_CData"]], Tuple[str, Type["_CData"], int]]] = [
        ("version", c_uint32, 4),
        ("traffic_cls", c_uint32, 8),
        ("flow_label", c_uint32, 20),
        ("length", c_uint16),
        ("next_header", c_uint8),
        ("hop_limit", c_uint8),
        ("src_addr", c_ubyte * 16),
        ("dst_addr", c_ubyte * 16),
    ]
    header_len = 40

    @property
    def encap_proto(self) -> str:
        return self.proto_nums.get(self.next_header, f"Unsupported: {self.next_header}")

    @property
    def dscp(self) -> int:
        first_6_bits = bin(self.traffic_cls)[2:8]  # skip "0b" prefix
        return int(first_6_bits, 2)

    @property
    def ecn(self) -> int:
        last_2_bits = bin(self.traffic_cls)[-2:]
        return int(last_2_bits, 2)

    @property
    def service_class(self) -> Optional[str]:
        return self.service_classes.get(self.dscp)

    @property
    def ecn_str(self) -> str:
        return self.ecn_codes.get(self.ecn, "Invalid")

    def describe(self) -> JSONType:
        return {
            "Version": self.version,
            "Traffic class": {
                "DSCP": f"{self.dscp}: {self.service_class}",
                "ECN": self.ecn_str,
            },
            "Flow label": self.flow_label,
            "Payload length": self.length,
            "Next header": self.encap_proto,
            "Hop limit": self.hop_limit,
            "Source address": self.array_to_proto_addr(self.src_addr, socket.AF_INET6),
            "Destination address": self.array_to_proto_addr(self.dst_addr, socket.AF_INET6),
        }
