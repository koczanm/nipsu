from nipsu.protocols.layer2 import Ethernet


class TestEthernet:
    def test_decode(self) -> None:
        # given
        raw_eth_header = b"\xc0\x01\x14|\x00\x01\xc0\x02\x12h\x00\x00\x08\x00"
        # when
        eth_header = Ethernet.decode(raw_eth_header)
        # then
        assert eth_header.describe() == {
            "Destination MAC address": "C0:1:14:7C:0:1",
            "Source MAC address": "C0:2:12:68:0:0",
            "EtherType": "IPv4",
        }
