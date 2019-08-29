from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import ArticlePost
from .forms import ArticlePostForm

from django.contrib.auth.models import User
from django.urls import reverse

from django.core.paginator import Paginator

import markdown

# Create your views here.


#def article_list(request):
#    return HttpResponse('Hello World!') 

def article_update(request, id):
    article = ArticlePost.objects.get(id=id)
    print('post it here')
    if request.method == 'POST':
        article_post_form = ArticlePostForm(data=request.POST)
#        print('post it here')
        if article_post_form.is_valid():
            article.title = request.POST['title']
            article.body = request.POST['body']
            article.save()
            return redirect('articles:article_detail', id=id)
        else:
            return HttpResponse('Opps, Something is Wrong')
    else:
        article_post_form = ArticlePostForm()
        context = {'article':article, 'article_post_form':article_post_form}
        return render(request, 'articles/update.html', context)


def article_delete(request, id):
    article = ArticlePost.objects.get(id=id)
    article.delete()
    return redirect('articles:article_list')


def article_create(request):
    if request.method == 'POST':
        article_post_form = ArticlePostForm(data=request.POST)
        
        if article_post_form.is_valid():
            new_article = article_post_form.save(commit=False)
            new_article.author = User.objects.get(id=1)
            new_article.save()

            return redirect('articles:article_detail', id=new_article.id)
        else:
            return HttpResponse('Opps, Something is Wrong')
    else:
        article_post_form = ArticlePostForm()
        context = {'article_post_form':article_post_form}

        return render(request, 'articles/create.html', context)

def article_list(request):

    if request.GET.get('order') == 'total_views':
        article_list = ArticlePost.objects.all().order_by('-total_views')
        order = 'total_views'
    else:
        article_list = ArticlePost.objects.all()
        order = 'normal'

    paginator = Paginator(article_list, 1)

    page = request.GET.get('page')
    articles = paginator.get_page(page)

    context = {'articles':articles, 'order':order}
    return render(request, 'articles/list.html', context)

def article_detail(request, id):
    article = ArticlePost.objects.get(id=id)

    article.body = markdown.markdown(article.body,
        extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])

    article.total_views += 1
    article.save(update_fields=['total_views'])
    context = {'article': article}
    return render(request, 'articles/detail.html', context)
