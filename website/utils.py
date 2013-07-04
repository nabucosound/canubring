from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings


def listing(request, obj_list):
    paginator = Paginator(obj_list, getattr(settings, 'DEFAULT_PAGINATOR_ITEMS', 24))
    page_param = request.GET.get('page')
    try:
        page = paginator.page(page_param)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    return page

def reference_saving(distance, weight, size, price):
    if weight == 0.4:
        weight = 2
    elif weight == 0.6:
        weight = 2
    elif weight == 0.8:
        weight = 3
    elif weight == 1.0:
        weight = 4
    elif weight == 1.2:
        weight = 5
    elif weight == 1.4:
        weight = 6
    elif weight == 1.6:
        weight = 6

    if price == 0.8:
        price = 1
    elif price == 1.0:
        price = 2
    elif price == 1.5:
        price = 3
    elif price == 2.0:
        price = 4
    elif price == 2.5:
        price = 5
    elif price == 3.0:
        price = 6

    return 50 + (float(distance) / 2500) + weight + size + price

def reference_price(distance, weight, size, price):
    return float(distance) / 100 * weight * size * price * (1 - (float(distance) / 20000))

#     if weight >= 0 and weight <= 3:
#         weight_c = 0.4
#     elif weight > 3 and weight <= 6:
#         weight_c = 0.6
#     elif weight > 6 and weight <= 11:
#         weight_c = 0.8
#     elif weight > 11 and weight <= 16:
#         weight_c = 1
#     elif weight > 16 and weight <= 21:
#         weight_c = 1.2
#     elif weight > 21 and weight <= 25:
#         weight_c = 1.4
#     elif weight > 25:
#         weight_c = 1.6

#     if size == 0:
#         size_c = 1
#     elif size == 1:
#         size_c = 1.3
#     elif size > 1:
#         size_c = 1.6

#     if price >= 0 and size <= 26:
#         price_c = 0.8
#     elif price >= 26 and size <= 51:
#         price_c = 1
#     elif price >= 51 and size <= 101:
#         price_c = 1.5
#     elif price >= 101 and size <= 201:
#         price_c = 2
#     elif price >= 201 and size <= 301:
#         price_c = 2.5
#     elif price > 301:
#         price_c = 3

#     return float(distance) / 100 * weight * size * price * (1 - (float(distance) / 20000))

