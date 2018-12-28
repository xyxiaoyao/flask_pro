# -*- coding: utf-8 -*-
from flask import Blueprint,render_template,request,jsonify
route_user = Blueprint( 'user_page',__name__ )

@route_user.route( "/login",methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("user/login.html")
    req = request.values
    print(req)
    resp = {'msg':"success",'code':200,'data':{}}
    login_name = req['login_name'] if 'login_name' else ''
    login_pwd = req['login_pwd'] if 'login_pwd' else ''
    if login_name is None or len(login_name) <1:
        resp['code'] = -1
        resp['msg'] = "name is not null"
        return jsonify(resp)

    if login_pwd == '' or len(login_pwd) <1:
        resp['code'] = -1
        resp['msg'] = "password is not null"
        return jsonify(resp)




@route_user.route( "/edit" )
def edit():
    return render_template( "user/edit.html" )

@route_user.route( "/reset-pwd" )
def resetPwd():
    return render_template( "user/reset_pwd.html" )