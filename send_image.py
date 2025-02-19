import requests
import json
import base64
import hmac
import hashlib
import time

with open('current_index.txt', 'r') as f:
    current_index = int(f.read().strip())

with open('images.json', 'r') as f:
    images = json.load(f)

image_url = images[current_index % len(images)]

access_token = 'f079ef11ed5fd3401f05edb3fc1932ff35ef8b05f9fa3a06077ffaaf6319b8d6'

secret = 'SECbcc381f4ea2d4aaa912b6a4d3bc09e89f3d094ca559daa014b98cacfb66006e7'

picURL = "https://q5.itc.cn/q_70/images03/20240612/5e4ff010635c4a0389e03a305271f8b2.jpeg"

timestamp = str(round(time.time() * 1000))

string_to_sign = '{}\n{}'.format(timestamp, secret)

sign = hmac.new(secret.encode('utf-8'), string_to_sign.encode('utf-8'), digestmod=hashlib.sha256).digest()
sign = base64.b64encode(sign).decode('utf-8')

webhook_url = 'https://oapi.dingtalk.com/robot/send?access_token={}&timestamp={}&sign={}'.format(access_token, timestamp, sign)

# msg = {
#         'msgtype':'text',
#         'text':{
#             'content': '要发送的文字'
#         }
#     }
msg = {
        "msgtype": "image",
        "image": {
            "picURL": image_url
    }
}

response = requests.post(webhook_url, data=json.dumps(msg), headers={'Content-Type': 'application/json'})

print(response.json())

print(response.status_code)

print(response.text)
#下标自增
new_index = current_index + 1
with open('current_index.txt', 'w') as f:
    f.write(str(new_index))
