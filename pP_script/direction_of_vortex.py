import os
import math
import pandas as pd
import numpy as np
from numpy import genfromtxt
# os.system('postProcess -func sampleDict_plane_U')

def Einlesen1(plotkind):
    cwd=os.getcwd()
    print('\n das ist die cwd:\n ', cwd)


    os.chdir(cwd+'/sampleDict_plane_vorticity')
    list_timesteps=os.listdir(os.getcwd())
    print('Timesteps', list_timesteps)
    # get latestTimestep
    latest_timestep = max([int(i) for i in list_timesteps])
    print('latest_timestep:', latest_timestep)
    samplewd=os.getcwd()
    #  itterating through every timestep
    for x_dir in list_timesteps[:]:
        #  print('xdir', x_dir)
        os.chdir(samplewd+'/'+str(x_dir))

        ls_data=os.listdir(os.getcwd())
        for filename in ls_data[:]:
            if filename[0] == 'v':
                # x  y  z  vorticity_x  vorticity_y  vorticity_z ndarray
                vorticity_1 = np.genfromtxt(str(filename), skip_header=2, dtype=float)
    return(vorticity_1)

def find_max(array):
    # x  y  z  vorticity_x  vorticity_y  vorticity_z ndarray
    v_xyz = array.item((0, 3))+ array.item((0, 4)) + array.item((0, 5))
    for i in array:
        v_xyz_new=i.item(3)**2 + i.item(4)**2 + i.item(5)**2
        if v_xyz <= v_xyz_new:
            max_line=i
    v_xyz_max_real = math.sqrt(max_line.item(3)**2 + max_line.item(4)**2 + max_line.item(5)**2)

    return(v_xyz_max_real, max_line)

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
    # norm vectors
    norm = max(a_1, a_2, a_3)
    a_1 = a_1/norm
    a_2 = a_2 / norm
    a_3 = a_3 / norm

    norm = max(b_1, b_2, b_3)
    b_1 = b_1 / norm
    b_2 = b_2 / norm
    b_3 = b_3 / norm

    norm = max(c_1, c_2, c_3)
    c_1 = c_1 / norm
    c_2 = c_2 / norm
    c_3 = c_3 / norm

    fenster_a = 0.5
    fenster_b = 0.5
    punkte = []
    # generate points
    # 1
    x_s = x_core + a_1*fenster_a - b_1*fenster_b
    y_s = y_core + a_2*fenster_a - b_2*fenster_b
    z_s = z_core + a_3*fenster_a - b_3*fenster_b

    x_e = x_core + a_1 * fenster_a + b_1 * fenster_b
    y_e = y_core + a_2 * fenster_a + b_2 * fenster_b
    z_e = z_core + a_3 * fenster_a + b_3 * fenster_b

    punkte.append((x_s, y_s ,z_s, x_e, y_e, z_e))

    # 2
    x_s = x_core + a_1 * fenster_a + b_1 * fenster_b
    y_s = y_core + a_2 * fenster_a + b_2 * fenster_b
    z_s = z_core + a_3 * fenster_a + b_3 * fenster_b

    x_e = x_core - a_1 * fenster_a + b_1 * fenster_b
    y_e = y_core - a_2 * fenster_a + b_2 * fenster_b
    z_e = z_core - a_3 * fenster_a + b_3 * fenster_b

    punkte.append((x_s, y_s, z_s, x_e, y_e, z_e))

    # 3
    x_s = x_core - a_1 * fenster_a + b_1 * fenster_b
    y_s = y_core - a_2 * fenster_a + b_2 * fenster_b
    z_s = z_core - a_3 * fenster_a + b_3 * fenster_b

    x_e = x_core - a_1 * fenster_a - b_1 * fenster_b
    y_e = y_core - a_2 * fenster_a - b_2 * fenster_b
    z_e = z_core - a_3 * fenster_a - b_3 * fenster_b

    punkte.append((x_s, y_s, z_s, x_e, y_e, z_e))

    # 4
    x_s = x_core - a_1 * fenster_a - b_1 * fenster_b
    y_s = y_core - a_2 * fenster_a - b_2 * fenster_b
    z_s = z_core - a_3 * fenster_a - b_3 * fenster_b

    x_e = x_core + a_1 * fenster_a - b_1 * fenster_b
    y_e = y_core + a_2 * fenster_a - b_2 * fenster_b
    z_e = z_core + a_3 * fenster_a - b_3 * fenster_b

    punkte.append((x_s, y_s, z_s, x_e, y_e, z_e))










    punkte.append((x - a_1*fenster_a , y - a_2*fenster_a, z - a_3*fenster_a,       x - , y + a, z, str(c_stern) + '_1'))



    punkte.append((x - b, y - a, z, x - b, y + a, z, str(c_stern) + '_1'))
    punkte.append((x - b, y + a, z, x + b, y + a, z, str(c_stern) + '_2'))
    punkte.append((x + b, y + a, z, x + b, y - a, z, str(c_stern) + '_3'))
    punkte.append((x + b, y - a, z, x - b, y - a, z - c, str(c_stern) + '_4'))

    print('end')

