from nipsu.protocols.layer3 import IPv4
from nipsu.protocols.layer3.ip import IPv6


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


class TestIPv6:
    def test_decode(self) -> None:
        # given
        raw_ipv6_header = (
            b"\x11\x00\x1d\xcd\x03o\x00!E\x00\x03m\x93Y\x00\x00\x80)d"
            b"\xaaF7\xd5\xd3\xc0Xc\x01`\x00\x00\x00\x031\x06\x80 \x02F7"
        )
        # when
        ipv6_header = IPv6.decode(raw_ipv6_header)
        # then
        assert ipv6_header.describe() == {
            "Version": 1,
            "Traffic class": {
                "DSCP": "16: Network operations, administration and management",
                "ECN": "Non ECN-Capable Transport",
            },
            "Flow label": 7629,
            "Payload length": 879,
            "Next header": "Unsupported: 0",
            "Hop limit": 33,
            "Source address": "4500:36d:9359:0:8029:64aa:4637:d5d3",
            "Destination address": "c058:6301:6000:0:331:680:2002:4637",
        }
