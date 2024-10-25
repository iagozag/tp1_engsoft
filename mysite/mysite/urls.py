"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from polls import views
urlpatterns = [
    path("admin/", admin.site.urls),
    path('cadastro/',views.cadastrar_usuario, name='cadastrar_usuario' ),
    path('veiculo/',views.cadastrar_veiculo, name='veiculo'),
    path('',views.home, name = 'home'),
    path('completa_cadastro/', views.completar_cadastro, name='completa'),
    path('login/', views.login_usuario, name = 'login'),
    path('configuracoes/',views.configuracoes,name='configuracoes'),
    path('criar_carona/',views.criar_carona,name='criar_carona'),
    path('visualizar_caronas/', views.visualizar_caronas, name='visualizar_caronas'),
    path('editar_carona/<int:carona_id>/', views.editar_carona, name='editar_carona'),
    path('cancelar_carona/<int:carona_id>/', views.cancelar_carona, name='cancelar_carona'),
    path('motorista', views.visualizar_caronas, name='visualizar_caronas'),
    path('logout/', views.logout_usuario, name = 'logout')
]
