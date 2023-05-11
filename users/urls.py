from django.urls import path, include
from users import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('', views.UserView.as_view(), name='user_profile'),
    path('signup/', views.UserView.as_view(), name='user_view'),
    path('sendmail/', views.SendVerificationCodeView.as_view(), name='user_view'),
    path('mock/', views.mockView.as_view(), name='mock_view'),
    path('login/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('kakao/' , views.kakaoLogin.as_view(), name='kakao_login_view'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),   
    path('follower/', views.FollowerView.as_view(), name='follower_view'),     
    path('following/', views.FollowingView.as_view(), name='following_view'), 


]