from django import forms

class Pesquisa(forms.Form):

     PORCENTAGEM_FALHA_UM = tuple([(r, r) for r in list(range(1, 100))])
     PORCENTAGEM_FALHA_DOIS = tuple([(r, r) for r in list(range(1, 100))])
     FALHA = (("ale", "Aleatorio"), ("seq", "Sequencial"))
     METODOS = (('1','SLR'),('2','MLR'),('3','Media'),('4','SVM'))


     porcentagem_um              = forms.ChoiceField(choices=PORCENTAGEM_FALHA_UM, required=False, widget=None, label='Porcentagem Falha')
     porcentagem_dois              = forms.ChoiceField(choices=PORCENTAGEM_FALHA_DOIS, required=False, widget=None, label='Porcentagem Falha')
     tipoFalha                =  forms.ChoiceField (choices=FALHA,required=False, widget=None,label='Falha')
     tipoFalhaConjunto        = forms.IntegerField(label="Falha Conjunto", max_value=100,required=False,widget=forms.TextInput(attrs={'style':"width:100px",'value':'0'}))
     variavelFalhada          = forms.IntegerField(label="Varialvel Falhada",max_value=100,required=False,widget=forms.TextInput(attrs={'style':"width:100px",'value':'4'}))
     metodoUtilizado          =  forms.ChoiceField (choices=METODOS,required=False, widget=None,label='Metodos')
