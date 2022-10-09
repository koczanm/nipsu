from __future__ import annotations

import socket
from abc import abstractmethod, abstractproperty
from ctypes import Array, BigEndianStructure
from typing import TYPE_CHECKING, Any, Dict, List, Union

if TYPE_CHECKING:
    from ctypes import _CData


JSONType = Union[bool, float, int, str, None, Dict[str, Any], List[Any]]


class Protocol(BigEndianStructure):
    _pack_: int = 1
    header_len: int

    @abstractproperty
    def encap_proto(self) -> str | None:
        raise NotImplementedError

    @abstractmethod
    def describe(self) -> JSONType:
        raise NotImplementedError

    @classmethod
    def decode(cls, packet: bytes) -> Protocol:
        header = cls.from_buffer_copy(packet)
        return header

    @classmethod
    def colon_hex_notation(cls, arr: Array[_CData]) -> str:
        return ":".join([cls.cdata_to_hex_str(el) for el in arr])

    @classmethod
    def array_to_proto_addr(cls, addr_arr: Array[_CData], addr_family: socket.AddressFamily | None = None) -> str:
        if addr_family:
            return socket.inet_ntop(addr_family, bytes(addr_arr))
        return cls.colon_hex_notation(addr_arr)

    @staticmethod
    def cdata_to_bin_str(value: _CData, pad: int = 0) -> str:
        return f"{value:0{pad}b}"

    @staticmethod
    def cdata_to_hex_str(value: _CData) -> str:
        return f"{value:X}"

    @staticmethod
    def cdata_to_int_str(value: _CData) -> str:
        return f"{value:d}"
