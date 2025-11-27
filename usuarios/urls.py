from django.urls import path
from . import views

urlpatterns = [
    # primeiro parametro -> rota
    # segundo parametro -> view
    # O parâmetro "name" é usado para fornecer um identificador exclusivo para esse padrão de URL,
    # que pode ser usado para pesquisas reversas de URL.
path('usuarios/', views.UsuarioListAPIView.as_view(), name='usuario-lista')
]    

path('usuarios/<int:id>/', views.UsuarioDetalhesAPIView.as_view(), name='usuario-detalhe')
