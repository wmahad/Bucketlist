from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from bucketlist import views

urlpatterns = [
    url(r'^auth/signup/$', views.UserSignUpView.as_view()),
    url(r'^auth/login/$', views.UserSignInView.as_view()),
    url(r'^auth/logout/$', views.LogoutView.as_view()),
    url(r'^bucketlists/$', views.BucketListView.as_view()),
    url(r'^bucketlists/(?P<pk>[0-9]+)/$', views.BucketDetailView.as_view()),
    url(r'^bucketlists/(?P<pk>[0-9]+)/items/$',
        views.BucketListItemView.as_view()),
    url(r'^bucketlists/(?P<bid>[0-9]+)/items/(?P<pk>[0-9]+)/$',
        views.BucketListItemDetailView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
