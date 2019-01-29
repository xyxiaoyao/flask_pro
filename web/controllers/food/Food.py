# -*- coding: utf-8 -*-
from flask import Blueprint, request, redirect, jsonify
from sqlalchemy import or_

from common.libs.Helper import (ops_render, iPagination, getDictFilterField,getCurrentDate)
from common.libs.UrlManager import UrlManager
from common.models.food.Food import Food
from common.models.food.FoodCat import FoodCat
from application import app,db
route_food = Blueprint( 'food_page',__name__ )

@route_food.route( "/index")
def index():
    resp_data={}
    req = request.values
    app.logger.info(request.full_path)
    page = int(req['p'] if ('p' in req and req['p']) else 1)
    query = Food.query
    if 'mix_kw' in req:
        rule = or_(Food.name.ilike("%{0}%".format(req['mix_kw'])), Food.tags.ilike("%{0}%".format(req['mix_kw'])))
        query = query.filter(rule)

    if 'status' in req and int(req['status'])>-1:
        query = query.filter(Food.status == int(req['status']))

    if 'cat_id' in req and int(req['cat_id'])>0:
        query = query.filter(Food.cat_id == int(req['cat_id']))
    page_params = {
        'total':query.count(),
        'page_size':app.config['PAGE_SIZE'],
        'page':page,
        'display':app.config['PAGE_DISPLAY'],
        'url':request.full_path.replace('&p={}'.format(page),"")
    }
    pages = iPagination(page_params)
    offset = (page-1) * app.config["PAGE_SIZE"]
    list = query.order_by(Food.cat_id.desc()).offset(offset).limit(app.config['PAGE_SIZE']).all()
    cat_mapping = getDictFilterField(FoodCat, FoodCat.id, "id", [])
    resp_data['list'] = list
    resp_data['pages'] = pages
    resp_data['search_con'] = req
    resp_data['status_mapping'] = app.config['STATUS_MAPPING']
    resp_data['cat_mapping'] = cat_mapping
    app.logger.info(req)
    resp_data['current'] = 'index'
    return ops_render( "food/index.html",resp_data)

@route_food.route( "/info" )
def info():
    resp_data = {}
    req = request.args
    id = int(req.get("id", 0))
    reback_url = UrlManager.buildUrl("/food/index")

    if id < 1:
        return redirect(reback_url)

    info = Food.query.filter_by(id=id).first()
    if not info:
        return redirect(reback_url)
    resp_data['info'] = info
    resp_data['current'] = 'index'
    return ops_render( "food/info.html",resp_data)


@route_food.route( "/set",methods=["GET","POST"])
def set():
    if request.method == "GET":
        resp_data = {}
        req = request.args
        id = int(req.get('id',0))
        resp_data['current'] = 'index'
        return ops_render( "food/set.html",resp_data)

    resp = {'code': 200, 'msg': '操作成功~~', 'data': {}}
    req = request.values




@route_food.route( "/cat" )
def cat():
    resp_data = {}
    req = request.values
    query = FoodCat.query
    if 'status' in req:
        query = query.filter(FoodCat.status == int(req['status']))
    list = query.order_by(FoodCat.created_time.desc()).all()

    resp_data['list'] = list
    resp_data['search_con'] = req
    resp_data['status_mapping'] = app.config['STATUS_MAPPING']
    resp_data['current'] = 'cat'
    return ops_render( "food/cat.html",resp_data)

@route_food.route( "/cat-set",methods=["GET","POST"])
def catSet():
    if request.method == "GET":
        resp_data = {}
        req = request.args
        id = int(req.get("id", 0))
        info = None
        if id:
            info = FoodCat.query.filter_by(id=id).first()
        resp_data['info'] = info
        resp_data['current'] = 'cat'
        return ops_render("food/cat_set.html", resp_data)
    resp = {'code':200,'msg':'操作成功','data':{}}
    req = request.values
    id = req['id'] if 'id' in req else 0
    name = req['name'] if 'name' in req else ''
    weight = int(req['weight']) if ('weight' in req and int(req['weight'])>1) else 1
    if name is None or len(name)<1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的分类名称~~"
        return jsonify(resp)
    food_cat_info = FoodCat.query.filter_by(id=id).first()
    if food_cat_info:
        model_food_cat = food_cat_info
    else:
        model_food_cat = FoodCat()
        model_food_cat.created_time = getCurrentDate()

    model_food_cat.name = name
    model_food_cat.weight = weight
    model_food_cat.updated_time = getCurrentDate()
    db.session.add(model_food_cat)
    db.session.commit()
    return jsonify(resp)

@route_food.route('/cat-ops',methods=['GET','POST'])
def catOps():
    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    req = request.values
    id = req['id'] if 'id' in req else 0
    act = req['act'] if 'act' in req else ''
    if not id:
        resp['code'] = -1
        resp['msg'] = '请选择要操作的账号~~'
        return jsonify(resp)
    if act not in ['remove','recover']:
        resp['code'] = -1
        resp['msg'] = '没有此操作类型~~'
        return jsonify(resp)

    food_cat_info = FoodCat.query.filter_by(id=id).first()
    if not food_cat_info:
        resp['code'] = -1
        resp['msg'] = '指定分类不存在~~'
        return jsonify(resp)
    if act == 'remove':
        food_cat_info.status = 0
    else:
        food_cat_info.status = 1

    db.session.add(food_cat_info)
    db.session.commit()
    return jsonify(resp)






