#coding=utf-8
from django.shortcuts import render,redirect
from hashlib import sha1
from df_user.models import UserInfos
from django.http import JsonResponse, HttpResponseRedirect
# Create your views here.
def register(request):
   context={'title':'用户注册'}
   
   return render(request,'df_user/register.html',context)

def register_handle(request):
#接受用户输入
   
    post=request.POST
    uname=post.get('user_name')
    upwd=post.get('pwd')
    upwd2=post.get('cpwd')
    uemail=post.get('email')
   #判断两次密码
    if upwd !=upwd2:
     return   redirect('/user/register/')

    s1=sha1()
    s1.update(upwd.encode("utf8"))
    upw3=s1.hexdigest()
    # 创建对象
    user=UserInfos()
    user.uname=uname
    user.upwd=upw3
    user.uemail=uemail
    user.save()
    # 注册成功。转到登陆面

    return   redirect('/user/login/')
def register_exist(request):
    uname=request.GET.get("uname")
    count=UserInfos.objects.filter(uname=uname).count()
    return JsonResponse({'count':count})

def login(request):
    uname = request.COOKIES.get('uname','')     #获取cookie
    context = {'title':'用户登录', 'error_name':0, 'error_pwd':0, 'uname': uname}
  
    return render(request,'df_user/login.html',context)

def login_handle(request):
    #接受请求到的信息
    post=request.POST
    uname=post.get('username')
    upwd=post.get('pwd')
    jizhu=post.get('jizhu',0)
    #根据用户名查找用户是否存在
    users=UserInfos.objects.filter(uname=uname)
    #print uname
    if len(users)==1:
        s1=sha1()
        s1.update(upwd.encode("utf8"))
        if s1.hexdigest()==users[0].upwd:
            url = request.COOKIES.get('url','/')    #获取登录之前进入的页面,如果没有,则进入首页
            red=HttpResponseRedirect('/user/info/') # 此处之所以没有直接使用“redirect”来直接返回，是因为我们要设置cookie,而redirect不能设置这些参数  HttpResponseRedirect继承于HttpResponse
            # 记住用户名
            if jizhu!=0:
               red.set_cookie('uname',uname)
            else:
               red.set_cookie('uname','',max_age=-1)    #过期时间为立刻过期
            request.session['user_id']=users[0].id
            request.session['user_name']=users[0].uname #用于在用户中心时可以找到用户的id和用户的名称
            return red
        else:
            context={'title':'用户登录','error_name': 0,'error_pwd':1, 'uname':uname, 'upwd':upwd}
            return render(request,'df_user/login.html',context)

    else:
        context = {'title': '用户登录', 'error_name': 1, 'error_pwd': 0, 'uname': uname, 'upwd': upwd}
        return render(request,'df_user/login.html',context)

def  info(request):
    user_email=UserInfos.objects.get(id=request.session['user_id']).uemail
    context={'title':'用户中心',
              'user_email':user_email,
              'user_name':request.session['user_name'] 
                    }
    return render(request,'df_user/user_center_info.html',context)

def  order(request):
    user_email=UserInfos.objects.get(id=request.session['user_id']).uemail
    context={'title':'用户中心',
              'user_email':user_email,
              'user_name':request.session['user_name'] 
                    }
    return render(request,'df_user/user_center_order.html')

def  site(request): #a标签链接请求过来的是get方式  如果要为post方式，可以通过表单提交或者在a标签的onclick方法中提交post请求 
    user=UserInfos.objects.get(id=request.session['user_id'])
    if request.method=='POST':
        post=request.POST
        user.ushou=post.get('ushou')
        user.uaddress=post.get('uaddress')
        user.uyoubian=post.get('uyoubian')
        user.uphone=post.get('uphone')
        user.save()
    context={'title':'用户中心','user':user}
    return render(request,'df_user/user_center_site.html',context)