import json
from typing import Any, Dict, Tuple, cast

from nipsu.output.base import Output
from nipsu.protocols.base import Protocol
from nipsu.sniffer import FrameInfo


class JsonOutput(Output):
    def display_start(self) -> None:
        pass

    def display_frame(self, frame: FrameInfo) -> None:
        protocols: Dict[str, Any] = {}
        for proto_info in frame.packet.get_protocols(with_headers=True):
            proto_info = cast(Tuple[str, Protocol], proto_info)
            proto_name, proto = proto_info
            protocols[proto_name] = proto.show()
        data = {
            "metadata": {
                "id": frame.id,
                "ts": frame.ts.isoformat(),
            },
            "data": protocols,
        }
        print(json.dumps(data))

    def display_end(self) -> None:
        pass
