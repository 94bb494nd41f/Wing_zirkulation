
from integration_gamma import Einlesen


if __name__ == '__main__':
    print('\n \n IMPORTANT: \'integration_gamma.py\' needs to be in same dir! \n \n')
    plotkind = 'wing'
    c_gamma = Einlesen(plotkind)
    # integration over wing
    h = (c_gamma[len(c_gamma) - 1][0] - c_gamma[0][0]) / float(len(c_gamma) - 1)
    g_wing=0
    for i in range(1, len(c_gamma) - 1):
        g_wing += h * c_gamma[i][1]
    gwinganfang = h * 0.5 * (c_gamma[0][1] + c_gamma[len(c_gamma) - 1][1])
    gwingtotal = g_wing + gwinganfang

    # integration value +Timestep
    #wingtotal_list.append((gwingtotal, int(x_dir)))
    print('integral ueber Fluegel:', gwingtotal, 'schrittweite:', h)

    print('Bitte README lesen')




