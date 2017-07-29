def empty(var):
    try:
        print(var.data)
        if(var.data['todosOsArquivos'] == 'ativado'):
            return True
    except:
       return False
