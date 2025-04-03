import im_share_chat.config.applying as cfg

from mcdreforged.api.all import *

from im_api.models.request import MessageType, SendMessageRequest, ChannelInfo
from im_api.models.platform import Platform

from im_share_chat.utils import remove_format_codes


def transfer_to_qq(server, content: str):
    request = SendMessageRequest(
        platforms=[Platform.QQ],
        channel=ChannelInfo(id=cfg.qq_group_number, type=MessageType.CHANNEL),
        content=remove_format_codes(content)
    )
    server.dispatch_event(LiteralEvent("im_api.send_message"), (request,))

def transfer_to_matrix(server, content: str):
    request = SendMessageRequest(
        platforms=[Platform.MATRIX],
        channel=ChannelInfo(id=cfg.matrix_room_id, type=MessageType.CHANNEL),
        content=remove_format_codes(content)
    )
    server.dispatch_event(LiteralEvent("im_api.send_message"), (request,))