import os
import math
import pandas as pd
import numpy as np
from numpy import genfromtxt
# os.system('postProcess -func sampleDict_plane_U')

# norming vector to a length
def length_norm(x, y, z, length):
    f = length/math.sqrt(
        x**2 + y**2 + z**2
    )
    x = f*x
    y = f*y
    z = f*z
    return x, y, z

def Einlesen1(plotkind):
    cwd = os.getcwd()
    print('\n das ist die cwd:\n ', cwd)

    os.chdir(cwd+'/sampleDict_plane_vorticity')
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
    return vorticity_1

def find_max(array):
    # x  y  z  vorticity_x  vorticity_y  vorticity_z ndarray
    v_xyz = array.item((0, 3))+ array.item((0, 4)) + array.item((0, 5))
    for i in array:
        v_xyz_new=i.item(3)**2 + i.item(4)**2 + i.item(5)**2
        if v_xyz <= v_xyz_new:
            max_line=i
    v_xyz_max_real = math.sqrt(max_line.item(3)**2 + max_line.item(4)**2 + max_line.item(5)**2)
    print('maximaler vortexdings', v_xyz_max_real, 'corresponding line:', max_line)
    return v_xyz_max_real, max_line

def sampledict (punkte):
    cwd = os.getcwd()
    print(cwd)
    # os.path.abspath(os.path.join(__file__ ,"../.."))
    # os.chdir('..')
    # os.chdir('..')
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


if __name__ == '__main__':
    array=Einlesen1(plotkind='wing')
    max_vor, max_line=find_max(array)
    # max_vor -> max vorticity
    # max line: x,y,z,v_x,v_y,v_z
    x_core = max_line.item(0)
    y_core = max_line.item(1)
    z_core = max_line.item(2)

    # calc vector, alpha: x-axis and vector, beta: y-axis and vector, eta: z-axis and vecotr
    alpha_cos = max_line.item(3)/max_vor
    beta_cos = max_line.item(4)/max_vor
    eta_cos = max_line.item(5)/max_vor
    # defining plane which is described by the vector a and b. a, b, c are orthogonal to each other. c is the vector
    # of the vortexcore
    c_1 = alpha_cos
    c_2 = beta_cos
    c_3 = eta_cos
    # confine system of equations
    a_1 = c_1
    a_2 = c_2
    b_2 = c_2

    # calculate missing parts of vectors
    a_3 = -(c_1**2 + c_2**2)/c_3
    b_1 = -(c_2**2 + c_3**2)/c_1
    b_3 = -(c_1**2 + c_2**2)/a_3

    # norm vectors so a defined length
    length = 0.25
    a_1, a_2, a_3 = length_norm(a_1, a_2, a_3, length)
    b_1, b_2, b_3 = length_norm(b_1, b_2, b_3, length)
    c_1, c_2, c_3 = length_norm(c_1, c_2, c_3, length)

    punkte = []
    # generate points
    # 1
    x_s = x_core + a_1 - b_1
    y_s = y_core + a_2 - b_2
    z_s = z_core + a_3 - b_3

    x_e = x_core + a_1 + b_1
    y_e = y_core + a_2 + b_2
    z_e = z_core + a_3 + b_3

    punkte.append((x_s, y_s,z_s, x_e, y_e, z_e, 1))

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

    sampledict(punkte)

    print('\n \n -------------------------end---------------------------------------')

