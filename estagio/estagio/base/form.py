from django import forms
from django.utils.translation import ugettext as _

class Pesquisa(forms.Form):

	SELECT = _("Select")
	PORCENTAGEM_FALHA_UM = tuple([('',SELECT)]+[(r, r) for r in list(range(1, 51))])
	PORCENTAGEM_FALHA_DOIS = tuple([('',SELECT)]+[(r, r) for r in list(range(1, 51))])
	FALHA = (('',SELECT),("ale", _("random")), ("seq", _("sequential")))
	
	FALHA_CONJUNTO =(('',SELECT),('0','NET, GLOBALI, GLOBALR, PARI, PAR')
					,('1',_('all_line'))
					,('2','T, RH')
					,('3','TSOIL, RHSOIL')
					,('4','NET')
					,('5','GLOBALI')
					,('6','GLOBALR')
					,('7','PARI')
					,('8','PARR')
					,('9','TSOIL')
					,('10','PPT')
					,('11','T')
					,('12','RH')
					,('13','U')
					,('14','RHSOIL'))

	porcentagem_um    =    forms.ChoiceField(choices=PORCENTAGEM_FALHA_UM, initial='', required=False, widget=None, label='Porcentagem Falha')
	porcentagem_dois  =    forms.ChoiceField(choices=PORCENTAGEM_FALHA_DOIS, required=False, widget=None, label='Porcentagem Falha')
	tipoFalha         =    forms.ChoiceField (choices=FALHA,required=False, widget=None,label='Falha')
	falha_conjunto         =    forms.ChoiceField (choices=FALHA_CONJUNTO,required=False, widget=None,label='Falha Conjunto')
	
