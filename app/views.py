from django.shortcuts import HttpResponse, render, redirect
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic import FormView, RedirectView, DetailView
from django import forms
from django.core.files.uploadedfile import InMemoryUploadedFile

import requests
from io import BytesIO

from app.forms import *
from app.models import Record

# Create your views here.
class HomePageView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        message = {
            'login':'登录成功',
            'logout':'退出成功',
            'register':'注册成功'
        }
        success = self.request.GET.get('success')
        if success:
            messages.success(self.request, message[success])
        else:
            messages.info(self.request, "欢迎来到图像处理系统")
        return context

class LoginView(FormView):
    template_name = "login.html"
    form_class = LoginForm
    success_url = '/?success=login'

    def form_valid(self, form):
        user = auth.authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        if user:
            auth.login(self.request, user)
            if self.request.GET.get('next'):
                self.success_url = self.request.GET['next']
            return super().form_valid(form)
        else:
            errors = form._errors.setdefault(forms.forms.NON_FIELD_ERRORS, forms.utils.ErrorList())
            errors.append('登录失败，请检查您的用户名或密码')
            return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET.get('next'):
            context['query_param'] = 'next=%s'%(self.request.GET['next'])
        else:
            context['query_param'] = ''
        return context

class LogoutView(RedirectView):
    permanent = False
    query_string = True
    url = '/?success=logout'

    def get_redirect_url(self, *args, **kwargs):
        auth.logout(self.request)
        return super().get_redirect_url(*args, **kwargs)

class RegisterView(FormView):
    template_name = "register.html"
    form_class = RegisterForm
    success_url ='/?success=register'

    def form_valid(self, form):
        try:
            user = User.objects.create_user(username=form.cleaned_data['username'], password=form.cleaned_data['password'], email=form.cleaned_data['email'])
            user.save()
            return super().form_valid(form)
        except:
            errors = form._errors.setdefault(forms.forms.NON_FIELD_ERRORS, forms.utils.ErrorList())
            errors.append('注册失败，请重试')
            return super().form_invalid(form)

def handle_classfify(user, file=None, path=None):
    if path:
        get = requests.get(path)
        if get.status_code == 200:
            data = get.content
            f = BytesIO()
            f.write(data)
            file = InMemoryUploadedFile(f, None, path.split('/')[-1], None, len(data), None, None)
    
    new_record = Record(user=user, file=file, filename=file.name, result='Pig')
    new_record.save()
    return new_record.pk

class ClassifyView(LoginRequiredMixin, TemplateView):
    template_name = "classify.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form1'] = FileForm
        context['form2'] = FilePathForm
        if 'fail' in self.request.GET.keys():
            messages.error(self.request, '操作失败，请重试')
        return context

    def post(self, request):
        try:
            pk = handle_classfify(user=request.user, file=request.FILES.get('file'), path=request.POST.get('file_path'))
        except:
            return redirect('/classify/?fail')
        return redirect('/classify/record/%d'%(pk))

class ClassifyRecordView(LoginRequiredMixin, DetailView):
    template_name = "classify_record.html"
    model = Record

class RecordsView(LoginRequiredMixin, ListView):
    template_name = 'records.html'
    model = Record
    paginate_by = 5
    start = None
    end = None

    def get_queryset(self):
        self.start = self.request.GET.get('start')
        self.end = self.request.GET.get('end')
        if self.start and self.end:
            return Record.objects.filter(time__gte=self.start, time__lte=self.end, user=self.request.user)
        else:
            return Record.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['start'] = self.start
        context['end'] = self.end
        if self.start and self.end:
            context['query_param']='start={0}&end={1}&'.format(self.start,self.end)
        else:
            context['query_param']=''
        success_message = {
            'delete':'删除记录成功',
        }
        fail_message = {
            'delete':'删除记录出错，请重试',
            'none': '未选择任何记录'
        }
        success = self.request.GET.get('success')
        if success:
            messages.success(self.request, success_message[success])
        fail = self.request.GET.get('fail')
        if fail:
            messages.error(self.request, fail_message[fail])
        return context

class RecordsDeleteView(LoginRequiredMixin, RedirectView):
    url = '/records/?success=delete'

    def get_redirect_url(self, *args, **kwargs):
        try:
            id_list = [i for i in map(int, self.request.POST.getlist('id'))]
            records = Record.objects.filter(id__in=id_list, user=self.request.user)
            if records.exists():
                records.delete()
            else:
                self.url = '/records/?fail=none'
        except:
            self.url = '/records/?fail=delete'
        return super().get_redirect_url(*args, **kwargs)

class AdminView(LoginRequiredMixin, ListView):
    template_name = "admin.html"
    model = Record
    paginate_by = 5
    query_user = None

    def get_queryset(self):
        if self.request.GET.get('user'):
            try:
                self.query_user = User.objects.get(username=self.request.GET['user'])
                return Record.objects.filter(user=self.query_user)
            except:
                return Record.objects.all()

        else:
            return Record.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_list'] = User.objects.all()
        context['query_user'] = self.query_user
        if self.query_user:
            context['query_param'] = 'user=%s&'%(self.query_user)
        else:
            context['query_param'] = ''

        success_message = {
            'delete':'删除记录成功',
        }
        fail_message = {
            'delete':'删除记录出错，请重试',
            'none': '未选择任何记录'
        }
        success = self.request.GET.get('success')
        if success:
            messages.success(self.request, success_message[success])
        fail = self.request.GET.get('fail')
        if fail:
            messages.error(self.request, fail_message[fail])
        return context

class AdminDeleteView(LoginRequiredMixin, RedirectView):
    url = '/records/?success=delete'

    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_staff:
            try:
                id_list = [i for i in map(int, self.request.POST.getlist('id'))]
                records = Record.objects.filter(id__in=id_list)
                if records.exists():
                    records.delete()
                else:
                    self.url = '/admin/?fail=none'
            except:
                self.url = '/admin/?fail=delete'
            return super().get_redirect_url(*args, **kwargs)
        else:
            return '/admin/'