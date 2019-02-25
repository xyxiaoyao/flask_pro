from web.controllers.api import route_api
from  flask import request,jsonify,g
from application import  app,db
import requests,json
from common.models.member.Member import Member
from common.models.member.OauthMemberBind import OauthMemberBind
from common.models.food.WxShareHistory import WxShareHistory
from common.libs.member.MemberService import MemberService
from common.libs.Helper import getCurrentDate

@route_api.route('/member/login',methods = ["GET","POST"])
def login():
    resp = {'code': 200, 'msg': '登录成功~~', 'data': {}}
    req = request.values
    app.logger.info(req)

    code = req['code'] if 'code' in req else ""
    if not code or len(code)<1:
        resp['code'] = -1
        resp['msg'] = '需要code'
        return jsonify(resp)
    #获取openid 用户唯一标识
    openid = MemberService.getWeChatOpenId(code)

    if openid is None:
        resp['code'] = -1
        resp['msg'] = "调用微信出错"
        return jsonify(resp)

    #获取用户基本信息
    nickname = req['nickName'] if 'nickName' in req else ''
    sex = req['gender'] if 'gender' in req else 0
    avatar = req['avatarUrl'] if 'avatarUrl' in req else ''
    #判断是否已经注册过，注册了直接返回一些信息
    bind_info = OauthMemberBind.query.filter_by(openid=openid,type = 1).first()
    if not bind_info:
        #创建用户
        model_member = Member()
        model_member.nickname = nickname
        model_member.sex = sex
        model_member.avatar = avatar
        model_member.salt = MemberService.geneSalt()
        model_member.updated_time = model_member.created_time = getCurrentDate()
        db.session.add(model_member)
        db.session.commit()
        #创建绑定用户，后期删除小程序，直接判断是否绑定
        model_bind = OauthMemberBind()
        model_bind.member_id = model_member.id
        model_bind.type = 1
        model_bind.openid = openid
        model_bind.extra = ''
        model_bind.updated_time = model_bind.created_time = getCurrentDate()
        db.session.add(model_bind)
        db.session.commit()

        bind_info = model_bind
    member_info = Member.query.filter_by(id = bind_info.member_id).first()
    #进行md5加密
    token = "%s#%s" %(MemberService.geneAuthCode(member_info),member_info.id)
    resp['data'] = {"token":token,"nickname":nickname}

    return jsonify(resp)

@route_api.route('/member/check-reg',methods = ["GET","POST"])
def check_reg():
    resp = {'code': 200, 'msg': '登录成功~~', 'data': {}}
    req = request.values
    app.logger.info(req)

    code = req['code'] if 'code' in req else ""
    if code is None or len(code)<1:
        resp['code'] = -1
        resp['msg'] = '需要code'
        return jsonify(resp)

    # 获取openid 用户唯一标识
    openid = MemberService.getWeChatOpenId(code)
    if openid is None:
        resp['code'] = -1
        resp['msg'] = "调用微信出错"
        return jsonify(resp)
    # 判断是否已经注册过，注册了直接返回一些信息
    bind_info = OauthMemberBind.query.filter_by(openid=openid, type=1).first()
    if not bind_info:
        resp['code'] = -1
        resp['msg'] = "未绑定"
        return jsonify(resp)
    member_info = Member.query.filter_by(id = bind_info.member_id).first()
    if not member_info:
        resp['code'] = -1
        resp['msg'] = "未查询到绑定信息"
        return jsonify(resp)

    # 进行md5加密
    token = "%s#%s" % (MemberService.geneAuthCode(member_info), member_info.id)
    resp['data'] = {"token": token}

    return jsonify(resp)

@route_api.route('/member/share',methods = ["POST"])
def memberShare():
    resp = {'code': 200, 'msg': '分享成功~~', 'data': {}}
    req = request.values
    url = req['url'] if 'url' in req else ''
    member_info = g.member_info
    model_share = WxShareHistory()
    if model_share:
        model_share.member_id = member_info.id
    model_share.share_url = url
    model_share.created_time = getCurrentDate()
    db.session.add(model_share)
    db.session.commit()
    return jsonify(resp)

