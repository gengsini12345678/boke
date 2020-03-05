'''
工具模块，专门定义各种小功能处理函数
如：缓存数据的同步
'''

from django.core.cache import cache

from . import models

def cache_index(is_changed=False):
    '''
    缓存首页数据
    :return:
    '''
    print("首页数据加载，查询缓存中的数据")
    article_list = cache.get("article_list")
    if article_list is None or is_changed == True:
        # 查询数据库
        print("开始连接查询数据库中的数据.....")
        article_list = models.Article.objects.all()
        print("数据库数据获取完成，同步缓存")
        cache.set("article_list",article_list)

    print("首页数据加载完成")
    return article_list


def cache_self_article(is_changed=False):
    '''
    缓存自己发表的文章
    :param is_changed:
    :return:
    '''
    pass

