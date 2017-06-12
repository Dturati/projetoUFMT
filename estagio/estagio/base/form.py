from django import forms

class Pesquisa(forms.Form):
     '''0000000030-1-ale-_13_0.4-1'''
     FALHA = (("ale", "Aleatorio"),("seq", "Sequencial"))
     NUMERO_SEQUENCIAL_UM = tuple([(r, r) for r in list(range(1, 100))])
     NUMERO_SEQUENCIAL_DOIS = tuple([(r, r) for r in list(range(1, 100))])

     # numeroSequencial    =  forms.IntegerField(label="Numero Sequencial",max_value=100,required=False,widget=forms.TextInput(attrs={'style':"width:100px",'value':'0000000030'}))
     numeroSequencialUm = forms.ChoiceField(choices=NUMERO_SEQUENCIAL_UM, required=False, widget=None, label='Numero sequencial Um')
     numeroSequencialDois = forms.ChoiceField(choices=NUMERO_SEQUENCIAL_DOIS, required=False, widget=None, label='Numero sequencial Dois')
     porcentagem         =  forms.IntegerField(label="Porcentagem",max_value=100,required=False,widget=forms.TextInput(attrs={'style':"width:100px",'value':'1'}))
     tipoFalha           =  forms.ChoiceField (choices=FALHA,required=False, widget=None,label='Falha')
     # treze               = forms.IntegerField(label="Numero Sequencial", max_value=100, required=False,disabled=True,widget=forms.TextInput(attrs={'style': "width:100px",'value':'_13_'}))
     tipoFalhaConjunto   = forms.IntegerField(label="Falha Conjunto", max_value=100,required=False,widget=forms.TextInput(attrs={'style':"width:100px",'value':'0'}))
     variavelFalhada     = forms.IntegerField(label="Varialvel Falhada",max_value=100,required=False,widget=forms.TextInput(attrs={'style':"width:100px",'value':'4'}))
     metodoUtilizado     = forms.IntegerField(label="Metodo Utilizado",max_value=100,required=False,widget=forms.TextInput(attrs={'style':"width:100px",'value':'1'}))