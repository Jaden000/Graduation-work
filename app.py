from flask import Flask,render_template,request,flash,jsonify
from xmlrpc.client import ServerProxy
import logging
import requests,json
import time
import json
app = Flask(__name__)
app.secret_key='some_secret'

#app.py

@app.route('/citations') # POST없이 페이지 접근 시,
def index():
    print('index')
    return render_template("/mainpage.html") # rendering

@app.route('/citations',methods=['POST']) # POST로 페이지 접근 시,
def post():
    
    ret = ""   

    data = request.get_json() # data from ajax 내 js의 ajax..그니까 웹에서 서버로 보내는.
    # print(data)
    print(json.dumps(data, indent="\t") ) ##json파일 보기 좋게 print
    keywords = data['inputs']
    sortingmethod= data['sortingmethod']
    dateRange = data['dateRange']
    fieldsOfStudy = data['fieldsOfStudy']

    server_url='http://10.100.54.166:5000/citations'
    org={'keywords':keywords, 'sortingmethod': sortingmethod, 'fieldsOfStudy': fieldsOfStudy, 'dateRange': dateRange}
    org=json.dumps(org)
    headers = {'Content-Type': 'application/json; charset=utf-8'}

    try:
        response=requests.post(url=server_url,data=org,headers=headers)
        ret=response.content.decode('utf-8') ## ret json
        print(ret)
    except requests.exceptions.ConnectionError as e:
        ret = json.dumps({'is_error':'503 Service Unavailable'})
    ret = json.loads(ret)
    return jsonify(request='success',result=ret)

@app.route('/citations/mainpage') #그냥 이 페이지 접근 시,
def main():
    print('main')
    return render_template("/mainpage.html") 
# methods=['GET'])
# def getmaindata():
    

if __name__=='__main__':
    app.run(host='0.0.0.0', port=5100, debug=True)
