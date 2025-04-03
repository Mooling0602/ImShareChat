import im_share_chat.config.applying as cfg

from mcdreforged.api.all import *

from im_share_chat.utils import execute_if
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
    server.register_event_listener("PlayerDeathEvent", on_player_death)
    server.register_event_listener("PlayerAdvancementEvent", on_player_advancement)

def on_server_start_pre(server: PluginServerInterface):
    transfer_to_qq(server, cfg.on_server_start_pre_format)
    transfer_to_matrix(server, cfg.on_server_start_pre_format)

def on_server_startup(server: PluginServerInterface):
    if cfg.on_player_death is True or cfg.on_player_advancement is True:
        if "mg_events" not in server.get_plugin_list():
            server.logger.warning("Dependency missing: enabled at least one option in transfer_game_event_to_im, but mg_events not found.")
    transfer_to_qq(server, cfg.on_server_startup_format)
    transfer_to_matrix(server, cfg.on_server_startup_format)

@execute_if(lambda: cfg.on_player_death is True)
def on_player_death(server: PluginServerInterface, player, event, content):
    player: str = player
    event: str = event
    for i in content:
        if i.locale == 'zh_cn':
            transfer_to_qq(server, i.raw)
            transfer_to_matrix(server, i.raw)

@execute_if(lambda: cfg.on_player_advancement is True)
def on_player_advancement(server: PluginServerInterface, player, event, content):
    player: str = player
    event: str = event
    for i in content:
        if i.locale == 'zh_cn':
            transfer_to_qq(server, i.raw)
            transfer_to_matrix(server, i.raw)    

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
