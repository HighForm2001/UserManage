from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from app01.models import Department, UserInfo,Task
# Create your views here.
from django import forms
from django.core.validators import RegexValidator
from django.utils.safestring import mark_safe
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
class MyForm(forms.ModelForm):
    # validate method 1
    # validator
    name = forms.CharField(label="名字",
                           validators=[RegexValidator(r'\w{30}','名字只允许有字母')])
    # make the attribute not able to edit
    age = forms.IntegerField(disabled=True,label="年龄")
    confirmed_password = forms.CharField(max_length=32,
                                     label="确认密码",
                                     widget=forms.PasswordInput(render_value=True),)
    # validate method 2
    def clean_name(self):

        txt_name = self.cleaned_data['name']

        # check no repeat
        exist = UserInfo.objects.exclude(id=self.instance.pk).filter(name=txt_name).exists()
        if exist:
            raise ValidationError("名字已存在")
        if len(txt_name) > 30:
            raise ValidationError("Name too long")
        return txt_name


    def clean_confirmed_password(self):
        pwd = self.cleaned_data.get("password")
        confirm = self.cleaned_data.get("confirmed_password")
        if pwd != confirm:
            raise ValidationError("密码不一致")

        return confirm

    class Meta:
        model = UserInfo
        # fields = ['name', 'password', 'app', 'gender']
        fields = "__all__"
        widgets = {
            'name': forms.TextInput(attrs={"class": "form-control"}),
            'password': forms.PasswordInput(render_value=True)
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # if need to custom on all the inputs


def depart_list(request):
    return render(request, 'depart_list.html')


def user_list(request):
    # set pages
    pages = request.GET.get('pages',1)
    # each page show how many row
    page_size = 30
    start = (pages-1) * page_size
    end = pages*page_size
    # get total data
    total = UserInfo.objects.all().count()
    # set total page needed
    page_num ,div= divmod(total,page_size)
    if div:
        page_num += 1
    query_set = UserInfo.objects.all()[start:end]
    for obj in query_set:
        # get gender by choices tuple
        obj.get_gender_display()
        depart_id = obj.depart_id  # department id original property
        depart = obj.depart.title  # get the department title based on the id
        create_date = obj.create_time.strftime("%Y-%M-%d")  # in python
        # in html should be writing like this
        # obj.create_time.strftime|date:"Y-M-D

    # calculate 5 pages before current page, and 5 pages after current page
    plus = 5
    if total <= 2*plus + 1:
        # data in database is quite small.
        start_page = 1
        end_page = total
    else:
        # data more than 11
        if pages<=plus:
            start_page = 1
            end_page = 2*plus+1
        else:
            if (pages+plus) > total:
                start_page = total - 2*plus
                end_page = total
            else:
                start_page = pages - plus
                end_page = pages + plus + 1


    page_str_list = []
    # fist page
    page_str_list.append('<li><a href="?page=1">首页</a></li>')
    # prev page
    if pages - 1 > 0:
        prev = '<li><a href="?page={}">上一页</a></li>'.format(pages-1)
        page_str_list.append(prev)

    # 页码
    for i in range(start_page,end_page):
        ele = '<li><a href="?page={}">{}</a></li>'.format(i,i)
        page_str_list.append(ele)

    # next page
    if pages + 1 < total:
        after = '<li><a href="?page={}">上一页</a></li>'.format(pages+1)
        page_str_list.append(after)

    # convert string to html notes
    page_string = mark_safe(''.join(page_str_list))

    return render(request, 'user_list.html',{'queryset':query_set,'page_string':page_string})


def user_add(request):
    if request.method == "GET":
        form = MyForm()
        return render(request, 'user_add.html', {"form": form})
    form = MyForm(data=request.POST)
    if form.is_valid():
        print(form.cleaned_data)
        # auto save
        form.save()
        return HttpResponse("successful")
    return render(request, "user_add.html", {"form": form})

def user_edit(request, nid):
    filter_dict = {}
    value = request.GET.get("something you want","")#
    if value:
        filter_dict = {'name__contains':value}
    row_obj = UserInfo.objects.filter(**filter_dict).order_by('-name')
    # row_obj = UserInfo.objects.filter(id=12).first() # filter id = 12
    # row_obj = UserInfo.objects.filter(id__gt=12).first() # filter id > 12
    # row_obj = UserInfo.objects.filter(id__gte=12).first() # filter id >= 12
    # row_obj = UserInfo.objects.filter(id__lt=12).first() # filter id < 12
    # row_obj = UserInfo.objects.filter(id__lte=12).first() # filter id <= 12
    # more filter:
    # __endswith="xxx"
    # __startswith = 'xxx'
    # _contains = "xxx"
    if request.method == "GET":

        form = MyForm(instance=row_obj)
        return render(request, "user_edit.html",{'form':form})
    form = MyForm(data=request.POST,instance=row_obj)
    if form.is_valid():
        form.save()
        return redirect("/user/list/")
    return render(request, 'user_edit.html',{'form':form})


def user_login(request):
    # session info
    request.session['info'] = 'aaaaa'
    # 可以设置超时
    # request.session.set_expiry(60)

    # 可以随意放
    # 检查之前有没有登陆过
    check = request.session.get('info')
    if not check:
        print("Did not login before")

def logout(request):
    request.session.clear()
    return HttpResponse("logout successful")


class TaskModelForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = "__all__"


def task_list(request):
    """任务列表"""
    query_set = Task.objects.all()
    form = TaskModelForm
    context = {"query":query_set,"form":form}
    return render(request,'task_list.html',context)



# to exempt csrf verification
@csrf_exempt
def task_ajax(request):
    print(request.GET)
    print(request.POST)
    data_dict = {"status":True,'data':[11,22,33]}
    return JsonResponse(data_dict)

@csrf_exempt
def task_add(request):
    print(request.POST)
    # 校验
    form = TaskModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        data_dict = {"status":True}
        return JsonResponse(data_dict)
    data_dict = {'status':False, 'error':form.errors}
    return JsonResponse(data_dict)

    return HttpResponse("成功了")