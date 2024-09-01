import requests
import time
from threading import Thread
import traceback
import json
from datetime import datetime
from collections import defaultdict
import model
import user

first_id = "chatcmpl-7FunqjtgiPrQhBR5hnOoOlqDsdxZr"

sendmslist=[]
sendlist = {}
banlist = []

with open("settings.json", "r", encoding="utf-8") as f:
    settings = json.load(f)
    __uid = settings['__uid']
    __cookie = settings['__cookie']
    __ask = settings['__ask']
    model.API_SECRET_KEY = settings['API_SECRET_KEY']

with open("ban.json", "r", encoding="utf-8") as ban:
	banlist = json.load(ban)


login_cookie = f'__client_id={__cookie}; login_referer=https%3A%2F%2Fwww.luogu.com.cn%2F; _uid={str(__uid)}'
csrf_token = '自动分配'
ad = '暂时没有'
help = '''1. 普通回答(model = gpt-4o-mini)
2. 传话
#传话 [对方UID] [问题]
3. API余额查询(请在有问题时使用)
#query
--------------
查看更新请输入“#更新”
查看关于请输入“#关于”
'''
gengxin = '''洛谷FunBot v2.1
Update date 2024/9/1
1. 更换使用GPT-4o-mini模型
2. 传话功能添加敏感词检测
3. 获取信息刷新速度从5s更为3s
将会持续更新
'''
about = '''时隔不知道多少天更新了……
不要问为什么，问就是这股风终究没被我带起来
作者：YuTianQwQ
访问洛谷Fun：https://luogu.fun
'''

is_ans = []  # 防止重复回答

gptuser = defaultdict(int)

def cut(obj, sec):
	return [obj[i:i + sec] for i in range(0, len(obj), sec)]

def sendms(ruid, msg):  # msgs是列表
	msgs=cut(msg, 250);
	if len(msgs) > 1:
		sendm(ruid, '发送的信息过长，已开启分段发送')
	for i in reversed(msgs):
		time.sleep(1)
		sendm(ruid, i)
		
def sendm(ruid, msg):
	sendmslist.append((ruid,msg))
	
def sendm2():
	print("sendm2线程，启动！")
	headers2 = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
		'_contentOnly': 'WoXiHuanFanQianXing',
		'x-luogu-type': 'content-only',
		'cookie': login_cookie,
		'x-requested-with': 'XMLHttpRequest',
		'referer': 'https://www.luogu.com.cn/',
		'x-csrf-token': csrf_token,
		"content-type": "application/json",
	}
	while True:
		if sendmslist==[]:
			continue
		ruid=sendmslist[-1][0]
		msg=sendmslist[-1][1]
		del sendmslist[-1]
		res_send = requests.post("https://www.luogu.com.cn/api/chat/new", headers=headers2, json={"user": ruid, "content": msg})
		if res_send.text != '{"_empty":true}':
			#ban(ruid)
			pass
		print('发送信息：', res_send.text)
		time.sleep(3)

def getcsrf():
	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE',
		'_contentOnly': 'WoXiHuanFanQianXing',
		'x-luogu-type': 'content-only',
		'cookie': login_cookie,
		'x-requested-with': 'XMLHttpRequest',
	}
	res2 = requests.get("https://www.luogu.com.cn/", headers=headers)
	# <meta name="csrf-token" content="1682209913:+IHBdXuEXdGyGjCgJFRKo/Ul3Yu3+AJhXC1qU8+CrC4=">
	res2 = res2.text
	csrftoken = res2.split("<meta name=\"csrf-token\" content=\"")[-1].split("\">")[0]
	print("csrftoken:", csrftoken)
	return csrftoken

