from django.conf.urls import url,include
from estagio.base.views import home,contatos,lista_em_arvore,download,view_compacta_pesquisa_selecionada,baixar_pesquisa,exemplo,view_compacta_toda_pesquisa
urlpatterns = [
    url(r'^home/$',home, name='home'), #Caminho da view home
    url(r'^ajax/lista_diretorios/$',lista_em_arvore, name='lista_diretorios'), #Caminho da view home
    url(r'^contatos/$',contatos, name='contatos'), #Caminho da view home
    url(r'^home/download/(?P<path>.*)/$',download, name='download'), #Caminho da view home
    url(r'^ajax/compacta_pesquisa/$',view_compacta_pesquisa_selecionada, name='view_compacta_pesquisa_selecionada'), #Caminho da view home
    url(r'^ajax/compacta_toda_pesquisa/$',view_compacta_toda_pesquisa, name='view_compacta_toda_pesquisa'), #Caminho da view home
    url(r'^home/ajax/baixar_pesquisa/$',baixar_pesquisa, name='baixar_pesquisa'), #Caminho da view home
    url(r'^exemplo/$',exemplo, name='exemplo'), #Caminho da view home
]