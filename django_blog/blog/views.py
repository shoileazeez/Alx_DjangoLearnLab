from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ProfileUpdateForm, PostForm, CommentForm
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView, UpdateView
from .models import Post, comment
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils.decorators import method_decorator

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page after successful registration
    else:
        form = CustomUserCreationForm()
    return render(request, 'blog/register.html', {'form': form})



@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'blog/profile.html', {'form': form})


class List_view(ListView):
    model = Post
    template_name = 'blog/list_view.html'
    
    
class Detail_View(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all()  # Get all comments for the post
        context['comment_form'] = CommentForm()  # Empty form for new comments
        return context
    
class create_view(CreateView, LoginRequiredMixin):
    model = Post
    form_class = PostForm
    template_name = 'blog/create_view.html'
     
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form) 
class Delete_view(DeleteView, LoginRequiredMixin, UserPassesTestMixin):
    model = Post
    form_class = PostForm
    template_name = 'blog/delete_view.html'    

class Update_View(UpdateView, UserPassesTestMixin, LoginRequiredMixin):
    model = Post
    form_class = PostForm
    template_name = "blog/create_view.html"


@method_decorator(login_required, name='dispatch')
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user.username  # Save the current user's username as the author
            comment.save()
            return redirect('post_detail', pk=post_id)
    else:
        form = CommentForm()

    return render(request, 'blog/post_detail.html', {'post': post, 'form': form, 'comments': post.comments.all()})

from django.views.generic.edit import DeleteView

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = comment
    template_name = 'blog/comment_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('blog/post_detail', kwargs={'pk': self.object.post.id})

    def test_func(self):
        comment = self.get_object()
        return comment.author == self.request.user.username  # Ensure only the author can delete the comment
class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.object.post.id})

    def test_func(self):
        comment = self.get_object()
        return comment.author == self.request.user.username