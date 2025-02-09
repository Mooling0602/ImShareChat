import json

def format_data(content: list) -> str:
    texts = []
    for item in content:
        if item['type'] == 'text':
            texts.append(item['data']['text'])
        elif item['type'] == 'face':
            try:
                face_text = item['data']['raw']['faceText']
            except KeyError:
                face_text = None
            if face_text:
                texts.append(face_text)
        elif item['type'] == 'record':
            summary = "[语音]"
            texts.append(summary)
        elif item['type'] == 'image':
            summary = item['data']['summary']
            if summary == '':
                summary = "[图像]"
            texts.append(summary)
        elif item['type'] == 'json':
            data = json.loads(item['data']['data'])
            prompt = data['prompt']
            texts.append(prompt)
        elif item['type'] == 'at':
            qq_name = item['data']['qq']
            if qq_name == 'all':
                qq_name = '全体成员'
            texts.append('@' + qq_name)
        elif item['type'] == 'reply':
            texts.append('[引用其他消息]')
        else:
            texts.append('[未知]')
    return ''.join(texts)