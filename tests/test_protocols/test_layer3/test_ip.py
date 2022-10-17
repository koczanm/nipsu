from nipsu.protocols.layer3 import IPv4


class TestIPv4:
    def test_decode(self) -> None:
        # given
        raw_ipv4_header = b"E\x00\x00,vE\x00\x00\xff\x06 \x81\x01\x01\x17\x03\x01\x01\x0c\x01"
        # when
        ipv4_header = IPv4.decode(raw_ipv4_header)
        # then
        assert ipv4_header.describe() == {
            "Version": 4,
            "IHL": 5,
            "DCSP": "0: Standard",
            "ECN": "Non ECN-Capable Transport",
            "Total length": 44,
            "Identifications": 30277,
            "Flags": "Not set",
            "Fragment offset": 0,
            "TTL": 255,
            "Protocol": "TCP",
            "Header checksum": "2081",
            "Source address": "1.1.23.3",
            "Destination address": "1.1.12.1",
        }
