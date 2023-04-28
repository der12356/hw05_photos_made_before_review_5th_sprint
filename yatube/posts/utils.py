from django.core.paginator import Paginator
from django.conf import settings

NUM_OF_POSTS = settings.NUM_OF_POSTS


def pagin_page(post_list, page_number):
    paginator = Paginator(post_list, NUM_OF_POSTS)
    paginator_page = paginator.get_page(page_number)
    return paginator_page
