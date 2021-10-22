from django.core.mail import EmailMultiAlternatives

cyrillic_letters = {
        u'а': u'a',
        u'б': u'b',
        u'в': u'v',
        u'г': u'g',
        u'д': u'd',
        u'е': u'e',
        u'ё': u'e',
        u'ж': u'zh',
        u'з': u'z',
        u'и': u'i',
        u'й': u'y',
        u'к': u'k',
        u'л': u'l',
        u'м': u'm',
        u'н': u'n',
        u'о': u'o',
        u'п': u'p',
        u'р': u'r',
        u'с': u's',
        u'т': u't',
        u'у': u'u',
        u'ф': u'f',
        u'х': u'h',
        u'ц': u'ts',
        u'ч': u'ch',
        u'ш': u'sh',
        u'щ': u'sch',
        u'ъ': u'',
        u'ы': u'y',
        u'ь': u'',
        u'э': u'e',
        u'ю': u'yu',
        u'я': u'ya',
        u'ґ': u'g',
        u'ї': u'yi',
        u'і': u'i',
    }


def from_cyrillic_to_eng(text: str):
    text = text.replace(' ', '_').lower()
    tmp = ''
    for ch in text:
        tmp += cyrillic_letters.get(ch, ch)
    return tmp


def get_paginate_tags(request):
    o = request.GET.get('o')
    author = request.GET.get('author')
    category = request.GET.get('category')
    title = request.GET.get('title')
    paginate_tags = {'o': o,
                     'author': author,
                     'category': category,
                     'title': title,
                     }
    return paginate_tags


def send(subject, html, from_email, to_email):
    msg = EmailMultiAlternatives(
    subject,
    html,
    from_email,
    to_email
    )
    msg.attach_alternative(html, "text/html")
    msg.send()


class ArticlePostMixin:
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
        return super().form_valid(rating_form)

    def like_form_valid(self, like_form):
        return super().form_valid(like_form)


