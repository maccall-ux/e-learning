from django.shortcuts import render,redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

def register(request):
    #register ner user
    if request.method=='POST':
        form=UserCreationForm(data=request.POST)
        if form.is_valid():
            new_user=form.save()
            #log in new user and redirect back to homepage
            login(request,new_user)
            return redirect('learning_logs:index')
    else:
        form=UserCreationForm()
    context={'form':form}
    return render(request,'registration/register.html',context)