# importar views e router
from rest_framework.routers import DefaultRouter
# router é responsável por gerar automaticamente
# todas as rotas REST

from usuarios import views

# criar uma instência (objeto) do router 
# Obs: DefaultRouter já gera a rota para
# a interface de navegação do DFR
router = DefaultRouter()

# registrar o viewset no router
# função register que tem 3 parametros
# 1º -> prefixo da rota ('usuarios/')
# 2º -> classe do viewset
# 3º -> nome base (nome interno usado pelo DRF)
# esse nome base evita conflitos
router.register('usuarios/', views.UsuarioViewSet, basename='usuarios')

# gerar as rotas
urlpatterns = router.urls
