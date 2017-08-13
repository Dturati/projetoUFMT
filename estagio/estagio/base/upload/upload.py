import zipfile
import os
from django.core.files.storage import FileSystemStorage
from ..ScriptR.scriptR import ScritpR
class Upload:
    def __init__(self):
        self.instScriptR = ScritpR()

    def upload(self,myfile):
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        zip_ref = zipfile.ZipFile(str(os.getcwd()) + "/estagio/arquivos/" + str(myfile.name), 'r')
        zip_ref.extractall(str(os.getcwd()) + "/estagio/arquivos/upload/" + str(myfile.name))
        zip_ref.close()
        os.remove(str(os.getcwd()) + "/estagio/arquivos/" + str(myfile.name))
        self.instScriptR.executaScript()

        return True,uploaded_file_url

