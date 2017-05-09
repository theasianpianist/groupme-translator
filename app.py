import os
import sys
import json
import re

from urllib.parse import urlencode
from urllib.request import Request, urlopen

from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['POST'])
def webhook():
  data = request.get_json()
  #log('Recieved {}'.format(data))

  # We don't want to reply to ourselves!
  if data['name'] != 'Translator':
    parse_message(data['text'])
    

  return "ok", 200

def parse_message(oMsg):
	msg = oMsg
	needsTranslate = False
	yuLoc = [m.start() for m in re.finditer('yu', msg)]
	if yuLoc:
		msg = replace_word("yu", "you", msg, yuLoc)
		needsTranslate = True
	YuLoc = [m.start() for m in re.finditer('Yu', msg)]
	if YuLoc:
		msg = replace_word("Yu", "You", msg, YuLoc)
		needsTranslate = True
	litsLoc = [m.start() for m in re.finditer('lits', msg)]
	if litsLoc:
		msg = replace_word("lits", "literally", msg, litsLoc)
		needsTranslate = True
	LitsLoc = [m.start() for m in re.finditer('Lits', msg)]
	if LitsLoc:
		msg = replace_word("Lits", "Literally", msg, LitsLoc)
		needsTranslate = True

	if needsTranslate:
		send_message(msg)

def replace_word(word, replacement, oMsg, locList):
	msg = oMsg
	length = len(word)
	for loc in reversed(locList):
		if msg[loc - 1] == " " or loc == 0:
			msg = msg[0:loc] + replacement + msg[loc + length:]
	return msg





def send_message(msg):
  url  = 'https://api.groupme.com/v3/bots/post'

  data = {
          'bot_id' : os.getenv('GROUPME_BOT_ID'),
          'text'   : msg,
         }
  request = Request(url, urlencode(data).encode())
  json = urlopen(request).read().decode()	