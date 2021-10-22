from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import AnonymousUser
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect, request
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.list import MultipleObjectMixin, ListView
from .models import Article, Comment, ArticleRating, Like, Image
from .forms import ArticleForm, CommentForm, RatingForm, LikeForm, ProfileForm, ArticleFormSet
from django_filters.views import FilterView
from .filters import ArticleFilter
from .utils import get_paginate_tags, ArticlePostMixin
from ..accounts.models import MyUser
from ..accounts.forms import MyPasswordChangeForm
from django.utils.translation import ugettext_lazy as _


class ArticleDetailView(MultipleObjectMixin, ArticlePostMixin, DetailView):
    model = Article
    template_name = 'blog/detail.html'
    form_class = CommentForm
    paginate_by = 8
    ordering = 'create_date'

    def get_context_data(self, **kwargs):
        object_list = Comment.objects.filter(article=self.get_object())
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['form'] = CommentForm(initial={'article': self.object, 'author': self.request.user})
        context['comments'] = self.object.comment_set.filter(is_published=True)
        images = Image.objects.filter(article=self.object).select_related('article')
        if images:
            context['images'] = images
        context['rating_form'] = RatingForm(
            initial={'article': self.object, 'user': self.request.user, 'rating': 5})
        context['like_form'] = LikeForm(initial={'article': self.object, 'user': self.request.user, 'like': True})
        if self.request.user.is_authenticated:
            like = Like.objects.filter(user=self.request.user, article=self.object, like=True)
            if like:
                context['button'] = '\u2661' + _('дизлайкнуть')
            else:
                context['button'] = '\u2764\uFE0F' + _('лайкнуть')
        else:
            context['button'] = '\u2764\uFE0F' + _('лайкнуть')
        return context

    def get_success_url(self):
        return reverse_lazy('article_detail', kwargs={'slug': self.object.slug})


class ArticleListView(FilterView):
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
    model = Article
    template_name = 'blog/article_create.html'
    success_message = _('Статья успешно добавлена')
    form_class = ArticleForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formset'] = ArticleFormSet(self.request.POST or None, self.request.FILES or None)
        return context

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            messages.add_message(self.request, messages.ERROR, _('Чтобы публиковать статьи, войдите на сайт!'))
        return super().dispatch(request, *args, **kwargs)

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


class ArticleUpdateView(SuccessMessageMixin, UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'blog/article_update.html'
    success_message = _('Статья успешно изменена')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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


class ArticleDeleteView(DeleteView):
    model = Article
    success_url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        messages.success(request, _('Статья успешно удалена'))
        return self.post(request, *args, **kwargs)

#todo
class CommentCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/detail.html'
    success_message = 'Комментарий опубликован'

    def form_invalid(self, form, **kwargs):
        messages.add_message(self.request, messages.ERROR, _('Поле комментария не может быть пустым!!!'))
        return redirect(reverse_lazy('profile'))

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            messages.add_message(self.request, messages.ERROR, _('Чтобы комментировать статьи, войдите на сайт!'))
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('article_detail', kwargs={'slug': self.object.article.slug})

#todo
class RatingCreateView(LoginRequiredMixin, CreateView):
    model = ArticleRating
    form_class = RatingForm
    template_name = 'blog/detail.html'

    def get_success_url(self):
        return reverse_lazy('article_detail', kwargs={'slug': self.object.article.slug})

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            messages.add_message(self.request, messages.ERROR, _('Чтобы оценивать статьи, войдите на сайт!'))
        return super().dispatch(request, *args, **kwargs)

#todo
class LikeCreateView(LoginRequiredMixin, CreateView):
    model = Like
    form_class = LikeForm
    template_name = 'blog/detail.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            messages.add_message(self.request, messages.ERROR, _('Чтобы лайкать статьи, войдите на сайт!'))
        return super().dispatch(request, *args, **kwargs)

    def get_redirect_field_name(self):
        return reverse_lazy('article_detail', kwargs={'slug': self.request.POST.get('slug')})

    def get_success_url(self):
        return redirect(reverse_lazy('article_detail', kwargs={'slug': self.object.article.slug}))


class ProfileDetailView(MultipleObjectMixin, LoginRequiredMixin, DetailView):
    model = MyUser
    template_name = 'blog/profile.html'
    paginate_by = 3

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


class ProfileUpdateView(PermissionRequiredMixin, UpdateView):
    model = MyUser
    form_class = ProfileForm
    permission_required = 'blog.change_article'
    template_name = 'blog/profile.html'

    def get_object(self, queryset=None):
        return self.request.user

    def form_invalid(self, form, **kwargs):
        messages.add_message(self.request, messages.ERROR, _(form.errors.as_text()))
        return redirect(reverse_lazy('profile'))

    def get_success_url(self):
        return reverse_lazy('profile')

#todo
class Subscribes(LoginRequiredMixin, View):
    def post(self, *args, **kwargs):
        article = Article.objects.filter(slug=kwargs['slug']).first()
        author = article.author
        current_user = self.request.user
        if current_user != author:
            if current_user.subscribes.filter(pk=author.pk).exists():
                current_user.subscribes.remove(author)
            else:
                current_user.subscribes.add(author)
        return HttpResponseRedirect(self.request.GET.get('next', '/'))

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            messages.add_message(self.request, messages.ERROR, _('Чтобы подписаться на автора, войдите на сайт!'))
        return super().dispatch(request, *args, **kwargs)


class MyUserFavouriteArticles(LoginRequiredMixin, ListView):
    paginate_by = 10
    model = Like
    template_name = 'blog/user_liked_articles.html'

    def get_queryset(self):
        # print(self.request.user.)
        qs = Like.objects.filter(user=self.request.user, like=True).select_related('article', 'user')
        object_list = []
        # get_articles.delay()
        for like in qs:
            object_list.append(like.article)
        return object_list
