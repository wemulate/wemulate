from typing import List, Tuple
from cement import Controller, ex
from cement.utils.version import get_version_banner
from ..core.version import get_version

VERSION_BANNER = """
A modern WAN Emulator %s
%s
""" % (
    get_version(),
    get_version_banner(),
)


class Base(Controller):
    class Meta:
        label: str = "base"

        # text displayed at the top of --help output
        description: str = "A modern WAN Emulator"

        # text displayed at the bottom of --help output
        epilog: str = "Usage: wemulate command --foo bar"

        # controller level arguments. ex: 'wemulate --version'
        arguments: List[Tuple] = [
            ### add a version banner
            (["-v", "--version"], {"action": "version", "version": VERSION_BANNER}),
        ]

    def _default(self):
        """Default action if no sub-command is passed."""

        self.app.args.print_help()
