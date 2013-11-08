# coding: utf-8

import os
import sys

erro = False

for subdir, _, filePys in os.walk('./'):
    for filePy in filePys:
        
        infoFile = filePy.split(".")
        if (len(infoFile) == 2 and infoFile[1] == "py"):
            if (filePy != "padronizar.py" and filePy != "runTestPep8.py"):
            
                # os.system("autopep8 --in-place --aggressive " + subdir +"/" + filePy)
                print("------ Run Pep8 in " + filePy + " -------")
                # os.system("pep8 --statistics " + subdir +"/" + filePy)
                os.system("pylint " + subdir + "/" + filePy + " --reports=n --disable=C,R,F0401,E1121,E0213,W0232,W0614,C0103,C0111,R0913,W0403,W0401,C0301,w0141,W0212 2> arquivo.rst ")
                arq = open("arquivo.rst")
                text = arq.readlines()
                if(len(text) > 0):
                    erro = True
                    for line in text:
                        print (line)
                arq.close()
                os.system("rm arquivo.rst")
                # os.system("flake8 --statistics " + subdir +"/" + filePy)
                print("------------------------------------\n")

if(erro):
    raise Exception("O codigo possui erros")
else:
    print("A analise do Pep8 e Pylint não encontrou erros")
