resultados = read.csv('3159562134.csv',header = TRUE,sep=',',dec='.')

tiposFalhas = c('ale','seq')
falhasConjunto  = c('f0','f1','f2','f3','f4')
dirVariaveis = c('globali','globalr','net','pari','parr','ppt','rh','rhsoil','t','tsoil','u')

#tiposFalhas = c('ale')
#falhasConjunto  = c('f0')

metodos = unique(resultados$Metodo)
variaveis = unique(resultados$Variavel)
juncoes = unique(resultados$Juncao)
metodosNomes = c('SLR','MLR','Media','SVM')
metodosCores = c('black','blue','red','green')
nomesGeral=c('net','globali','globalr','pari','parr','tsoil','ppt','t','rh','u','rhsoil')
colunas = c("R2",'d','MAE','RMSE')

# POR VARIAVEIS
path = './grafico/BoxplotVar/'
eixoX = 'Variáveis'
for(index in seq(1,length(colunas))){
  #index=1
  coluna = colunas[index]
  if(index > 2){
    limite = c()
  }else{
    limite = c(0,1)
  }

  variaveisUsadas = unique(resultados$Variavel)
  nomes = nomesGeral[variaveisUsadas-3]
  nomes
  titulo = paste(coluna)
  print(titulo)
  boxplot(resultados[,coluna]
          ~resultados$Variavel,
          ylab=coluna,names=c(nomes),main=titulo,ylim=limite)
  arquivo = paste(path,coluna,'/metodo',sep='')
  arquivo = paste(arquivo,coluna,sep='_')
  arquivo = paste(arquivo,'.png',sep='')
  dev.print(device=png, arquivo,width=1024,height=768)

  for(tipo in tiposFalhas){

    titulo = paste(coluna,tipo)
    print(titulo)
    boxplot(resultados[(resultados$Tipo==tipo),coluna]
            ~resultados$Variavel[resultados$Tipo==tipo],
            ylab=coluna,xlab=eixoX,names=nomes,main=titulo,ylim=limite)
    arquivo = paste(path,tipo,'/',coluna,'/metodo',sep='')
    arquivo = paste(arquivo,tipo,coluna,sep='_')
    arquivo = paste(arquivo,'.png',sep='')
    dev.print(device=png, arquivo,width=1024,height=768)

    for(juncao in juncoes){

      titulo = paste(coluna,tipo,'Falha',juncao)
      print(titulo)
      boxplot(resultados[(resultados$Tipo==tipo & resultados$Juncao==juncao),coluna]
              ~resultados$Variavel[resultados$Tipo==tipo & resultados$Juncao==juncao],
              ylab=coluna,xlab=eixoX,names=nomes,main=titulo,ylim=limite)
      arquivo = paste(path,tipo,'/f',juncao,'/',coluna,'/todos',sep='')
      arquivo = paste(arquivo,tipo,coluna,'FalhaConjunto',juncao,sep='_')
      arquivo = paste(arquivo,'.png',sep='')
      dev.print(device=png, arquivo,width=1024,height=768)

    }
  }
}