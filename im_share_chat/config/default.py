"""Config dict format
"""
from typing import Any


default_config: dict[str, Any] = {
    "groups": {
        "qq": "",
        "matrix": ""
    },
    "format": {
        "chat": {
            "im": "",
            "game": ""
        },
        "on_player_joined": "",
        "on_player_left": "",
        "on_server_start_pre": "",
        "on_server_startup": "",
        "on_server_stop": "",
        "on_server_crash": ""
    },
    "transfer_game_event_to_im": {
        "on_player_death": True,
        "on_player_advancement": True
    },
    "allowed_rcon_commands": [
        "list",
        "ver",
        "version",
        "tps",
        "mspt"
    ]
}


default_im_perm: dict[str, Any] = {
    "owner": [],
    "admin": [],
    "helper": [],
    "user": [
        "qq!12345678",
        "matrix!@user:example.com"
    ],
    "guest": []
}
