# from django.urls import path
# from .views import home,callback_view,callback_listener_view
# # webhook_callback
# from . import views
# urlpatterns = [
#     path('home/', home, name="home"),
#     path('callback/', callback_view, name='callback_view'),
#     path('callback_listener/', views.callback_listener_view, name='callback_listener'),
#     # path('webhook/', webhook_callback, name='webhook-callback'),


# ]


from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('callback/', views.callback_view, name='callback_view'),
    path('callback_listener/', views.callback_listener_view, name='callback_listener'),
]



