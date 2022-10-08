from ctypes import c_ubyte, c_uint8, c_uint16, c_uint32
from typing import TYPE_CHECKING, Sequence

from nipsu.protocols.base import Protocol

if TYPE_CHECKING:
    from ctypes import _CData
