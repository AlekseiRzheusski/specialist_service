from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('register/',views.register_page, name = 'register'),
    path('update/', views.user_update_page, name = 'userupdate'),
    path('makespecialist/', views.make_specialist, name = 'makespecialist'),
    path('updatespecialist',views.specialist_update_page, name = 'specialistupdate'),
    path('specialists/', views.SpecialistListView.as_view(), name = 'specialists'),
    path('specialist1/<int:pk>', views.specialist_detail_view, name='specialist-detail'),
    path('addrequest/<int:pk>', views.add_request, name='add-request'),
    path('requestlist/', views.RequestsListView.as_view(), name='request-list'),
    path('deleterequest/<int:pk>', views.delete_request, name='delete-request'),
    path('userdetail/<int:pk>', views.UserDetailView.as_view(), name = 'user-detail'),

]