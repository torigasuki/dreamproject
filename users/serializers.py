from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from users.models import User, Verify
from django.shortcuts import get_object_or_404

class UserSerializer(serializers.ModelSerializer):
    class Meta :
        model = User
        fields = "__all__"
        #비밀번호 마이페이지에서 안보이게 하기, 비밀번호 입력할때만 조회 가능
        extra_kwargs = {
           "password":{
                "write_only":True,
            }, 
        }
        
    def create(self, validated_data):
        user= super().create(validated_data)
        password = user.password
        user.set_password(password)
        user.save()
        return user    
    
    def update(self, validated_data):
        user= super().create(validated_data)
        password = user.password
        user.set_password(password)
        user.save()
        return user    



class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        return token
    
    
class VerificationCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)
    
    def validate(self, data):
        # attrs에서 email과 code 값 추출
        email = data.get('email')
        code = data.get('code')
        verify = get_object_or_404(Verify, email=email)
        if code == verify.code:  # 인증코드 일치 여부 확인
            verify.delete()  # 인증코드 삭제
            return data
        else:
            raise serializers.ValidationError("Invalid verification code")    