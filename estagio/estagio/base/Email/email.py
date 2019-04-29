from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect

def send_email(email, chave):
    try:
        mensagem = """Seus arquivos estão prontos para o download.
        <br/>
        <a href="http://200.129.242.4:51001/requisicao_enviada/baixar_pesquisa/?chave="""+chave+""">Clique aqui</a>
        """

        send_mail('Seu arquivos estão prontos', mensagem, 'davidturati@gmail.com', [str(email)], fail_silently=False)
    except:
        pass