def ToPaste(content):
	headers2 = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
		'_contentOnly': 'WoXiHuanFanQianXing',
		'x-luogu-type': 'content-only',
		'cookie': login_cookie,
		'x-requested-with': 'XMLHttpRequest',
		'referer': 'https://www.luogu.com.cn/',
		'x-csrf-token': csrf_token,
		"content-type": "application/json",
	}
	return1 = requests.post("https://www.luogu.com.cn/paste/new", headers=headers2, json={"public":'true',"data":content})
	retrun_data = return1.json()
	return "消息过长转换为链接https://www.luogu.com.cn/paste/" + retrun_data["id"]

def answermsg(uid, content):  # 这个模块主要用于多线程，回答后给sendms。
	print(str(uid) + " " + content)
	# try:
	if content[:3] == "#传话":#传话
		if model.if_msg(content.split(' ')[2]) == "true":
			sendms(uid,'检测到敏感信息，消息被驳回')
		else:
			sendms(uid,'消息发送成功，对方确认后可查看你的消息。')
			sendms(int(content.split(' ')[1]),'你有一条匿名信息，回复“#OK”即可查看，如有任何违反社区规则的信息本bot和其作者不承担相关责任')
			sendlist[int(content.split(' ')[1])] = content.split(' ')[2]
	elif content[:3] == "#OK":
		try:
			sendms(uid, "这是此bot代发送的匿名消息，本bot和其作者不承担相关责任\n" + sendlist[uid])
		except:
			sendms(uid, "出现错误，有可能你没有消息……")
	elif content == "help" or content == "Help":
		sendms(uid, help)
	elif content[:3] == "#更新":
		sendms(uid, gengxin)
	elif content[:3] == "#关于":
		sendms(uid, about)
	elif content == "#query":
		sendms(uid, "正在查询请稍等……")
		get = model.credit_grants()
		sendms(uid, f"服务器 API 余额剩余：{get}")
	else:
		with open("users.json", "r", encoding="utf-8") as f:
			msg = json.load(f)
		if not(str(uid) in msg):
			print(f"{uid} 注册成功")
			user.add_new(str(uid), __ask)
		user.change(uid, content)
		with open("users.json", "r", encoding="utf-8") as f:
			msg = json.load(f)
		tmp = msg[str(uid)]
		print(tmp)
		content_gpt = model.chat_gpt('gpt-4o-mini', tmp) # 可修改为你的提示词
		print(content_gpt)
		user.change_system(uid, content_gpt)
		if len(content_gpt) > 250:
			content_gpt = ToPaste(content_gpt)
		sendms(uid, content_gpt)
	# except:
	# 	print("Error")
#sendms(uid, gpt35("字数限制在250字以内，问题："+content.split(' ')[1],uid))
def auto_replace_csrf_token():
	print("auto_replace_csrf_token，启动！")
	global csrf_token
	while True:
		csrf_token = getcsrf()
		print("csrftoken更换成功!", csrf_token)
		time.sleep(3600)


##################

headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE',
	'_contentOnly': 'WoXiHuanFanQianXing',
	'x-luogu-type': 'content-only',
	'cookie': login_cookie,
	'x-requested-with': 'XMLHttpRequest',
}
Thread(target=auto_replace_csrf_token).start()
time.sleep(2)#等待csrftoken更换
Thread(target=sendm2).start()
time.sleep(2)
sendm(655082, '开机')

while True:
	try:
		while True:

			time.sleep(2)
			res = requests.get('https://www.luogu.com.cn/chat', headers=headers)
			resjson = res.json()
			print(resjson['code'])
			for key, value in gptuser.items():
				print(f"用户: {key}, 次数: {value}",end = ",")
			print("")
			for i in resjson['currentData']['latestMessages']['result']:
				# print(i['id'],i['time'],i['sender']['uid'],"->",i['receiver']['uid'],i['content'])
				if ((i['receiver']['uid'] == __uid)  and (not i['id'] in is_ans)):
					is_ans.append(i['id'])
					Thread(target=answermsg, args=(i['sender']['uid'], i['content'])).start()

					time.sleep(1)  

					# sendms(i['sender']['uid'],answer(i['content']))
					# is_answer_id.append(i['id'])
	except Exception as e:
		traceback.print_exc()