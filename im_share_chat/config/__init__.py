import os
import im_share_chat.config.applying as cfg
# type: ignore
# pylint: skip-file
from mcdreforged.api.all import PluginServerInterface
from ..utils import extract_file  # type: ignore
from .default import *  # noqa: F403


def load_config(server: PluginServerInterface):  # noqa: F405
    configDir = server.get_data_folder()
    if not os.path.exists(os.path.join(configDir, 'config.yml')):
        if server.get_mcdr_language() != 'zh_cn':
            extract_file(server, os.path.join('resources', 'config.default.yml'), os.path.join(configDir, 'config.yml'))
        else:
            extract_file(server, os.path.join('resources', 'config.default_zh-cn.yml'), os.path.join(configDir, 'config.yml'))
    if not os.path.exists(os.path.join(configDir, 'im_permissions.yml')):
        extract_file(server, os.path.join('resources', 'im_permissions.yml'), os.path.join(configDir, 'im_permissions.yml'))
    config = server.load_config_simple('config.yml', default_config) # type: ignore  # noqa: F405
    im_perm = server.load_config_simple('im_permissions.yml', default_im_perm, echo_in_console=False)  # type: ignore  # noqa: F405
    if os.path.exists(os.path.join(configDir, 'config.json')):
        server.logger.warning("Config warning: old json config detected, but it's invalid.")
    cfg.qq_group_number = config['groups']['qq']
    cfg.matrix_room_id = config['groups']['matrix']
    cfg.chat_format_im = config['format']['chat']['im']
    cfg.chat_format_game = config['format']['chat']['game']
    cfg.on_player_joined_format = config['format']['on_player_joined']
    cfg.on_player_left_format = config['format']['on_player_left']
    cfg.on_server_start_pre_format = config['format']['on_server_start_pre']
    cfg.on_server_startup_format = config['format']['on_server_startup']
    cfg.on_server_stop_format = config['format']['on_server_stop']
    cfg.on_server_crash_format = config['format']['on_server_crash']
    cfg.on_player_death = config['transfer_game_event_to_im']['on_player_death']
    cfg.on_player_advancement = config['transfer_game_event_to_im']['on_player_advancement']
    cfg.allowed_rcon_commands = config['allowed_rcon_commands']
    if im_perm['owner'] is not None:
        cfg.perm_owners = im_perm['owner']
    if im_perm['admin'] is not None:
        cfg.perm_admins = im_perm['admin']
    if im_perm['helper'] is not None:
        cfg.perm_helpers = im_perm['helper']
    if im_perm['user'] is not None:
        cfg.perm_users = im_perm['user']
    if im_perm['guest'] is not None:
        cfg.perm_guests = im_perm['guest']
