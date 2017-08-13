from rpy2.robjects.packages import STAP
import os
class ScritpR:
    def executaScript(self):
        with open(os.getcwd()+"/estagio/base/ScriptR/scriptR.r", "r") as r:
            string = r.read()
        fun = STAP(string, "grafico")
