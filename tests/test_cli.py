from typer.testing import CliRunner

from nipsu import __appname__, __version__, cli


class TestCli:
    def test_version(self) -> None:
        # given
        runner = CliRunner()
        # when
        result = runner.invoke(cli.app, ["--version"])
        # then
        assert result.exit_code == 0
        assert f"{__appname__} v{__version__}\n" in result.stdout
