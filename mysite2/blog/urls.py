from django.conf.urls import url

from . import views

app_name = "blog"
urlpatterns = [
    url(r'^index/(?P<index>\d*)$',views.index,name="index"),

    # url(r'^(?P<index>\d*)/$',views.index,name="index"),
    url(r'^user_login/$',views.user_login,name="user_login"),
    url(r'^register/$',views.register,name="register"),
    url(r'^article_publish/$',views.article_publish,name="article_publish"),
    url(r'^(?P<article_id>\d+)/article_details/$',views.article_details,name="article_details"),
    url(r'^articlelist/(?P<inde>\d*)$',views.article_list,name="articlelist"),
    # 修改密码
    url(r'^reset_psw/$',views.reset_psw,name="reset_psw"),
    # 删除文章
    # url(r'^(?P<article_id>\d+)/delete_artical/$',views.delete_artical,name="delete_artical"),
    # url(r'^delete_artical/$',views.delete_artical,name="delete_artical"),
    url(r'^(?P<article_id>\d+)/artical_delete/$',views.artical_delete,name="artical_delete"),
    # 修改文章内容
    url(r'^(?P<article_id>\d+)/xiuGai_article/$',views.xiuGai_article,name="xiuGai_article"),

    url(r'^logout_view/$',views.logout_view,name="logout_view"),

]