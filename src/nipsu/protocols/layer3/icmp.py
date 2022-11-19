from ctypes import c_ubyte, c_uint8, c_uint16
from typing import TYPE_CHECKING, Any, Dict, Sequence, Tuple, Type, Union

from nipsu.protocols.base import Protocol

if TYPE_CHECKING:
    from ctypes import _CData


class ICMP(Protocol):
    _fields_: Sequence[Union[Tuple[str, Type["_CData"]], Tuple[str, Type["_CData"], int]]] = [
        ("type", c_uint8),
        ("code", c_uint8),
        ("checksum", c_uint16),
        ("rest", c_ubyte * 4),
    ]
    header_len: int = 8
    imcp_types: Dict[int, str] = {
        0: "Echo Reply",
        3: "Destination Unreachable",
        4: "Source Quench (Deprecated)",
        5: "Redirect",
        6: "Alternate Host Address (Deprecated)",
        8: "Echo",
        9: "Router Advertisement",
        10: "Router Solicitation",
        11: "Time Exceeded",
        12: "Parameter Problem",
    }

    @property
    def type_str(self) -> str:
        return self.imcp_types.get(self.type, "Unassigned")

    def show(self) -> Dict[str, Any]:
        return {
            "Type": f"{self.type}: {self.type_str}",
            "Code": self.code,
            "Checksum": self.cdata_to_hex_str(self.checksum),
            # "Rest of header": self.rest,
        }
