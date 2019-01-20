from .models import Profile, Post, Comment
from .forms import ProfileForm, PostForm, ContactForm, CommentForm
from django.views import generic, View
from django.views.generic import TemplateView
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
# from django.contrib import auth
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
# from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.core.mail import EmailMessage, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy, reverse

from django.contrib.auth import login, authenticate
from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            city = form.cleaned_data.get('city')
            biography = form.cleaned_data.get('biography')
            contacts = form.cleaned_data.get('contacts')
            avatar = form.cleaned_data.get('avatar')
            sex = form.cleaned_data.get('sex')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            other_info = form.cleaned_data.get('other_info')
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            profile = user.profile
            profile.city = city
            profile.email = email
            profile.avatar = avatar
            profile.first_name = first_name
            profile.last_name = last_name
            profile.biography = biography
            profile.contacts = contacts
            profile.sex = sex
            profile.other_info = other_info
            profile.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


# class Home(TemplateView):
#     template_name = 'index.html'

from django.utils.http import is_safe_url, urlunquote
from django.conf import settings
import geoip2.database
import requests

PRIVATE_IPS_PREFIX = ('10.', '172.', '192.', )
def index(request):
    num_posts=Post.objects.all().count()
    num_visits=request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits+1


    remote_address = request.META.get('REMOTE_ADDR')
    ip = remote_address
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        proxies = x_forwarded_for.split(',')
        while (len(proxies) > 0 and
                proxies[0].startswith(PRIVATE_IPS_PREFIX)):
            proxies.pop(0)
        if len(proxies) > 0:
            ip = proxies[0]

    reader = geoip2.database.Reader('post/GeoLite2-City_20190108/GeoLite2-City.mmdb')
    try:
        city = reader.city(ip).city.name
    except:
        city = 'Dnipro'

    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&lang=ru&appid=4e328f5a34221d8b56cc9e2f55417a76'
    city_weather = requests.get(url.format(city)).json()

    weather = {
        'city' : city,
        'temperature' : str(city_weather['main']['temp'])+'°C,',
        'description' : city_weather['weather'][0]['description'],
        'icon' : city_weather['weather'][0]['icon']
    }

    next = request.META.get('HTTP_REFERER')
    if next:
        next = urlunquote(next)  # HTTP_REFERER may be encoded.
    if not is_safe_url(url=next, allowed_hosts={request.get_host()}):
        next = '/'
    return render(
        request,
        'index.html',
        context={'num_posts':num_posts, 'num_visits':num_visits, 'ip': ip, 'next': next, 'city': city, 'weather' : weather }
        )


class ProfileListView(generic.ListView):
    model = Profile
    paginate_by = 5


class ProfileDetailView(generic.DetailView):
    model = Profile


class ProfileUpdateView(UpdateView):
    model = Profile
    fields = ['avatar', 'first_name', 'last_name', 'email', 'city', 'sex',
         'biography', 'contacts', 'other_info']


class ProfileUpdatePhotoView(UpdateView):
    model = Profile
    fields = ['avatar']


class PostCreateView(FormView):
    form_class = PostForm
    template_name = 'post/post_form.html'
    success_url = reverse_lazy('posts')

    def form_valid(self, form):
        response = super(PostCreateView, self).form_valid(form)
        form.instance.user = self.request.user
        form.save()
        return response

from django.forms import modelform_factory

class PostUpdateView(UpdateView):
    model = Post

    def get_form_class(self):
        fields = ['title', 'body', 'logo']
        if self.request.user.is_staff:
            fields.append('moderation')

        return modelform_factory(self.model, fields=fields)

class PostDelete(DeleteView):
    model = Post
    success_url = reverse_lazy('posts')

class CommentUpdateView(UpdateView):
    model = Comment
    fields = ['description']
    success_url = reverse_lazy('posts')

class CommentDelete(DeleteView):
    model = Comment
    success_url = reverse_lazy('posts')

class PostListView(generic.ListView):
    model = Post
    paginate_by = 5

    def get_queryset(self):
        queryset = super(PostListView, self).get_queryset()
        return queryset.filter(moderation=True)

class ProposedPostListView(generic.ListView):
    model = Post
    template_name = 'post/proposed_post_list.html'

    def get_queryset(self):
        queryset = super(ProposedPostListView, self).get_queryset()
        return queryset.filter(moderation=False)


class PostDetailView(generic.DetailView):
    model = Post

    def get_context_data(self, **kwargs):
       context = super(PostDetailView, self).get_context_data(**kwargs)
       context['commentform'] = CommentForm()
       return context

    def post(self, request, pk):
       post = get_object_or_404(Post, pk=pk)
       form = CommentForm(request.POST)

       if form.is_valid():
           obj  = form.save(commit=False)
           obj.post = post
           obj.author = self.request.user
           obj.save()
           return redirect('post-detail', post.pk)

# def moderator_approval_view(request, **kwargs):
#     if request.method == 'POST':
#         post = Post.objects.get(pk=kwargs['post_id'])
#         post.moderation = True
#         post.save()
#         return HttpResponseRedirect('posts')


class SearchView(View):
	template_name = 'search.html'

	def get(self, request, *args, **kwargs):
		query = self.request.GET.get('q')
		founded = Post.objects.filter(Q(title__icontains=query)|Q(description__icontains=query))
		context = {'founded': founded}
		return render(self.request, self.template_name, context)


def contact(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            contact_name = form.cleaned_data['contact_name']
            contact_email = form.cleaned_data['contact_email']
            content = form.cleaned_data['content']

            try:
                email = EmailMessage(subject,
                                    content,
                                    contact_email,
                                    ['dinamo.mutu111@gmail.com'],
                                    reply_to=[contact_email],
                                    )
                email.send()
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('thanks')
    return render(request, 'contact.html', {'form': form})

def thanks(request):
    return render(request, 'thanks.html', {})
