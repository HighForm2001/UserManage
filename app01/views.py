from django.http import HttpResponse
from django.shortcuts import render
from app01.models import Department, UserInfo
# Create your views here.
from django import forms


class MyForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ['name', 'password', 'app', 'gender']
        widgets = {
            'name': forms.TextInput(attrs={"class": "form-control"}),
            'password': forms.PasswordInput()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # if need to custom on all the inputs


def depart_list(request):
    return render(request, 'depart_list.html')


def user_list(request):
    query_set = UserInfo.objects.all()

    for obj in query_set:
        # get gender by choices tuple
        obj.get_gender_display()
        depart_id = obj.depart_id  # department id original property
        depart = obj.depart.title  # get the department title based on the id
        create_date = obj.create_time.strftime("%Y-%M-%d")  # in python
        # in html should be writing like this
        # obj.create_time.strftime|date:"Y-M-D
    return render(request, 'user_list.html')


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
