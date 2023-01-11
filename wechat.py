from datetime import date, datetime
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import math


today = datetime.now()
start_date = os.environ['START_DATE']
app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]
user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]

def get_action():
  url = "https://api.github.com/repos/Gainss/Kernel-schedule/releases/latest"
  res = requests.get(url).json()
  kernel = res['assets'][0]
  return res['name'], kernel['browser_download_url']

def get_size():
  url = "https://api.github.com/repos/Gainss/Kernel-schedule/releases/latest"
  res = requests.get(url).json()
  kernel = res['assets'][0]
  return kernel['size']

def get_conversion():
  size = get_size() / 1048576
  return math.floor(size)

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

client = WeChatClient(app_id, app_secret)
wm = WeChatMessage(client)
name, url = get_action()
data = {"name":{"value":name},"url":{"value":url},"size":{"value":get_conversion()},"run_days":{"value":get_count()}}
res = wm.send_template(user_id, template_id, data)
print(res)
