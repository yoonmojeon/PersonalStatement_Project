from django.db import models
from django.contrib.auth.models import User


class Company(models.Model):
    name = models.CharField(max_length=100)
    employee_count = models.IntegerField()  # 직원 수는 정수형 필드로 변경
    founding_date = models.DateField()  # 설립 일은 날짜 필드로 변경
    company_type = models.CharField(max_length=50)  # 회사 종류
    overview = models.TextField()  # 사업 개요
    job_fields = models.TextField()  # 텍스트 필드로 변경
    revenue = models.CharField(max_length=50)  # 매출액 (문자열)
    operating_profit = models.CharField(max_length=50)  # 영업 이익 (문자열)
    strength = models.TextField()  # 강점
    weakness = models.TextField()  # 약점
    opportunities = models.TextField()  # 기회
    threats = models.TextField()  # 위협
    rating = models.DecimalField(max_digits=3, decimal_places=1)  # 새 필드 추가
    percent = models.IntegerField() # 감정분류 퍼센트
    goodkeywords = models.TextField()  # 텍스트 필드로 변경
    badkeywords = models.TextField()  # 텍스트 필드로 변경

    use_mysql = True  # MySQL 데이터베이스를 사용하도록 속성 추가

    class Meta:
        db_table = 'companydata'  # 실제 데이터베이스 테이블 이름 지정

    def __str__(self):
        return self.name

# myapp/models.py
from django.db import models
from django.contrib.auth.models import User

class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)  # 자기소개서 제목 필드
    content = models.TextField()  # 자기소개서 내용 필드
    created_at = models.DateTimeField(auto_now_add=True)  # 생성 날짜와 시간

    def __str__(self):
        return self.title

