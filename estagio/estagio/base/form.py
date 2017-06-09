from django import forms

class Pesquisa(forms.Form):
     '''0000000030-1-ale-_13_0.4-1'''
     FALHA = (("ale", "Aleatorio"),("seq", "Sequencial"))

     numeroSequencial    =  forms.IntegerField(label="Numero Sequencial",max_value=100,required=False,widget=forms.TextInput(attrs={'style':"width:100px",'value':'0000000030'}))
     porcentagem         =  forms.IntegerField(label="Porcentagem",max_value=100,required=False,widget=forms.TextInput(attrs={'style':"width:100px",'value':'1'}))
     tipoFalha           =  forms.ChoiceField (choices=FALHA,required=False, widget=None,label='Numero Sequencial')
     treze               = forms.IntegerField(label="Numero Sequencial", max_value=100, required=False,disabled=True,widget=forms.TextInput(attrs={'style': "width:100px",'value':'_13_'}))
     tipoFalhaConjunto   = forms.IntegerField(label="Falha Conjunto", max_value=100,required=False,widget=forms.TextInput(attrs={'style':"width:100px",'value':'0'}))
     variavelFalhada     = forms.IntegerField(label="Varialvel Falhada",max_value=100,required=False,widget=forms.TextInput(attrs={'style':"width:100px",'value':'4'}))
     metodoUtilizado     = forms.IntegerField(label="Metodo Utilizado",max_value=100,required=False,widget=forms.TextInput(attrs={'style':"width:100px",'value':'1'}))