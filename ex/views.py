from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import User
from .models import Comment, Post
from .models import UserDescrip
from django.views.generic import DetailView, ListView, FormView, CreateView
from django.contrib.auth import authenticate, login, logout
from .log_in import LogForm
from .log_in import UpdateUser
from .log_in import PubliForm
from .log_in import ComForm
from .log_in import PostForm
from django.contrib import auth
from .models import CustomUserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

class RegisterPost(FormView):
    model = Post
    template_name =  "publish.html"
    form_class = PostForm
    def get(self, request):
        form = PostForm()
        return render(request, "publish.html", {"form":form})

    def post(self, request):
        if request.user.is_authenticated: 
            form = PostForm(request.POST)
            if form.is_valid():
                content = form.cleaned_data['content']
                title = form.cleaned_data['title']
                save = Post(
                    content = content,
                    author = request.user,
                    title = title
                )
                save.save()
        return redirect("/forums")

class ComCom(FormView):
    model = Comment
    template_name =  "details_post.html"
    form_class = ComForm

    def get(self, request, pk):
        post = Post.objects.get(id=pk) 
        form = PubliForm()
        com = Comment.objects.filter(post_id= pk)
        return render(request, "details_post.html", {'post':post, "form":form, "com":com, "form1":form, "form2":form})

    def post(self, request, pk):
        form = ComForm(request.POST)
        id = request.user.id
        a = User.objects.get(id=id)
        c = Comment.objects.get(id=pk)
        p = c.post.id
        post = Post.objects.get(id=p)
        com = Comment.objects.filter(post_id= p)
        if form.is_valid():
            content = form.cleaned_data['content']
            save = Comment(
                post = post,
                author =   a,
                content =  content,
                parent = c
            )
            save.save()
        form = ComForm()
        return render(request, "details_post.html", {'post':post, "form":form, "com":com, "form1":form, "form2":form})

class Publish(FormView):
    model = Comment
    template_name =  "details_post.html"
    form_class = PubliForm

    def get(self, request, pk):
        post = Post.objects.get(id=pk) 
        form = PubliForm()
        queryset = Comment.objects.all().order_by('id')
        com = Comment.objects.filter(post_id= pk)
        p = Paginator(com, 10)
        page = request.GET.get('page')
        venues = p.get_page(page)
        return render(request, "details_post.html", {'post':post, "form":form, "com":com, "form1":form, "form2":form, "venues":venues})

    def post(self, request, pk):
        if request.user.is_authenticated: 
            form = PubliForm(request.POST)
            if form.is_valid():
                content = form.cleaned_data['content']
                print('PUBLISH CONTENT=>', content)
                post = Post.objects.get(id=pk)
                save = Comment(
                    content = content,
                    author = request.user,
                    post = post
                )
                save.save()
        com = Comment.objects.filter(post_id= pk)
        return render(request, "details_post.html", {'post':post, "form1":form, "form2":form, "com":com})

class PostDisplay(ListView):
    model = Post
    template_name = 'article.html'
    paginate_by = 10
    def get(self, request):
        post = Post.objects.all() 
        p = Paginator(post, 10)
        page = request.GET.get('page')
        venues = p.get_page(page)
        return render(request, "article.html", {"post":post, "venues":venues})

class DetailsPost(DetailView):
    model = Post
    template_name = 'details_post.html'

class Details(FormView):
    model = UserDescrip
    template_name = 'details.html'
    form_class = UpdateUser
    def get(self, request, pk):
        form = UpdateUser()
        return render(request, 'details.html', {"form":form})
    def post(self, request, pk):
        who = request.user.id
        form = UpdateUser(self.request.POST, self.request.FILES)
        if form.is_valid():
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            email = form.cleaned_data['email']
            description = form.cleaned_data['description']
            picture = form.cleaned_data['picture']
            u = User.objects.get(id = pk)
            u.username = username
            u.first_name = first_name
            u.email = email
            u.save()
            t = UserDescrip.objects.filter(id=pk)
            if t:
                len = UserDescrip.objects.get(id=pk)
                len.description = description
                len.picture = picture
                len.user = User.objects.get(id=pk)
                len.save()
                form = UpdateUser()
                return render(request, 'details.html', {"form":form})
            else:
                save = UserDescrip(
                description = description,
                picture = picture,
                user = User.objects.get(id=pk)
                )
                save.save()
                form = UpdateUser()
                return render(request, 'details.html', {"form":form})
        else:
            form = UpdateUser()
            return render(request, 'details.html', {"form":form})

