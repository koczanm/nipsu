from enum import Enum
from typing import Dict, Optional, Type

import typer

from nipsu import __appname__, __version__
from nipsu.output import JsonOutput, Output, RichOutput, YamlOutput
from nipsu.sniffer import Sniffer

app = typer.Typer()


OUTPUT_CLASSES: Dict[str, Type[Output]] = {
    "json": JsonOutput,
    "rich": RichOutput,
    "yaml": YamlOutput,
}


class OutputFormat(str, Enum):
    json = "json"
    rich = "rich"
    yaml = "yaml"


def version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__appname__} v{__version__}")
        raise typer.Exit()


@app.command()
def main(
    interface: str = typer.Argument(..., help="Name of the interface to listen to."),
    output: OutputFormat = typer.Option(OutputFormat.rich.value),
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Print version information.",
        callback=version_callback,
        is_eager=True,
    ),
) -> None:
    sniffer = Sniffer(interface)
    output_cls = OUTPUT_CLASSES[output]
    with output_cls() as out:
        try:
            for frame in sniffer.listen():
                out.display_frame(frame)
        except KeyboardInterrupt:
            pass
