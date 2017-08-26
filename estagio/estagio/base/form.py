from django import forms

class Pesquisa(forms.Form):

     PORCENTAGEM_FALHA_UM = tuple([(r, r) for r in list(range(1, 100))])
     PORCENTAGEM_FALHA_DOIS = tuple([(r, r) for r in list(range(1, 100))])
     FALHA = (("ale", "Aleatorio"), ("seq", "Sequencial"))
     METODOS = (('1','SLR'),('2','MLR'),('3','Media'),('4','SVM'))

     FALHA_CONJUNTO =(('0','NET GLOBALI GLOBALR PARI E PAR')
                      ,('1','TODA A LINHA FALHADA'),('2','T e UR')
                      ,('3','TSOLO e URSOLO')
                      ,('4','Individual'))

     porcentagem_um    =    forms.ChoiceField(choices=PORCENTAGEM_FALHA_UM, required=False, widget=None, label='Porcentagem Falha')
     porcentagem_dois  =    forms.ChoiceField(choices=PORCENTAGEM_FALHA_DOIS, required=False, widget=None, label='Porcentagem Falha')
     tipoFalha         =    forms.ChoiceField (choices=FALHA,required=False, widget=None,label='Falha')
     falha_conjunto         =    forms.ChoiceField (choices=FALHA_CONJUNTO,required=False, widget=None,label='Falha Conjunto')
     # tipoFalhaConjunto =    forms.IntegerField(label="Falha Conjunto", max_value=100,required=False,widget=forms.TextInput(attrs={'style':"width:100px",'value':'0'}))
     # variavelFalhada   =    forms.IntegerField(label="Varialvel Falhada",max_value=100,required=False,widget=forms.TextInput(attrs={'style':"width:100px",'value':'4'}))
     metodoUtilizado   =    forms.ChoiceField (choices=METODOS,required=False, widget=None,label='Metodos')

