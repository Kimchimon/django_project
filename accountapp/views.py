from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render

# Create your views here.
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView

from accountapp.decorators import account_ownership_reqired
from accountapp.forms import AccountUpdateForm
from accountapp.models import HelloWorld


has_ownership = [login_required,account_ownership_reqired]

@login_required
def hello_world(request):
    if request.method == "POST":

        temp = request.POST.get('hello_world_input')

        new_hello_world = HelloWorld()
        new_hello_world.text = temp
        new_hello_world.save()

        return HttpResponseRedirect(reverse('accountapp:hello_world'))
    else:
        hello_world_list = HelloWorld.objects.all()
        return render(request, 'hello_world.html', context={'hello_world_list': hello_world_list})


class AccountCreateView(CreateView):
    model = User
    # 기본적인 Form을 제공해줌
    form_class = UserCreationForm
    # 회원가입 성공시 리턴할 html
    success_url = reverse_lazy('accountapp:hello_world')
    # 회원가입시 보여주는 html
    template_name = 'create.html'


class AccountDetailView(DetailView):
    model = User
    # 상대편의 정보를 보여주도록 설정
    context_object_name = 'target_user'
    template_name = 'detail.html'


@method_decorator(has_ownership, 'get')
@method_decorator(has_ownership, 'post')
class AccountUpdateView(UpdateView):
    model = User
    context_object_name = 'target_user'
    # 기본적인 Form을 제공해줌
    form_class = AccountUpdateForm
    # 업데이트 성공시 리턴할 html
    success_url = reverse_lazy('accountapp:hello_world')
    # 업데이트시 보여주는 html
    template_name = 'create.html'


@method_decorator(has_ownership, 'get')
@method_decorator(has_ownership, 'post')
class AccountDeleteView(DeleteView):
    model = User
    context_object_name = 'target_user'
    success_url = reverse_lazy('accountapp:login')
    template_name = 'delete.html'
