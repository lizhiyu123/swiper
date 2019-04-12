from django.core.cache import cache
from lib.sms import send_sms
from  lib.http import render_json
from common import errors,keys
from user.models import User
from user.forms import ProfileFrom
from user.logics import upload_avatar_to_server
from django import forms
import os
from swiper import settings

def submit_phone(request):
    """获取短信验证码"""
    if not request.method == "POST":
        return render_json("request method error",errors.REQUEST_ERROR)
    phone = request.POST.get("phone")
    result,msg = send_sms(phone)

    data = {"status":"ok","msg":msg}
    # data = "秋风秋雨"

    return render_json(msg)


def submit_vcode(request):
    """通过验证码登录注册"""
#     判断是否是post请求
    if not request.method == "POST":
        return render_json("request method error",errors.REQUEST_ERROR)

    phone = request.POST.get("phone")
    #     取到发送到手机的验证码
    vcode = request.POST.get("vcode")
    # 取到缓存中的验证码

    cache_vcode = cache.get(keys.VCODE_KEY%phone)


#     对比验证码是够一致
    if vcode == cache_vcode:
        # users = User.objects.filter(phonenum = phone)
        # if not users:
        #     User.objects.create(phonenum = phone, nickname = phone)
        user,_ = User.objects.get_or_create(phonenum=phone,nickname=phone)
        request.session["uid"] = user.id
        return render_json(user.to_string())
    else:
        return render_json("verify code error",errors.VCODE_ERROR)

def get_profile(request):
    """获取个人资料"""
    uid = request.session.get("uid")
    user = User.objects.get(id = uid)

    profile = user.profile

    return render_json(profile.to_string())

def set_profile(request):
    """修改个人资料"""
    if not request.method == "POST":
        return render_json("request method error",errors.REQUEST_ERROR)
    profile_form = ProfileFrom(request.POST)
    uid = request.session.get("uid")
    print(request.session)

    if profile_form.is_valid():
        profile = profile_form.save(commit=False)
        print(profile.location)
        profile.id = uid
        profile.save()
        return render_json("modify profile success")
    else:
        # raise forms.ValidationError
        return render_json(profile_form.errors,errors.FORM_VALID_ERROR)

def upload_avatar(request):
    """头像上传"""
    if not request.method == "POST":
        return render_json("request method error", errors.REQUEST_ERROR)
    avatar = request.FILES.get("avatar")
    uid = request.session.get("uid")

    upload_avatar_to_server(uid,avatar)

    return render_json("upload success")