from django.conf.urls import url
#from .views import emailView, successView
from . import views
from .templatetags.abc import *

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^posts/$', views.PostListView.as_view(), name='posts'),
	url(r'^proposed_posts/$', views.ProposedPostListView.as_view(), name='proposed_posts'),
	url(r'^profile/(?P<pk>\d+)$', views.ProfileDetailView.as_view(), name='profile-detail'),
	url(r'^post/(?P<pk>\d+)$', views.PostDetailView.as_view(), name='post-detail'),
	url(r'^profiles/$', views.ProfileListView.as_view(), name='profiles'),
	url(r'^post/create/$', views.PostCreateView.as_view(), name='post_create'),
	url(r'^post/(?P<pk>\d+)/update/$', views.PostUpdateView.as_view(), name='post_update'),
	url(r'^post/(?P<pk>\d+)/comment_update/$', views.CommentUpdateView.as_view(), name='comment_update'),
	url(r'^post/(?P<pk>\d+)/delete/$', views.PostDelete.as_view(), name='post_delete'),
	url(r'^post/(?P<pk>\d+)/comment_delete/$', views.CommentDelete.as_view(), name='comment_delete'),
	url(r'^profile/(?P<pk>\d+)/update/$', views.ProfileUpdateView.as_view(), name='profile_update'),
	url(r'^profile/(?P<pk>\d+)/updatephoto/$', views.ProfileUpdatePhotoView.as_view(), name='profile_update_photo'),
	url(r'^search/$', views.SearchView.as_view(), name='search_view'),
	url(r'^contact/$', views.contact, name='contact'),
	url(r'^thanks/$', views.thanks, name='thanks'),
	# url(r'^moderator-approval/(?P<pk>\d+)$', views.moderator_approval_view, name="moderator-approval"),
	url(r'^signup/$', views.signup, name='signup'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
	#url(r'email/$', emailView, name='email'),
	#url(r'success/$', successView, name='success'),
]
