import json

def format_data(content: list) -> str:
    """美化消息内容

    Args:
        content (list): message.content

    Returns:
        str: 美化后的消息内容文本
    """
    processMap = {
        'text': lambda x: x['data']['text'],
        'face': lambda x: x['data']['raw'].get('faceText', ''),
        'record': lambda x: "[语音]",
        'image': lambda x: x['data']['summary'] if x['data']['summary'] != '' else "[图像]",
        'json': lambda x: json.loads(x['data']['data'])['prompt'],
        'at': lambda x: '@' + (x['data']['qq'] if x['data']['qq'] != 'all' else '全体成员'),
        'reply': lambda x: '[引用其他消息]',
    }

    def __processData(subcontent)->str:
        return processMap.get(subcontent["type"], lambda x: '')(subcontent)

    texts = list(map(__processData, content))
        
    return ''.join(texts)