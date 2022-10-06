from ctypes import c_ubyte, c_uint8, c_uint16, c_uint32
from typing import TYPE_CHECKING, Sequence

from nipsu.protocols.base import Protocol

if TYPE_CHECKING:
    from ctypes import _CData


class TCP(Protocol):
    _fields_: Sequence[tuple[str, type["_CData"]] | tuple[str, type["_CData"], int]] = [
        ("src_port", c_uint16),
        ("dst_port", c_uint16),
        ("seq_num", c_uint32),
        ("ack_num", c_uint32),
        ("data_off", c)
    ]
