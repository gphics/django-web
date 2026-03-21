from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from .forms import CommentForm
from django.core.paginator import Paginator, EmptyPage
from django.views.decorators.http import require_GET, require_POST
from django.contrib import messages
# Create your views here.

def post_list(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, 3)
    page_number = request.GET.get("page", 1)
    try:
        posts = paginator.page(page_number)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    return render(request, "social/posts/list.html", {"data":posts})

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, 
                             slug=post, 
                             created__year = year,
                               created__month = month,
                                 created__day = day)
    post_comments = Comment.objects.filter(post = post)
    comment_form = CommentForm()
    return render(
        request,
        "social/posts/detail.html",
        {"data": post, "comments": post_comments, "form":comment_form}
    )


# cOMMENTS

@require_POST
def create_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(data =request.POST)
    comment = None
    if form.is_valid():
        comment = form.save(commit=False)

        comment.post = post
  
        comment.save()
        messages.success(request, "Post comment created ...")
    previous_url = request.META.get("HTTP_REFERER")
    return redirect(previous_url)
    
          






