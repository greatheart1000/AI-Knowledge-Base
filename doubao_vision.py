#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025/1/14 17:08
# @Author  : caijian
# @File    : doubao_vision.py
# @Software: PyCharm
from volcenginesdkarkruntime import Ark

client = Ark(
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    ak  = None,
    sk = None,
    api_key='f62bafd2-1269-4169-b072-7994b36541a7',
    region = "cn-beijing"
)
# Image input:
response = client.chat.completions.create(
    model="ep-20250114165957-cw22t",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "请你描述一下图片里的内容"},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "http://118.145.187.17:9001/api/v1/download-shared-object/aHR0cDovLzEyNy4wLjAuMTo5MDAwL2NhaWppYW4vJUU0JUJFJThCJUU1JUFEJTkwLnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPVdLRjhVQzEzVFdZMktJTUpYWDJZJTJGMjAyNTAxMTQlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjUwMTE0VDA5MzYwMVomWC1BbXotRXhwaXJlcz00MzE5OSZYLUFtei1TZWN1cml0eS1Ub2tlbj1leUpoYkdjaU9pSklVelV4TWlJc0luUjVjQ0k2SWtwWFZDSjkuZXlKaFkyTmxjM05MWlhraU9pSlhTMFk0VlVNeE0xUlhXVEpMU1UxS1dGZ3lXU0lzSW1WNGNDSTZNVGN6TmpnNU1EVXpOQ3dpY0dGeVpXNTBJam9pYldsdWFXOWhaRzFwYmlKOS5zSHdyZUMxMGEtNGI3cmZIbGpmWUhxeGt4Yml4cDV2NWVNa1ZyLUk5WXhGSXF5OHpZOFNVbHJROHd4a0ladGZqbnZ5MlFyZ09TdFdvV1JyaU1QSE9fdyZYLUFtei1TaWduZWRIZWFkZXJzPWhvc3QmdmVyc2lvbklkPW51bGwmWC1BbXotU2lnbmF0dXJlPTA2ODFmNDE4NzhjMmY2OGY2ZWRkMjk1NGU2MzZmZWQ4ZWU5YTk1ZDEwZDRmZDE3ZjZhN2FhM2VhZmYzMjI4Yjg"
                    }
                },
            ],
        }
    ],
    # 免费开启推理会话应用层加密，访问 https://www.volcengine.com/docs/82379/1389905 了解更多
    extra_headers={'x-is-encrypted': 'true'},
)
print(response.choices[0].message.content)