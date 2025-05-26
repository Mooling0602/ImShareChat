"""Plugin entrypoint.
"""
import time

from mcdreforged.api.all import Info, PluginCommandSource, PluginServerInterface, \
    SimpleCommandBuilder, CommandSource, CommandContext, QuotableText
from mcdreforged.command.builder.callback import CallbackError

import im_share_chat.config.applying as cfg
from im_share_chat.command_source import ImCommandSource
from im_share_chat.config import load_config
from im_share_chat.core.listener import on_im_message
from im_share_chat.core.reporter import transfer_to_matrix, transfer_to_qq
from im_share_chat.rcon import query_rcon_result  # type: ignore
from im_share_chat.utils import execute_if


builder: SimpleCommandBuilder = SimpleCommandBuilder()


def on_load(server: PluginServerInterface, prev_module):  # type: ignore  # pylint: disable=unused-argument
    """__Description__
    """
    load_config(server)
    server.register_event_listener("im_api.message", on_im_message)  # type: ignore
    if cfg.qq_group_number == '':
        server.logger.warning("Config missing: groups.qq")
    if cfg.matrix_room_id == '':
        server.logger.warning("Config missing: groups.matrix")
    configDir = server.get_data_folder()  # pylint: disable=invalid-name
    server.logger.info(f"ImShareChat config folder: {configDir}")
    server.register_event_listener("PlayerDeathEvent", on_player_death) # type: ignore
    server.register_event_listener("PlayerAdvancementEvent", on_player_advancement) # type: ignore
    builder.arg("command", QuotableText)
    builder.register(server)


def on_server_start_pre(server: PluginServerInterface):
    """__Description__
    """
    transfer_to_qq(server, cfg.on_server_start_pre_format) # type: ignore
    transfer_to_matrix(server, cfg.on_server_start_pre_format) # type: ignore


def on_server_startup(server: PluginServerInterface):
    """__Description__
    """
    if cfg.on_player_death is True or cfg.on_player_advancement is True:
        if "mg_events" not in server.get_plugin_list():
            server.logger.warning(
                "Dependency missing: enabled at least one option "
                "in transfer_game_event_to_im, but mg_events not found."
            )
    transfer_to_qq(server, cfg.on_server_startup_format) # type: ignore
    transfer_to_matrix(server, cfg.on_server_startup_format) # type: ignore


@execute_if(lambda: cfg.on_player_death is True)
def on_player_death(server: PluginServerInterface, player, event, content): # type: ignore
    """__Description__
    """
    player: str = player # type: ignore
    event: str = event # type: ignore
    for i in content: # type: ignore
        if i.locale == 'zh_cn': # type: ignore
            transfer_to_qq(server, i.raw) # type: ignore
            transfer_to_matrix(server, i.raw) # type: ignore


@execute_if(lambda: cfg.on_player_advancement is True)
def on_player_advancement(server: PluginServerInterface, player, event, content): # type: ignore
    """__Description__
    """
    player: str = player # type: ignore
    event: str = event # type: ignore
    for i in content: # type: ignore
        if i.locale == 'zh_cn': # type: ignore
            transfer_to_qq(server, i.raw) # type: ignore
            transfer_to_matrix(server, i.raw) # type: ignore


@builder.command("!!ichat rcon <command>") # type: ignore
def on_command_rcon(src: CommandSource, ctx: CommandContext):
    """__Description__
    """
    if not isinstance(src, ImCommandSource):
        src.reply("该命令只能在外部Im平台中使用！") # type: ignore
        return
    rcon_command = ctx['command']
    server = src.get_server()
    for i in [
        "op",
        "ban",
        "pardon",
        "whitelist",
        "stop"
    ]:
        if i in rcon_command.lower():
            src.reply("[ImShareChat] 不允许通过Rcon执行高风险操作如关闭服务器等！")
            return
    src.reply(
        "[ImShareChat]\n" +
        "- 警告：\n" +
        "Rcon查询是实验性功能，任何人都可使用！\n" +
        "请不要在生产环境使用此开发中版本，等待正式更新！\n" +
        "- 备注：\n" +
        f"用户 - {src.user_id}\n" +
        f"指令内容 - {rcon_command}\n"
    )
    resp = query_rcon_result(server, rcon_command) # type: ignore
    result = None
    for attempt in range(3):
        try:
            result = resp.get_return_value() # type: ignore
            break
        except (CallbackError, RuntimeError):
            if attempt == 2:
                raise
            time.sleep(0.1)
    src.reply(f"[ImShareChat] 命令返回结果: \n{result}")


def on_player_joined(server: PluginServerInterface, player: str, info: Info):  # pylint: disable=unused-argument
    """__Description__
    """
    transfer_to_qq(server, cfg.on_player_joined_format.format(player=player)) # type: ignore
    transfer_to_matrix(server, cfg.on_player_joined_format.format(player=player)) # type: ignore


def on_user_info(server: PluginServerInterface, info: Info):
    """__Description__
    """
    if info.is_player and not info.content.startswith('!!'): # type: ignore
        player = info.player
        message = info.content
        content = cfg.chat_format_game.format(player=player, message=message) # type: ignore
        transfer_to_qq(server, content)
        transfer_to_matrix(server, content)


def on_player_left(server: PluginServerInterface, player: str):
    """__Description__
    """
    transfer_to_qq(server, cfg.on_player_left_format.format(player=player)) # type: ignore
    transfer_to_matrix(server, cfg.on_player_left_format.format(player=player)) # type: ignore


def on_server_stop(server: PluginCommandSource, return_code: int):
    """__Description__
    """
    if return_code != 0:
        transfer_to_qq(server, cfg.on_server_crash_format) # type: ignore
        transfer_to_matrix(server, cfg.on_server_crash_format) # type: ignore
    else:
        transfer_to_qq(server, cfg.on_server_stop_format) # type: ignore
        transfer_to_matrix(server, cfg.on_server_stop_format) # type: ignore
