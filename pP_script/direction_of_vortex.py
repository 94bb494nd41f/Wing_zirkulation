import os
import math
# import pandas as pd
import numpy as np
# from numpy import genfromtxt
# os.system('postProcess -func sampleDict_plane_U')


def length_norm(x, y, z, length): # norming vector to a length
    f = length/math.sqrt(
        x**2 + y**2 + z**2
    )
    x = f*x
    y = f*y
    z = f*z
    return x, y, z


def Einlesen1(plotkind):
    cwd = os.getcwd()
    print('\n das ist die cwd:\n ', cwd, '\n')
    # t1 = os.path.getctime(cwd + '/sampleDict_plane_vorticity')
    # t2 = os.path.getctime(cwd + '/sampleDict_plane_pressure')
    if 'sampleDict_plane_vorticity' in os.listdir(cwd) and 'sampleDict_plane_pressure' in os.listdir(cwd):
        if os.path.getctime(cwd + '/sampleDict_plane_vorticity') > os.path.getctime(cwd + '/sampleDict_plane_pressure'):
            # determine the newest File/ Folder
            os.chdir(cwd + '/sampleDict_plane_vorticity')
        elif os.path.getctime(cwd + '/sampleDict_plane_vorticity') < os.path.getctime(cwd + '/sampleDict_plane_pressure'):
            os.chdir(cwd + '/sampleDict_plane_pressure')

    elif 'sampleDict_plane_vorticity' not in os.listdir(cwd) or 'sampleDict_plane_pressure' not in os.listdir(cwd):
        if 'sampleDict_plane_pressure' in os.listdir(cwd):
            os.chdir(cwd + '/sampleDict_plane_pressure')
        if 'sampleDict_plane_vorticity' in os.listdir(cwd):
            os.chdir(cwd + '/sampleDict_plane_vorticity')
        if 'sampleDict_plane_vorticity' not in os.listdir(cwd) and 'sampleDict_plane_pressure' not in os.listdir(cwd):
            dummy = 'n'
            array = None
            return array, dummy

    list_timesteps = os.listdir(os.getcwd())
    print('Timesteps', list_timesteps)
    # get latestTimestep
    latest_timestep = max([int(i) for i in list_timesteps])
    print('latest_timestep:', latest_timestep)
    samplewd = os.getcwd()
    #  itterating through every timestep
    for x_dir in list_timesteps[:]:
        #  print('xdir', x_dir)
        os.chdir(samplewd+'/'+str(x_dir))

        ls_data=os.listdir(os.getcwd())
        for filename in ls_data[:]:
            if filename[0] == 'v':
                # x  y  z  vorticity_x  vorticity_y  vorticity_z ndarray
                vorticity_1 = np.genfromtxt(str(filename), skip_header=2, dtype=float)
                os.chdir(cwd)
                dummy = "v"
                return vorticity_1, dummy
            if filename[0] == 'p':
                # x  y  z  vorticity_x  vorticity_y  vorticity_z ndarray
                pressure_1 = np.genfromtxt(str(filename), skip_header=2, dtype=float)
                os.chdir(cwd)
                dummy = "p"
                return pressure_1, dummy


def find_max(array, xup, xlow, yup, ylow, zup, zlow, dummy):
    # x  y  z  vorticity_x  vorticity_y  vorticity_z ndarray
    # init values
    if dummy == "v":
        v_xyz_max = array.item((0, 3))**2 + array.item((0, 4))**2 + array.item((0, 5))**2
    elif dummy == "p":
        p_min = array.item((0, 3))
    max_line = array.item(0)

    # boundaries
    x_bound = [xup, xlow]
    x_bound.sort()  # now x_bound=[x_low,x_up]

    y_bound = [yup, ylow]
    y_bound.sort()

    z_bound = [zup, zlow]
    z_bound.sort()

    for i in array:
        if x_bound[0] < i.item(0) < x_bound[1]:
            if y_bound[0] < i.item(1) < y_bound[1]:
                if z_bound[0] < i.item(2) < z_bound[1]:

                    if dummy == "v": # looking for vorticity max
                        v_xyz_new = i.item(3) ** 2 + i.item(4) ** 2 + i.item(5) ** 2
                        if v_xyz_new > v_xyz_max:
                            max_line = i
                            v_xyz_max = v_xyz_new
                            #print('current_vor:', v_xyz_new, 'max_vor', v_xyz_max)
                            #print('\n i\n', i, 'max_line \n', max_line)
                    elif dummy == "p": # looking for min pressure
                        p_min_new = i.item (3)
                        if p_min > p_min_new:
                            p_min = p_min_new
                            max_line = i

    if dummy == "v":
        v_xyz_max_real = math.sqrt(
            max_line.item(3)**2 + max_line.item(4)**2 + max_line.item(5)**2
        )
        f = open('v_max', 'w')  # schreiben von xyz v_i in datei fuer bestimmung viskoser radius
        f.write(str(max_line.item(0)) + ' , ')
        f.write(str(max_line.item(1)) + ' , ')
        f.write(str(max_line.item(2)) + ' , ')
        f.write(str(max_line.item(3)) + ' , ')
        f.write(str(max_line.item(4)) + ' , ')
        f.write(str(max_line.item(5)) + ' , ')
        f.close
        return v_xyz_max_real, max_line, dummy
    if dummy == "p":

        f = open('p_min', 'w')  # schreiben von xyz pmin in datei fuer bestimmung viskoser radius
        f.write(str(max_line.item(0)) + ' , ')
        f.write(str(max_line.item(1)) + ' , ')
        f.write(str(max_line.item(2)) + ' , ')
        f.write(str(p_min))
        f.close
        return p_min, max_line, dummy


