from nipsu.protocols.layer4 import TCP


class TestTCP:
    def test_show(self) -> None:
        # given
        raw_tcp_header = b"\xb5\xdd\x00P\n\xaf`N\x00\x00\x00\x00`\xc2\x10 D\xb2\x00\x00"
        # when
        tcp_header = TCP.decode(raw_tcp_header)
        # then
        assert tcp_header.show() == {
            "Source port": 46557,
            "Destination port": 80,
            "Sequence number": 179265614,
            "Acknowledgment number": 0,
            "Data offset": 6,
            "Reserved": "000",
            "Flags": ["NS", "CWR", "RST"],
            "Window size": 4128,
            "Checksum": "44B2",
            "Urgent pointer": 0,
        }
