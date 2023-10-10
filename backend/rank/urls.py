from django.urls import path

from rank import user

urlpatterns = [

    path('customers', user.add_user),

]
