import time
import im_share_chat.config.applying as cfg

from mcdreforged.api.all import *
from mcdreforged.command.builder.callback import CallbackError

from im_share_chat.utils import execute_if
from im_share_chat.config import load_config
from im_share_chat.core.listener import on_im_message
from im_share_chat.core.reporter import transfer_to_qq, transfer_to_matrix
from im_share_chat.rcon import query_rcon_result
from im_share_chat.command_source import ImCommandSource


builder = SimpleCommandBuilder()


def on_load(server: PluginServerInterface, prev_module):
    load_config(server)
    server.register_event_listener("im_api.message", on_im_message)
    if cfg.qq_group_number == '':
        server.logger.warning("Config missing: groups.qq")
    if cfg.matrix_room_id == '':
        server.logger.warning("Config missing: groups.matrix")
    configDir = server.get_data_folder()
    server.logger.info(f"ImShareChat config folder: {configDir}")
    server.register_event_listener("PlayerDeathEvent", on_player_death)
    server.register_event_listener("PlayerAdvancementEvent", on_player_advancement)
    builder.arg("command", QuotableText)
    builder.register(server)

def on_server_start_pre(server: PluginServerInterface):
    transfer_to_qq(server, cfg.on_server_start_pre_format)
    transfer_to_matrix(server, cfg.on_server_start_pre_format)

def on_server_startup(server: PluginServerInterface):
    if cfg.on_player_death is True or cfg.on_player_advancement is True:
        if "mg_events" not in server.get_plugin_list():
            server.logger.warning("Dependency missing: enabled at least one option in transfer_game_event_to_im, but mg_events not found.")
    transfer_to_qq(server, cfg.on_server_startup_format)
    transfer_to_matrix(server, cfg.on_server_startup_format)

@execute_if(lambda: cfg.on_player_death is True)
def on_player_death(server: PluginServerInterface, player, event, content):
    player: str = player
    event: str = event
    for i in content:
        if i.locale == 'zh_cn':
            transfer_to_qq(server, i.raw)
            transfer_to_matrix(server, i.raw)

@execute_if(lambda: cfg.on_player_advancement is True)
def on_player_advancement(server: PluginServerInterface, player, event, content):
    player: str = player
    event: str = event
    for i in content:
        if i.locale == 'zh_cn':
            transfer_to_qq(server, i.raw)
            transfer_to_matrix(server, i.raw)


@builder.command("!!ichat rcon <command>")
def on_command_rcon(src: CommandSource, ctx: CommandContext):
    if not isinstance(src, ImCommandSource):
        src.reply("该命令只能在外部Im平台中使用！")
        return
    rcon_command = ctx['command']
    server = src.get_server()
    src.reply(
        "[ImShareChat]\n" +
        "- 警告：\n" +
        "Rcon查询是实验性功能，任何人都可使用！\n" +
        "请不要在生产环境使用此开发中版本，等待正式更新！\n" +
        "- 备注：\n" +
        f"用户 - {src.user_id}\n" +
        f"指令内容 - {rcon_command}\n"
    )
    resp = query_rcon_result(server, rcon_command)
    result = None
    for attempt in range(3):
        try:
            result = resp.get_return_value()
            break
        except (CallbackError, RuntimeError):
            if attempt == 2:
                raise
            time.sleep(0.1)
    src.reply(f"[ImShareChat] 命令返回结果: \n{result}")

def on_player_joined(server: PluginServerInterface, player: str, info: Info):
    transfer_to_qq(server, cfg.on_player_joined_format.format(player=player))
    transfer_to_matrix(server, cfg.on_player_joined_format.format(player=player))

def on_user_info(server: PluginServerInterface, info: Info):
    if info.is_player and not info.content.startswith('!!'):
        player = info.player
        message = info.content
        content = cfg.chat_format_game.format(player=player, message=message)
        transfer_to_qq(server, content)
        transfer_to_matrix(server, content)

def on_player_left(server: PluginServerInterface, player: str):
    transfer_to_qq(server, cfg.on_player_left_format.format(player=player))
    transfer_to_matrix(server, cfg.on_player_left_format.format(player=player))

def on_server_stop(server: PluginCommandSource, return_code: int):
    if return_code != 0:
        transfer_to_qq(server, cfg.on_server_crash_format)
        transfer_to_matrix(server, cfg.on_server_crash_format)
    else:
        transfer_to_qq(server, cfg.on_server_stop_format)
        transfer_to_matrix(server, cfg.on_server_stop_format)
