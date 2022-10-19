from nipsu.packet import Packet
from nipsu.protocols.layer2 import Ethernet
from nipsu.protocols.layer3 import IPv4
from nipsu.protocols.layer4 import TCP


class TestPacket:
    def test_tcp_packet(self) -> None:
        # given
        raw_packet = (
            b"\xc0\x01\x14|\x00\x01\xc0\x02\x12h\x00\x00\x08\x00E\x00\x00,vE\x00\x00\xff\x06 \x81\x01\x01\x17\x03"
            b"\x01\x01\x0c\x01\xb5\xdd\x00P\n\xaf`N\x00\x00\x00\x00`\xc2\x10 D\xb2\x00\x00\x02\x04\x02\x18\x00\x00"
        )
        eth_header = Ethernet.decode(raw_packet)
        ipv4_header = IPv4.decode(raw_packet[Ethernet.header_len :])
        tcp_header = TCP.decode(raw_packet[Ethernet.header_len + IPv4.header_len :])
        # when
        packet = Packet(eth_header, ipv4_header, tcp_header)
        # then
        assert packet.get_protocols() == [
            "Ethernet",
            "IPv4",
            "TCP",
        ]
        assert packet.get_protocols(with_headers=True) == [
            ("Ethernet", eth_header),
            ("IPv4", ipv4_header),
            ("TCP", tcp_header),
        ]
