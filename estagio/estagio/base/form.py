from django import forms
from django.utils.translation import ugettext as _

class Pesquisa(forms.Form):

	SELECT = _("Select")
	PORCENTAGEM_FALHA_UM = tuple([('',SELECT)]+[(r, r) for r in list(range(1, 50))])
	PORCENTAGEM_FALHA_DOIS = tuple([('',SELECT)]+[(r, r) for r in list(range(1, 50))])
	FALHA = (('',SELECT),("ale", "Aleatorio"), ("seq", "Sequencial"))
	
	FALHA_CONJUNTO =(('',SELECT),('0','NET GLOBALI GLOBALR PARI E PAR')
				  ,('1','TODA A LINHA FALHADA'),('2','T e UR')
				  ,('3','TSOLO e URSOLO')
				  ,('4','Individual'))

	porcentagem_um    =    forms.ChoiceField(choices=PORCENTAGEM_FALHA_UM, initial='', required=False, widget=None, label='Porcentagem Falha')
	porcentagem_dois  =    forms.ChoiceField(choices=PORCENTAGEM_FALHA_DOIS, required=False, widget=None, label='Porcentagem Falha')
	tipoFalha         =    forms.ChoiceField (choices=FALHA,required=False, widget=None,label='Falha')
	falha_conjunto         =    forms.ChoiceField (choices=FALHA_CONJUNTO,required=False, widget=None,label='Falha Conjunto')
	
