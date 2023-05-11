from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework import status
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
import requests
from users.models import User,Verify
from boards.models import Board
from boards.serializers import BoardListSerializer
from users.serializers import CustomTokenObtainPairSerializer, UserSerializer,VerificationCodeSerializer
from django.core.mail import EmailMessage
from django.utils.crypto import get_random_string
from rest_framework_simplejwt.tokens import RefreshToken
import re
from dream.settings import REST_API_KEY
EMAIL_REGEX = re.compile(r"[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?")
KAKAO_URL = "https://kauth.kakao.com/oauth/token"

class SendVerificationCodeView(APIView):
    def post(self, request):
        email = request.data.get('email', '')            
        if not email:
            return Response({"message": "이메일을 입력해주세요."}, status=status.HTTP_400_BAD_REQUEST)
        elif User.objects.filter(email=email).exists():
            return Response({"message": "이미 가입된 이메일입니다."}, status=status.HTTP_400_BAD_REQUEST)
        elif not EMAIL_REGEX.match(email):
            return Response({'message': 'Invalid email'}, status=status.HTTP_400_BAD_REQUEST)
        code = Verify.objects.filter(email=email)
        if code.exists():
            code.delete()
        verification_code = get_random_string(length=6) 
        message = f"인증코드는 {verification_code}  입니다"
        email_message = EmailMessage(
            subject='Verification Code',
            body=message,
            to=[email],
        )
        verify_code = Verify(email=email, code=verification_code)
        verify_code.save()
        email_message.send() # 이메일 전송
        # return Response({'verification_code': verification_code}) # 인증 코드 반환
        return Response ({"message": "이메일을 전송했습니다."}, status=status.HTTP_200_OK)

 
class UserView(APIView) :
    permission_classes = [permissions.AllowAny]
    def get(self, request):
        my_board= Board.objects.filter(user=request.user).order_by('-created_at')[:10]
        serializer = BoardListSerializer(my_board, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        verification_serializer = VerificationCodeSerializer(data=request.data)
        if verification_serializer.is_valid():
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"massage":"가입완료"}, status= status.HTTP_201_CREATED)
            else:
                return Response({"message":f"${serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST)   
        else:
            return Response({"message":f"${verification_serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request):
        """ 회원 정보를 수정합니다. """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"massage":"수정완료"}, status= status.HTTP_201_CREATED)
        else:
            return Response({"message":f"${serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        """ 회원 탈퇴 기능입니다. """
        user= request.user
        user.is_active = False
        user.save()
        return Response({'message': 'delete 요청입니다.'})
    

class FollowingView(APIView) :       # 팔로우
    def get(self, request):
        """ 사용자 정보를 response 합니다."""
        me= request.user
        return Response(UserSerializer(me.following.all(), many=True).data)
    #get이 두개여도 싸우지 않는다..! 먼저 있는애가 무시됨, 따라서 두개 있는것이 의막 없음
    #클래스 두개 있어야하고, url도 달라야함 
    
    # follower 등록, 내 팔로워 목록 확인, 내 팔로잉 목록 확인 url 만들기 
    def post(self, request):
        you = get_object_or_404(User, id=request.data.get('id'))
        me = request.user
        print(you,me)
        if you in me.following.all():
            me.following.remove(you)
            return Response("unfllow했습니다.", status=status.HTTP_200_OK)
        else:
            me.following.add(you)
            return Response("follow했습니다.", status=status.HTTP_200_OK)
        return Response()

class FollowerView(APIView):
    def get(self, request):
        """ 사용자 팔로워 정보를 response 합니다."""
        me= request.user
        return Response(UserSerializer(me.followers.all(), many=True).data)
    
class CustomTokenObtainPairView(TokenObtainPairView) :
    serializer_class = CustomTokenObtainPairSerializer
# 회원탈퇴 구현은 인증방식과 상관이 없음  
# 1. 인증의 방식 2. 세션/ 토큰 인증 방식 차이 인식 



class mockView(APIView) :
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        print(request.user)
        user = request.user
        # user.is_admin = True
        # user.save()
        return Response("get 요청")       
         

class kakaoLogin(APIView):
    def post(self,request):
        code = request.data.get('code')
        access_token = requests.post(
            KAKAO_URL,
            headers={"Content-Type":"application/x-www-form-urlencoded"},
            data={
                "grant_type":"authorization_code",
                "client_id":REST_API_KEY,
                "redirect_uri":"http://127.0.0.1:5500/html/main.html",
                "code":code,
            },
        )
        access_token = access_token.json().get("access_token")
        user_data = requests.get(
                "https://kapi.kakao.com/v2/user/me",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
                },
            )
        user_data = user_data.json()
        kakao_email = user_data.get("kakao_account")['email']
        kakao_nickname = user_data.get("properties")['nickname']
        
        
        if User.objects.filter(email=kakao_email).exists():
            user = User.objects.get(email=kakao_email)
            refresh = RefreshToken.for_user(user)
            refresh["email"] = kakao_email
            refresh["nickname"] = kakao_nickname
            refresh["social"]="kakao"
            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                status=status.HTTP_200_OK
            )
        else:
            user = User.objects.create(email=kakao_email,nickname=kakao_nickname)
            user.set_unusable_password()
            user.save()
            refresh = RefreshToken.for_user(user)
            refresh["email"] = kakao_email
            refresh["nickname"] = kakao_nickname
            refresh["social"]="kakao"
            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                status=status.HTTP_200_OK
            )

