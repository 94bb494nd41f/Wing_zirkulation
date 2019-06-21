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


# def intalt():
#
#     norm = max(v_1, v_2, v_3)
#     v_1 = v_1 / norm
#     v_2 = v_2 / norm
#     v_3 = v_3 / norm
#
#     # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#     # Watch out for len_array already reduced by one!
#     # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#     len_array = len(data_array) - 1
#     summe = 0.0
#
#     h = (
#                 (data_array.item((len_array, 0)) - data_array.item((0, 0))) ** 2
#                 + (data_array.item((len_array, 1)) - data_array.item((0, 1))) ** 2
#                 + (data_array.item((len_array, 2)) - data_array.item((0, 2))) ** 2
#         ) \
#         / float(len_array)
#     h = math.sqrt(h)
#     ########################################################################################################
#     # inner part
#     for i in range(1, len_array - 0):
#         #  mydata: X|y|z|ux|uy|uz
#         summe += h * math.sqrt(
#             (data_array.item((i, 3)) * v_1)**2 + (data_array.item((i, 4)) * v_2)**2 + (data_array.item((i, 5)) * v_3)
#     ########################################################################################################
#     # beginning and end
#     summe += h * 0.5 * (
#             math.sqrt(
#                 (data_array.item((0, 3)) * v_1) ** 2 + (data_array.item((0, 4)) * v_2) ** 2 + (
#                             data_array.item((0, 5)) * v_3) ** 2
#             )
#             +
#             math.sqrt((data_array.item((len_array, 3)) * v_1) ** 2 + (data_array.item((len_array, 4)) * v_2) ** 2 + (
#                     data_array.item((len_array, 5)) * v_3) ** 2
#                       )
#     )
#
#     return (summe)


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
            #  print('c', c)
            #  layout
            #  x,y,z,u_x,u_y,u_z

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
                    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
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
                    print('gamma_total', gamma_total)
                    # c_gamma.append((mydata_1.item((0, 0)), gamma_total))

        # plotting(c_gamma, )
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
            print('\n Rho mit Rho=', rho, 'definiert')

            Radius = c_gamma / (2* 3.1415926) * (pmin / (rho * -0.871))**-0.5

            print('viskoser Radius:', Radius, 'm \n')


    print('\n \n -------------------------ende---------------------------------------')


def integration(data_array):
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # Watch out for len_array already reduced by one!
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    summe = 0.0

    h = sqrt((((data_array.item((len_array, 0))) ** 2 + (data_array.item((len_array, 1))) ** 2 + (
        data_array.item((len_array, 2))) ** 2)
              - (((data_array.item((0, 0))) ** 2 + (data_array.item((0, 1))) ** 2 + (
                    data_array.item((0, 2)) ** 2))) / float(len_array)))

    for i in range(1, len_array - 0):
        #  mydata: X|y|z|ux|uy|uz
        summe += h * data_array.item((i, point))

    summe += h * 0.5 * (data_array.item((0, point)) + data_array.item((len_array, point)))
    return (summe)


def plotting(c_gamma, plotkind):
    print('plot of gamma*' 'cwd', os.getcwd())
    # print(c_gamma)
    os.chdir(os.getcwd() + '/plots/')

    f = plt.figure()
    x_val = [x[0] for x in c_gamma]
    y_val = [x[1] for x in c_gamma]
    plt.ylabel('-Zirkulation')
    plt.plot(x_val, y_val, linestyle='None')
    plt.plot(x_val, y_val, 'or', linestyle='None')

    # spezifisch
    if 'vortex' in plotkind:
        # plott
        plt.xlabel('Abstand zur x=0 in, hier x_kood ')
        f.savefig('gammaspitzenwirbel' + '.pdf', bbox_inches='tight')
        # file

        f = open('gamma_spitzenwirbelverlauf.data', 'w')
        f.write('# x in m  \t Gamma in m^2/s \n')


    elif 'wing' in plotkind:
        plt.xlabel('Abstand zur wurzel in, hier z_kood ')
        f.savefig('gamma*_wing' + '.pdf', bbox_inches='tight')
        # file
        f = open('gamma_wing.data', 'w')
        f.write('# x in m  \t Gamma in m^2/s \n')

    # write file
    for x in c_gamma:
        a = x[0]
        b = x[1]
        f.write(str(a) + '\t' + str(b) + '\n')
    f.close

    print('plot and Datafile located in:', os.getcwd())
