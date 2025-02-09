from enum import Enum
from mcdreforged.api.all import *
from im_api.drivers.base import Platform
from im_api.models.message import Event, Message

from im_share_chat.formatter.qq import format_data as format_qq_data
from im_share_chat.core.reporter import transfer_to_matrix, transfer_to_qq


class PlatformDisplayname(Enum):
    Matrix = "MATRIX"
    QQ = "QQ"

def on_im_message(server: PluginServerInterface, platform: Platform, message: Message):
    platform_name = platform.name
    im_platform = PlatformDisplayname(platform_name).name
    group_name = f'{message.channel.name}' if message.channel.name is not None else message.channel.id
    user_name = message.user.nick if message.user.nick is not None else message.user.name
    content = message.content
    if im_platform == "QQ":
        if isinstance(content, list):
            content = format_qq_data(content)
            if content == '' or content == ' ':
                content = "[未知消息类型]"
        transfer_to_matrix(server, f"[{im_platform} | {group_name}] <{user_name}> {content}")
    if im_platform == "Matrix":
        transfer_to_qq(server, f"[{im_platform} | {group_name}] <{user_name}> {content}")
    server.broadcast(f"[{im_platform} | {group_name}] <{user_name}> {content}")
    