@login_required
def add_admin(request):
    id = request.user.id
    des = User.objects.get(id=id)
    des.is_staff = True
    des.save()
    return HttpResponse("User add as Admin")

@login_required
def Staff(request):
    id = request.user.username
    user = User.objects.all()
    return render(request, "staff.html", {'f':user, "id":id})

@login_required
def SuperUser(request, pk):
    id = request.user.username
    user = User.objects.all()
    t = User.objects.get(id=pk)
    if t.is_superuser == False:
        t.is_superuser = True
    else:
        t.is_superuser = False
    t.save()
    return render(request, "staff.html", {'f':user, "id":id})

@login_required
def Admin(request, pk):
    id = request.user.username
    user = User.objects.all()
    t = User.objects.get(id=pk)
    if t.is_staff == False:
        t.is_staff = True
    else:
        t.is_staff = False
    t.save()
    return render(request, "staff.html", {'f':user, "id":id})

@login_required
def user_profile(request, pk):
    id = request.user.id
    user = User.objects.get(id=id)
    try:
        des = UserDescrip.objects.filter(user_id=id)
    except(Exception):
        return render(request, "user_profile.html", {'user':user, "res":res, "img":img})
    res =''
    img =''
    for i in des:
        res = i.description
        img = i.picture
    return render(request, "user_profile.html", {'user':user, "res":res, "img":img})

def home_view(request):
	return render(request, "home.html")

def is_login(request):
    id = request.user.id
    len = User.objects.all()
    for i in len:
        res = i.id
    user = User.objects.get(id=res)
    auth.login(request, user)
    return render(request, "home_login.html")

class Login(FormView):
    form_class = LogForm
    template_name = 'log_in.html'
    success_url ="/"
    def form_valid(self, form):
        form = LogForm(self.request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(self.request, user)
                return redirect("/log")
        return redirect("/Login")

class Register(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = "registration.html"
    success_url="/log"

class Logout(DetailView):
    def get(self,request): 
        auth.logout(request)
        return redirect('/')

class Populate(ListView):
    def get(self, request):
        id = request.user.id
        a = User.objects.get(id=id)
        save = Post(
            title = 'The Phantom Menace',
            author =   a,
            content =  'Rick McCallum',
            created = '1999-05-19'
        )
        save.save()
        save = Post(
            title = 'Attack of the Clones',
            author =  a,
            content =  'Rick McCallum',
            created = '2002-05-16'
        )
        save.save()
        save = Post(
            title = 'Revenge of the Sith',
           author =  a,
            content =  'Rick McCallum',
            created  = '2005-05-19'
        )
        save.save()
        save = Post(
            title = 'Revenge of the Sith',
           author =  a,
            content =  'Rick McCallum',
            created  = '2005-05-19'
        )
        save.save()
        save = Post(
            title = 'Revenge of the Sith',
           author =  a,
            content =  'Rick McCallum',
            created  = '2005-05-19'
        )
        save.save()
        save = Post(
            title = 'Revenge of the Sith',
           author =  a,
            content =  'Rick McCallum',
            created  = '2005-05-19'
        )
        save.save()
        save = Post(
            title = 'Revenge of the Sith',
           author =  a,
            content =  'Rick McCallum',
            created  = '2005-05-19'
        )
        save.save()
        save = Post(
            title = 'Revenge of the Sith',
           author =  a,
            content =  'Rick McCallum',
            created  = '2005-05-19'
        )
        save.save()
        save = Post(
            title = 'Revenge of the Sith',
           author =  a,
            content =  'Rick McCallum',
            created  = '2005-05-19'
        )
        save.save()
        save = Post(
            title = 'Revenge of the Sith',
           author =  a,
            content =  'Rick McCallum',
            created  = '2005-05-19'
        )
        save.save()
        save = Post(
            title = 'Revenge of the Sith',
           author =  a,
            content =  'Rick McCallum',
            created  = '2005-05-19'
        )
        save.save()
        save = Post(
            title = 'Revenge of the Sith',
           author =  a,
            content =  'Rick McCallum',
            created  = '2005-05-19'
        )
        save.save()
        save = Post(
            title = 'Revenge of the Sith',
           author =  a,
            content =  'Rick McCallum',
            created  = '2005-05-19'
        )
        save.save()
        return HttpResponse("OK POPULATE")

class PopulateCom(ListView):
    def get(self, request):
        id = request.user.id
        a = User.objects.get(id=id)
        p = Post.objects.get(id=1)
        c = Comment.objects.get(id=3)
        save = Comment(
            post = p,
            author =   a,
            content =  '4eme com',
            parent = c
        )
        save.save()
        return HttpResponse("OK POPULATE")