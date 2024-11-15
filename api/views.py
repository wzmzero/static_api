import uuid
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from api import models
from utils.viewsets import ModelViewSet



class DepartSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Depart
        fields = "__all__"
class DepartView(ModelViewSet):
    authentication_classes = []
    permission_classes = []
    queryset = models.Depart.objects.all()
    serializer_class = DepartSerializer




class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserInfo
        fields = "__all__"
class UserInfoView(ModelViewSet):
    queryset = models.UserInfo.objects.all()
    serializer_class = UserInfoSerializer


class LoginView(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self,request,*args,**kwargs):
        res = {'code': 100, 'msg': '登录成功'}
        username = request.data.get('username')
        password = request.data.get('password')
        # 查询数据库
        user = models.UserInfo.objects.filter(username=username, password=password).first()
        if user:
            token = uuid.uuid4()  # 生成一个随机字符串
            # 把token存到UserToken表中（如果是第一次登录：新增，如果不是第一次：更新）
            models.UserToken.objects.update_or_create(defaults={'token': token}, user=user)
            res['token'] = token
            return Response(res)
        else:
            res['code'] = 101
            res['msg'] = '用户名或密码错误'
            return Response(res)

class RegisterView(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self,request,*args,**kwargs):
        res = {'code': 100, 'msg': '注册成功'}
        username = request.data.get('username')
        password = request.data.get('password')
        phone = request.data.get('phone')
        import re
        reg = r"^(1[3|4|5|6|7|8|9])\d{9}$"
        if not re.match(reg, phone):
            res['code'] = 102
            res['msg'] = '手机号格式错误'
            return Response(res)
        reg = r"^[\s\S]*.*[^\s][\s\S]*$"
        if not re.match(reg, username):
            res['code'] = 102
            res['msg'] = '用户名格式错误'
            return Response(res)
        # reg = r"^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{6,20}$"
        # if not re.match(reg, password):
        #     res['code'] = 102
        #     res['msg'] = '密码格式错误'
        #     return Response(res)
        # 查询数据库
        user = models.UserInfo.objects.filter(username=username).first()
        user2 = models.UserInfo.objects.filter(phone=phone).first()
        if user:
            res['code'] = 102
            res['msg'] = '用户名已存在'
            return Response(res)
        elif user2:
            res['code'] = 102
            res['msg'] = '手机号已存在'
            return Response(res)
        else:
            models.UserInfo.objects.create(username=username, password=password,phone=phone)
            return Response(res)