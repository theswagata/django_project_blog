from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post
#from django.http import HttpResponse

post=[
    {'author':'Author1',
    'title':'First Blog',
    'context':'Context 1',
    'date_posted':'1st Jan'},
    {'author':'Author2',
    'title':'Second Blog',
    'context':'Context 2',
    'date_posted':'2nd Feb'}
    ]



def home(request):
    context={
    'posts':Post.objects.all(),
    'title':'HOMIE'
    }
    return render(request,'blog/home.html',context)
 
def about(request):
    #return HttpResponse('<h1> Blog About </h1>')
    return render(request,'blog/about.html',{'title':'Abouti'})
    
    
class PostListView(ListView):
    model=Post
    template_name='blog/home.html'
    context_object_name='posts'
    ordering=['-date_posted']
    paginate_by=5
    
    
class PostDetailView(DetailView):
    model=Post
    
class PostCreateView(LoginRequiredMixin, CreateView):
    model=Post
    fields=['title','context']
    
    def form_valid(self,form):
        form.instance.author=self.request.user
        return super().form_valid(form)
        
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model=Post
    fields=['title','context']
    
    def form_valid(self,form):
        form.instance.author=self.request.user
        return super().form_valid(form)
        
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
        
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model=Post
    fields=['title','context']
    success_url='/'
    
    def form_valid(self,form):
        form.instance.author=self.request.user
        return super().form_valid(form)
        
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
        
class UserPostListView(ListView):
    model=Post
    template_name='blog/user_posts.html'
    context_object_name='posts'
    ordering=['-date_posted']
    paginate_by=5  
       
    def get_queryset(self):
        user= get_object_or_404(User, username= self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')
    
    

