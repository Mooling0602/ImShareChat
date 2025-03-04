import im_share_chat.config.applying as cfg

from mcdreforged.api.all import *

from im_share_chat.config import load_config
from im_share_chat.core.listener import on_im_message
from im_share_chat.core.reporter import transfer_to_qq, transfer_to_matrix


def on_load(server: PluginServerInterface, prev_module):
    load_config(server)
    server.register_event_listener("im_api.message", on_im_message)
    if cfg.qq_group_number == '':
        server.logger.warning("Config missing: groups.qq")
    if cfg.matrix_room_id == '':
        server.logger.warning("Config missing: groups.matrix")
    configDir = server.get_data_folder()
    server.logger.info(f"ImShareChat config folder: {configDir}")

def on_server_start_pre(server: PluginServerInterface):
    transfer_to_qq(server, cfg.on_server_start_pre_format)
    transfer_to_matrix(server, cfg.on_server_start_pre_format)

def on_server_startup(server: PluginServerInterface):
    transfer_to_qq(server, cfg.on_server_startup_format)
    transfer_to_matrix(server, cfg.on_server_startup_format)

def on_player_joined(server: PluginServerInterface, player: str, info: Info):
    transfer_to_qq(server, cfg.on_player_joined_format.format(player=player))
    transfer_to_matrix(server, cfg.on_player_joined_format.format(player=player))

def on_user_info(server: PluginServerInterface, info: Info):
    if info.is_player and not info.content.startswith('!!'):
        player = info.player
        message = info.content
        content = cfg.chat_format_game.format(player=player, message=message)
        transfer_to_qq(server, content)
        transfer_to_matrix(server, content)

def on_player_left(server: PluginServerInterface, player: str):
    transfer_to_qq(server, cfg.on_player_left_format.format(player=player))
    transfer_to_matrix(server, cfg.on_player_left_format.format(player=player))

def on_server_stop(server: PluginCommandSource, return_code: int):
    if return_code != 0:
        transfer_to_qq(server, cfg.on_server_crash_format)
        transfer_to_matrix(server, cfg.on_server_crash_format)
    else:
        transfer_to_qq(server, cfg.on_server_stop_format)
        transfer_to_matrix(server, cfg.on_server_stop_format)
