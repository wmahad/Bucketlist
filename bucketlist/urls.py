from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from bucketlist import views

urlpatterns = [
    url(r'^auth/signup/$', views.UserSignUpView.as_view(), name='auth_signup'),
    
    url(r'^api-token-auth/', 'rest_framework_jwt.views.obtain_jwt_token', name='auth_signin'),
    url(r'^api-token-verify/', 'rest_framework_jwt.views.verify_jwt_token'),

    url(r'^bucketlists/$', views.BucketListView.as_view(), name='all_bucketlists'),
    url(r'^bucketlists/(?P<pk>[0-9]+)/$', views.BucketDetailView.as_view(), name='single_bucketlist'),
    url(r'^bucketlists/(?P<pk>[0-9]+)/items/$',
        views.BucketListItemView.as_view(), name='all_items'),
    url(r'^bucketlists/(?P<bid>[0-9]+)/items/(?P<pk>[0-9]+)/$',
        views.BucketListItemDetailView.as_view(), name='single_item'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
