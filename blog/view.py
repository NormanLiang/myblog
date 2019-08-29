#from django.http import HttpResponse
from django.shortcuts import render
from articles.models import ArticlePost
from django.core.paginator import Paginator

#def Hello(request):
#    return HttpResponse('Hello World!')

def hello(request):
    context = {}
    context['hello'] = 'Hello World!'
    return render(request, 'hello.html', context)

def index(request):

    articles = ArticlePost.objects.all()

    paginator = Paginator(articles, 10)

#    page = request.GET.get('page')
    num = paginator.num_pages

    articles = paginator.get_page(num)

    context = {'articles':reversed(articles)}
    return render(request, 'index.html', context)