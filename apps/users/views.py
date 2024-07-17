import base64
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from captcha.views import CaptchaStore, captcha_image

from utils.filters import UsersManageTimeFilter
from .serializers import UserManageSerializer, UserManageCreateSerializer, UserManageUpdateSerializer, LoginSerializer, \
    UsersSerializer, UserCreateSerializer, UserUpdateSerializer
from utils.viewset import CustomModelViewSet
from utils.jsonResponse import SuccessResponse, ErrorResponse, DetailResponse

# Create your views here.
Users = get_user_model()


# Create your views here.
# ********************************** 后端用户管理 view ************************************ #

class UserManageViewSet(CustomModelViewSet):
    """
    管理后台用户的接口，包括禁用用户操作
    """
    # 排除管理员
    queryset = Users.objects.filter(identity=2).order_by("-create_datetime")
    serializer_class = UserManageSerializer
    create_serializer_class = UserManageCreateSerializer
    update_serializer_class = UserManageUpdateSerializer
    filterset_class = UsersManageTimeFilter

    @staticmethod
    def disable_user(request, *args, **kwargs):
        """禁用用户"""
        instance = Users.objects.filter(id=kwargs.get('pk')).first()
        if instance:
            if instance.is_active:
                instance.is_active = False
            else:
                instance.is_active = True
            instance.save()
            return SuccessResponse(data=None, msg="修改成功")
        else:
            return ErrorResponse(msg="未获取到用户")


class UsersViewSet(CustomModelViewSet):
    """
    post:
    【功能描述】管理普通用户的接口，包括获取用户信息、修改用户信息和修改密码等功能</br>
    【参数说明】username为手机号</br>
    【参数说明】password为密码</br>
    【参数说明】captcha为验证码</br>
        """
    queryset = Users.objects.filter(identity=1, is_delete=False).order_by('create_datetime')
    serializer_class = UsersSerializer
    create_serializer_class = UserCreateSerializer
    update_serializer_class = UserUpdateSerializer
    filterset_class = UsersManageTimeFilter

    @staticmethod
    def user_info(request):
        """
        获取当前用户信息
        """
        user = request.user
        result = {
            'username': user.username,
            'name': user.name,
            'mobile': user.mobile,
            'email': user.email,
            'gender': user.gender,
        }
        return SuccessResponse(data=result, msg='获取成功')

    @staticmethod
    def update_user_info(request):
        """
        修改当前用户信息
        """
        user = request.user
        Users.objects.get(id=user.id).update(**request.data)
        return SuccessResponse(data=None, msg='修改成功')

    @staticmethod
    def change_password(request):
        """
        修改密码
        """
        user = request.user
        instance = Users.objects.filter(id=user.id, identity__in=[0, 1]).first()
        data = request.data
        old_password = data.get('old_password')
        new_password = data.get('new_password')
        new_password_2 = data.get('new_password_2')
        if instance:
            if new_password != new_password_2:
                return ErrorResponse(msg='2次密码不匹配')
            elif instance.check_password(old_password):
                instance.password = make_password(new_password)
                instance.save()
                return SuccessResponse(data=None, msg='修改成功')
            else:
                return ErrorResponse(msg='旧密码不正确')
        else:
            return ErrorResponse(msg='未获取到用户')


class LoginView(TokenObtainPairView):
    """
    【功能描述】处理用户登录认证的接口：验证用户名、密码和验证码进行用户身份验证</br>
    【参数说明】username为手机号</br>
    【参数说明】password为密码</br>
    【参数说明】captcha_key为验证码接口返回的id</br>
    【参数说明】captcha为验证码</br>
    """
    serializer_class = LoginSerializer
    permission_classes = []


class CaptchaView(APIView):
    """
    获取图片验证码
    """
    authentication_classes = []

    @swagger_auto_schema(
        responses={
            '200': openapi.Response('获取成功')
        },
        security=[],
        operation_id='captcha-get',
        operation_description='验证码获取',
    )
    def get(self, request):
        hash_key = CaptchaStore.generate_key()
        image_id = CaptchaStore.objects.filter(hashkey=hash_key).first().id
        image = captcha_image(request, hash_key)
        # 将图片转换为base64
        image_base = base64.b64encode(image.content)
        json_data = {"captcha_key": image_id, "image_base": "data:image/png;base64," + image_base.decode('utf-8')}
        return SuccessResponse(data=json_data)
