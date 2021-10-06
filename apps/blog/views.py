from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy, reverse
from django.utils.text import slugify
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.list import MultipleObjectMixin
from .models import Article, Comment, ArticleRating
from .forms import ArticleForm, CommentForm, RatingForm
from django_filters.views import FilterView
from .filters import ArticleFilter
# from .utils import get_paginate_tags


class ArticleDetailView(MultipleObjectMixin, DetailView):
    model = Article
    template_name = 'blog/detail.html'
    form_class = CommentForm
    paginate_by = 1

    def get_context_data(self, **kwargs):
        object_list = Comment.objects.filter(article=self.get_object())
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['form'] = CommentForm(initial={'article': self.object, 'author': self.request.user})
        context['rating_form'] = RatingForm(initial={'article': self.object, 'user': self.request.user, 'rating': 5} )
        context['comments'] = self.object.comment_set.all()
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

    def rating_form_valid(self, rating_form):
        return super().rating_form_valid(rating_form)

    def get_success_url(self):
        return reverse_lazy('article_detail', kwargs={'slug': self.object.slug})


class ArticleListView(FilterView):
    model = Article
    paginate_by = 3
    template_name = 'blog/home.html'
    filterset_class = ArticleFilter

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        # tags = get_paginate_tags(self.request)
        # context.update(**tags)
        # print(tags)
        print(context)
        print(self.request.GET)
        return context


class ArticleCreateView(SuccessMessageMixin, CreateView):
    model = Article
    template_name = 'blog/article_create.html'
    success_message = 'Статья успешно добавлена'
    form_class = ArticleForm

    def form_valid(self, form):
        self.obj = form.save(commit=False)
        self.obj.author = self.request.user
        self.obj.save()
        return super().form_valid(form)

    # def post(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #     form = self.get_form()
    #     if form.is_valid():
    #         return self.form_valid(form)
    #     else:
    #         return self.form_invalid(form)
    #
    # def form_valid(self, form):
    #     self.art = form.save(commit=False)
    #     self.art.author = self.request.user
    #     self.art.slug = slugify(str(self.art.title).replace(' ', '-'))
    #     self.art.save()
    #     return super().form_valid(form)
    #
    # def get_success_url(self):
    #     return reverse_lazy('article_detail', kwargs={'slug': self.object.slug})


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


class CommentCreateView(SuccessMessageMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/detail.html'
    success_message = 'Комментарий опубликован'

    def get_success_url(self):
        return reverse_lazy('article_detail', kwargs={'slug': self.object.article.slug})


class RatingCreateView(CreateView):
    model = ArticleRating
    form_class = RatingForm
    template_name = 'blog/detail.html'

    def get_success_url(self):
        return reverse_lazy('article_detail', kwargs={'slug': self.object.article.slug})