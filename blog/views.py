from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormMixin
from .forms import CommentaryForm
from .models import User, Post, Commentary


@login_required
def index(request):
    """View function for the home page of the site."""
    posts = Post.objects.all().order_by("-created_time")

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "posts": posts,
        "num_visits": num_visits + 1,
    }

    return render(request, "blog/index.html", context=context)


class PostDetailView(LoginRequiredMixin, FormMixin, generic.DetailView):
    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"
    form_class = CommentaryForm

    def get_success_url(self):
        return reverse("blog:post-detail", kwargs={"pk": self.object.pk})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def form_valid(self, form):
        commentary = form.save(commit=False)
        commentary.post = self.object
        commentary.user = self.request.user
        commentary.save()
        return super().form_valid(form)

