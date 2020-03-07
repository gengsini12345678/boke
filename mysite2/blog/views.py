from django.shortcuts import render, redirect

from django.urls import reverse

from django.contrib.auth.hashers import make_password, check_password

from  django.contrib.auth.models import User

from django.contrib.auth import authenticate,login,logout

from django.contrib.auth.decorators import login_required

from django.core.cache import cache

from django.core.serializers import serialize

from django.http import HttpResponse

from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

from . import models, utils

from . import forms

# Create your views here.

def index(request,index):
    '''
    博客首页视图处理函数
    :param request:
    :return:
    '''
    # 查询所有文章，按照发表时间的倒叙查询
    # article_list = models.Article.objects.order_by("-publish")
    # article_list = models.Article.objects.all()
    # return render(request,"blog/index.html",{"alist":article_list})
    # 缓存v 1.0 版本
    # 查询缓存中的数据
    # article_list = utils.cache_index()  # 数据没有发生变化
    if request.method == "GET":
        # alist = models.Wanda.objects.all()
        article_list = utils.cache_index()  # 数据没有发生变化
        # 分页 每页显示3条
        paginator = Paginator(article_list,3)
        # 3.获取第一页
        if index == '':
            index = 1
        else:
            index = int(index)
        page = paginator.page(index)
        return render(request, "blog/index.html", {"page": page})
    # return render(request, "blog/index.html", {"alist": article_list})


def user_login(request):
    '''
    登录处理函数
    :param request:
    :return:
    '''
    form = forms.CustomerForm()
    if request.method == 'GET':
        return render(request, "blog/login.html", {"form":form,"error":""})
        # 登录成功后跳转的下一个路径

        # try:
        #     next_url = request.GET['next']
        # except:
        #     next_url = "/"

    elif request.method == 'POST':

        # 获取账号和密码
        # username = request.POST['username']
        # userpass = request.POST['userpass']
        # next_url = request.POST['next_url'] # 跳转的下一个路径
        # print("路径2：%s" % next_url)
        # 验证账号密码是否正确
        # 获取数据

        # if form.is_valid():
        #     print(form.changed_data)
        # 获取数据
        form = forms.CustomerForm(request.POST)
        print(form.is_valid())

        if form.is_valid():
            username  = form.cleaned_data['username']
            password  = form.cleaned_data['userpass']
            print("账号：%s" % username)
            print("密码：%s" % password)

            user = authenticate(request, username=username, password=password)
            if  user is not None:
                # 记录登录状态，跳转页面
                login(request,user)
                request.session['login_user'] = user
                author = models.Author(user=user)
                author.save()
                return redirect(reverse("blog:index",kwargs={'index':'1'}))
            else:
                return  render(request, "blog/login.html", {"form":form,"error_msg":'账号不存在'})

        # -------------原始方法------------
        # user_name = authenticate(request, username=username, password=userpass)
        # # user_name=User.objects.get(username=username)
        # if  user_name is not None:
        #     # 记录登录状态，跳转页面
        #     login(request,user_name)
        #     request.session['login_user'] = user_name
        #     author = models.Author(user=user_name)
        #     author.save()
        #     return redirect(reverse("blog:index",kwargs={'index':'1'}))
        # else:
        #     return  render(request, "blog/login.html", {"error_msg":'账号不存在'})


        # -------------原始方法------------
        # if not check_password(userpass,user_name.password):
        #     return  render(request, "blog/login.html", {"error_msg":'密码错误'})
        # 登录成功
        # request.session['login_user'] = user_name
        # author = models.Author(user=user_name)
        # author.save()
        # return redirect(reverse("blog:index",kwargs={'index':'1'}))
        # return redirect(next_url)
       # -------------------第一种方法  走不通----------------------
        # try:
        #     pws = User.objects.get(username=username)
        #     pws = pws.password
        #     print(pws)
        #     userpass = check_password(userpass,)
        #
        #
        #     user = User.objects.get(username=username, password=userpass)
        #     # user = authenticate(username=username,password=userpass)
        #
        #
        # except:
        #     return render(request, "blog/login.html", {"error_msg": "账号或密码错误"})
        #
        #
        # # 跳转系统首页
        # # return render(request,"blog/login.html",{})  错
        # request.session['login_user'] = user
        # print(userpass)
        # return redirect(reverse("blog:index"))
        # -------------------第一种方法  走不通----------------------


