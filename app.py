from flask import Flask, json
from flask import request
from flask import jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
app = Flask(__name__)
CORS(app)
@app.route("/fetchUrl", methods=['GET', 'OPTIONS'])
def hello_world():
    m = request.args.get('url', '')
    print(m)
    try:
        r = requests.get(m)
        if r.status_code ==200:
            s = BeautifulSoup(r.content,"lxml")
            metas = s.find_all('meta')
            x = {}
            for m in metas:
                if not bool(m.get('property')):
                    continue
                key = m.get('property')
                try:
                    key =key.lstrip('og:')
                except:
                    pass
                if key == "image":
                    image = {"url":m.get('content')}
                    x["image"] = image
                    continue
                x[key] = m.get('content')
            print(x)
            lo = {
            "success" : 1,
            # "link":m,
            'meta':x
            }   
            print(lo)
            res = jsonify(lo)
            return res
        else:
            raise IndexError
    except:
        lo = { 'status':0}
        res = jsonify(lo)
        return res
