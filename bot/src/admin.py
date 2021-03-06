# -*- coding: utf-8 -*-
"""Untitled0.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1iPHZwFkfk3tZ85kTxNrOwfMyBRiU29sV
"""

import json 

class Intent:

    def __init__(self, tag, patterns, responses, context):
        self.tag = tag
        self.patterns = patterns
        self.responses = responses 
        self.context = context

def obtener_intent(intents, tag):
  for intent in intents:
    if intent.tag.lower() == tag.lower():
      return intent
  return None

def obtener_json():  
  with open('src/intents.json', encoding='utf8') as file:
    data = json.load(file)
  intents = []
  for intent in data['intents']:
    get_intent = Intent(intent['tag'], intent['patterns'], intent['responses'], intent['context'])
    intents.append(get_intent)
  return intents

def json_default(object):
    return object.__dict__

def agregar_nuevo_intent(tag, pattern, responses):
  intents = obtener_json()
  intent : Intent = obtener_intent(intents, tag)
  if intent == None:
    intent = Intent(tag, [pattern], [responses], [""])
    intents.append(intent)
  else:
    intent.patterns.append(pattern)
    intent.responses.append(responses)
  data = {}
  data['intents'] = []
  for item in intents:
    json_object = json.dumps(item, default=json_default)
    print(json_object)
    data['intents'].append(item)
  json_data = json.dumps(data, default=json_default, indent=4)
  print(json_data)
  with open('src/intents.json', 'w') as file:
    file.write(json_data)

def get_tags():
  intents = obtener_json()
  tags = "Tags disponibles: \n"
  for intent in intents:
    tags += '\n\t' + intent.tag
  return tags

def get_responses_and_patterns(tag):
  intents = obtener_json()
  intent : Intent = obtener_intent(intents, tag)
  if intent == None:
    return "No eh aprendido informacion con el tag: " + str(tag)
  else:
    cadena = "Tag: " + str(tag) + "\n"
    cadena += "\tPreguntas: " + str(intent.patterns) + "\n"
    cadena += "\tRespuestas: " + str(intent.responses)
    return cadena

"""# Secci??n nueva"""