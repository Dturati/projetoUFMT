from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect

def send_email(email):
    try:
        send_mail('Seu arquivos estão prontos', 'Seus arquivos estão prontos para o download', 'davidturati@gmail.com', [str(email)], fail_silently=False)
    except:
        pass