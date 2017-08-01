from flask import Flask
import random as ran
import requests as r
import pandas as pd
import string
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


URL = 'https://api.whatdoestrumpthink.com/api/v1/quotes'

def cwid():
    return ''.join([ran.choice(string.ascii_uppercase) for i in range(5)])

def generate_random_comments(symbol):
    data = r.get(URL)
    quotes = data.json().get('messages').get('personalized')

    comments = []
    for i in range(ran.randint(1,10)):
        curcomment = {'user':cwid(), 'comment': "{symbol} {trump}".format(symbol = symbol, trump = ran.choice(quotes))}
        comments.append(curcomment)
    comments = pd.DataFrame(comments)
    return comments

@app.route('/<symbol>')
def ask_trump(symbol):
    quotes = generate_random_comments(symbol)
    return quotes.to_json(orient = 'records')

if __name__=='__main__':
    app.run(host='0.0.0.0', port=5000)
