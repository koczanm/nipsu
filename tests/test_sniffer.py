import datetime

from nipsu.sniffer import Decoder


class TestDecoder:
    def test_decode_packet(self) -> None:
        # given
        ts = 1669311805.478877
        raw_packet = (
            b"\xc0\x01\x14|\x00\x01\xc0\x02\x12h\x00\x00\x08\x00E\x00\x00,vE\x00\x00\xff\x06 \x81\x01\x01\x17\x03"
            b"\x01\x01\x0c\x01\xb5\xdd\x00P\n\xaf`N\x00\x00\x00\x00`\xc2\x10 D\xb2\x00\x00\x02\x04\x02\x18\x00\x00"
        )
        # when
        frame_info = Decoder.decode_packet((ts, raw_packet))
        # then
        assert frame_info.id == 0
        assert type(frame_info.ts) == datetime.datetime
        assert frame_info.packet.get_protocols() == [
            "Ethernet",
            "IPv4",
            "TCP",
        ]
