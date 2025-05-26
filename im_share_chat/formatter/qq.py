"""Format QQ message data.
"""
import json


def format_data(content: list) -> str:  # type: ignore
    """美化消息内容

    Args:
        content (list): message.content

    Returns:
        str: 美化后的消息内容文本
    """

    processMap = {  # type: ignore  #pylint: disable=invalid-name
        'text': lambda x: x['data']['text'],  # type: ignore
        'face': lambda x: x['data']['raw'].get('faceText', ''),  # type: ignore
        'record': lambda x: "[语音]",  # type: ignore
        'image': lambda x: (  # type: ignore
            x['data']['summary'] if x['data']['summary'] != '' else "[图像]"
        ),  # type: ignore
        'json': lambda x: json.loads(x['data']['data'])['prompt'],  # type: ignore
        'at': lambda x: (  # type: ignore
            '@' + (x['data']['qq'] if x['data']['qq'] != 'all' else '全体成员')),  # type: ignore
        'reply': lambda x: '[引用其他消息]',  # type: ignore
    }

    def __processData(subcontent)->str:  # type: ignore  # pylint: disable=invalid-name
        """__Description__
        """
        return processMap.get(subcontent["type"], lambda x: '')(subcontent)  # type: ignore

    texts = list(map(__processData, content))  # type: ignore

    return ''.join(texts)
