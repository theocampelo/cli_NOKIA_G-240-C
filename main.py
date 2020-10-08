from bs4 import BeautifulSoup as bs
import requests
import sys

# desabilita os avisos de certificado SSL inválido
requests.packages.urllib3.disable_warnings()

def err():
	print('Invalid parameters')
	quit()

if len(sys.argv) == 1:
	print('usage: main.py <HOST> <WAN_START>-<WAN_END> <LAN_START>-<LAN_END> <PROTOCOL>')
	print('ex:\n\t main.py 192.168.1.201 66330-66339 6660-6669 TCP\n\t main.py 192.168.10.2 8080-8080 8080-8080 TCP')
	print('valid protocol entries:\n\t TCP\n\t UDP\n\t TCP/UDP',end='\n\n')
	quit()
else:
	HOST = sys.argv[1]
	print('** HOST ->' + HOST)	

	wan_port = sys.argv[2]
	wan_splt = wan_port.split('-')
	print('** WAN PORTS ->' + str(wan_splt))

	WAN_PORT_START = wan_splt[0]
	WAN_PORT_END   = wan_splt[1]
	
	lan_port = sys.argv[3]
	lan_splt = lan_port.split('-')
	print('** LAN PORTS ->' + str(lan_splt))

	LAN_PORT_START = lan_port[0]
	LAN_PORT_END = lan_port[1]

	proto_str = str(sys.argv[4]).upper()
	if proto_str == 'TCP':
		PROTO = 'TCP'
	elif proto_str == 'UDP':
		PROTO = 'UDP'
	elif '/' in proto_str:
		if proto_str == 'TCP/UDP':
			PROTO = 'TCPorUDP'	
	else:
		err()

	# VALIDATE INPUTS -- TEST	
	print(str(type(HOST)) + '->' + HOST)
	print(str(type(WAN_PORT_START)) + '->' + WAN_PORT_START)
	print(str(type(WAN_PORT_END)) + '->' + WAN_PORT_END)
	print(str(type(LAN_PORT_START)) + '->' + LAN_PORT_START)
	print(str(type(LAN_PORT_END)) + '->' + LAN_PORT_END)
	print(str(type(PROTO)) + '->' + PROTO, end='\n')

url = 'https://192.168.1.254/'
session = requests.session()

headers_std = {
	'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:81.0) Gecko/20100101 Firefox/81.0'
}

headers_vhost = {
	'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:81.0) Gecko/20100101 Firefox/81.0',
	'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
	'Accept-Encoding':'gzip, deflate, br',
	'Connection':'keep-alive',
	'Content-Type':'application/x-www-form-urlencoded',
	'Host':'192.168.1.254',
	'Origin':'https://192.168.1.254',
	'Referer':'https://192.168.1.254/nat_glb.cgi?v=vhost',
	'Upgrade-Insecure-Requests':'1'
}

headers_add_vhost = {
	'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:81.0) Gecko/20100101 Firefox/81.0',
	'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
	'Accept-Encoding':'gzip, deflate, br',
	'Connection':'keep-alive',
	'Content-Type':'application/x-www-form-urlencoded',
	'Host':'192.168.1.254',
	'Origin':'https://192.168.1.254',
	'Referer':'https://192.168.1.254/nat_glb.cgi?v=add_vhost',
	'Upgrade-Insecure-Requests':'1'
}

print('* Checking connection with the router')
host_status = session.get(url, verify=False)
if int(host_status.status_code) == 200:
	print('* Success! Router is up and reachable', end='\n\n')

def login():
	global url
	global headers_std
	global session

	cgi = 'login.cgi'

	data = {
		'userhash':'PwdGep7A3OxgQyzHHrBpghnVmZxhHGTvjbVLlCptjCI.',	# esses valores são gerados pelo código da cgi do login
		'response':'53ItLLmtl8L8iWJaTyBVvHgFuh63F2Bw6l1Q4_IKkok.',	# hardcoded não funcionam depois que os tokens expiram
		'nonce':'BUZQttpvPDRPgwK-3QuXlpv0ohrKhfnNk96XNt2OPKs.',
		'enckey':'JzLBX9KUcRwSzjTPi-bQRw..',
		'enciv':'CdOFNZZdASMt5nycQk2jkg'
	}

	post_response = session.post(url + cgi, data=data, headers=headers_vhost, verify=False)
	print('* Logged in web access')
	print(str(session.cookies))

	return post_response

def get_page():
	global url
	global headers_std
	global session

	cgi = 'nat_glb.cgi?v=vhost'
	full_addr = url + cgi
	
	port_page = session.get(full_addr, verify=False)

	return port_page

def forward_port(HOST, WAN_PORT_START, WAN_PORT_END, LAN_PORT_START, LAN_PORT_END, PROTO):
	global url
	global headers_add_vhost
	global session
	
	cgi = 'nat_glb.cgi?v=add_vhost'

	form = {
		'csrf_token':'',
		'passwd_token_value':'',
		'appname':'0',
		'nat_value':'',
		'etPortStart':WAN_PORT_START,
		'etPortEnd':WAN_PORT_END,
		'inPortStart':LAN_PORT_START,
		'inPortEnd':LAN_PORT_END,
		'servername':'0',
		'serverIp':HOST,
		'proto':PROTO,
		'en_map':'on',
		'wanif':'ip,1,1,1',	
	}
	print('** FORM ->\n' + str(form), end='\n\n')

	response = session.post(url + cgi, data=form, headers=headers_add_vhost, verify=False)
	
	return response

# terminar método delete
def delete_port():
	print('_delete_port')

	global url
	global session

	page = get_page()
	soup = bs(page.content, 'html.parser')
	
	del_btn = ''
	print(soup.prettify())
	for a in soup.findAll('a', href=True, text=True):
		del_btn = a['href']
		print(del_btn)

login()
print('* Requesting port forwarding')
forward = forward_port(HOST, WAN_PORT_START, WAN_PORT_END, LAN_PORT_START, LAN_PORT_END, PROTO)

print(get_page().content)	# teste de login (busca a página depois de logado)

print(f'* Post request status: {forward.status_code}')
print('\nDone')

session.close()
