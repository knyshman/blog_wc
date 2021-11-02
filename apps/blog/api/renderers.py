from rest_framework.renderers import JSONRenderer
from django.utils.translation import ugettext_lazy as _


class CustomRenderer(JSONRenderer):

    def render(self, data, accepted_media_type=None, renderer_context=None):
        if renderer_context['response'].status_code == 200:
            response = {'response': {'error': False,
                                     'status_code': renderer_context['response'].status_code,
                                     'message': _("Успех"),
                                     },
                        'object_data': data
                        }
        elif renderer_context['response'].status_code == 201:
            response = {'response': {'error': False,
                                     'status_code': renderer_context['response'].status_code,
                                     'message': _("Запрос выполнен"),
                                     },
                        'object_data': data,
                        'object_data_message': _(" Внесение изменений в базу данных ")
                        },
        elif renderer_context['response'].status_code == 400:
            response = {'response': {'error': True,
                                     'status_code': renderer_context['response'].status_code,
                                     'message': _("Синтаксическая ошибка"),
                                     },
                        'object_data': data
                        }
        elif renderer_context['response'].status_code == 403:
            response = {'response': {'error': True,
                                     'status_code': renderer_context['response'].status_code,
                                     'message': _("У Вас нет доступа к этой странице"),
                                     },
                        'object_data': data
                        }
        elif renderer_context['response'].status_code == 404:
            response = {'response': {'error': True,
                                     'status_code': renderer_context['response'].status_code,
                                     'message': _("Запрашиваемая страница не найдена") ,
                                     },
                        'object_data': data
                        }
        elif renderer_context['response'].status_code == 500:
            response = {'response': {'error': True,
                                     'status_code': renderer_context['response'].status_code,
                                     'message': _("Ошибка сервера"),
                                     },
                        'object_data': data
                        }
        else:
            try:
                response = {'response': {'error': True,
                                         'status_code': renderer_context['response'].status_code,
                                         'message': data['detail'],
                                         }
                            }
            except KeyError:
                response = {'response': {'error': True,
                                         'code': renderer_context['response'].status_code,
                                         'message': _("Ошибка значения"),
                                         }
                            }
        return super().render(response, accepted_media_type, renderer_context)