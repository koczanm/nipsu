import pytest

from nipsu.protocols.layer2 import Ethernet


class TestEthernet:
    def test_decode(self):
        eth_header = Ethernet
