import time
import math
import base64
import hmac, hashlib
import urllib.parse
import requests
import os
import json

# 빗썸 API 키 설정 (환경변수로부터 읽어옴)
BITHUMB_API_KEY = os.getenv('BITHUMB_API_KEY')
BITHUMB_SECRET = os.getenv('BITHUMB_SECRET')
BITHUMB_API_URL = 'https://api.bithumb.com'


class XCoinAPI:
	api_url = "https://api.bithumb.com"
	api_key = 'api_key'
	api_secret = 'api_secret'

	def __init__(self, api_key, api_secret):
		self.api_key = api_key
		self.api_secret = api_secret

	def body_callback(self, buf):
		self.contents = buf

	def microtime(self, get_as_float = False):
		if get_as_float:
			return time.time()
		else:
			return '%f %d' % math.modf(time.time())

	def usecTime(self) :
		mt = self.microtime(False)
		mt_array = mt.split(" ")[:2]
		return mt_array[1] + mt_array[0][2:5]

	def xcoinApiCall(self, endpoint, rgParams):
		# 1. Api-Sign and Api-Nonce information generation.
		# 2. Request related information from the Bithumb API server.
		#
		# - nonce: it is an arbitrary number that may only be used once.
		# - api_sign: API signature information created in various combinations values.

		str_data = urllib.parse.urlencode(rgParams)

		nonce = self.usecTime()

		data = endpoint + chr(0) + str_data + chr(0) + nonce
		utf8_data = data.encode('utf-8')

		key = self.api_secret
		utf8_key = key.encode('utf-8')

		h = hmac.new(bytes(utf8_key), utf8_data, hashlib.sha512)
		hex_output = h.hexdigest()
		utf8_hex_output = hex_output.encode('utf-8')

		api_sign = base64.b64encode(utf8_hex_output)
		utf8_api_sign = api_sign.decode('utf-8')

		headers = {
			"Accept": "application/json",
			"Content-Type": "application/x-www-form-urlencoded",
			"Api-Key": self.api_key,
			"Api-Nonce": nonce,
			"Api-Sign": utf8_api_sign
		}

		url = self.api_url + endpoint

		response = requests.post(url, headers=headers, data=rgParams)
		return response.json()




