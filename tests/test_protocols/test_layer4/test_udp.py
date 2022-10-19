from nipsu.protocols.layer4 import UDP


class TestUDP:
    def test_describe(self) -> None:
        # given
        raw_udp_header = b"\x8f\x1b\x00\x13\x00\x16\xf5p"
        # when
        udp_header = UDP.decode(raw_udp_header)
        # then
        assert udp_header.describe() == {
            "Source port": 36635,
            "Destination port": 19,
            "Length": 22,
            "Checksum": "F570",
        }
