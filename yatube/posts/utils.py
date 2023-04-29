from django.core.paginator import Paginator
from django.conf import settings


def pagin_page(post_list, page_number):
    paginator = Paginator(post_list, settings.NUM_OF_POSTS)
    return paginator.get_page(page_number)
