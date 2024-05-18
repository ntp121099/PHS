import requests
import os
def get_token_id():
	path = os.path.dirname(__file__)[0:len(os.path.dirname(__file__))-len('facebook_api')]
	f = open(path+'token_id_telegram.txt','r+',encoding='utf-8')
	data = f.read().replace('\n','')
	data_split = data.split('|')
	TOKEN = data_split[0]
	ID = data_split[1]
	return TOKEN,ID
def upload_file(path_file):
	TOKEN,ID = get_token_id()
	url = "https://api.telegram.org/bot"+TOKEN+"/sendDocument"
	payload={'chat_id': ID}
	files=[
	('document',(path_file,open(path_file,'rb'),'application/zip'))
	]
	headers = {}
	response = requests.request("POST", url, headers=headers, data=payload, files=files)
	# print(response.json())
def send_message(message):
	TOKEN,ID = get_token_id()
	url = "https://api.telegram.org/bot" + TOKEN + "/sendMessage?chat_id=" + ID + "&text="+message+"&parse_mode=HTML"
	p = requests.post(url)
	# print(p.text)
# send_message('hehe')
# upload_file('he.txt')

# print(get_token_id())