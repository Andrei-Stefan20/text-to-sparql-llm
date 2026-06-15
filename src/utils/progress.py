"""
Shared rich console and a consistent progress-bar factory.

Both the evaluator and the GERBIL file generator import `console` and
`make_progress` from here so they render identical bars and never fight over
stdout (a single shared Console keeps logging and progress output in sync).
"""

from rich.console import Console
from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
)

# One shared console for the whole process.
console = Console()


def make_progress() -> Progress:
    """
    Build a reusable progress bar: spinner, description, bar, M/N counter,
    elapsed time and an ETA. The description is updated live by callers to
    show the current status (e.g. ok / err / rate-limit counts).
    """
    return Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        MofNCompleteColumn(),
        TextColumn("[dim]•[/]"),
        TimeElapsedColumn(),
        TextColumn("[dim]eta[/]"),
        TimeRemainingColumn(),
        console=console,
    )
