"""Listen im messages and format, transfer them.
"""
from enum import Enum

from im_api.drivers.base import Platform
from im_api.models.message import Message
from mcdreforged.api.all import PluginServerInterface

import im_share_chat.config.applying as cfg
from im_share_chat.command_source import ImCommandSource
from im_share_chat.core.reporter import transfer_to_matrix, transfer_to_qq
from im_share_chat.formatter.qq import format_data as format_qq_data  # type: ignore


class PlatformDisplayname(Enum):
    """__Description__
    """
    Matrix = "MATRIX"  # pylint:disable=invalid-name
    QQ = "QQ"


# 根据频道ID配置处理逻辑：转发函数和消息格式化方法
def get_handler() -> dict:  # type: ignore
    """__Description__
    """
    CHANNEL_HANDLERS = {  # type: ignore  # pylint:disable=invalid-name
        cfg.qq_group_number: {
            'transfer_func': transfer_to_matrix,  # QQ消息转发至Matrix
            'format_func': lambda content: (  # type: ignore
                format_qq_data(content) if isinstance(content, list) else content)  # type: ignore
        },
        cfg.matrix_room_id: {
            'transfer_func': transfer_to_qq,       # Matrix消息转发至QQ
            'format_func': lambda content: content  # type: ignore  # Matrix消息无需额外格式化
        }
    }
    return CHANNEL_HANDLERS  # type: ignore

def on_im_message(server: PluginServerInterface, platform: Platform, message: Message):
    """__Description__"""

    CHANNEL_HANDLERS = get_handler()  # type: ignore  # pylint:disable=invalid-name

    # 获取平台显示名称（例如 "QQ" 或 "MATRIX"）
    im_platform = PlatformDisplayname(platform.name).name
    group_name = message.channel.name or message.channel.id
    user_name = message.user.nick or message.user.name
    raw_content = message.content

    # 根据消息所在频道判断是否需要处理
    handler = CHANNEL_HANDLERS.get(message.channel.id)  # type: ignore
    if not handler:
        server.logger.info(f"No handler found for channel id: {message.channel.id}")
        return  # 非目标群组，不处理

    # 格式化消息内容
    content = handler['format_func'](raw_content)  # type: ignore
    if isinstance(content, str) and content.strip() == "":
        content: str = "[未知消息类型]"

    if not isinstance(content, str):
        content = str(content)  # type: ignore

    src = ImCommandSource(server, message, platform)
    match content:
        case content if content.startswith("/"):
            command = content[len("/"):].strip()
            if " " in command:
                command = f'"{command}"'
            server.execute_command(f"!!ichat rcon {command}", src)
        case content if content.startswith("!!"):
            server.execute_command(content, src)
        case _:
            if not isinstance(cfg.chat_format_im, str):
                raise TypeError('Config error!')

            formatted: str = cfg.chat_format_im.format(
                im_platform=im_platform,
                group_name=group_name,
                user_name=user_name,
                content=content
            )

            # 调用对应转发函数
            handler['transfer_func'](server, formatted)
            server.broadcast(formatted)
