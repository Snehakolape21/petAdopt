
from django.urls import path
from petadoptapp import views

from django.conf import settings
from django.conf.urls.static import static 

urlpatterns = [
    
    path("",views.index),
    path("login",views.userlogin),
    path("register",views.register) ,
    path("logout",views.userlogout),
    path("about",views.aboutus),
    path("contact",views.contactus) ,
    path('search', views.search),
    path("addtocart/<petid>",views.addtocart),
    path('removecart/<cartid>',views.removecart), 
    path("placeadopt",views.placeadopt),
    path("confirmadopt",views.confirmadopt),
    path("myadoptions",views.myadoptions),
    path("adopt_success",views.adopt_success),
]

urlpatterns += static(settings.MEDIA_URL, document_root =settings.MEDIA_ROOT)
