from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from .models import Article, Author
from .forms import ArticleForm

#filterview
class ArticleDetailView(DetailView):
    model = Article
    template_name = 'blog/detail.html'


class ArticleListView(ListView):
    model = Article
    paginate_by = 16
    template_name = 'blog/home.html'


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