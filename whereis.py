from datetime import datetime
from random import randint
import requests, json, redis
from bottle import response, auth_basic, request
import time

redis_host = ""
redis_port = 9999
redis_auth = ""

def get_user_data(user):
    rc = redis.StrictRedis(host=redis_host, port=redis_port, db=0, password=redis_auth)
    rdata1 = rc.get("whereis_" + user)
    empty={}
    if rdata1 == None:
        return empty
    rdata=json.loads(rdata1)
    return rdata

def whereis_check(user, pw):
    d = get_user_data(user)
    if pw == d["token"]:
        return True
    return False

def whereis_me():

    user=request.auth[0]
    d = get_user_data(user)

    try:
        payload=json.loads(request.body.read())
    except:
        return "error in request"

    try:
        new_info = payload["info"]
        d["info"] = new_info
    except:
        pass

    try:
        new_location = payload["location"]
        d["location"] = new_location
    except:
        pass

    try:
        new_timezone = payload["timezone"]
        d["timezone"] = new_timezone
    except:
        pass

    d["last_updated"] = str(int(time.time()))
    rc = redis.StrictRedis(host=redis_host, port=redis_port, db=0, password=redis_auth)
    rdata1 = rc.set("whereis_" + user, json.dumps(d))

    return dict({"message":"Info updated for " + user})

def whereis_getall():

    rc = redis.StrictRedis(host=redis_host, port=redis_port, db=0, password=redis_auth)
    user_list = rc.scan_iter("whereis_*")
    users = []
    for u in user_list:
        uname = u.replace("whereis_","")
        udata = whereis_getuser(uname)
        udata["id"] = uname
        users.append(udata)
    response.set_header('Access-Control-Allow-Origin', '*')
    response.add_header('Access-Control-Allow-Methods', 'GET, POST, PUT, OPTIONS')

    return dict(list=users)

def whereis_getuser(id):

    rdata = get_user_data(id)

    if rdata == {}:
        response.status = 404
        response.content_type = 'application/json'

        return dict( {"message": "error - no such user"})

    del rdata["token"]
    response.set_header('Access-Control-Allow-Origin', '*')
    response.add_header('Access-Control-Allow-Methods', 'GET, POST, PUT, OPTIONS')
    return dict(rdata)
