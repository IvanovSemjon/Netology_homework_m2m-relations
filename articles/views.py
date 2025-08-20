from django.shortcuts import render
from django.db.models import Case, When, BooleanField

from articles.models import Article


def articles_list(request):
    template = 'articles/news.html'
    
    articles = Article.objects.prefetch_related(
        'articlescope_set__scope'
    ).order_by('-published_at')
    
    # Для каждой статьи сортируем разделы: основной первым, остальные по алфавиту
    for article in articles:
        scopes = article.articlescope_set.select_related('scope').order_by(
            Case(When(is_main=True, then=0), default=1),
            'scope__topic'
        )
        article.sorted_scopes = scopes
    
    context = {'object_list': articles}
    return render(request, template, context)
