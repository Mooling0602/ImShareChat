"""ImCommandSource for mcdr plugins to handle commands from im chat messages.
"""
import im_share_chat.config.applying as cfg 

from typing import override
from mcdreforged.api.all import PluginCommandSource, ServerInterface, CommandSource
from mcdreforged.utils import class_utils
from mcdreforged.utils.types.message import MessageText
from im_api.drivers.base import Platform
from im_api.models.message import Message
from im_share_chat.core.reporter import transfer_to_matrix, transfer_to_qq


class ImCommandSource(PluginCommandSource):
    """Main class of ImCommandSource.
    """
    def __init__(  # pylint: disable=super-init-not-called
        self,
        server: 'ServerInterface',
        im_message: Message,
        platform: Platform
    ):
        self.__server = server.as_basic_server_interface()
        self.user_id: str = im_message.user.id
        self.__content: str = im_message.content
        self.__platform: Platform = platform

    @override
    def get_server(self) -> 'ServerInterface':
        return self.__server

    @override
    def get_permission_level(self) -> int:
        if not cfg:
            return 0
        if f"{self.__platform.value}!{self.user_id}" in cfg.perm_owners:
            return 4
        elif f"{self.__platform.value}!{self.user_id}" in cfg.perm_admins:
            print(self.__platform.value, self.user_id, cfg.perm_admins)
            return 3
        elif f"{self.__platform.value}!{self.user_id}" in cfg.perm_helpers:
            return 2
        elif f"{self.__platform.value}!{self.user_id}" in cfg.perm_users:
            return 1
        else:
            return 0

    @override
    def reply(self, message: MessageText, **kwargs: object) -> None:
        match self.__platform:
            case Platform.MATRIX:
                self.__server.logger.info("Sending command response to matrix...")
                transfer_to_matrix(self.__server, str(message))
            case Platform.QQ:
                self.__server.logger.info("Sending command response to qq...")
                transfer_to_qq(self.__server, str(message))
            case _:
                raise NotImplementedError()

    def __eq__(self, other: CommandSource):
        return isinstance(other, ImCommandSource) and self.__platform == other.__platform  # pylint: disable=protected-access

    def __str__(self):
        return 'ImMessage {}'.format(self.__content)  # pylint: disable=consider-using-f-string

    def __repr__(self):
        return class_utils.represent(self, {  # type: ignore
            'user_id': self.user_id,
            'content': self.__content,
            'platform': self.__platform.value
        })
