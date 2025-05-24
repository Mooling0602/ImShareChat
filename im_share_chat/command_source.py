from typing import override
from mcdreforged.api.all import *
from mcdreforged.utils import class_utils
from mcdreforged.utils.types.message import MessageText
from im_api.drivers.base import Platform
from im_api.models.message import Message
from im_share_chat.core.reporter import transfer_to_matrix, transfer_to_qq


class ImCommandSource(PluginCommandSource):
    def __init__(self, server: 'ServerInterface', im_message: Message, platform: Platform):
        self.__server = server.as_basic_server_interface()
        self.user_id = im_message.user.id
        self.__content = im_message.content
        self.__platform = platform

    @override
    def get_server(self) -> 'ServerInterface':
        return self.__server

    @override
    def get_permission_level(self) -> int:
        return 1

    @override
    def reply(self, message: MessageText, **kwargs) -> None:
        match self.__platform:
            case Platform.MATRIX:
                self.__server.logger.info("Sending command response to matrix...")
                transfer_to_matrix(self.__server, str(message))
            case Platform.QQ:
                self.__server.logger.info("Sending command response to qq...")
                transfer_to_qq(self.__server, str(message))

    def __eq__(self, other):
        return isinstance(other, ImCommandSource) and self.__platform == other.__platform
    
    def __str__(self):
        return 'ImMessage' if self.__content is None else 'ImMessage {}'.format(self.__content)
    
    def __repr__(self):
        return class_utils.represent(self, {
            'user_id': self.user_id,
            'content': self.__content,
            'platform': self.__platform
        })