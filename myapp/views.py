from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .models import Company
from .forms import ResumeForm
from .models import Resume
from django.urls import reverse
from .forms import SignUpForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
import openai
from django.conf import settings
from django.http import JsonResponse
from django.views import View
import json
from django.db import connection
import json
import logging


# myapp/views.py
#API_KEY = 'asst_BwRYOHpdRjaSwAookDNSCWqV'


class ChatGPTView(View):
    def get(self, request):
        resume = request.GET.get('resume', '')
        # 세션 초기화 및 초기 메시지 설정
        request.session['messages'] = [
            {"role": "system", "content": "You are a helpful assistant."},
        ]
        if resume:
            request.session['messages'].append(
                {"role": "user", "content": resume}
            )
            request.session['messages'].append(
                {"role": "assistant", "content": resume}
            )
        return render(request, 'myapp/chat.html', {'resume': resume})

    def post(self, request):
        prompt = request.POST.get('prompt', '')
        if not prompt:
            return JsonResponse({'error': 'No prompt provided'}, status=400)

        # 이전 대화 메시지들을 세션에서 불러옴
        messages = request.session.get('messages', [])
        messages.append({"role": "user", "content": prompt})

        # OpenAI API 호출
        client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                max_tokens=1000
            )
            assistant_message = response.choices[0].message.content.strip()
            messages.append({"role": "assistant", "content": assistant_message})

            # 세션에 메시지 저장
            request.session['messages'] = messages

            return JsonResponse({'response': assistant_message})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

class GenerateResumeView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            name = data.get('name')
            project_experience = data.get('project_experience')
            company = data.get('company')
            application_field = data.get('application_field')
            resume_field = data.get('resume_field')
            min_length = data.get('min_length')
            max_length = data.get('max_length')

            if not name or not project_experience or not company or not resume_field or not min_length or not max_length or not application_field:
                return HttpResponseBadRequest("Missing information")

            # OpenAI API 호출
            client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant. Assistant ID: {settings.OPENAI_ASSISTANT_ID}"},
                    {"role": "user", "content": (
                        f"이름: {name}\n"
                        f"프로젝트 경험: {project_experience}\n"
                        f"지원 기업: {company}\n"
                        f"지원 분야: {application_field}\n"
                        f"자기소개서 항목: {resume_field}\n"
                        f"이 정보를 바탕으로 {min_length}자에서 {max_length}자 사이의 자기소개서를 작성해줘."
                    )},
                ],
                max_tokens=1000
            )
            generated_resume = response.choices[0].message.content.strip()

            # 만족 여부를 묻는 메시지 추가
            generated_resume += "\n\n이 자기소개서가 만족스러우신가요? 수정할 부분이 있으면 말씀해주세요!"

            # 생성된 자기소개서를 세션에 저장
            messages = request.session.get('messages', [])
            messages.append({"role": "user", "content": generated_resume})
            request.session['messages'] = messages

            return JsonResponse({'resume': generated_resume})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def put(self, request):
        try:
            data = json.loads(request.body)
            user_response = data.get('user_response')
            session_messages = request.session.get('messages', [])

            if not user_response or not session_messages:
                return HttpResponseBadRequest("Missing information or session messages")

            if user_response.upper() == 'O':
                return JsonResponse({'message': "감사합니다. 지원 준비가 완료되었습니다!"})
            elif user_response.upper() == 'X':
                return JsonResponse({'message': "어떤 부분을 수정하고 싶으신가요?"})
            else:
                return HttpResponseBadRequest("Invalid response")

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


