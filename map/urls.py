from .views import MainView, EditView, DeleteView, share_marker
from django.urls import path


urlpatterns = [
    path('', MainView.as_view(), name='index'),
    path('share/<uuid:public_id>/', share_marker, name='share_marker'),
    path('<slug:slug>/delete', DeleteView.as_view(), name='delete'),
    path('<slug:slug>', EditView.as_view(), name='edit')
]