def register(request):
    '''
    注册处理函数
    :param request:
    :return:
    '''
    if request.method == 'GET':
        return render(request, "blog/register.html", {})
    elif request.method == 'POST':
        # 获取需要的数据
        username = request.POST['username']
        userpass = request.POST['userpass']
        re_userpass = request.POST['re_userpass']
        realname = request.POST['realname']
        # 验证数据
        if len(username) < 6:
            return render(request, "blog/register.html",
                          {"error_msg": "用户名不能小于六位"})
        if len(userpass) < 6:
            return render(request, "blog/register.html",
                          {"error_msg": "密码不能小于六位"})
        if re_userpass != userpass:
            return render(request, "blog/register.html",
                          {"error_msg": "两次的密码不一致"})
        # 保存数据
        try:
            user = User.objects.get(username=username)
            return render(request,'blog/register.html',
                          {"error_msg": "改用户名已存在，请重新注册"})
        except:
            # 创建用户注册
            # user = User.objects.create_user(username=username,password=userpass)
            # make_password 对密码进行加密
            userpass = make_password(userpass)
            # print(userpass)
            user = User(username=username,password=userpass)
        # author = models.Author(username=username, userpass=userpass, realname=realname)
        user.save()
        author = models.Author(realname=realname,user=user)
        author.save()
        return render(request, "blog/login.html", {"error_msg": "注册成功"})


def article_publish(request):
    '''
    用户发表文章
    :param request:
    :return:
    '''
    if request.method == 'GET':
        return render(request, "blog/article_publish.html", {})
    elif request.method == 'POST':
        # 获取文章标题和内容
        title = request.POST['title']
        content = request.POST['content']
        user = request.session['login_user']
        # print(user.id)
        author = models.Author.objects.filter(user_id = user.id).first()
        # 创建文章对象，并保存到数据库
        article = models.Article(title=title, content=content, author=author)
        # 执行完save()函数，article数据已经存储在数据库了，同时程序中的article被自动赋值了id
        article.save()
        # 同步缓存数据，数据改变了 重新查询数据库
        utils.cache_index(True)
        # 跳转到详情页面，展示发表的文章
        return redirect(reverse('blog:article_details',
                                kwargs={"article_id": article.id}))


def article_details(request, article_id):
    '''
    查看文章详情
    :param request:
    :param article_id:
    :return:
    '''
    # 查询对应的文章
    article = models.Article.objects.get(pk=article_id)
    # 更新阅读量
    article.count += 1
    article.save()
    # 跳转到文章详情页面
    return render(request, 'blog/article_details.html', {"article": article})

@login_required
def article_list(request,inde):
    '''
    查看用户自己发表的文章
    :param request:
    :return:
    '''
    if request.method == "GET":
        # alist = models.Wanda.objects.all()
        # 获取当前用户
        user = request.session['login_user']
        author = models.Author.objects.filter(user_id = user.id).first()
        # 查询当前用户发表的文章
        article_list = models.Article.objects.filter(author=author).order_by("-publish")
        # 分页 每页显示3条
        paginator = Paginator(article_list,3)

        # 3.获取第一页
        if inde == '':
            inde = 1
        else:
            inde = int(inde)
        page = paginator.page(inde)
        return render(request, "blog/article_list.html", {"page": page})
    # 返回网页直接展示数据
    # return render(request, "blog/article_list.html", {"alist": article_list})


