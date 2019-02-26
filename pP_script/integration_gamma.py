import os
import shutil
import math
import matplotlib.pyplot as plt
import numpy as np


def Einlesen():
    cwd=os.getcwd()
    print('\n das ist die cwd:\n ', cwd)


    os.chdir(cwd+'/sampleDict_python_plotlines')
    list_timesteps=os.listdir(os.getcwd())
    print('Timesteps', list_timesteps)
    #konvertieren der string-liste in float um spaeter den maximalen timestep zu finden.
    list_timesteps_float=[float(i) for i in list_timesteps]

    samplewd=os.getcwd()
    for x_dir in list_timesteps[:]:
        print('xdir', x_dir)
        os.chdir(samplewd+'/'+str(x_dir))

        # removing previous plots
        if 'plots' in os.listdir(os.getcwd()):
            shutil.rmtree(os.getcwd() + '/plots')
        os.mkdir(os.getcwd() + '/plots', 0o777)

        l_data=os.listdir(os.getcwd())
        print('current timestep', x_dir)
        #x=l_data
        c_list = []
        line_list = []
        #muss so eingelesen werden, sonst zuordnung lines zu plane schwierig. gibt bestimmt einfacheren weg
        for y_dir in l_data[:]:
            #sonst werden auch ordner etc versucht zu laden
            if 'c'==y_dir[0]:
               if y_dir[2:5] not in c_list:
                   c_list.append(y_dir[2:5])
               line_list.append(y_dir[6])


                #print('linelist:', line_list, 'max', max(line_list))
        c_gamma = []
        c_list.sort() #sortieren fuer Datei
        for c in c_list[:]:
            print('c', c)
            #x,y,z,u_x,u_y,u_z

            #loading into mydata
            n=0
            for i in range(1, int(max(line_list))+1):
                filename='c*'+str(c)+'_'+str(i) + '_' + 'U.xy'
                #print('timestep', x_dir, 'currentfile', str(c)+'_'+str(i) + '_' + 'U')
                if i==1:
                    mydata_1 = np.genfromtxt(str(filename), skip_header=0, dtype=float)
                    #print(mydata_1.item((0, 0)),mydata_1.item((0, 1)), mydata_1.item((0, 2)))
                    n +=1
                if i==2:
                    mydata_2 = np.genfromtxt(str(filename), skip_header=0, dtype=float)
                    #print(mydata_2.item((0, 0)), mydata_2.item((0, 1)), mydata_2.item((0, 2)))
                    n +=1
                if i==3:
                    mydata_3 = np.genfromtxt(str(filename), skip_header=0, dtype=float)
                    #print(mydata_3.item((0, 0)), mydata_3.item((0, 1)), mydata_3.item((0, 2)))
                    n +=1
                if i==4:
                    mydata_4 = np.genfromtxt(str(filename), skip_header=0, dtype=float)
                    #print(mydata_4.item((0, 0)), mydata_4.item((0, 1)), mydata_4.item((0, 2)))
                    n +=1
                #print('n:',n)
                if n>=4:
                #if not mydata_1 and mydata_2 and mydata_3 and mydata_4:
                    ############################################################################################
                     #                       -u_z 2
                     #           ____________________________
                     #           |           <-              |
                     #   -u_y 3  |                           |/\ u_y 1
                     #       \/  |                           |
                     #           |___________________________|_
                     #                   ->
                     #                       u_z 4

                    #Signum defined by stepwidth h
                    #############################################################################################################
                    ############################integration of mydata_1
                    #############################################################################################################
                    # Berechnung der Schrittweite funktioniert nur für den Fall von Linien, die sich nicht auf mehr als einer var aendern!
                    data_array = mydata_1
                    len_array = len(data_array)-1
                    summe_1 = 0.0
                    #h=(b-a)/n
                    h=(((data_array.item((len_array, 0)) + data_array.item((len_array, 1))  + data_array.item((len_array, 2)))\
                    -(data_array.item((0, 0)) + data_array.item((0, 1)) + data_array.item((0, 2))))/float(len_array))

                    print('h1', h)
                    for i in range(1, len_array - 2):
                        # mydata: X|y|z|ux|uy|uz
                        summe_1 += h * data_array.item((i, 5))

                    summe_1 += h *0.5*( data_array.item((0, 5))  + data_array.item((len_array, 5)))
                    #############################################################################################################
                    ############################integration of mydata_2
                    #############################################################################################################
                    data_array = mydata_2
                    len_array = len(data_array)-1
                    summe_2 = 0.0
                    h = (((data_array.item((len_array, 0)) + data_array.item((len_array, 1)) + data_array.item(
                    (len_array, 2))) \
                     - (data_array.item((0, 0)) + data_array.item((0, 1)) + data_array.item((0, 2)))) / float(len_array))
                    print('h2',h)
                    for i in range(1, len_array - 2):
                        # mydata: X|y|z|ux|uy|uz
                        summe_2 += h *data_array.item((i, 4))

                    summe_2 += h *-0.5*( data_array.item((0, 4))  + data_array.item((len_array, 4)))
                    #############################################################################################################
                    ############################integration of mydata_3
                    #############################################################################################################
                    data_array = mydata_3
                    len_array = len(data_array)-1
                    summe_3 = 0.0
                    h = (((data_array.item((len_array, 0)) + data_array.item((len_array, 1)) + data_array.item((len_array, 2))) \
                    - (data_array.item((0, 0)) + data_array.item((0, 1)) + data_array.item((0, 2)))) / float(len_array))
                    print('h3', h)
                    for i in range(1, len_array - 2):
                        # mydata: X|y|z|ux|uy|uz
                        summe_3 += h *data_array.item((i, 5))

                    summe_3 += h * 0.5 * (data_array.item((0, 5)) + data_array.item((len_array, 5)))
                    #############################################################################################################
                    ############################integration of mydata_4
                    #############################################################################################################
                    data_array = mydata_4
                    len_array = len(data_array)-1
                    summe_4 = 0.0
                    h = (((data_array.item((len_array, 0)) + data_array.item((len_array, 1)) + data_array.item(
                        (len_array, 2))) \
                         - (data_array.item((0, 0)) + data_array.item((0, 1)) + data_array.item((0, 2)))) / float(
                        len_array))
                    print('h4', h)
                    for i in range(1, len_array - 2):
                        # mydata: X|y|z|ux|uy|uz
                        summe_4 += h * data_array.item((i, 4))

                    summe_4 += h * 0.5 * (data_array.item((0, 4)) + data_array.item((len_array, 4)))


                    print('summen:', summe_1, summe_2, summe_3, summe_4)
                    gamma_total=summe_1+summe_2+summe_3+summe_4
                    c_gamma.append((c, gamma_total))
                    gamma_total = 0
            #struktur: c|gamma


    f = plt.figure()

    print('plot of gamma*' 'cwd', os.getcwd())
    print(c_gamma)
    x_val = [x[0] for x in c_gamma]
    y_val = [x[1] for x in c_gamma]
    plt.xlabel('abstand zu hinterkante in c')
    plt.ylabel('Zirkulation')
    plt.plot(x_val, y_val,  linestyle='None')
    plt.plot(x_val, y_val, 'or',  linestyle='None')
    f.savefig('plots/c_gamma*' + '.pdf', bbox_inches='tight')

    os.chdir(os.getcwd() + "/plots/")
    f = open('c_gamma_wing.data', 'w')
    f.write('#x in x/b  \t Gamma in m^2/s \n')
    for x in c_gamma:
        a = x[0]
        b = x[1]
        f.write(str(a) + '\t' + str(b) + '\n')
    f.close

    print('plot and Datafile located in:', os.getcwd())
    plt.show()



    plt.close()


    return()


if __name__ == '__main__':
    print('Bitte README lesen')
    n=Einlesen()



