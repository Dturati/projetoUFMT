from django.conf.urls import url,include
from estagio.base.views import home,contatos,lista_diretorios,download,compacta_pesquisa,baixar_pesquisa,exemplo,compacta_toda_pesquisa

urlpatterns = [
    url(r'^home/$',home, name='home'), #Caminho da view home
    url(r'^ajax/lista_diretorios/$',lista_diretorios, name='lista_diretorios'), #Caminho da view home
    url(r'^contatos/$',contatos, name='contatos'), #Caminho da view home
    url(r'^home/download/(?P<path>.*)/$',download, name='download'), #Caminho da view home
    url(r'^ajax/compacta_pesquisa/$',compacta_pesquisa, name='compacta_pesquisa'), #Caminho da view home
    url(r'^ajax/compacta_toda_pesquisa/$',compacta_toda_pesquisa, name='compacta_toda_pesquisa'), #Caminho da view home
    url(r'^home/ajax/baixar_pesquisa/$',baixar_pesquisa, name='baixar_pesquisa'), #Caminho da view home
    url(r'^exemplo/$',exemplo, name='exemplo'), #Caminho da view home
]