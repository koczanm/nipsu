from nipsu.protocols.layer2 import Ethernet


class TestEthernet:
    def test_decode(self):
        # given
        raw_eth_header = b"\xc0\x01\x14|\x00\x01\xc0\x02\x12h\x00\x00\x08\x00"
        # when
        eth_header = Ethernet.decode(raw_eth_header)
        # then
        assert eth_header.describe() == {
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
