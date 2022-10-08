from nipsu.protocols.layer3 import IPv4


class TestIPv4:
    def test_decode(self):
        # given
        raw_ipv4_header = b"E\x00\x00,vE\x00\x00\xff\x06 \x81\x01\x01\x17\x03\x01\x01\x0c\x01"
        # when
        eth_header = IPv4.decode(raw_ipv4_header)
        # then
        assert eth_header.describe() == {
            "Destination MAC address": "C0:1:14:7C:0:1",
            "Source MAC address": "C0:2:12:68:0:0",
            "EtherType": "IPv4",
        }
