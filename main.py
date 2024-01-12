from openai import OpenAI
from elevenlabs import generate, play

import json

info = json.load(open('info.json'))