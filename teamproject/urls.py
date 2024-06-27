from django.contrib import admin
from django.urls import path, include
from myapp import views  # 모든 뷰를 myapp에서 가져옴
from myapp.views import ChatGPTView, GenerateResumeView, user_info_form, home, register, login_view, logout_view, resume_create, resume_list, resume_detail, resume_delete



urlpatterns = [
    path("admin/", admin.site.urls),
    path('', views.home, name='home'),  # 홈페이지
    path('signup/', views.signup, name='signup'), # 로그인 페이지
    path('login/',views.login_view, name='login'),
    path('company_analysis/', views.company_analysis, name='company_analysis'),  # 기업분석 페이지
    path('user-info-form/', views.user_info_form, name='user_info_form'),  # 사용자 정보 폼
    path('user-info/', views.user_info, name='user_info'),  # 사용자 정보 폼
    path('logout/', views.logout_view, name='logout'),
    path('resumes/', views.resume_list, name='resume_list'),
    path('resumes/create/', views.resume_create, name='resume_create'),
    path('resumes/<int:id>/', views.resume_detail, name='resume_detail'),  # 자기소개서 상세 페이지
    path('register/', views.register, name='register'),
    path('', include('myapp.urls')),  # myapp을 실제 앱 이름으로 변경
    path('generate_resume/', views.GenerateResumeView.as_view(), name='generate_resume'),
    path('resumes/delete/<int:id>/', views.resume_delete, name='resume_delete'),    # 자기소개서 페이지
    # 추가적인 앱 URLconf 포함 (필요한 경우)
    # path('someapp/', include('someapp.urls')),
]
