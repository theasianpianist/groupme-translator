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
  log('Recieved {}'.format(data))

  # We don't want to reply to ourselves!
  if data['name'] != 'Translator':
    parse_message(data['text'])


  return "ok", 200

def parse_message(oMsg):
	msg = oMsg
	global needsTranslate
	needsTranslate = False
	origWords = ["yu", "lits", "ax", "gcl", "lamo", "yur"]
	replaceWords = ["you", "literally", "actually", "gfc", "lmao", "your"]
	for i in range(len(origWords)):
		wordLoc = [m.start() for m in re.finditer(origWords[i], msg, re.IGNORECASE)]
		if wordLoc:
			msg = replace_word(origWords[i], replaceWords[i], msg, wordLoc)

	if needsTranslate:
		send_message(msg)

def replace_word(word, replacement, oMsg, locList):
	global needsTranslate
	punctuation = [" ", "~", "`", "!", "#", "$", "%", "^", "&", "*","(",")","_","-","=","+","[","{","]","}","|","\\",";",":","\'","\"",",","<",".",">","/","?"]
	needsTranslate = False
	msg = oMsg
	replaceLength = len(replacement)
	origLength = len(word)
	for loc in reversed(locList):
		if (loc == 0 or msg[loc - 1] in punctuation) and (loc + origLength >= len(msg) or msg[loc + origLength] in punctuation or msg[loc + origLength] == msg[loc + origLength - 1]):
			msg = msg[0:loc + origLength] + "x" * (abs(replaceLength - origLength)) + msg[loc + origLength:] #Inserts placeholder letters if replacement word is longer than original
			needsTranslate = True
			replaceIndex = 0
			allCaps = False
			for i in range(loc, loc + replaceLength):
				if 65 <= ord(msg[i]) <= 90: #If letter to be replaced is a capital, capitalize replacement letter
					msg = msg[0:i] + replacement[replaceIndex].capitalize() + msg[i + 1:]
					allCaps = True
				else:
					if replaceIndex >= origLength:
						if allCaps:
							msg = msg[0:i] + replacement[replaceIndex].capitalize() + msg[i+1:]
						else:
							msg = msg[0:i] + replacement[replaceIndex] + msg[i+1:]
					else:
						msg = msg[0:i] + replacement[replaceIndex] + msg[i+1:]
						allCaps = False
				replaceIndex += 1
	return msg


def send_message(msg):
  url  = 'https://api.groupme.com/v3/bots/post'

  data = {
          'bot_id' : os.getenv('GROUPME_BOT_ID'),
          'text'   : msg,
         }
  request = Request(url, urlencode(data).encode())
  json = urlopen(request).read().decode()

def log(msg):
  print(str(msg))
  sys.stdout.flush()

if __name__ == "__main__":
	parse_message("YU, ax lits gcl lamo")
	parse_message("\"yu\"")

