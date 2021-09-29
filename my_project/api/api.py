# -*- coding: utf-8 -*-
import ujson
import hashlib

from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseBadRequest, HttpResponseRedirect
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now
from django.db.models import Q, ObjectDoesNotExist

import api.data as db

appKey1 = "a7b67a3e5ceeabda78521fe9d3caccc0"
appKey2 = "15146675a892e6fef003aa0fdc9fc76a"
appKey3 = "a92fce84dee6051377d64292d6bb1bda"



def check_sign (appId, appKey, token, sign):
    md = hashlib.md5()
    md.update((appId + appKey + token).encode("utf8"))
    if (sign == md.hexdigest()):
        return True
    else:
        return False





def response(func = HttpResponse, code = 'Null', data = 'Null'):
    resp = dict(
        code = code,
        data = data,
    )
    return func(ujson.dumps(resp,ensure_ascii=False), content_type='application/json')





@require_http_methods(['POST'])
@csrf_exempt
def online(request, *args, **kwargs):
    appId = request.POST.get('appId', '')
    token = request.POST.get('token', '')
    sign = request.POST.get('sign', '')
    if not check_sign (appId, appKey1, token, sign):
        return response(HttpResponse, 'SIGN_ERR', 'Invalid App Id, Key or Signature')
    else:
        try:
            data = ujson.loads(request.POST.get('data', ''))
        except:
            return response(HttpResponse, 'INPUT_ERR', 'Invalid data structure, should be a Json String')
        db.mobileAppend(data)
        return response(HttpResponse, '25200', '25200')





@require_http_methods(['POST'])
@csrf_exempt
def sms(request, *args, **kwargs):
    appId = request.POST.get('appId', '')
    token = request.POST.get('token', '')
    sign = request.POST.get('sign', '')
    if not check_sign (appId, appKey1, token, sign):
        return response(HttpResponse, 'SIGN_ERR', 'Invalid App Id or Signature')
    else:
        try:
            data = ujson.loads(request.POST.get('data', ''))
        except:
            return response(HttpResponse, 'INPUT_ERR', 'Invalid data structure, should be a Json String')
        db.smsAppend(data)
        return response(HttpResponse, '25200', '25200')





@require_http_methods(['POST'])
@csrf_exempt
def offline(request, *args, **kwargs):
    appId = request.POST.get('appId', '')
    token = request.POST.get('token', '')
    sign = request.POST.get('sign', '')
    if not check_sign (appId, appKey1, token, sign):
        return response(HttpResponse, 'SIGN_ERR', 'Invalid App Id or Signature')
    else:
        try:
            data = ujson.loads(request.POST.get('data', ''))
        except:
            return response(HttpResponse, 'INPUT_ERR', 'Invalid data structure, should be a Json String')

        return response(HttpResponse, '25200', db.popExpiredMobile())





@require_http_methods(['POST'])
@csrf_exempt
def requestMobile(request, *args, **kwargs):
    appId = request.POST.get('appId', '')
    token = request.POST.get('token', '')
    sign = request.POST.get('sign', '')
    if not check_sign (appId, appKey2, token, sign):
        return response(HttpResponse, 'SIGN_ERR', 'Invalid App Id or Signature')
    else:
        try:
            data = ujson.loads(request.POST.get('data', ''))
        except:
            return response(HttpResponse, 'INPUT_ERR', 'Invalid data structure, should be a Json String')

        if not isinstance(data,dict):
            return response(HttpResponse, 'TYPE_ERR', 'data should be a dictinary')
        if 'projectId' not in data.keys():
            return response(HttpResponse, 'KEY_ERR', 'key "projectId" not found in data field')
        
        result = db.requestMobile(data['projectId'])
        if result == "":
            return response(HttpResponse, 'EMPTY', 'no avaliable mobile in provided projectId')
        return response(HttpResponse, '25200', result)





@require_http_methods(['POST'])
@csrf_exempt
def getMessage(request, *args, **kwargs):
    appId = request.POST.get('appId', '')
    token = request.POST.get('token', '')
    sign = request.POST.get('sign', '')
    if not check_sign (appId, appKey2, token, sign):
        return response(HttpResponse, 'SIGN_ERR', 'Invalid App Id or Signature')
    else:
        try:
            data = ujson.loads(request.POST.get('data', ''))
        except:
            return response(HttpResponse, 'INPUT_ERR', 'Invalid data structure, should be a Json String')

        if not isinstance(data,dict):
            return response(HttpResponse, 'TYPE_ERR', 'data should be a dictinary')
        if 'projectId' not in data.keys():
            return response(HttpResponse, 'KEY_ERR', 'key "projectId" not found in data field')
        if 'mobile' not in data.keys():
            return response(HttpResponse, 'KEY_ERR', 'key "mobile" not found in data field')

        result = db.smsQuery(data['projectId'],data['mobile'])
        if not result =="" :
            return response(HttpResponse, '25200', result)
        if db.isMobileExist(data['projectId'],data['mobile']):
            return response(HttpResponse, 'EMPTY', 'message not received')
        return response(HttpResponse, 'EXPIRED', 'mobile in projecId might be expired')
        
        




@require_http_methods(['POST'])
@csrf_exempt
def requestOffline(request, *args, **kwargs):
    appId = request.POST.get('appId', '')
    token = request.POST.get('token', '')
    sign = request.POST.get('sign', '')
    if not check_sign (appId, appKey2, token, sign):
        return response(HttpResponse, 'SIGN_ERR', 'Invalid App Id or Signature')
    else:
        try:
            data = ujson.loads(request.POST.get('data', ''))
        except:
            return response(HttpResponse, 'INPUT_ERR', 'Invalid data structure, should be a Json String')

        if not isinstance(data,dict):
            return response(HttpResponse, 'TYPE_ERR', 'data should be a dictinary')
        if 'projectId' not in data.keys():
            return response(HttpResponse, 'KEY_ERR', 'key "projectId" not found in data field')
        if 'mobile' not in data.keys():
            return response(HttpResponse, 'KEY_ERR', 'key "mobile" not found in data field')
        
        db.requestOffline(data['projectId'],data['mobile'])
        return response(HttpResponse, '25200', '25200')





@require_http_methods(['POST'])
@csrf_exempt
def log(request, *args, **kwargs):
	password =request.POST.get('password', '')
	username =request.POST.get('username', '')
	print(password)
	print(username)
	return response(HttpResponse, '25200', '25200')
	
	
	
	
    #appId = request.POST.get('appId', '')
    #token = request.POST.get('token', '')
    #sign = request.POST.get('sign', '')
    #if not check_sign (appId, appKey3, token, sign):
    #    return response(HttpResponse, 'SIGN_ERR', 'Invalid App Id or Signature')
    #else:
    #    
    #    db.log()
    #    return response(HttpResponse, '25200', '25200')