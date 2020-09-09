from django.shortcuts import render,get_object_or_404,redirect
from django.utils import timezone
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.generic import (TemplateView,ListView,DetailView,CreateView,UpdateView,DeleteView)
from django.contrib.auth.views import LoginView
from django.contrib.auth import login,logout,authenticate
from django.urls import reverse_lazy,reverse
from blog.models import Comment,Post
from blog.forms import PostForm,CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
class AboutView(TemplateView):
    template_name='about.html'

class PostListView(ListView):
    model=Post

    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

class PostDeleteView(DeleteView):
    model=Post
    success_url=reverse_lazy('blog:post_draft_list')

class PostDetailView(DetailView):
    model=Post

class CreatePostView(LoginRequiredMixin,CreateView):
    login_url='/login/'
    redirect_field_name='blog/post_detail.html'

    form_class=PostForm

    model=Post
    success_url=reverse_lazy('blog:post_list')
class UpdatePostView(LoginRequiredMixin,UpdateView):
    login_url='/login/'
    redirect_field_name='blog/post_detail.html'

    form_class=PostForm
    model=Post
    success_url=reverse_lazy('blog:post_list')
class DeletePostView(LoginRequiredMixin,DeleteView):
    model=Post

    success_url=reverse_lazy('blog:post_list')

class DraftListView(LoginRequiredMixin,ListView):
    login_url='/login/'
    template_name='blog/post_draft_list.html'

    model=Post

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('create_date')

        #####################################################33
        ######################################################

def add_comment_to_post(request,pk):
    post=get_object_or_404(Post,pk=pk)

    if request.method=="POST":
         form=CommentForm(request.POST)
         if form.is_valid():
             comment=form.save(commit=False)
             comment.post=post
             comment.save()
             return redirect('blog:post_detail',pk=post.pk)

    else:
            form=CommentForm()

    return render(request,'blog/comment_form.html',{'form':form})

@login_required
def comment_approve(request,pk):
    comment=get_object_or_404(Comment,pk=pk)
    comment.approve()
    return redirect('blog:post_detail',pk=comment.post.pk)

@login_required
def comment_remove(request,pk):
    comment=get_object_or_404(Comment,pk=pk)
    post_pk=comment.post.pk
    comment.delete()
    return redirect('blog:post_detail',pk=post_pk)

@login_required
def post_publish(request,pk):
    post=get_object_or_404(Post,pk=pk)
    post.publish()
    return redirect('blog:post_detail',pk=pk)

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('blog:post_list'))

def login_view(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get("password")
        user=authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('blog:post_list'))
            else:
                return HttpResponse("user not active")
        else:
            print("someone tried to login ")
            print("username {0} and password {1}".format(username,password))
    else:
        return render(request,"blog/loginse.html",{})
