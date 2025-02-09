import im_share_chat.config.applying as cfg

from mcdreforged.api.all import *

from .default import *

def load_config(server: PluginServerInterface):
    config = server.load_config_simple('config.json', default_config)
    cfg.qq_group_number = config['groups']['qq']
    cfg.matrix_room_id = config['groups']['matrix']