def avg_vorticity(array, max_line, radius ):
    n = 0
    avg_list = []
    #np.array(avg_list,)
    avg_x = 0
    avg_y = 0
    avg_z = 0
    sig_x = np.sign(max_line.item(0))
    sig_y = np.sign(max_line.item(1))
    sig_z = np.sign(max_line.item(2))

    #determine boundaries
    x_bound = [max_line.item(0) + radius, max_line.item(0) - radius ]
    x_bound.sort()      # now x_bound=[x_low,x_up]

    y_bound = [max_line.item(1) + radius, max_line.item(1) - radius]
    y_bound.sort()

    z_bound = [max_line.item(2) + radius, max_line.item(2) - radius]
    z_bound.sort()

    for i in array:
        if x_bound[0] < i.item(0) < x_bound[1]:
            if y_bound[0] < i.item(1) < y_bound[1]:
                if z_bound[0] < i.item(2) < z_bound[1]:
                    # every value is now inside a cube, now cancle values out, whose euclidean distance is larger than
                    # radius. avoid SQRT!
                    if ((max_line.item(0)-i.item(0))**2+(max_line.item(1)-i.item(1))**2 +(max_line.item(2)-i.item(2))**2) < radius**2:
                        n += 1
                        avg_list.append((i.item(3), i.item(4), i.item(5)))

    frac = 1/(len(avg_list))
    avg_list = np.asanyarray(avg_list)

    for i in avg_list:      #sum for average
        avg_x += i.item(0)
        avg_y += i.item(1)
        avg_z += i.item(2)
    # multiply with 1/n
    avg_x = frac * avg_x
    avg_y = frac * avg_y
    avg_z = frac * avg_z

    avg_vort = math.sqrt(
        (avg_x)**2 +
        (avg_y)**2 +
        (avg_z)**2
    )
    n_line = (max_line.item(0), max_line.item(1), max_line.item(2), avg_x, avg_y, avg_z)
    n_line = np.asanyarray(n_line)
    return avg_vort, n_line



def sampledict (punkte):
    cwd = os.getcwd()

    os.chdir('..')
    os.chdir(os.getcwd() + '/system/')
    # print(os.getcwd())
    f = open('sampleDict_python_plotlines', 'w')
    # f.write('\\\\    File to get lines for calculation of gamma\n \n')
    # schreiben des Openfoamheaders
    f.write('FoamFile\n'
            '{\n'
            'version\t2.0;\n'
            'format\tascii;\n'
            'class\tdictionary;\n'
            'object\tsampleDict;\n'
            '}\n\n\n')
    # schreiben settings für sampleDict
    f.write('type sets;\n libs    ("libsampling.so");\n setFormat  raw;\n interpolationScheme cellPoint;\n  \
    writeControl writeTime;\n startTime latestTime;\ntimeInterval 1;\nfields (U);\n sets \n( \n')

    # schreiben der auszulesenden lines
    n = 0
    for i in punkte[:]:
        # print('i,punkte',i)
        # Welche liniennummer

        line_nummer = i[6]
        # kontrollausgabe
        # print('i:', i[6])
        x_1 = i[0]
        y_1 = i[1]
        z_1 = i[2]
        x_2 = i[3]
        y_2 = i[4]
        z_2 = i[5]
        # kontrollausgaben
        # print('c*'+str(c)+'_'+str(line_nummer)+'\n')
        # print('c*' + i[6] + '_' + str(line_nummer) + '\n')

        f.write('c' + str('1') + '_' + str(line_nummer) + '\n'
                                                          ' {\n'
                                                          ' type uniform;\n'
                                                          ' axis xyz;\n'
                                                          ' start ( ' + str(x_1) + ' ' + str(y_1) + ' ' + str(
            z_1) + ');\n'
                   ' end (' + str(x_2) + ' ' + str(y_2) + ' ' + str(z_2) + ');\n'
                                                                           ' nPoints \t 1000;\n'
                                                                           '}\n\n')

    f.write(');')
    f.close()
    os.chdir(cwd)
    return()


