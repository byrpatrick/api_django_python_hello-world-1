from django.urls import path

from .views import PublicMessageApiView, AuthMessageApiView, AdminMessageApiView


urlpatterns = [
    path('public', PublicMessageApiView.as_view(), name='public-message'),
    path(
        'protected', AuthMessageApiView.as_view(), name='protected-message'
    ),
    path('admin', AdminMessageApiView.as_view(), name='admin-message'),
]
