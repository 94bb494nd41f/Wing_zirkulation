# -*- coding: utf-8 -*-

import os
import math
import pandas as pd
import numpy as np
from numpy import genfromtxt
def linienlegen(finaleliste):
    punkte = []
    for letztereintrag in finaleliste:
        #print('finaleliste:', finaleliste[i])
        #letztereintrag=finaleliste[i]
        a=0.4  #max ist 0.31, grob gerechnet
        b=0.6 # max ist 0.365, grob gerechnet
        # fenster hat die Groesse 2a*2b

        c_stern=letztereintrag[1]

        x=letztereintrag[3]
        y=letztereintrag[4]
        z=letztereintrag[5]
        # linie ergibt sich aus start(bspw:y-b) und ende (bspw. x+b)
        punkte.append((x, y - a, z - b, x, y - a, z + b, str(c_stern) + '_1')) #senkrechter schnitt fuer chow
        punkte.append((x, y - a, z + b, x, y + a, z + b, str(c_stern)+ '_2'))
        punkte.append((x, y + a, z + b, x, y + a, z - b, str(c_stern)+'_3'))
        punkte.append((x, y + a, z - b, x, y - a, z - b, str(c_stern)+'_4'))
    return(punkte)

def sampledict(punkte):
    cwd=os.getcwd()
    print(cwd)
    #os.path.abspath(os.path.join(__file__ ,"../.."))
    #os.chdir('..')
    #os.chdir('..')
    os.chdir('..')
    os.chdir(os.getcwd()+'/system/')
    #print(os.getcwd())
    f=open('sampleDict_python_plotlines','w')
    #f.write('\\\\    File to get lines for calculation of gamma\n \n')
    #schreiben des Openfoamheaders
    f.write('FoamFile\n'
            '{\n'
            'version\t2.0;\n'
            'format\tascii;\n'
            'class\tdictionary;\n'
            'object\tsampleDict;\n'
            '}\n\n\n')
    #schreiben settings für sampleDict
    f.write( 'type sets;\n libs    ("libsampling.so");\n setFormat  raw;\n interpolationScheme cellPoint;\n  \
    writeControl writeTime;\n startTime latestTime;\ntimeInterval 1;\nfields (U);\n sets \n( \n')

    #schreiben der auszulesenden lines
    for i in punkte[:]:
        #print('i,punkte',i)
        #Welche liniennummer
        line=i[6]
        line_nummer=line[len(line)-1]
        c=round(float(i[0])/1.2192, 2)
        #kontrollausgabe
        #print('i:', i[6])
        x_1=i[0]
        y_1=i[1]
        z_1=i[2]
        x_2=i[3]
        y_2=i[4]
        z_2=i[5]
        f.write('c*'+str(c)+'_'+str(line_nummer)+'\n'
            ' {\n'
            ' type uniform;\n'
            ' axis xyz;\n'
            ' start ( '+str(x_1)+' '+str(y_1)+' '+str(z_1)+');\n'
            ' end (' +str(x_2)+' '+str(y_2)+' '+str(z_2)+');\n'
            ' nPoints \t 1000;\n'
            '}\n\n')

    f.write(');')
    f.close()



if __name__ == '__main__':
    finaleliste=[]
    c = 1.2192
    y = 0.16
    z = 0.61
    x_list=[0.12192,	0.24384	,0.36576	,0.48768	,0.6096	,0.73152	,0.85344,0.97536	,1.09728\
        ,1.2192	,1.34112	,1.46304	,1.58496	,1.70688	,1.8288	,1.95072	,2.07264\
        ,2.19456	,2.31648	,2.4384	,2.56032	,2.68224	,2.80416	,2.92608	,3.048\
        ,3.16992	,3.29184]
    for x in x_list:
        finaleliste.append((480, round(x/c,3), 5 , x, y, z))
    punkte=linienlegen(finaleliste)
    sampledict(punkte)
    cwd=os.getcwd()


