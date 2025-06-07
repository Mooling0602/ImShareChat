# pylint: disable=invalid-name
"""Storage configs after they loaded.
"""
qq_group_number: str | None = None
matrix_room_id: str | None = None
chat_format_im: str | None = None
chat_format_game: str | None = None
on_player_joined_format: str | None = None
on_player_left_format: str | None = None
on_server_start_pre_format: str | None = None
on_server_startup_format: str | None = None
on_server_stop_format: str | None = None
on_server_crash_format: str | None = None
on_player_death: bool = True
on_player_advancement: bool = True
allowed_rcon_commands: list[str] = []
perm_owners: list[str] = []
perm_admins: list[str] = []
perm_helpers: list[str] = []
perm_users: list[str] = []
perm_guests: list[str] = []
