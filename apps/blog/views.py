from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ValidationError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.list import MultipleObjectMixin, ListView
from .models import Article, Comment, ArticleRating, Like, Image
from .forms import ArticleForm, CommentForm, RatingForm, LikeForm, ProfileForm, ArticleFormSet
from django_filters.views import FilterView
from .filters import ArticleFilter
from .utils import get_paginate_tags
from ..accounts.models import MyUser
from ..accounts.forms import MyPasswordChangeForm
from django.utils.translation import ugettext_lazy as _


class ArticleDetailView(MultipleObjectMixin, DetailView):
    """Формируем страницу детального отображения статьи"""
    model = Article
    template_name = 'blog/detail.html'
    form_class = CommentForm
    paginate_by = 8
    ordering = '-create_date'

    def get_context_data(self, **kwargs):
        object_list = Comment.objects.select_related('article', 'author').filter(article=self.get_object(), is_published=True)
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['form'] = CommentForm(initial={'article': self.object, 'author': self.request.user})
        images = Image.objects.select_related('article').filter(article=self.object)
        if images:
            context['images'] = images
        context['rating_form'] = RatingForm(
            initial={'article': self.object, 'user': self.request.user, 'rating': 5})

        if self.request.user.is_authenticated:
            context['like_form'] = LikeForm(initial={'article': self.object, 'user': self.request.user, 'like': True})
            like = Like.objects.select_related('article', 'user').filter(user=self.request.user, article=self.object, like=True)
            if like:
                context['button'] = '\u2661' + _('дизлайкнуть')
            else:
                context['button'] = '\u2764\uFE0F' + _('лайкнуть')
        return context

    def get_success_url(self):
        return reverse_lazy('article_detail', kwargs={'slug': self.object.slug})


class ArticleListView(FilterView):
    """Список всех статей"""
    model = Article
    paginate_by = 16
    template_name = 'blog/home.html'
    filterset_class = ArticleFilter

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        params = get_paginate_tags(self.request)
        context.update(**params)
        return context


class ArticleCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    """Создание статей авторизованными пользователями"""
    model = Article
    template_name = 'blog/article_create.html'
    success_message = _('Статья успешно добавлена')
    form_class = ArticleForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ArticleForm(initial={'author': self.request.user})
        context['formset'] = ArticleFormSet(self.request.POST or None, self.request.FILES or None)
        return context

    def form_valid(self, form):
        """Check if form valid"""
        formset = ArticleFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object)
        if formset.is_valid():
            response = super().form_valid(form)
            formset.instance = self.object
            formset.save()
            return response
        else:
            return super().form_invalid(form)


class ArticleUpdateView(SuccessMessageMixin, PermissionRequiredMixin, UpdateView):
    """Редактирование статьи"""
    model = Article
    form_class = ArticleForm
    template_name = 'blog/article_update.html'
    success_message = _('Статья успешно изменена')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formset'] = ArticleFormSet(self.request.POST or None, self.request.FILES or None)
        return context

    def has_permission(self):
        if self.get_object().author == self.request.user:
            return True
        return False

    def form_valid(self, form):
        """Check if form valid"""
        formset = ArticleFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object)
        if formset.is_valid():
            response = super().form_valid(form)
            formset.instance = self.object
            formset.save()
            return response
        else:
            return super().form_invalid(form)


class ArticleDeleteView(DeleteView):
    model = Article
    success_url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        messages.success(request, _('Статья успешно удалена'))
        return self.post(request, *args, **kwargs)


class CommentCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    """Создание комментария"""
    model = Comment
    form_class = CommentForm
    template_name = 'blog/detail.html'
    success_message = 'Комментарий опубликован'

    def form_invalid(self, form, **kwargs):
        messages.add_message(self.request, messages.ERROR, _('Поле комментария не может быть пустым!!!'))
        return redirect(reverse_lazy('article_detail', kwargs={'slug': self.kwargs['slug']}))

    def get_success_url(self):
        return reverse_lazy('article_detail', kwargs={'slug': self.object.article.slug})


class RatingCreateView(LoginRequiredMixin, CreateView):
    """Создание оценки статьи пользователем"""
    model = ArticleRating
    form_class = RatingForm
    template_name = 'blog/detail.html'

    def get_success_url(self):
        return reverse_lazy('article_detail', kwargs={'slug': self.object.article.slug})


class LikeCreateView(CreateView):
    """Добавление статьи в избранное"""
    model = Like
    form_class = LikeForm
    template_name = 'blog/detail.html'

    def get_success_url(self):
        return reverse_lazy('article_detail', kwargs={'slug': self.object.article.slug})


class ProfileDetailView(MultipleObjectMixin, LoginRequiredMixin, DetailView):
    """Профиль пользователя"""
    model = MyUser
    template_name = 'blog/profile.html'
    paginate_by = 20

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        object_list = Article.objects.filter(author=self.request.user).select_related('author')
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['form'] = MyPasswordChangeForm(user=self.request.user)
        context['profile_form'] = ProfileForm(instance=self.request.user)
        return context

    def get_success_url(self):
        return reverse_lazy('profile')


class ProfileUpdateView(UpdateView):
    """Редактирование профиля"""
    model = MyUser
    form_class = ProfileForm
    template_name = 'blog/profile.html'

    def get_object(self, queryset=None):
        return self.request.user

    def form_invalid(self, form, **kwargs):
        messages.add_message(self.request, messages.ERROR, _(form.errors.as_text()))
        return redirect(reverse_lazy('profile'))

    def get_success_url(self):
        return reverse_lazy('profile')


class Subscribes(View):
    """Подписка на автора"""
    def post(self, *args, **kwargs):
        article = Article.objects.select_related('author', 'category').filter(slug=kwargs['slug']).first()
        author = article.author
        current_user = self.request.user
        if current_user != author:
            if author.subscribes.filter(pk=current_user.pk).exists():
                author.subscribes.remove(current_user)
            else:
                author.subscribes.add(current_user)
        return redirect(reverse_lazy('article_detail', kwargs={'slug': article.slug}))


class MyUserFavouriteArticles(LoginRequiredMixin, ListView):
    """Список избранных статей пользователя"""
    paginate_by = 10
    model = Like
    template_name = 'blog/user_liked_articles.html'

    def get_queryset(self):
        qs = Like.objects.filter(user=self.request.user, like=True).select_related('article', 'user')
        object_list = []
        for like in qs.select_related('article', 'user'):
            object_list.append(like.article)
        return object_list
