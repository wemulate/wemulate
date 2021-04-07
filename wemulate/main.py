import os

from wemulate.utils.settings import get_db_location
from wemulate.controllers.load_controller import LoadController
from wemulate.controllers.save_controller import SaveController
from wemulate.controllers.config_controller import ConfigController
from wemulate.controllers.reset_controller import ResetController
from wemulate.controllers.delete_controller import DeleteController
from wemulate.controllers.set_controller import SetController
from wemulate.controllers.list_controller import ListController
from wemulate.controllers.add_controller import AddController
from wemulate.controllers.show_controller import ShowController
from cement import App, TestApp, init_defaults
from cement.utils import fs
from cement.core.exc import CaughtSignal
from wemulate.core.exc import WEmulateError
from wemulate.controllers.base import Base

from wemulate.core.database.setup import (
    pre_setup_profile,
    pre_setup_device,
    pre_setup_interfaces,
)
from wemulate.core.database.models import (
    ProfileModel,
    DeviceModel,
    LogicalInterfaceModel,
    InterfaceModel,
    ConnectionModel,
    ParameterModel,
)


class WEmulate(App):
    """WEmulate primary application."""

    class Meta:
        label = "wemulate"

        # configuration defaults
        # config_defaults = CONFIG

        # call sys.exit() on close
        exit_on_close = True

        # load additional framework extensions
        extensions = ["yaml", "colorlog", "jinja2", "tabulate"]

        # configuration handler
        config_handler = "yaml"

        # configuration file suffix
        config_file_suffix = ".yml"

        # set the log handler
        log_handler = "colorlog"

        # set the output handler
        output_handler = "tabulate"

        # template directory
        template_dir = "templates"

        # register handlers
        handlers = [
            Base,
            ShowController,
            AddController,
            ListController,
            SetController,
            DeleteController,
            ResetController,
            ConfigController,
            SaveController,
            LoadController,
        ]

        # register hooks
        hooks = [
            ("pre_setup", pre_setup_profile, -99),
            ("pre_setup", pre_setup_device, 0),
            ("pre_setup", pre_setup_interfaces, 100),
        ]


class WEmulateTest(TestApp, WEmulate):
    """A sub-class of WEmulate that is better suited for testing."""

    class Meta:
        label = "wemulate"


def main():
    with WEmulate() as app:
        try:
            app.run()

        except AssertionError as e:
            print("AssertionError > %s" % e.args[0])
            app.exit_code = 1

            if app.debug is True:
                import traceback

                traceback.print_exc()

        except WEmulateError as e:
            print("WEmulateError > %s" % e.args[0])
            app.exit_code = 1

            if app.debug is True:
                import traceback

                traceback.print_exc()

        except CaughtSignal as e:
            # Default Cement signals are SIGINT and SIGTERM, exit 0 (non-error)
            print("\n%s" % e)
            app.exit_code = 0


if __name__ == "__main__":
    main()
