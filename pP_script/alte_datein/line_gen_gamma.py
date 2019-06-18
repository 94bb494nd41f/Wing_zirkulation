# -*- coding: utf-8 -*-

import os
from linge_gen_wing_gamma import linienlegen
from linge_gen_wing_gamma import sampledict


if __name__ == '__main__':
    finaleliste=[]
    kind='vortex'
    #chord = 1.2192
    # width and hight of fenster
    a = 0.1  # total hight=2*ahoehe alters y
    c = a  # alters z
    # not needed for calculation of vortex gamma
    b = 0.0  # total width =2*b alters x

    # central point
    y = 0.0
    z = 0.8
    # z_list wird mit excel und diesem tool erstellt: https://convert.town/column-to-comma-separated-list
    #x_list=[0.06,0.0614,0.0628,0.0642,0.0656,0.067,0.0684,0.0698,0.0712,0.0726,0.074,0.0754,0.0768,0.0782,0.0796,0.081,0.0824,0.0838,0.0852,0.0866,0.088,0.0894,0.0908,0.0922,0.0936,0.095,0.0964,0.0978,0.0992,0.1006,0.102,0.1034,0.1048,0.1062,0.1076,0.109,0.1104,0.1118,0.1132,0.1146,0.116,0.1174,0.1188,0.1202,0.1216,0.123,0.1244,0.1258,0.1272,0.1286,0.13,0.1314,0.1328,0.1342,0.1356,0.137,0.1384,0.1398,0.1412,0.1426,0.144,0.1454,0.1468,0.1482,0.1496,0.151,0.1524,0.1538,0.1552,0.1566,0.158,0.1594,0.1608,0.1622,0.1636,0.165,0.1664,0.1678,0.1692,0.1706,0.172,0.1734,0.1748,0.1762,0.1776,0.179,0.1804,0.1818,0.1832,0.1846,0.186,0.1874,0.1888,0.190200000000001,0.191600000000001,0.193000000000001,0.194400000000001,0.195800000000001,0.197200000000001,0.198600000000001,0.200000000000001,0.201400000000001,0.202800000000001,0.204200000000001,0.205600000000001,0.207000000000001,0.208400000000001,0.209800000000001,0.211200000000001,0.212600000000001,0.214000000000001,0.215400000000001,0.216800000000001,0.218200000000001,0.219600000000001,0.221000000000001,0.222400000000001,0.223800000000001,0.225200000000001,0.226600000000001,0.228000000000001,0.229400000000001,0.230800000000001,0.232200000000001,0.233600000000001,0.235000000000001,0.236400000000001,0.237800000000001,0.239200000000001,0.240600000000001,0.242000000000001,0.243400000000001,0.244800000000001,0.246200000000001,0.247600000000001,0.249000000000001,0.250400000000001,0.251800000000001,0.253200000000001,0.254600000000001,0.256000000000001,0.257400000000001,0.258800000000001,0.260200000000001,0.261600000000001,0.263000000000001,0.264400000000001,0.265800000000001,0.267200000000001,0.268600000000001,0.270000000000001,0.271400000000001,0.272800000000001,0.274200000000001,0.275600000000001,0.277000000000001,0.278400000000001,0.279800000000001,0.281200000000001,0.282600000000001,0.284000000000001,0.285400000000001,0.286800000000001,0.288200000000001,0.289600000000001,0.291000000000001,0.292400000000001,0.293800000000001,0.295200000000001,0.296600000000001,0.298000000000001,0.299400000000001,0.300800000000001,0.302200000000001,0.303600000000001,0.305000000000001,0.306400000000001,0.307800000000001,0.309200000000002,0.310600000000002,0.312000000000002,0.313400000000002,0.314800000000002,0.316200000000002,0.317600000000002,0.319000000000002,0.320400000000002,0.321800000000002,0.323200000000002,0.324600000000002,0.326000000000002,0.327400000000002,0.328800000000002,0.330200000000002,0.331600000000002,0.333000000000002,0.334400000000002,0.335800000000002,0.337200000000002,0.338600000000002,0.340000000000002,0.341400000000002,0.342800000000002,0.344200000000002,0.345600000000002,0.347000000000002,0.348400000000002,0.349800000000002,0.351200000000002,0.352600000000002,0.354000000000002,0.355400000000002,0.356800000000002,0.358200000000002,0.359600000000002,0.361000000000002,0.362400000000002,0.363800000000002,0.365200000000002,0.366600000000002,0.368000000000002,0.369400000000002,0.370800000000002,0.372200000000002,0.373600000000002,0.375000000000002,0.376400000000002,0.377800000000002,0.379200000000002,0.380600000000002,0.382000000000002,0.383400000000002,0.384800000000002,0.386200000000002,0.387600000000002,0.389000000000002,0.390400000000002,0.391800000000002,0.393200000000002,0.394600000000002,0.396000000000002,0.397400000000002,0.398800000000002,0.400200000000002,0.401600000000002,0.403000000000002,0.404400000000002,0.405800000000002,0.407200000000002,0.408600000000002,0.410000000000002,0.411400000000002,0.412800000000002,0.414200000000002,0.415600000000002,0.417000000000003,0.418400000000003,0.419800000000002,0.421200000000002,0.422600000000003,0.424000000000003,0.425400000000003,0.426800000000003,0.428200000000003,0.429600000000003,0.431000000000003,0.432400000000003,0.433800000000003,0.435200000000003,0.436600000000003,0.438000000000003,0.439400000000003,0.440800000000003,0.442200000000003,0.443600000000003,0.445000000000003,0.446400000000003,0.447800000000003,0.449200000000003,0.450600000000003,0.452000000000003,0.453400000000003,0.454800000000003,0.456200000000003,0.457600000000003,0.459000000000003,0.460400000000003,0.461800000000003,0.463200000000003,0.464600000000003,0.466000000000003,0.467400000000003,0.468800000000003,0.470200000000003,0.471600000000003,0.473000000000003,0.474400000000003,0.475800000000003,0.477200000000003,0.478600000000003,0.480000000000003]
    x_list=[0.006095, 0.25, 0.5, 1, 1.5]
    for x in x_list:
        finaleliste.append((480, x, 5 , x, y, z))
    punkte=linienlegen(finaleliste, a, b, c, kind)
    sampledict(punkte, kind)
    cwd=os.getcwd()

