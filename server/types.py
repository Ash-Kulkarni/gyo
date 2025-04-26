from typing import Dict, List, Any, NamedTuple

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
