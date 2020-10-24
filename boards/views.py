from django.shortcuts import render, get_object_or_404, redirect
from .models import Board
from django.http import HttpResponse, Http404
from django.contrib.auth.models import User
from .models import Topic, Post
from .forms import NewTopicForm,PostForm
from django.contrib.auth.decorators import login_required


# Create your views here.
def home(request):
    boards = Board.objects.all()
    return render(request, 'home.html', {'boards': boards})


def board_topics(request, board_id):
    # try:
    #       board= Board.objects.get(pk=board_id)
    # except Board.DoesNotExist :
    #       raise Http404
    board = get_object_or_404(Board, pk=board_id)
    return render(request, 'topics.html', {'board': board})


@login_required
def new_topic(request, board_id):
    board = get_object_or_404(Board, pk=board_id)

    form = NewTopicForm()
    # user = User.objects.first()
    if request.method == "POST":
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.created_by = request.user
            topic.save()
            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                created_by=request.user,
                topic=topic
            )
            return redirect("board_topic", board_id=board.pk)

    return render(request, 'new_topic.html', {'board': board, 'form': form})


def topic_posts(request, board_id, topic_id):
    topic = get_object_or_404(Topic, board__pk=board_id, pk=topic_id)
    return render(request, 'topic_posts.html', {'topic': topic})


@login_required
def reply(request, board_id, topic_id):
    topic = get_object_or_404(Topic, board__pk=board_id, pk=topic_id)
    form = PostForm()
    # user = User.objects.first()
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()
            return redirect("topic_posts", board_id=board_id,topic_id=topic.pk)

    return render(request, 'reply.html' ,{'topic':topic,'form':form})