def logout_view(request):
    '''
    退出系统
    :param request:
    :return:
    '''
    # 【2020-3-4编辑】
    logout(request)
    return redirect(reverse("blog:index",kwargs={'index':'1'}))
    # try:
    #     del request.session['login_user']
    #     # logout(request)
    #     return render(request,"blog/index.html",)
    #
    # except:
    #     pass
        # return redirect(reverse("blog:index",kwargs={'index':'1'}))



    # del request.session['login_user']
    # 转发到首页
    # return redirect(reverse("blog:index",kwargs={'index':'1'}))


def reset_psw(request):
    '''
    修改用户密码
    :param request:
    :return:
    '''
    if request.method == 'GET':
        return render(request, "blog/update_pass.html", {})
    elif request.method == 'POST':
        # 获取需要的数据
        username = request.POST['username']
        userpass = request.POST['userpass']
        new_pass = request.POST['new_pass']

        if userpass == new_pass:
             return render(request, "blog/update_pass.html",
                           {"error_msg": "新密码和旧密码不能重复"})
        else:
            try:
                # 先查询数据库是否有此用户
                # author = models.Author.objects.get(username=username,userpass=userpass)
                user = authenticate(username=username,password = userpass)
                # user = User.objects.get(username=username,password = userpass)
            except:
                # 如果没有这个用户
                error_msg = "用户名或密码不正确！！！！"
                return render(request, "blog/update_pass.html",
                              {"error_msg": error_msg})
            else:
                # 修改其中一个id=1的name字段，再save，相当于SQL中的UPDATE
                # test1 = Test.objects.get(id=1)
                # test1.name = 'Google'
                # test1.save()
                # 另外一种方式
                #Test.objects.filter(id=1).update(name='Google')
                # 加密处理
                new_pass = make_password(new_pass)
                user.password = new_pass
                # user.set_password(password=new_pass)
                user.save()
                # print("新密码：%s" % new_pass)
                return render(request, "blog/login.html",
                              {"error_msg":"密码修改成功，请重新登录"})
                # # 如果注册过，判断密码对不对
                # ret = models.Author.objects.filter(username=username).first()
                # # 校验密码
                # is_psw_true = check_password(userpass,ret.userpass)
                #
                # if is_psw_true:
                #     author = models.Author()
                #     author = make_password(new_pass)
                #     author.save()
                #     error_msg = "密码修改成功！"
                # else:
                #     error_msg = "密码错误"
                # return render(request, "blog/update_pass.html", {"error_msg": error_msg})
        # author = models.Author.objects.get(username=username,userpass=userpass)

        # if len(new_pass) < 6:
        #     return render(request,"blog/update_pass.html",{"error_msg":"密码不能小于六位"})
        #
        # author.update(userpass=new_pass)
        # author.save()
        # return render(request,"blog/update_pass.html",{"error_msg":"修改成功"})


def artical_delete(request,article_id):
    '''
    删除发表的文章
    :param request:
    :param article_id:
    :return:
    '''
    # artical_id = request.POST['article_id']
    article = models.Article.objects.get(pk=article_id)
    article.delete()
    # # 跳转到文章列表页面
    # return redirect(reverse('blog:articlelist',kwargs={'inde':2}))
    return HttpResponse('删除成功')


def xiuGai_article(request,article_id):
    '''
    修改文章内容
    :param request:
    :param article_id:
    :return:
    '''
     # 获取当前的文章
    if request.method == 'GET':
        article = models.Article.objects.get(pk=article_id)
        return render(request,"blog/xiuGai_article.html", {"alist":article})
    elif request.method == 'POST':
        # 获取文章标题和内容
        title = request.POST['title']
        content = request.POST['content']
        #  创建文章对象，并保存到数据库
        article = models.Article.objects.get(pk=article_id)
        article.title=title
        article.content= content
        # # 执行完save()函数，article数据已经存储在数据库了，同时程序中的article被自动赋值了id
        article.save()
        # 同步缓存数据，数据改变了 重新查询数据库
        utils.cache_index(True)
        # 跳转到详情页面，展示发表的文章
        return render(request, 'blog/xiugai_article_ok.html',{})







