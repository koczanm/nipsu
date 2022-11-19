from ctypes import c_uint16
from typing import TYPE_CHECKING, Any, Dict, Sequence, Tuple, Type, Union

from nipsu.protocols.base import Protocol

if TYPE_CHECKING:
    from ctypes import _CData


class UDP(Protocol):
    _fields_: Sequence[Union[Tuple[str, Type["_CData"]], Tuple[str, Type["_CData"], int]]] = [
        ("src_port", c_uint16),
        ("dst_port", c_uint16),
        ("length", c_uint16),
        ("checksum", c_uint16),
    ]
    header_len: int = 8

    def show(self) -> Dict[str, Any]:
        return {
            "Source port": self.src_port,
            "Destination port": self.dst_port,
            "Length": self.length,
            "Checksum": self.cdata_to_hex_str(self.checksum),
        }
