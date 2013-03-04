from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings


def listing(request, obj_list):
    paginator = Paginator(obj_list, getattr(settings, 'DEFAULT_PAGINATOR_ITEMS', 2))
    page_param = request.GET.get('page')
    try:
        page = paginator.page(page_param)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    return page

