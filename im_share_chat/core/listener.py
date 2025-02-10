import im_share_chat.config.applying as cfg

from enum import Enum
from mcdreforged.api.all import *
from im_api.drivers.base import Platform
from im_api.models.message import Event, Message

from im_share_chat.formatter.qq import format_data as format_qq_data
from im_share_chat.core.reporter import transfer_to_matrix, transfer_to_qq


class PlatformDisplayname(Enum):
    Matrix = "MATRIX"
    QQ = "QQ"

# 根据频道ID配置处理逻辑：转发函数和消息格式化方法
def get_handler() -> dict:
    CHANNEL_HANDLERS = {
        cfg.qq_group_number: {
            'transfer_func': transfer_to_matrix,  # QQ消息转发至Matrix
            'format_func': lambda content: format_qq_data(content) if isinstance(content, list) else content
        },
        cfg.matrix_room_id: {
            'transfer_func': transfer_to_qq,       # Matrix消息转发至QQ
            'format_func': lambda content: content  # Matrix消息无需额外格式化
        }
    }
    return CHANNEL_HANDLERS

def on_im_message(server: PluginServerInterface, platform: Platform, message: Message):

    CHANNEL_HANDLERS = get_handler()
    
    # 获取平台显示名称（例如 "QQ" 或 "MATRIX"）
    im_platform = PlatformDisplayname(platform.name).name
    group_name = message.channel.name or message.channel.id
    user_name = message.user.nick or message.user.name
    raw_content = message.content

    # 根据消息所在频道判断是否需要处理
    handler = CHANNEL_HANDLERS.get(message.channel.id)
    if not handler:
        server.logger.info(f"No handler found for channel id: {message.channel.id}")
        return  # 非目标群组，不处理

    # 格式化消息内容
    content = handler['format_func'](raw_content)
    if isinstance(content, str) and content.strip() == "":
        content = "[未知消息类型]"

    formatted = f"[{im_platform} | {group_name}] <{user_name}> {content}"
    server.logger.info(f"Formatted message: {formatted}")
    
    # 调用对应转发函数
    handler['transfer_func'](server, formatted)
    server.broadcast(formatted)
