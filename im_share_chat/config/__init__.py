import os
import im_share_chat.config.applying as cfg

from mcdreforged.api.all import *
from ..utils import extract_file
from .default import *


def load_config(server: PluginServerInterface):
    configDir = server.get_data_folder()
    if not os.path.exists(os.path.join(configDir, 'config.yml')):
        if server.get_mcdr_language() != 'zh_cn':
            extract_file(server, os.path.join('resources', 'config.default.yml'), os.path.join(configDir, 'config.yml'))
        else:
            extract_file(server, os.path.join('resources', 'config.default_zh-cn.yml'), os.path.join(configDir, 'config.yml'))
    config = server.load_config_simple('config.yml', default_config)
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