def berechnung_Rechteckvektor(c_1, c_2, c_3):
    #gewaehlte RB
    a_1 = c_1
    a_2 = c_2
    b_2 = c_2

    # calculate missing parts of vectors
    a_3 = -(c_1 ** 2 + c_2 ** 2) / c_3
    b_1 = -(c_2 ** 2) / c_1

    b_3 = (c_2 ** 2 - c_2 * b_2) / (c_3 - a_3)  # = 0, not needed

    # norm vectors so a defined length
    length = real_length / 2
    a_1, a_2, a_3 = length_norm(a_1, a_2, a_3, length)
    b_1, b_2, b_3 = length_norm(b_1, b_2, b_3, length)
    c_1, c_2, c_3 = length_norm(c_1, c_2, c_3, length)
    print('\n c_i colinear to vortex, a,c,b are orthogonal to eachother and normed to a length of', length)
    print('c1,c2,c3: \t', c_1, c_2, c_3)
    print('a1,a2,a3: \t', a_1, a_2, a_3)
    print('b1,b2,b3: \t', b_1, b_2, b_3)

    return a_1, a_2, a_3, b_1, b_2, b_3


if __name__ == '__main__':
    # Parameter
    ######################################################
    #   _________________
    #   |                |
    #   |                |
    #   |        +       |       das soll quadratisch sein
    #   |                |
    #   |________________|
    #    <--------------->
    #       real_length
    #
    #
    ##############################################################
    real_length = 0.4 # absolute groeße des Fensters, ist quadratisch

    cellsize = 0.0082  # cellsize in core vortex

    cellcount = 20      # calculates with the cellsize to the radius, which is used to average around the maximum

    # Grenzen in denen Nach Maxi/minima gesucht werden soll
    xup =10000
    xlow =-10000

    yup = 10000
    ylow = -10000

    zup = 10000
    zlow = -10000

    radius = cellcount * cellsize
    # Manuelle Definition des Zentrums
    #x_c
    #y_c
    #z_c

    #definition der Vektoren
    #Richtung des Wirbels:
    # c_1=
    # c_2=
    # c_3=
    #
    # #Vektor fuer Rechteck in Richtung 1
    # a_1=9
    # a_2=9
    # a_3=9
    #
    # # Vektor fuer Rechteck in Richtung 2
    # b_1=9
    # b_2=9
    # b_3=9


    ##########################################################################################################
    # keine Parameter mehr
    ##################################################################################################################



    array, dummy = Einlesen1(plotkind='wing') # liest die Druck oder Voritcity datei ein

    #######################################################################
    #           Manuell Definiert
    if dummy == "n":
        print('Verfahren im manuellen Modus')
        try:
            a_1 and a_2 and a_3 and b_1 and b_2 and b_3
        except NameError:
            print('\n Vektoren fuer Liniengeneration (\" Rechteckvektoren\") fehlen\n')
            try:
                c_1 and c_2 and c_3
            except NameError:
                print('\n Wirbelachse definieren, Rechteckvektoren koennen nicht berechnet werden\n')
                definiert = False
            else:
                print('\n Rechteckvektoren werden basierend auf wirbelachse berechnet \n')

                a_1, a_2, a_3, b_1, b_2, b_3 = berechnung_Rechteckvektor(c_1, c_2, c_3)

                definiert = True

        else:
            print('\n Vektoren definiert\n ')
            definiert = True
        try:
            x_c and y_c and z_c
        except NameError:
            print('\n wirbelzentrum nicht definiert')
            definiert = False
        else:
            if definiert == True:
                x_core = x_c
                y_core = y_c
                z_core = z_c


    #############################################################################################################
    #               Druck
    if dummy == "p":
        print('Verfahren im Druck Modus')
        max_vor, max_line, dummy = find_max(array, xup, xlow, yup, ylow, zup, zlow,
                                            dummy)  # Bestimmung des maxi/minimalen werts
        try:
            a_1 and a_2 and a_3 and b_1 and b_2 and b_3
        except NameError:
            print('\n Vektoren fuer Liniengeneration (\" Rechteckvektoren\") fehlen\n')
            try:
                c_1 and c_2 and c_3
            except NameError:
                print('\n Wirbelachse definieren, Rechteckvektoren werden auf dieser Basis berchnet\n')
                definiert = False
            else:
                print('\n Rechteckvektoren werden basierend auf wirbelachse berechnet \n')
                a_1, a_2, a_3, b_1, b_2, b_3 = berechnung_Rechteckvektor(c_1, c_2, c_3)

                x_core = max_line.item(0)
                y_core = max_line.item(1)
                z_core = max_line.item(2)
                p_min = max_line.item(3)

                definiert = True


        else:
            print('Variablen definiert')
            max_vor, max_line, dummy = find_max(array, xup, xlow, yup, ylow, zup, zlow,
                                                dummy)  # Bestimmung des maxi/minimalen werts
            x_core = max_line.item(0)
            y_core = max_line.item(1)
            z_core = max_line.item(2)
            p_min = max_line.item(3) #fuer Berechnung des Viskosen durchmessers

            # check if Vectors are defined
            definiert = True
    ############################################################################################################
    #          Vorticity
    if dummy == "v":  # wenn vorticity
        print('Verfahren im Vorticity Modus')

        max_vor, max_line, dummy = find_max(array, xup, xlow, yup, ylow, zup, zlow,
                                            dummy)  # Bestimmung des maxi/minimalen werts
        max_vor, max_line = avg_vorticity(array, max_line, radius)  # Mittelung


        # checken ob Vektoren definiert sind
        try:
            a_1 and a_2 and a_3 and b_1 and b_2 and b_3
        except NameError:
            print('\n Vektoren werden Berechnet. \n')
            definiert = False
        else:
             print('Variablen definiert')
             definiert = True


        print('maximaler vorticity', max_vor, '\ncorresponding line:\n x \t | y\t| z\t| vorticity_X |v_y\t| v_z\n', \
              max_line.item(0), '\t',
              max_line.item(1), '\t',
              max_line.item(2), '\t',
              max_line.item(3), '\t',
              max_line.item(4), '\t',
              max_line.item(5))

        # max_vor -> max vorticity
        # max line: x,y,z,v_x,v_y,v_z
        x_core = max_line.item(0)
        y_core = max_line.item(1)
        z_core = max_line.item(2)

        v_x = max_line.item(3)
        v_y = max_line.item(4)
        v_z = max_line.item(5)
        print('point of max_vor:(x|y|z)', x_core, y_core, z_core)

        # calc vector, alpha: x-axis and vector, ceta: y-axis and vector, eta: z-axis and vecotr
        max_vor = math.sqrt(
            v_x ** 2 + v_y ** 2 + v_z ** 2
        )

        if definiert == False:
            alpha_cos = v_x / max_vor
            beta_cos = v_y / max_vor
            eta_cos = v_z / max_vor
            # defining plane which is described by the vector a and b. a, b, c are orthogonal to each other. c is the vector
            # of the vortexcore
            c_1 = alpha_cos
            c_2 = beta_cos
            c_3 = eta_cos

            a_1, a_2, a_3, b_1, b_2, b_3 = berechnung_Rechteckvektor(c_1, c_2, c_3)

            definiert = True

        elif definiert == True:
            print('!!!Achtung: Es werden die in \"Parameter\" definierten Vektoren genutzt ')


    ##########################################################################
    # # generate points
    #######################################################################

    if definiert == False:
        print('\n Die Benoetigten Parameter fehlen. Bitte direction_of_vortex entsprechende bearbeiten. Beachte die getätigen Ausgaben \n')

    elif definiert == True:
        print('\n Alle Variablen vorhanden, berechne Punkte \n')
        punkte = []
        # 1 start
        x_s = x_core + a_1 - b_1
        y_s = y_core + a_2 - b_2
        z_s = z_core + a_3 - b_3
        # ende
        x_e = x_core + a_1 + b_1
        y_e = y_core + a_2 + b_2
        z_e = z_core + a_3 + b_3

        punkte.append((x_s, y_s,z_s, x_e, y_e, z_e, 1)) # 1 ist line ID

        # 2
        x_s = x_core + a_1 + b_1
        y_s = y_core + a_2 + b_2
        z_s = z_core + a_3 + b_3

        x_e = x_core - a_1 + b_1
        y_e = y_core - a_2 + b_2
        z_e = z_core - a_3 + b_3

        punkte.append((x_s, y_s, z_s, x_e, y_e, z_e, 2))

        # 3
        x_s = x_core - a_1 + b_1
        y_s = y_core - a_2 + b_2
        z_s = z_core - a_3 + b_3

        x_e = x_core - a_1 - b_1
        y_e = y_core - a_2 - b_2
        z_e = z_core - a_3 - b_3

        punkte.append((x_s, y_s, z_s, x_e, y_e, z_e, 3))

        # 4
        x_s = x_core - a_1 - b_1
        y_s = y_core - a_2 - b_2
        z_s = z_core - a_3 - b_3

        x_e = x_core + a_1 - b_1
        y_e = y_core + a_2 - b_2
        z_e = z_core + a_3 - b_3
        punkte.append((x_s, y_s, z_s, x_e, y_e, z_e, 4))

        sampledict(punkte)  # schreibt die Punkte ins Sampledict
    print('\n \n -------------------------end---------------------------------------')