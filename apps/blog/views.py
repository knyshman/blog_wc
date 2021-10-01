import stats
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpRequest
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormMixin
from django.views.generic.list import MultipleObjectMixin
from .models import Article, Author, Comment
from .forms import ArticleForm, CommentForm
from django_filters.views import FilterView
from .filters import ArticleFilter


class ArticleDetailView(MultipleObjectMixin, DetailView):
    model = Article
    template_name = 'blog/detail.html'
    form_class = CommentForm
    paginate_by = 2

    def get_context_data(self, **kwargs):
        object_list = Comment.objects.filter(article=self.get_object())
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['form'] = CommentForm(initial={'article': self.object})
        context['comments'] = self.object.comment_set.all()
        if context['comments']:
            qs = Article.objects.prefetch_related('comment_set').filter(title=self.object)
            if qs:
                for obj in qs:
                    grade = str(round(stats.mean([int(comment.rating) for comment in obj.comment_set.all()]), 2))
                context['rating'] = grade
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.comment = form.save(commit=False)
        self.comment.author = self.request.user
        self.comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('article_detail', kwargs={'slug': self.object.slug})


class ArticleListView(FilterView):
    model = Article
    paginate_by = 16
    template_name = 'blog/home.html'
    filterset_class = ArticleFilter

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        print(context)
        return context


class ArticleCreateView(SuccessMessageMixin, CreateView):
    model = Article
    template_name = 'blog/article_create.html'
    success_message = 'Статья успешно добавлена'
    form_class = ArticleForm


class ArticleUpdateView(SuccessMessageMixin, UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'blog/article_update.html'
    success_message = 'Статья успешно добавлена'


class ArticleDeleteView(DeleteView):
    model = Article
    success_url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        messages.success(request, 'Статья успешно удалена')
        return self.post(request, *args, **kwargs)


class CommentCreateView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/detail.html'

    def get_success_url(self):
        return reverse_lazy('article_detail', kwargs={'slug': self.object.article.slug})

# 'article_detail', kwargs={'slug': self.object.articles.slug}




