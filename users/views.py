from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework import status
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from users.models import User,Verify
from users.serializers import CustomTokenObtainPairSerializer, UserSerializer,VerificationCodeSerializer
from django.core.mail import EmailMessage
from django.utils.crypto import get_random_string

class SendVerificationCodeView(APIView):
    def post(self, request):
        email = request.data.get('email', '')            
        if not email:
            return Response({"message": "이메일을 입력해주세요."}, status=status.HTTP_400_BAD_REQUEST)
        elif User.objects.filter(email=email).exists():
            return Response({"message": "이미 가입된 이메일입니다."}, status=status.HTTP_400_BAD_REQUEST)
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
        return Response({'verification_code': verification_code}) # 인증 코드 반환

class UserView(APIView) :
    def get(self, request):
        """ 사용자 정보를 response 합니다."""

        return Response(UserSerializer(request.user).data)
    
    def post(self, request):
        verification_serializer = VerificationCodeSerializer(data=request.data)
        if verification_serializer.is_valid():
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"massage":"가입완료"}, status= status.HTTP_201_CREATED)
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
    

class FollowView(APIView) :       # 팔로우
    def post(self, request, user_id):
        you = get_object_or_404(User, id=user_id)
        me = request.user
        if me in you.followers.all():
            you.followers.remove(me)
            return Response("unfllow했습니다.", status=status.HTTP_200_OK)
        else:
            you.followers.add(me)
            return Response("follow했습니다.", status=status.HTTP_200_OK)
        
 

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
