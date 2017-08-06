from django.conf.urls import url,include
from estagio.base.views import home,contatos,lista_em_arvore,\
    download,view_compacta_pesquisa_selecionada,\
    baixar_pesquisa,exemplo,view_compacta_toda_pesquisa,exemplo_assinc,get_resultado,define_sessao,requisicao_enviada,\
    status_stak_celery,cancelar_requisicao,fila_celery,upload
urlpatterns = [
    url(r'^home/$',home, name='home'), #Caminho da view home
    url(r'^ajax/lista_diretorios/$',lista_em_arvore, name='lista_diretorios'), #Caminho da view home
    url(r'^contatos/$',contatos, name='contatos'), #Caminho da view home
    url(r'^home/download/(?P<path>.*)/$',download, name='download'), #Caminho da view dowload
    url(r'^ajax/compacta_pesquisa/$',view_compacta_pesquisa_selecionada, name='view_compacta_pesquisa_selecionada'), #Caminho da view home
    url(r'^ajax/compacta_toda_pesquisa/$',view_compacta_toda_pesquisa, name='view_compacta_toda_pesquisa'), #Caminho da view home
    url(r'^requisicao_enviada/baixar_pesquisa/$',baixar_pesquisa, name='baixar_pesquisa'), #Caminho da view home
    url(r'^home/ajax/baixar_pesquisa/$',baixar_pesquisa, name='baixar_pesquisa'), #Caminho da view home
    url(r'^home/exemplo/$',exemplo, name='exemplo'), #Caminho da view home
    url(r'^websocket/$',exemplo_assinc, name='websocket'), #Caminho da view home
    url(r'^ajax/resultado/$',get_resultado, name='resultado'), #Caminho da view home
    url(r'^ajax/define_sessao/$',define_sessao, name='define_sessao'), #Caminho da view home
    url(r'^requisicao_enviada/$',requisicao_enviada, name='requisicao_enviada'), #Caminho da view dowload
    url(r'^requisicao_enviada/ajax/status_stak_celery',status_stak_celery,name='status_stak_celery'),
    url(r'^requisicao_enviada/ajax/fila_celery',fila_celery,name='fila_celery'),
    url(r'^ajax/cancelar_requisicao',cancelar_requisicao,name='cancelar_requisicao'),
    url(r'^upload/$',upload,name='upload'),
]