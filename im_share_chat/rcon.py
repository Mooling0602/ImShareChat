from typing import Optional
from concurrent.futures import ThreadPoolExecutor
from mcdreforged.api.all import *
from im_share_chat.utils import psi


def handle_rcon_requests(src: CommandSource, cmd: str):
    psi.execute_command(f"!!ichat rcon {cmd}", src)


@new_thread('RconQueryThread')
def query_rcon_result(
        server: PluginServerInterface | ServerInterface,
        command: str,
        reconnect_after: Optional[int | float] = 0.5,
        timeout: Optional[int | float] = 1
) -> str | None:
    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(server.rcon_query, command)
        try:
            result = future.result(timeout=reconnect_after)
        except TimeoutError:
            if server.get_mcdr_language() == "zh_cn":
                server.logger.warning("RCON查询超时，需要重建MCDR与服务端之间的连接。")
            else:
                server.logger.warning("RCON query timeout, need to reopen the connection between MCDR and the server.")
            try:
                server._mcdr_server.connect_rcon()
                result = future.result(timeout=timeout)
            except TimeoutError as exc:
                if server.get_mcdr_language() == "zh_cn":
                    raise TimeoutError("RCON查询长时间无响应！") from exc
                else:
                    raise TimeoutError("Long time no response for RCON query!") from exc
    return result