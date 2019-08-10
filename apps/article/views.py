from django.shortcuts import render,redirect

from django.http import HttpResponse

from .models import ArticlePost, ArticleColumn, ArticleCourse

from .forms import ArticlePostForm

from apps.comment.models import Comment

from apps.comment.forms import CommentForm

import markdown

from django.contrib.auth.models import  User

from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator

from django.db.models import Q


#视图函数
def article_list(request):
    # 从 url 中提取查询参数
    search = request.GET.get('search')
    order = request.GET.get('order')
    column = request.GET.get('column')
    course = request.GET.get('course')
    tag = request.GET.get('tag')

    # 初始化查询集
    article_list = ArticlePost.objects.all()

    # 搜索查询集
    if search:
        article_list = article_list.filter(
            Q(title__icontains=search) |
            Q(body__icontains=search)
        )
    else:
        search = ''

    # 栏目查询集
    if column is not None and column.isdigit():
        article_list = article_list.filter(column=column)
    # 栏目查询集
    if course is not None and course.isdigit():
        article_list = article_list.filter(course=course)

    # 标签查询集
    if tag and tag != 'None':
        article_list = article_list.filter(tags__name__in=[tag])

    # 查询集排序
    if order == 'total_views':
        article_list = article_list.order_by('-total_views')

    paginator = Paginator(article_list, 10)
    page = request.GET.get('page')
    articles = paginator.get_page(page)

    # 需要传递给模板（templates）的对象
    context = {
        'articles': articles,
        'order': order,
        'search': search,
        'column': column,
        'course': course,
        'tag': tag,
    }

    return render(request, 'article/list.html', context)


def article_detail(request,id):
    #
    article = ArticlePost.objects.get(id=id)

    comments = Comment.objects.filter(article=id)

    article.total_views += 1

    article.save(update_fields=['total_views'])

    #将markdown语法渲染成html样式
    # 修改 Markdown 语法渲染
    md = markdown.Markdown(
        extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ]
    )
    article.body = md.convert(article.body)

    comment_form = CommentForm()
    # 新增了md.toc对象
    context = {'article': article,
               'toc': md.toc,
               'comments': comments,
               'comment_form': comment_form,
               }

    return render(request, 'article/detail.html', context)


@login_required
def article_create(request):
    if request.method == "POST":

        article_post_form = ArticlePostForm(request.POST, request.FILES)
        # 判断提交的数据是否满足模型的要求
        if article_post_form.is_valid():
            # 保存数据，但暂时不提交到数据库中
            new_article = article_post_form.save(commit=False)
            # 指定数据库中 id=1 的用户为作者
            # 如果你进行过删除数据表的操作，可能会找不到id=1的用户
            # 此时请重新创建用户，并传入此用户的id
            new_article.author = User.objects.get(id=request.user.id)

            # 新增的代码
            if request.POST['column'] != 'none':
                new_article.column = ArticleColumn.objects.get(id=request.POST['column'])

            # 新增的代码
            if request.POST['course'] != 'none':
                new_article.course = ArticleCourse.objects.get(id=request.POST['course'])

            # 将新文章保存到数据库中
            new_article.save()
            # 新增代码，保存 tags 的多对多关系
            article_post_form.save_m2m()
            # 完成后返回到文章列表
            return redirect("article:article_list")
        # 如果数据不合法，返回错误信息
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    # 如果用户请求获取数据
    else:
        # 创建表单类实例
        article_post_form = ArticlePostForm()

        columns = ArticleColumn.objects.all()

        courses = ArticleCourse.objects.all()
        # 赋值上下文
        context = {'article_post_form': article_post_form, 'columns': columns,'courses':courses,}
        # 返回模板
        return render(request, 'article/create.html', context)


@login_required
def article_delete(request,id):
    #删除文章
    #根据 id 获取要删除的文章
    article = ArticlePost.objects.get(id=id)

    if request.user != article.author:
        return HttpResponse("抱歉，你无权修改这篇文章。")
    #调用delete（）方法删除文章
    else:
        article.delete()
    #完成删除后返回文章列表
        return redirect("article:article_list")



@login_required
def article_update(request, id):
    # 更新文章
    """
    更新文章的视图函数
    通过POST方法提交表单，更新titile、body字段
    GET方法进入初始表单页面
    id： 文章的 id
    """

    # 获取需要修改的具体文章对象
    article = ArticlePost.objects.get(id=id)

    if request.user != article.author:
        return HttpResponse("抱歉，你无权修改这篇文章。")


    # 判断用户是否为 POST 提交表单数据
    if request.method == "POST":
        # 将提交的数据赋值到表单实例中
        article_post_form = ArticlePostForm(data=request.POST)
        print(article_post_form)
        # 判断提交的数据是否满足模型的要求
        if article_post_form.is_valid():
            print("gsdgsd")
            # 保存新写入的 title、body 数据并保存
            article.title = request.POST['title']
            article.body = request.POST['body']
            article.summary = request.POST['summary']

            if request.POST['column'] != 'none':
                article.column = ArticleColumn.objects.get(id=request.POST['column'])
            else:
                article.column = None

            if request.POST['course'] != 'none':
                article.course = ArticleCourse.objects.get(id=request.POST['course'])
            else:
                article.course = None

            if request.FILES.get('avatar'):
                article.avatar = request.FILES.get('avatar')

            article.tags.set(*request.POST.get('tags').split(','), clear=True)

            article.save()
            # 完成后返回到修改后的文章中。需传入文章的 id 值
            return redirect("article:article_detail", id=id)
        # 如果数据不合法，返回错误信息
        else:
            return HttpResponse("表单内容有误，请重新填写。")

    # 如果用户 GET 请求获取数据
    else:
        # 创建表单类实例
        article_post_form = ArticlePostForm()
        # 赋值上下文，将 article 文章对象也传递进去，以便提取旧的内容
        columns = ArticleColumn.objects.all()

        courses = ArticleCourse.objects.all()

        context = {
            'article': article,
            'article_post_form': article_post_form,
            'columns': columns,
            'courses': courses,
            'tags': ','.join([x for x in article.tags.names()]),
        }
        # 将响应返回到模板中
        return render(request, 'article/update.html', context)


