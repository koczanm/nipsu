from ctypes import c_uint16, c_uint32
from typing import TYPE_CHECKING, Any, Dict, List, Sequence, Tuple, Type, Union

from nipsu.protocols.base import Protocol

if TYPE_CHECKING:
    from ctypes import _CData


class TCP(Protocol):
    _fields_: Sequence[Union[Tuple[str, Type["_CData"]], Tuple[str, Type["_CData"], int]]] = [
        ("src_port", c_uint16),
        ("dst_port", c_uint16),
        ("seq_num", c_uint32),
        ("ack_num", c_uint32),
        ("offset", c_uint16, 4),  # TODO: support the options field if offset > 5
        ("reserved", c_uint16, 3),
        ("flags", c_uint16, 9),
        ("win_size", c_uint16),
        ("checksum", c_uint16),
        ("urg_ptr", c_uint16),
    ]
    header_len: int = 20
    flag_codes: List[str] = ["NS", "CWR", "ECE", "URG", "ACK", "PSH", "RST", "SYN", "FIN"]

    @property
    def active_flags(self) -> List[str]:
        return [self.flag_codes[i] for i, flag in enumerate(self.cdata_to_bin_str(self.flags)) if flag == "1"]

    def show(self) -> Dict[str, Any]:
        return {
            "Source port": self.src_port,
            "Destination port": self.dst_port,
            "Sequence number": self.seq_num,
            "Acknowledgment number": self.ack_num,
            "Data offset": self.offset,
            "Reserved": self.cdata_to_bin_str(self.reserved, pad=3),
            "Flags": self.active_flags,
            "Window size": self.win_size,
            "Checksum": self.cdata_to_hex_str(self.checksum),
            "Urgent pointer": self.urg_ptr,
        }
