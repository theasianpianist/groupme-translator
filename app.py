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
	global needsTranslate
	needsTranslate = False

	yuLoc = [m.start() for m in re.finditer('yu', msg)]
	if yuLoc:
		msg = replace_word("yu", "you", msg, yuLoc)
	YuLoc = [m.start() for m in re.finditer('Yu', msg)]
	if YuLoc:
		msg = replace_word("Yu", "You", msg, YuLoc)
	YULoc = [m.start() for m in re.finditer('YU', msg)]
	if YULoc:
		msg = replace_word("YU", "YOU", msg, YuLoc)

	litsLoc = [m.start() for m in re.finditer('lits', msg)]
	if litsLoc:
		msg = replace_word("lits", "literally", msg, litsLoc)
	LitsLoc = [m.start() for m in re.finditer('Lits', msg)]
	if LitsLoc:
		msg = replace_word("Lits", "Literally", msg, LitsLoc)
	LITSLoc = [m.start() for m in re.finditer('LITS', msg)]
	if LitsLoc:
		msg = replace_word("LITS", "LITERALLY", msg, LitsLoc)

	axLoc = [m.start() for m in re.finditer('ax', msg)]
	if axLoc:
		msg = replace_word("ax", "actually", msg, axLoc)
	AxLoc = [m.start() for m in re.finditer('Ax', msg)]
	if AxLoc:
		msg = replace_word("Ax", "Actually", msg, AxLoc)
	AXLoc = [m.start() for m in re.finditer('AX', msg)]
	if AxLoc:
		msg = replace_word("AX", "ACTUALLY", msg, AxLoc)

	gclLoc = [m.start() for m in re.finditer('gcl', msg)]
	if gclLoc:
		msg = replace_word("gcl", "gfc", msg, gclLoc)
	GCLLoc = [m.start() for m in re.finditer('GCL', msg)]
	if GCLLoc:
		msg = replace_word("GCL", "GFC", msg, GCLLoc)
	GclLoc = [m.start() for m in re.finditer('Gcl', msg)]
	if GclLoc:
		msg = replace_word("Gcl", "Gfc", msg, GclLoc)

	lamoLoc = [m.start() for m in re.finditer('lamo', msg)]
	if lamoLoc:
		msg = replace_word("lamo", "lmao", msg, lamoLoc)
	LamoLoc = [m.start() for m in re.finditer('Lamo', msg)]
	if LamoLoc:
		msg = replace_word('Lamo', 'Lmao', msg, LamoLoc)
	LAMOLoc = [m.start() for m in re.finditer('LAMO', msg)]
	if LAMOLoc:
		msg = replace_word('LAMO', 'LMAO', msg, LAMOLoc)

	if needsTranslate:
		send_message(msg)

def replace_word(word, replacement, oMsg, locList):
	global needsTranslate
	needsTranslate = False
	msg = oMsg
	length = len(word)
	for loc in reversed(locList):
		if loc == 0 or msg[loc - 1] in [".", ",", ";", "!", ":", " "]:
			msg = msg[0:loc] + replacement + msg[loc + length:]
			needsTranslate = True
	return msg


def send_message(msg):
  url  = 'https://api.groupme.com/v3/bots/post'

  data = {
          'bot_id' : os.getenv('GROUPME_BOT_ID'),
          'text'   : msg,
         }
  request = Request(url, urlencode(data).encode())
  json = urlopen(request).read().decode()	