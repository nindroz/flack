import os

from flask import Flask,render_template,request,session,redirect, url_for, jsonify
from flask_socketio import SocketIO, emit
from collections import deque

app = Flask(__name__)
app.config["SECRET_KEY"] = "fdjdkfksajfasdj"
socketio = SocketIO(app)

channels=[]
messages=[]

@app.route("/",methods=['GET',"POST"])
def index():
    #gets form 
    name=request.form.get("display")
    
    #makes sure that session is null if it doesent exist
    if(not("displayName" in session)):
        session["displayName"]=None
    
    #sets session and logs in
    if(session['displayName']==None):
        session['displayName']=name
        if(session["displayName"]==None):
            #loads page for first time when user hasnt submitted a name
            return render_template("index.html")
    return redirect(url_for('dashboard'))
    
   

@app.route("/dashboard",methods=['post','get'])
def dashboard():
    return render_template("dashboard.html",name=session['displayName'])

#test purposes
@app.route("/pop")
def pop():
    session.pop("displayName")
    return redirect('/')

@app.route("/getChannels",methods=['GET'])
def getChannels():
    return jsonify({"channels":channels})

@app.route("/clean")
def clean():
    channels.clear()
    return redirect(url_for("index"))

@app.route("/select", methods=['POST'])
def select():
    channel = request.form.get("channel")
    print("pp")
    print(channel)
    return "pp"


@socketio.on("make channel")
def channelM(data):
    name=data['name']
    print(f"Hello")
    #channels[name]=deque(maxlen=100)
    channels.append(name)
    emit("cast channel", {"channel": name}, broadcast=True)

@socketio.on("send message")
def message(data):
    msg=data['message']
    #channels[data['channel']].append(msg)
    print(msg)
    emit("display message", {"message": msg},broadcast=True) 

@socketio.on("select channel")
def channel(data):
    print("pp")
    print(data["channel"])
    session['currentChannel']=data['channel']
    emit("show channel", {"channel": session["currentChannel"]})



if __name__ == '__main__':
    socketio.run(app)