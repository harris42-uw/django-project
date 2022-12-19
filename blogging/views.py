from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import loader
from django.views.generic import ListView, DetailView
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import permissions
from blogging.models import Post, Category
from blogging.serializers import UserSerializer, PostSerializer, CategorySerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class PostViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = Post.objects.exclude(published_date__exact=None).order_by(
        "-published_date"
    )
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = Category.objects.all().order_by("-name")
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


def stub_view(request, *args, **kwargs):
    body = "Stub View\n\n"
    if args:
        body += "Args:\n"
        body += "\n".join(["\t%s" % a for a in args])
    if kwargs:
        body += "Kwargs:\n"
        body += "\n".join(["\t%s: %s" % i for i in kwargs.items()])
    return HttpResponse(body, content_type="text/plain")


def list_view_explicit(request):
    published = Post.objects.exclude(published_date__exact=None)
    posts = published.order_by("-published_date")
    template = loader.get_template("blogging/list.html")
    context = {"posts": posts}
    body = template.render(context)
    return HttpResponse(body, content_type="text/html")


def list_view(request):
    published = Post.objects.exclude(published_date__exact=None)
    posts = published.order_by("-published_date")
    context = {"posts": posts}
    return render(request, "blogging/list.html", context)


def detail_view(request, post_id):
    published = Post.objects.exclude(published_date__exact=None)
    try:
        post = published.get(pk=post_id)
    except Post.DoesNotExist:
        raise Http404
    context = {"post": post}
    return render(request, "blogging/detail.html", context)


class PostListView(ListView):
    model = Post
    queryset = Post.objects.exclude(published_date__exact=None).order_by(
        "-published_date"
    )
    template_name = "blogging/list.html"


class PostDetailView(DetailView):
    model = Post
    queryset = Post.objects.exclude(published_date__exact=None)
    template_name = "blogging/detail.html"