def user_info_form(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        project_experience = request.POST.get('project_experience')
        company = request.POST.get('company')
        # 여기서는 받은 데이터를 처리하거나 저장할 수 있음
        
        # GenerateResumeView로 POST 요청을 보냅니다
        return redirect(f'/generate_resume/', data={
            'name': name,
            'project_experience': project_experience,
            'company': company
        })
    
    return render(request, 'myapp/user_info_form.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'myapp/signup.html', {'form': form})

def user_info_form(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        project_experience = request.POST.get('project_experience')
        company = request.POST.get('company')
        resume_field = request.POST.get('resume_field')
        min_length = request.POST.get('min_length')
        max_length = request.POST.get('max_length')
        
        # GenerateResumeView로 POST 요청을 보냅니다
        return redirect('/generate_resume/', {
            'name': name,
            'project_experience': project_experience,
            'company': company,
            'resume_field': resume_field,
            'min_length': min_length,
            'max_length': max_length
        })
    
    return render(request, 'myapp/user_info_form.html')

@login_required
def user_info(request):
    return render(request, 'myapp/user_info.html')



def home(request):
    return render(request, 'myapp/home.html')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        # 비밀번호와 비밀번호 확인이 일치하는지 확인
        if password == confirm_password:
            # 사용자 생성
            user = User.objects.create_user(username=username, password=password)
            # 생성한 사용자로 로그인
            login(request, user)
            # 로그인 후 홈페이지로 리다이렉트
            return redirect('home')
        else:
            # 비밀번호와 비밀번호 확인이 일치하지 않으면 에러 메시지 표시
            return render(request, 'myapp/register.html', {'error': '비밀번호와 비밀번호 확인이 일치하지 않습니다.'})
    
    # GET 요청인 경우에는 회원가입 폼을 보여줌
    return render(request, 'myapp/register.html')

def company_analysis(request):
    company_info = None
    if request.method == 'POST':
        company_name = request.POST.get('company_name')
        try:
            company_info = Company.objects.get(name=company_name)
        except Company.DoesNotExist:
            company_info = None

    return render(request, 'myapp/company_analysis.html', {'company_info': company_info})



def user_info(request):
    if not request.user.is_authenticated:
        # 사용자가 로그인하지 않았을 경우
        return render(request, 'myapp/login_prompt.html')  # 로그인 유도 페이지로 리다이렉트
    else:
        # 로그인한 사용자의 정보 표시
        return render(request, 'myapp/user_info.html')




@csrf_exempt
def company_info(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        search_query = data['searchQuery']
        # 여기에서 실제 데이터베이스 또는 외부 API를 조회할 로직 구현
        dummy_company_info = {
            'name': search_query,
            'description': '이 기업은 가상의 기업입니다.'
        }
        return JsonResponse(dummy_company_info)

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)  # 올바르게 user 객체를 전달
            return HttpResponseRedirect('/')  # 성공 URL로 리디렉트
        else:
            # 로그인 실패 시 에러 메시지와 함께 로그인 페이지를 다시 렌더링
            return render(request, 'myapp/login.html', {'error_message': 'Invalid credentials'})
    else:
        return render(request, 'myapp/login.html')


def logout_view(request):
    logout(request)
    # 로그아웃 후 리다이렉트할 URL을 설정합니다.
    return redirect('home')

def resume_list(request):
    resumes = Resume.objects.filter(user=request.user)
    return render(request, 'myapp/resume_list.html', {'resumes': resumes})

@login_required
def resume_create(request):
    if request.method == 'POST':
        form = ResumeForm(request.POST)
        if form.is_valid():
            resume = form.save(commit=False)
            resume.user = request.user  # 로그인한 사용자 할당
            resume.save()
            return redirect('resume_list')  # 자기소개서 목록 페이지로 리디렉션
    else:
        form = ResumeForm()
    return render(request, 'myapp/resume_form.html', {'form': form})

@login_required
def resume_list(request):
    resumes = Resume.objects.filter(user=request.user)
    return render(request, 'myapp/resume_list.html', {'resumes': resumes})

@login_required
def resume_detail(request, id):
    resume = get_object_or_404(Resume, pk=id)
    return render(request, 'myapp/resume_detail.html', {'resume': resume})
@login_required
def resume_delete(request, id):
    resume = get_object_or_404(Resume, pk=id)
    if request.method == 'POST':
        resume.delete()
        return redirect('resume_list')