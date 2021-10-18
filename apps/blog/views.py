from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.list import MultipleObjectMixin, ListView
from .models import Article, Comment, ArticleRating, Like
from .forms import ArticleForm, CommentForm, RatingForm, LikeForm, ProfileForm
from django_filters.views import FilterView
from .filters import ArticleFilter
from .utils import get_paginate_tags
from ..accounts.models import MyUser
from ..accounts.forms import MyPasswordChangeForm
from django.utils.translation import ugettext_lazy as _
from .tasks import print_hello


class ArticleDetailView(MultipleObjectMixin, DetailView):
    model = Article
    template_name = 'blog/detail.html'
    form_class = CommentForm
    paginate_by = 1
    ordering = 'create_date'

    def get_context_data(self, **kwargs):
        object_list = Comment.objects.filter(article=self.get_object())
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['form'] = CommentForm(initial={'article': self.object, 'author': self.request.user})
        context['comments'] = self.object.comment_set.filter(is_published=True)
        if self.request.user.is_authenticated:
            context['rating_form'] = RatingForm(
                initial={'article': self.object, 'user': self.request.user, 'rating': 5})
            context['like_form'] = LikeForm(initial={'article': self.object, 'user': self.request.user, 'like': True})
            like = Like.objects.filter(user=self.request.user, article=self.object, like=True)
            if like:
                context['button'] = '\u2661' + _('дизлайкнуть')
            else:
                context['button'] = '\u2764\uFE0F' + _('лайкнуть')
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
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

    def like_form_valid(self, like_form):
        return super().like_form_valid(like_form)

    def get_success_url(self):
        return reverse_lazy('article_detail', kwargs={'slug': self.object.slug})


class ArticleListView(FilterView):
    model = Article
    paginate_by = 3
    template_name = 'blog/home.html'
    filterset_class = ArticleFilter

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        params = get_paginate_tags(self.request)
        context.update(**params)
        return context


class ArticleCreateView(SuccessMessageMixin, CreateView):
    model = Article
    template_name = 'blog/article_create.html'
    success_message = _('Статья успешно добавлена')
    form_class = ArticleForm

    def form_valid(self, form):
        self.obj = form.save(commit=False)
        self.obj.author = self.request.user
        self.obj.save()
        return super().form_valid(form)


class ArticleUpdateView(SuccessMessageMixin, UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'blog/article_update.html'
    success_message = _('Статья успешно изменена')


class ArticleDeleteView(DeleteView):
    model = Article
    success_url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        messages.success(request, _('Статья успешно удалена'))
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


class LikeCreateView(CreateView):
    model = Like
    form_class = LikeForm
    template_name = 'blog/detail.html'

    def get_success_url(self):
        return reverse_lazy('article_detail', kwargs={'slug': self.object.article.slug})


class ProfileDetailView(MultipleObjectMixin, DetailView):
    model = MyUser
    template_name = 'blog/profile.html'
    query_pk_and_slug = True
    paginate_by = 3

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        object_list = Article.objects.filter(author=self.request.user).select_related('author')
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['form'] = MyPasswordChangeForm(user=self.request.user)
        context['profile_form'] = ProfileForm(instance=self.request.user)
        print_hello.delay()

        return context

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'pk': self.request.user.pk})


class ProfileUpdateView(UpdateView):
    model = MyUser
    form_class = ProfileForm
    template_name = 'blog/profile.html'

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, _('Номер телефона должен содержать только цифры(не более 10)'))
        return redirect(reverse_lazy('profile', kwargs={'pk': self.request.user.pk}), self.get_context_data(profile_form=form))

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'pk': self.request.user.pk})


class Subscribes(View):
    def post(self, *args, **kwargs):
        author = MyUser.objects.get(pk=kwargs['pk'])
        current_user = self.request.user
        if current_user != author:
            if current_user.subscribes.filter(pk=author.pk).exists():
                current_user.subscribes.remove(author)
            else:
                current_user.subscribes.add(author)
        return HttpResponseRedirect(self.request.GET.get('next', '/'))


class MyUserFavouriteArticles(ListView):
    paginate_by = 10
    model = Like
    template_name = 'blog/user_liked_articles.html'

    def get_queryset(self):
        qs = Like.objects.filter(user=self.request.user, like=True).select_related('article', 'user')
        object_list = []
        for like in qs:
            object_list.append(like.article)
        return object_list
