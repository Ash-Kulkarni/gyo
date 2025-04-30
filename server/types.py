from typing import Dict, List, Any, NamedTuple
from rich.console import Console
from rich.pretty import Pretty

from rich.live import Live
from rich.table import Table

import time

console = Console()


AppState = NamedTuple(
    "AppState",
    [
        ("players", Dict[str, Dict[str, Any]]),
        ("bullets", List[Dict[str, Any]]),
        ("enemies", List[Dict[str, Any]]),
        ("scoreboard", Dict[str, Dict[str, int]]),
        ("world_size", Dict[str, int]),
    ],
)


live = None


def start_live_logging():
    """Starts the live logging pane."""
    global live
    if live is None:
        live = Live(console=console, refresh_per_second=4)
        live.start()


def stop_live_logging():
    """Stops the live logging pane."""
    global live
    if live is not None:
        live.stop()
        live = None


def update_live_app_state(state: AppState, dt: float):
    """Updates the live logging pane with the current application state."""
    if live is None:
        return

    # Create a condensed table view of the app state
    table = Table(
        title=f"📋 App State (dt: {dt:.2f})",
        show_header=True,
        header_style="bold green",
    )
    table.add_column("Key", style="dim", width=20)
    table.add_column("Value", style="bold")

    # Add key details from the app state
    table.add_row("Players", Pretty(len(state.players)))
    table.add_row("Bullets", Pretty(len(state.bullets)))
    table.add_row("Enemies", Pretty(len(state.enemies)))

    # Update the live display
    live.update(table)
