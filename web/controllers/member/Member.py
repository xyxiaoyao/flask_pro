# -*- coding: utf-8 -*-
from flask import Blueprint
from common.libs.Helper import ( ops_render )
route_member = Blueprint( 'member_page',__name__ )

@route_member.route( "/index" )
def index():
    resp_data = {}
    resp_data['current'] = 'index'

    return ops_render( "member/index.html" ,resp_data)

@route_member.route( "/info" )
def info():
    resp_data = {}
    resp_data['info'] = 'info'
    return ops_render( "member/info.html" ,resp_data)

@route_member.route( "/set" )
def set():
    resp_data = {}
    resp_data['set'] = 'set'
    return ops_render( "member/set.html" ,resp_data)


@route_member.route( "/comment" )
def comment():
    resp_data = {}
    resp_data['current'] = 'comment'
    return ops_render( "member/comment.html" ,resp_data)
