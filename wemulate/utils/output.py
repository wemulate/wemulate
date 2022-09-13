from typing import List

from rich.console import Console
from rich.table import Table


console = Console()
err_console = Console(stderr=True)


def create_table(title: str, headers: List[str]) -> Table:
    table = Table(title=title)
    for header in headers:
        table.add_column(header)
    return table
