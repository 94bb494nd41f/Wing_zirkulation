import os
import shutil
import matplotlib.pyplot as plt
import numpy as np
import math

def integration(data_array):
    #############################################################
    # get orientation of vector and norm it to one to later calculate the velocity along the line
    ##################################
    v_1 = data_array.item((1, 0)) - data_array.item((0, 0))
    v_2 = data_array.item((1, 1)) - data_array.item((0, 1))
    v_3 = data_array.item((1, 2)) - data_array.item((0, 2))

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # Watch out for len_array already reduced by one!
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    len_array = len(data_array) - 1
    summe = 0.0

    # inner part
    for i in range(1, len_array - 0):
        summe += v_1 * data_array.item((i, 3)) + \
                 v_2 * data_array.item((i, 4)) + \
                 v_3 * data_array.item((i, 5))
    # first item
    summe += 0.5 * (
            v_1 * data_array.item((0, 3)) +
            v_2 * data_array.item((0, 4)) +
            v_3 * data_array.item((0, 5))
    )

    # last item
    summe += 0.5 * (
            v_1 * data_array.item((len_array, 3)) +
            v_2 * data_array.item((len_array, 4)) +
            v_3 * data_array.item((len_array, 5))
    )
    return summe


# load data
def Einlesen():
    cwd = os.getcwd()
    print('\n das ist die cwd:\n ', cwd)

    #  wingtotal_list=[]

    #  cwd is "postProcessing, switching to calculated lines

    os.chdir(cwd + '/sampleDict_python_plotlines')
    list_timesteps = os.listdir(os.getcwd())
    print('Timesteps', list_timesteps)

    #  konvertieren der string-liste in float um spaeter den maximalen timestep zu finden.
    list_timesteps_float = [float(i) for i in list_timesteps]

    samplewd = os.getcwd()
    #  itterating through every timestep
    for x_dir in list_timesteps[:]:
        #  print('xdir', x_dir)

        os.chdir(samplewd + '/' + str(x_dir))

        #   removing previous plots
        if 'plots' in os.listdir(os.getcwd()):
            shutil.rmtree(os.getcwd() + '/plots')
        #  creat 'plots'folder
        os.mkdir(os.getcwd() + '/plots', 0o777)
        #  assume l is for "line"
        l_data = os.listdir(os.getcwd())
        print('current timestep', x_dir)
        #  x=l_data
        c_list = []
        line_list = []
        #  muss so eingelesen werden, sonst zuordnung lines zu plane schwierig. gibt bestimmt einfacheren weg

        #  get string until '_'
        for y_dir in l_data:
            if 'c' == y_dir[0]:  # ensure only files created by previous tools are loaded
                if y_dir.partition('_')[0] not in c_list:
                    c_list.append(y_dir.partition('_')[0])  # string till first '_'
                line_list.append(y_dir.split('_')[1])  # string till second '_'

                #  print('linelist:', line_list, 'max', max(line_list))
        c_gamma = []
        #  sort ascending
        c_list.sort()
        for c in c_list[:]:
                        #  loading into mydata
            #  stupid way to ensure every of the four lines has been loaded
            aa = 0
            bb = 0
            cc = 0
            dd = 0
            #  loading is ugly af, solve by replace if with for
            #  check for load of all files by avoiding/counting erros during np.genfromtext and wrong filename
            for i in range(1, int(max(line_list)) + 1):
                filename = str(c) + '_' + str(i) + '_' + 'U.xy'
                # print('timestep', x_dir, 'currentfile', str(c)+'_'+str(i) + '_' + 'U')
                if i == 1:
                    mydata_1 = np.genfromtxt(str(filename), skip_header=0, dtype=float)
                    # print(mydata_1.item((0, 0)),mydata_1.item((0, 1)), mydata_1.item((0, 2)))
                    aa = 1
                if i == 2:
                    mydata_2 = np.genfromtxt(str(filename), skip_header=0, dtype=float)
                    # print(mydata_2.item((0, 0)), mydata_2.item((0, 1)), mydata_2.item((0, 2)))
                    bb = 1
                if i == 3:
                    mydata_3 = np.genfromtxt(str(filename), skip_header=0, dtype=float)
                    # print(mydata_3.item((0, 0)), mydata_3.item((0, 1)), mydata_3.item((0, 2)))
                    cc = 1
                if i == 4:
                    mydata_4 = np.genfromtxt(str(filename), skip_header=0, dtype=float)
                    # print(mydata_4.item((0, 0)), mydata_4.item((0, 1)), mydata_4.item((0, 2)))
                    dd = 1
                # print('n:',n)
                if aa == 1 and bb == 1 and cc == 1 and dd == 1:
                    # if not mydata_1 and mydata_2 and mydata_3 and mydata_4:
                    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                    #                        -u_z 2
                    #            ____________________________
                    #            |           <-              |
                    #    -u_y 3  |                           |/\ u_y 1
                    #        \/  |                           |
                    #            |___________________________|_
                    #                    ->105:70
                    #                        u_z 4
                    # integration around wing
                    summe_1 = integration(mydata_1)
                    summe_2 = integration(mydata_2)
                    summe_3 = integration(mydata_3)
                    summe_4 = integration(mydata_4)
                    gamma_total = summe_1 + summe_2 + summe_3 + summe_4
                    #  mydata: X|y|z|ux|uy|uz

        os.chdir(cwd)
    return (gamma_total)

if __name__ == '__main__':
    ################################################################################
    # PARAMETER
    #############################################################################

    rho = 1 # in kg/m^3 nur für die Bestimmung des Viskosen Kerns wichtig


    ############################################################################
    # keine Parameter mehr
    ####################################################################################
    print('Bitte README lesen')

    c_gamma = Einlesen() # berechnen Zirkulation
    print('\n Ergebnisse:\n')
    print('zirkulation:', c_gamma, ' m ^2/s \n')

    cwd = os.getcwd()
    if 'p_min' in os.listdir(cwd): # einlesen des Druckminimums, gefunden in "direction of vortex
        p_file = np.genfromtxt('p_min', skip_header=0, dtype=float, delimiter=",")
        pmin = p_file.item(3)

        try:    # schauen ob rho definiert ist
           rho
        except NameError:
            print('\n Achtung \n Rho nicht definiert!\n')

        else:
            print('\n Rho mit Rho=', rho, '\n', 'p_min:', pmin, 'definiert')

            Radius = c_gamma / (2* 3.1415926) * (pmin / (rho * -0.871))**-0.5

            print('viskoser Radius basierend auf Druck:', Radius, 'meter \n')

    if 'v_max' in os.listdir(cwd):
        v_file = np.genfromtxt('v_max', skip_header=0, dtype=float, delimiter=",")
        v_max = math.sqrt(v_file.item(3)**2 + v_file.item(4)**2 + v_file.item(5)**2)
        t = 2.513 * c_gamma /(2*3.1415926 * v_max)
        Radius = math.sqrt(2.513 * abs(c_gamma) /(2*3.1415926 * v_max))
        print('viskoser Radius basierend auf Wirbelstärke:', Radius, 'm \n')

    print('\n \n -------------------------ende---------------------------------------')
