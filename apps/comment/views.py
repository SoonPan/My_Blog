from django.shortcuts import render, get_object_or_404, redirect

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from apps.article.models import ArticlePost
from .forms import CommentForm

from notifications.signals import notify
from django.contrib.auth.models import User

from django.http import JsonResponse

from .models import Comment

# 文章评论
@login_required(login_url='/userprofile/login/')


# def post_comment(request, article_id):
#     article = get_object_or_404(ArticlePost, id=article_id)
#
#     # 处理 POST 请求
#     if request.method == 'POST':
#         comment_form = CommentForm(request.POST)
#         if comment_form.is_valid():
#             new_comment = comment_form.save(commit=False)
#             new_comment.article = article
#             new_comment.user = request.user
#             new_comment.save()
#             return redirect(article)
#         else:
#             return HttpResponse("表单内容有误，请重新填写。")
#     # 处理错误请求
#     else:
#         return HttpResponse("发表评论仅接受POST请求。")

def post_comment(request, article_id, parent_comment_id=None):
    article = get_object_or_404(ArticlePost, id=article_id)

    # 处理 POST 请求
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.article = article
            new_comment.user = request.user

            # 二级回复
            if parent_comment_id:
                parent_comment = Comment.objects.get(id=parent_comment_id)
                # 若回复层级超过二级，则转换为二级
                new_comment.parent_id = parent_comment.get_root().id
                # 被回复人
                new_comment.reply_to = parent_comment.user
                new_comment.save()

                if not parent_comment.user.is_superuser:
                        notify.send(
                            request.user,
                            recipient=parent_comment.user,
                            verb='回复了你',
                            target=article,
                            action_object=new_comment,
                        )
                    # 新增代码，添加锚点
                return JsonResponse({"code": "200 OK", "new_comment_id": new_comment.id})
            new_comment.save()

            if not request.user.is_superuser:
                    notify.send(
                        request.user,
                        recipient=User.objects.filter(is_superuser=1),
                        verb='回复了你',
                        target=article,
                        action_object=new_comment,
                    )
            redirect_url = article.get_absolute_url() + '#comment_elem_' + str(new_comment.id)
            return redirect(redirect_url)
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    # 处理 GET 请求
    elif request.method == 'GET':
        comment_form = CommentForm()
        context = {
            'comment_form': comment_form,
            'article_id': article_id,
            'parent_comment_id': parent_comment_id
        }
        return render(request, 'comment/reply.html', context)
    # 处理其他请求
    else:
        return HttpResponse("仅接受GET/POST请求。")


def comment_delete(request, article_id, comment_id,flag):
    article = get_object_or_404(ArticlePost, id=article_id)
    delete_comment = Comment.objects.get(id=comment_id)

    if flag:
        delete_comment.delete()
        redirect_url = article.get_absolute_url()
    else:
        delete_comment.body = '该评论已被删除！'
        delete_comment.save()
        redirect_url = article.get_absolute_url() + '#comment_elem_' + str(comment_id)
    return redirect(redirect_url)

def edit_comment(request, article_id,comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    article = get_object_or_404(ArticlePost, id=article_id)
    # 处理 POST 请求
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment.body = request.POST['body']
            comment.save()
            return JsonResponse({"code": "200 OK", "comment_id": comment_id})
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    # 处理 GET 请求
    elif request.method == 'GET':
        comment= get_object_or_404(Comment, id=comment_id)
        content = comment.body
        data ={"body":content}
        comment_form = CommentForm(data)

        context = {
            'comment_form': comment_form,
            'article_id': article_id,
            'comment_id': comment_id
        }
        return render(request, 'comment/change.html', context)
    # 处理其他请求
    else:
        return HttpResponse("仅接受GET/POST请求。")
