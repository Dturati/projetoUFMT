from django.core.mail import send_mail, BadHeaderError, EmailMessage, EmailMultiAlternatives
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.utils.html import strip_tags
from django.utils.translation import ugettext as _

def send_email(email, chave):
    print('Enviando: ' + email)
    try:
        subject = _('subject')
        mensagem = _('text_email') + """<br/>
        <a href="http://thegaps.ic.ufmt.br/baixar_pesquisa/?chave="""+chave['chave']+""">"""+_('click_email')+"""</a>"""

        text_body = strip_tags(mensagem,)
        html_body = mensagem

        #send_mail(subject, mensagem, settings.EMAIL_HOST_USER, [str(email)], fail_silently=False, html_message=html)
        #msg = EmailMessage(subject, mensagem, settings.EMAIL_HOST_USER, [str(email)])
        #msg.content_subtype = 'html'
        msg = EmailMultiAlternatives(subject=subject, body=text_body, from_email=settings.EMAIL_HOST_USER, to=[str(email)])
        msg.attach_alternative(html_body, "text/html")
        if(msg.send(fail_silently=False)):
            print('Enviado: ' + email)
        else:
            print('Não Enviado: ' + email)
    except Exception as e:
        print("Erro: " + email)
        print(e)
        print(type(e))
        print(dir(e))
        pass