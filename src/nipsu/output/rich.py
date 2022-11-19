from typing import Any, Tuple, cast

from rich import print
from rich.panel import Panel
from rich.tree import Tree

from nipsu.output.base import Output
from nipsu.protocols.base import Protocol
from nipsu.sniffer import FrameInfo


class RichOutput(Output):
    def display_start(self) -> None:
        print("Sniffing incoming packets. Press [bold]Ctrl-C[/bold] to abort...")

    def _add_header(self, branch: Tree, field_name: str, field_value: Any) -> None:
        if isinstance(field_value, dict):
            branch = branch.add(f"[cyan]{field_name}")
            for key, value in field_value.items():
                self._add_header(branch, key, value)
        else:
            branch.add(f"[cyan]{field_name} ➜ [blue]{field_value}")

    def display_frame(self, frame: FrameInfo) -> None:
        root = branch = None
        for proto_info in frame.packet.get_protocols(with_headers=True):
            proto_info = cast(Tuple[str, Protocol], proto_info)
            proto_name, proto = proto_info
            if not branch:
                root = branch = Tree(f"[bold magenta] {proto_name}")
            else:
                branch = branch.add(f"[bold magenta] {proto_name}")
            for key, value in proto.show().items():
                self._add_header(branch, key, value)
        if root:
            panel = Panel(
                root,
                style="white",
                width=79,
                title=f"[italic]Frame #{frame.id} at {frame.ts}",
                title_align="left",
            )
            print(panel)

    def display_end(self) -> None:
        print("Aborting packet sniffing...")
