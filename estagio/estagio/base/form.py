from django import forms

class Pesquisa(forms.Form):
     '''0000000030-1-ale-_13_0.4-1'''
     NUMERO_SEQUENCIAL_UM = tuple([(r, r) for r in list(range(1, 100))])
     NUMERO_SEQUENCIAL_DOIS = tuple([(r, r) for r in list(range(1, 100))])
     FALHA = (("ale", "Aleatorio"), ("seq", "Sequencial"))
     METODOS = (('1','SLR'),('2','MLR'),('3','Media'),('4','SVM'))
     PORCENTAGEM_FALHA = tuple([(r, r) for r in list(range(1, 100))])

     numeroSequencialUm       = forms.ChoiceField(choices=NUMERO_SEQUENCIAL_UM, required=False, widget=None, label='Numero sequencial Um')
     numeroSequencialDois     = forms.ChoiceField(choices=NUMERO_SEQUENCIAL_DOIS, required=False, widget=None, label='Numero sequencial Dois')
     porcentagem              = forms.ChoiceField(choices=PORCENTAGEM_FALHA, required=False, widget=None, label='Porcentagem Falha')
     tipoFalha                =  forms.ChoiceField (choices=FALHA,required=False, widget=None,label='Falha')
     tipoFalhaConjunto        = forms.IntegerField(label="Falha Conjunto", max_value=100,required=False,widget=forms.TextInput(attrs={'style':"width:100px",'value':'0'}))
     variavelFalhada          = forms.IntegerField(label="Varialvel Falhada",max_value=100,required=False,widget=forms.TextInput(attrs={'style':"width:100px",'value':'4'}))
     # metodoUtilizado          = forms.IntegerField(label="Metodo Utilizado",max_value=100,required=False,widget=forms.TextInput(attrs={'style':"width:100px",'value':'1'}))
     metodoUtilizado = forms.ChoiceField(choices=METODOS, required=False, widget=None, label='Metodo')