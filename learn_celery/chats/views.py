from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Post
from .bg_tasks import add_comment


@api_view(["POST"])
def create_post(request):

    # for post
    author = request.data.get("author")
    content = request.data.get("content")

    # for comment
    comment_messages:list = request.data.get("comments")

    post = Post.objects.create(author=author, content=content)

    # background work
    add_comment.delay(messages =comment_messages, post_id=post.pk)
    
    return Response({"msg":"Comment is beign created in the background"})