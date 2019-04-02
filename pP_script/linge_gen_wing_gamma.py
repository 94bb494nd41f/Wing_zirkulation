# -*- coding: utf-8 -*-

import os



def linienlegen(finaleliste, a, b, c):
    punkte = []
    for letztereintrag in finaleliste:
        # min hight: delta Y_min:0.211=sin(10 deg) *1.21921 ->a=0.1059
        # min width delta x min: 1.2192 -> b=0.6096
        # a_max=0.3476

        # fenster hat die Groesse 2a*2b

        c_stern = letztereintrag[1]
        x = letztereintrag[3]
        y = letztereintrag[4]
        z = letztereintrag[5]
        # linie ergibt sich aus start(bspw:y-b) und ende (bspw. x+b)
        punkte.append((x - b, y - a, z - c, x + b, y - a, z + c, str(c_stern) + '_1'))  # senkrechter schnitt fuer chow
        punkte.append((x + b, y - a, z + c, x + b, y + a, z + c, str(c_stern) + '_2'))
        punkte.append((x + b, y + a, z + c, x - b, y + a, z - c, str(c_stern) + '_3'))
        punkte.append((x - b, y + a, z - c, x - b, y - a, z - c, str(c_stern) + '_4'))
    return (punkte)


def sampledict(punkte):
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
        line = i[6]
        line_nummer = line[len(line) - 1]
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
        f.write('c' + str(z_1) + '_' + str(line_nummer) + '\n'
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


if __name__ == '__main__':
    ##############################################################
    # hier werden die zentralen punkte x,y,z definiert
    ##############################################################
    finaleliste = []
    c = 0.91
    # width and hight of fenster
    a = 0.  # total hight=2*ahoehe
    b = 1.8285  # total width =2*b
    c = 0.0
    # central point
    x = -0.6
    y = 0.1
    # z_list wird mit excel und diesem tool erstellt: https://convert.town/column-to-comma-separated-list
    z_list = [0.001, 0.003453634085213, 0.005907268170426, 0.008360902255639, 0.010814536340852, 0.013268170426065,
              0.015721804511278, 0.018175438596491, 0.020629072681704, 0.023082706766917, 0.02553634085213,
              0.027989974937343, 0.030443609022556, 0.03289724310777, 0.035350877192983, 0.037804511278196,
              0.040258145363409, 0.042711779448622, 0.045165413533835, 0.047619047619048, 0.050072681704261,
              0.052526315789474, 0.054979949874687, 0.0574335839599, 0.059887218045113, 0.062340852130326,
              0.064794486215539, 0.067248120300752, 0.069701754385965, 0.072155388471178, 0.074609022556391,
              0.077062656641604, 0.079516290726817, 0.08196992481203, 0.084423558897243, 0.086877192982456,
              0.089330827067669, 0.091784461152882, 0.094238095238095, 0.096691729323308, 0.099145363408521,
              0.101598997493734, 0.104052631578947, 0.10650626566416, 0.108959899749373, 0.111413533834586,
              0.113867167919799, 0.116320802005012, 0.118774436090225, 0.121228070175439, 0.123681704260652,
              0.126135338345865, 0.128588972431078, 0.131042606516291, 0.133496240601504, 0.135949874686717,
              0.13840350877193, 0.140857142857143, 0.143310776942356, 0.145764411027569, 0.148218045112782,
              0.150671679197995, 0.153125313283208, 0.155578947368421, 0.158032581453634, 0.160486215538847,
              0.16293984962406, 0.165393483709273, 0.167847117794486, 0.170300751879699, 0.172754385964912,
              0.175208020050125, 0.177661654135338, 0.180115288220551, 0.182568922305765, 0.185022556390978,
              0.187476190476191, 0.189929824561404, 0.192383458646617, 0.19483709273183, 0.197290726817043,
              0.199744360902256, 0.202197994987469, 0.204651629072682, 0.207105263157895, 0.209558897243108,
              0.212012531328321, 0.214466165413534, 0.216919799498747, 0.21937343358396, 0.221827067669173,
              0.224280701754386, 0.226734335839599, 0.229187969924812, 0.231641604010025, 0.234095238095238,
              0.236548872180451, 0.239002506265664, 0.241456140350877, 0.243909774436091, 0.246363408521304,
              0.248817042606517, 0.25127067669173, 0.253724310776943, 0.256177944862156, 0.258631578947369,
              0.261085213032582, 0.263538847117795, 0.265992481203008, 0.268446115288221, 0.270899749373434,
              0.273353383458647, 0.27580701754386, 0.278260651629073, 0.280714285714286, 0.283167919799499,
              0.285621553884712, 0.288075187969925, 0.290528822055138, 0.292982456140351, 0.295436090225564,
              0.297889724310777, 0.30034335839599, 0.302796992481203, 0.305250626566417, 0.30770426065163,
              0.310157894736843, 0.312611528822056, 0.315065162907269, 0.317518796992482, 0.319972431077695,
              0.322426065162908, 0.324879699248121, 0.327333333333334, 0.329786967418547, 0.33224060150376,
              0.334694235588973, 0.337147869674186, 0.339601503759399, 0.342055137844612, 0.344508771929825,
              0.346962406015038, 0.349416040100251, 0.351869674185464, 0.354323308270677, 0.35677694235589,
              0.359230576441103, 0.361684210526316, 0.36413784461153, 0.366591478696743, 0.369045112781956,
              0.371498746867169, 0.373952380952382, 0.376406015037595, 0.378859649122808, 0.381313283208021,
              0.383766917293234, 0.386220551378447, 0.38867418546366, 0.391127819548873, 0.393581453634086,
              0.396035087719299, 0.398488721804512, 0.400942355889725, 0.403395989974938, 0.405849624060151,
              0.408303258145364, 0.410756892230577, 0.41321052631579, 0.415664160401003, 0.418117794486216,
              0.420571428571429, 0.423025062656643, 0.425478696741856, 0.427932330827069, 0.430385964912282,
              0.432839598997495, 0.435293233082708, 0.437746867167921, 0.440200501253134, 0.442654135338347,
              0.44510776942356, 0.447561403508773, 0.450015037593986, 0.452468671679199, 0.454922305764412,
              0.457375939849625, 0.459829573934838, 0.462283208020051, 0.464736842105264, 0.467190476190477,
              0.46964411027569, 0.472097744360903, 0.474551378446116, 0.477005012531329, 0.479458646616542,
              0.481912280701756, 0.484365914786969, 0.486819548872182, 0.489273182957395, 0.491726817042608,
              0.494180451127821, 0.496634085213034, 0.499087719298247, 0.50154135338346, 0.503994987468673,
              0.506448621553886, 0.508902255639099, 0.511355889724312, 0.513809523809525, 0.516263157894738,
              0.518716791979951, 0.521170426065164, 0.523624060150377, 0.52607769423559, 0.528531328320803,
              0.530984962406016, 0.533438596491229, 0.535892230576442, 0.538345864661655, 0.540799498746869,
              0.543253132832082, 0.545706766917295, 0.548160401002508, 0.550614035087721, 0.553067669172934,
              0.555521303258147, 0.55797493734336, 0.560428571428573, 0.562882205513786, 0.565335839598999,
              0.567789473684212, 0.570243107769425, 0.572696741854638, 0.575150375939851, 0.577604010025064,
              0.580057644110277, 0.58251127819549, 0.584964912280703, 0.587418546365916, 0.589872180451129,
              0.592325814536342, 0.594779448621555, 0.597233082706768, 0.599686716791982, 0.602140350877195,
              0.604593984962408, 0.607047619047621, 0.609501253132834, 0.611954887218047, 0.61440852130326,
              0.616862155388473, 0.619315789473686, 0.621769423558899, 0.624223057644112, 0.626676691729325,
              0.629130325814538, 0.631583959899751, 0.634037593984964, 0.636491228070177, 0.63894486215539,
              0.641398496240603, 0.643852130325816, 0.646305764411029, 0.648759398496242, 0.651213032581455,
              0.653666666666668, 0.656120300751881, 0.658573934837095, 0.661027568922308, 0.663481203007521,
              0.665934837092734, 0.668388471177947, 0.67084210526316, 0.673295739348373, 0.675749373433586,
              0.678203007518799, 0.680656641604012, 0.683110275689225, 0.685563909774438, 0.688017543859651,
              0.690471177944864, 0.692924812030077, 0.69537844611529, 0.697832080200503, 0.700285714285716,
              0.702739348370929, 0.705192982456142, 0.707646616541355, 0.710100250626568, 0.712553884711781,
              0.715007518796994, 0.717461152882207, 0.71991478696742, 0.722368421052634, 0.724822055137847,
              0.72727568922306, 0.729729323308273, 0.732182957393486, 0.734636591478699, 0.737090225563912,
              0.739543859649125, 0.741997493734338, 0.744451127819551, 0.746904761904764, 0.749358395989977,
              0.75181203007519, 0.754265664160403, 0.756719298245616, 0.759172932330829, 0.761626566416042,
              0.764080200501255, 0.766533834586468, 0.768987468671681, 0.771441102756894, 0.773894736842107,
              0.77634837092732, 0.778802005012533, 0.781255639097747, 0.78370927318296, 0.786162907268173,
              0.788616541353386, 0.791070175438599, 0.793523809523812, 0.795977443609025, 0.798431077694238,
              0.800884711779451, 0.803338345864664, 0.805791979949877, 0.80824561403509, 0.810699248120303,
              0.813152882205516, 0.815606516290729, 0.818060150375942, 0.820513784461155, 0.822967418546368,
              0.825421052631581, 0.827874686716794, 0.830328320802007, 0.83278195488722, 0.835235588972433,
              0.837689223057646, 0.840142857142859, 0.842596491228072, 0.845050125313286, 0.847503759398499,
              0.849957393483712, 0.852411027568925, 0.854864661654138, 0.857318295739351, 0.859771929824564,
              0.862225563909777, 0.86467919799499, 0.867132832080203, 0.869586466165416, 0.872040100250629,
              0.874493734335842, 0.876947368421055, 0.879401002506268, 0.881854636591481, 0.884308270676694,
              0.886761904761907, 0.88921553884712, 0.891669172932333, 0.894122807017546, 0.896576441102759,
              0.899030075187972, 0.901483709273185, 0.903937343358399, 0.906390977443612]
    for z in z_list:
        finaleliste.append((480, round(z / c, 2), 5, x, y, z))
    punkte = linienlegen(finaleliste, a, b, c)  # definition der start und endpunkte ANPASSUNG DOMAIN HIER
    sampledict(punkte)  # definierte punkte werden hier in sampledict geschrieben
    cwd = os.getcwd()
