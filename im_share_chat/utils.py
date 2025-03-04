from mcdreforged.api.all import *


def extract_file(server: PluginServerInterface, file_path, target_path):
    with server.open_bundled_file(file_path) as file_handler:
        with open(target_path, 'wb') as target_file:
            target_file.write(file_handler.read())