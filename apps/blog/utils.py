# def get_filter(request):
#
#
# cyrillic_letters = {
#         u'а': u'a',
#         u'б': u'b',
#         u'в': u'v',
#         u'г': u'g',
#         u'д': u'd',
#         u'е': u'e',
#         u'ё': u'e',
#         u'ж': u'zh',
#         u'з': u'z',
#         u'и': u'i',
#         u'й': u'y',
#         u'к': u'k',
#         u'л': u'l',
#         u'м': u'm',
#         u'н': u'n',
#         u'о': u'o',
#         u'п': u'p',
#         u'р': u'r',
#         u'с': u's',
#         u'т': u't',
#         u'у': u'u',
#         u'ф': u'f',
#         u'х': u'h',
#         u'ц': u'ts',
#         u'ч': u'ch',
#         u'ш': u'sh',
#         u'щ': u'sch',
#         u'ъ': u'',
#         u'ы': u'y',
#         u'ь': u'',
#         u'э': u'e',
#         u'ю': u'yu',
#         u'я': u'ya',
#         u'ґ': u'g',
#         u'ї': u'yi',
#         u'і': u'i',
#     }
#
#
# def from_cyrillic_to_eng(text: str):
#     text = text.replace(' ', '_').lower()
#     tmp = ''
#     for ch in text:
#         tmp += cyrillic_letters.get(ch, ch)
#     return tmp

#
# def get_paginate_tags(request):
#     o = request.GET.get('o')
#     author = request.GET.get('author')
#     category = request.GET.get('category')
#     title = request.GET.get('title')
#     paginate_tags = {'o': o,
#                      'author': author.strip(),
#                      'category': category.strip(),
#                      'title': title,
#                      }
#     return paginate_tags

