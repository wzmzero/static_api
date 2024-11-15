from rest_framework.permissions import BasePermission
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from api import models

class MIneAuthentication(BaseAuthentication):
    def authenticate(self, request):
        #读取token
        token = request.META.get("HTTP_TOKEN")
        token_obj = models.UserToken.objects.filter(token=token).first()
        if not token_obj:
            raise exceptions.AuthenticationFailed("用户认证失败")
        #在rest_framework内部会将整个字段赋值给request，以供后续操作使用
        #token_obj->user是对应的UserInfo (request,auth)
        return token_obj.user,token_obj
    def authenticate_header(self, request):
        return "API"

class MinePermission(BasePermission):
    def has_permission(self, request, view):

        from django.conf import settings
        permission_dict = settings.PERMISSIONS[request.user.role]
        #print(request.resolver_match.url_name,request.method)
        #2.当前用户访问url和方法
        url_name = request.resolver_match.url_name
        method = request.method
        #3.权限判定
        method_list = permission_dict.get(url_name)
        if not method_list:
            return False
        if method in method_list:
            return True
        return False
    # def has_object_permission(self, request, view, obj):
    #     return True
