"""Methods to send messages to im platforms.
"""
from im_api.models.platform import Platform
from im_api.models.request import ChannelInfo, MessageType, SendMessageRequest
from mcdreforged.api.all import PluginServerInterface, ServerInterface, LiteralEvent

import im_share_chat.config.applying as cfg
from im_share_chat.utils import remove_format_codes


def transfer_to_qq(server: PluginServerInterface | ServerInterface, content: str):
    """Send a message to the QQ group.
    """
    if not isinstance(cfg.qq_group_number, str) and cfg.qq_group_number is not None:
        cfg.qq_group_number = str(cfg.qq_group_number)

    if cfg.qq_group_number is None:
        raise TypeError('Config error!')

    request = SendMessageRequest(
        platforms={Platform.QQ},
        channel=ChannelInfo(id=cfg.qq_group_number, type=MessageType.CHANNEL),
        content=remove_format_codes(content)
    )
    server.dispatch_event(LiteralEvent("im_api.send_message"), (request,))

def transfer_to_matrix(server: PluginServerInterface | ServerInterface, content: str):
    """Send a message to the Matrix room.
    """
    if not isinstance(cfg.matrix_room_id, str) and cfg.matrix_room_id is not None:
        cfg.matrix_room_id = str(cfg.matrix_room_id)

    if cfg.matrix_room_id is None:
        raise TypeError('Config error!')

    request = SendMessageRequest(
        platforms={Platform.MATRIX},
        channel=ChannelInfo(id=cfg.matrix_room_id, type=MessageType.CHANNEL),
        content=remove_format_codes(content)
    )
    server.dispatch_event(LiteralEvent("im_api.send_message"), (request,))
