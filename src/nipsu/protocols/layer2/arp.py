import socket
from ctypes import Array, c_ubyte, c_uint8, c_uint16
from typing import TYPE_CHECKING, Any, Dict, Sequence, Tuple, Type, Union

from nipsu.protocols.base import Protocol
from nipsu.protocols.layer2.ethernet import ETHERTYPES

if TYPE_CHECKING:
    from ctypes import _CData


class ARP(Protocol):
    _fields_: Sequence[Union[Tuple[str, Type["_CData"]], Tuple[str, Type["_CData"], int]]] = [
        ("htype", c_uint16),
        ("ptype", c_uint16),
        ("hlen", c_uint8),
        ("plen", c_uint8),
        ("oper", c_uint16),
        ("sha", c_ubyte * 6),
        ("spa", c_ubyte * 4),
        ("tha", c_ubyte * 6),
        ("tpa", c_ubyte * 4),
    ]
    header_len: int = 28
    hardware_types: Dict[int, str] = {
        1: "Ethernet",
        6: "IEEE 802 Networks",
        7: "ARCNET",
        15: "Frame Relay",
        16: "ATM",
        17: "HDLC",
        18: "Fibre Channel",
        19: "ATM",
        20: "Serial Line",
        21: "ATM",
        31: "IPsec tunnel",
    }
    protocol_types: Dict[int, str] = ETHERTYPES
    operations: Dict[int, str] = {
        1: "ARP request",
        2: "ARP reply",
        3: "RARP request",
        4: "RARP reply",
        5: "DRARP request",
        6: "DRARP reply",
        7: "DRARP error",
        8: "InARP request",
        9: "InARP reply",
    }

    @property
    def htype_str(self) -> str:
        return self.hardware_types.get(self.htype, f"Unsupported: {self.htype}")

    @property
    def ptype_str(self) -> str:
        return self.protocol_types.get(self.ptype, f"Unsupported: {self.ptype}")

    @property
    def oper_str(self) -> str:
        return self.operations.get(self.oper, f"Unsupported: {self.oper}")

    def proto_addr(self, addr_arr: Array) -> str:
        if self.ptype_str == "IPv4":
            return self.array_to_proto_addr(addr_arr, socket.AF_INET)
        elif self.ptype_str == "IPv6":
            return self.array_to_proto_addr(addr_arr, socket.AF_INET6)
        else:
            return self.array_to_proto_addr(addr_arr)

    def show(self) -> Dict[str, Any]:
        return {
            "Hardware type": self.htype_str,
            "Protocol type": self.ptype_str,
            "Hardware length": self.hlen,
            "Protocol length": self.plen,
            "Operation": self.oper_str,
            "Sender hardware address": self.colon_hex_notation(self.sha),
            "Sender protocol address": self.proto_addr(self.spa),
            "Target hardware address": self.colon_hex_notation(self.tha),
            "Target protocol address": self.proto_addr(self.tpa),
        }
