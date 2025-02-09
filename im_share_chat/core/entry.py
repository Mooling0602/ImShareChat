import im_share_chat.config.applying as cfg

from mcdreforged.api.all import *

from im_share_chat.config import load_config
from im_share_chat.core.listener import on_im_message
from im_share_chat.core.reporter import transfer_to_qq, transfer_to_matrix


def on_load(server: PluginServerInterface, prev_module):
    load_config(server)
    server.register_event_listener("im_api.message", on_im_message)
    if cfg.qq_group_number == '':
        server.logger.warning("尚未配置要转发的QQ群号，请修改插件配置！")
    if cfg.matrix_room_id == '':
        server.logger.warning("尚未配置要转发的Matrix房间ID，请修改插件配置！")
    configDir = server.get_data_folder()
    server.logger.info(f"ImShareChat的配置目录在相对MCDR工作目录的{configDir}")

def on_user_info(server: PluginServerInterface, info: Info):
    if info.is_player and not info.content.startswith('!!'):
        player = info.player
        message = info.content
        content = f"[MC] <{player}> {message}"
        transfer_to_qq(server, content)
        transfer_to_matrix(server, content)
