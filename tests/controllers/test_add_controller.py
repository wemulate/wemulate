from typer.testing import CliRunner

from wemulate.controllers.add_controller import app

runner = CliRunner()


def test_add_connection():
    result = runner.invoke(app, ["connection", "--connection-name", "--interfaces", ""])
    print(result)
