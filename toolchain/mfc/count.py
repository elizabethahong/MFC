import os, glob, typing, typing
import rich.table

from .state   import ARG
from .common  import MFC_ROOTDIR, format_list_to_string
from .printer import cons

def handle_dir(dirpath: str) -> typing.Tuple[typing.List[typing.Tuple[str, int]], int]:
    files = []
    total = 0

    for filepath in glob.glob(os.path.join(dirpath, '*.*f*')):
        with open(filepath) as f:
            n = sum(1 if not l.isspace() else 0 for l in f.read().split('\n'))
            files.append((filepath, count))
            total += n

    files.sort(key=lambda x: x[1], reverse=True)

    return (files, total)

def count():
    target_str_list = format_list_to_string(ARG('targets'), 'magenta')

    cons.print(f"[bold]Counting lines of code in {target_str_list}[/bold] (excluding whitespace lines)")
    cons.indent()

    total = 0
    for codedir in ['common'] + ARG("targets"):
        dirfiles, dircount = handle_dir(os.path.join(MFC_ROOTDIR, 'src', codedir))
        table = rich.table.Table(show_header=True, box=rich.table.box.SIMPLE)
        table.add_column(f"File (in [magenta]{codedir}[/magenta])", justify="left")
        table.add_column(f"Lines ([cyan]{dircount}[/cyan])", justify="right")

        for filepath, n in dirfiles:
            table.add_row(f"{os.path.basename(filepath)}", f"[bold cyan]{n}[/bold cyan]")

        total += dircount

        cons.raw.print(table)

    cons.print(f"[bold]Total {target_str_list} lines: [bold cyan]{total}[/bold cyan].[/bold]")
    cons.print()
    cons.unindent()
