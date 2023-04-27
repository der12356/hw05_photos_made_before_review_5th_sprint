from django.core.paginator import Paginator

from yatube.settings import NUM_OF_POSTS


def paginator(post_list):
    paginator = Paginator(post_list, NUM_OF_POSTS)
    return paginator


def pagin_page(post_list, page_number):
    paginator = Paginator(post_list, NUM_OF_POSTS)
    paginator_page = paginator.get_page(page_number)
    return paginator_page
