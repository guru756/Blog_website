from django.shortcuts import render,HttpResponse,redirect
from .forms import LoginForm,BlogForm
from .models import User,Blog
import datetime
# Create your views here.

def login(request):
    username='not logged in'
    
    if request.method=='POST':
        MyLoginForm=LoginForm(request.POST)
        
        if MyLoginForm.is_valid():
            username=MyLoginForm.cleaned_data['username']
    else:
        MyLoginForm=LoginForm()
    
    response=render(request,'loggedin.html',{'username':username})
    
    response.set_cookie('last_connection',datetime.datetime.now())
    
    response.set_cookie('username',datetime.datetime.now())
    
    return response


def formView(request):
    form=LoginForm()
    if 'username' in request.COOKIES and 'last_connection' in request.COOKIES:
        username=request.COOKIES['username']
        
        last_connection=request.COOKIES['last_connection']
        last_connection_time=datetime.datetime.strptime(last_connection[:-7],"%Y-%m-%d %H:%M:%S")
        
        if(datetime.datetime.now() - last_connection_time).seconds<10:
            return render(request,'loggedin.html',{'username':username})
        else:
            return render(request,'login.html',{'form':form}) 
    else:
        return render(request,"login.html",{"form":form})
    


# Create your views here.
def home(request):
    if 'user' in request.session:
        current_user = request.session['user']
        param = {'current_user': current_user}
        return render(request, 'show.html', param)
    else:
        return render(request, 'signin.html')
    



def signup(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        uname = request.POST.get('uname')
        pwd = request.POST.get('pwd')
        # print(uname, pwd)
        if User.objects.filter(username=uname).count()>0:
            return HttpResponse('Username already exists.')
        else:
            user = User(username=uname, password=pwd,full_name=full_name)
            user.save()
            return redirect('signin')
    else:
        return render(request, 'signup.html')



def signin(request):
    if request.method == 'POST':
        uname = request.POST.get('uname')
        pwd = request.POST.get('pwd')

        check_user = User.objects.filter(username=uname, password=pwd)
        if check_user:
            request.session['user'] = uname
            return redirect('home')
        else:
            return HttpResponse('Please enter valid Username or Password.')

    return render(request, 'signin.html')


def logout(request):
    try:
        del request.session['user']
    except:
        return redirect('signin')
    return redirect('signin')

def emp(request):
    if request.method=="POST":
        form=BlogForm(request.POST,request.FILES)
        if form.is_valid():
            try:
                form.save()
                return redirect("/show")
            except:
                pass
    else:
        form=BlogForm()
    
    return render(request,"index.html",{"form":form})

def show(request):
    blogs=Blog.objects.all()
    return render(request,"show.html",{"blogs":blogs})


def edit(request,id):
    blog=Blog.objects.get(id=id)
    return render(request,"edit.html",{"blog":blog})

def update(request,id):
    blog=Blog.objects.get(id=id)
    form=BlogForm(request.POST,request.FILES)
    if form.is_valid():
        form.save()
        return redirect("/show")
    
    return render(request,"edit.html",{"blog":blog})

def destroy(request,id):
    blog=Blog.objects.get(id=id)
    blog.delete()
    return redirect("/show")