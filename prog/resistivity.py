#!/usr/bin/env python3
# =============================================================================#
#  Package for performing resistivity calculation from                         #
#  resistance package output                                                   #
#  Made by Bordeaux University Institute of Technology (IUT), France and       #
#  Novosibirsk State University (NSU), Russia                                  #
#  T. Giverne, Bordeaux IUT    N. A. Nebogatikova, NSU                         #
#                                                                              #
#  Optimized for graphene                                                      #
#                                                                              #
#  See the LICENSE file for terms of usage and distribution.                   #
# =============================================================================#

import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

resistance_content = np.loadtxt('resistance_out.dat')
# L_val, R, T, meanTrans
L = resistance_content[:, 0]
R = resistance_content[:, 1]
T = resistance_content[:, 2]
Trans = resistance_content[:, 3]

rho = stats.linregress(L, R)[0]
r_value = stats.linregress(L, R)[2]
sigma = 1/rho


print('R value     : {:.4e}\n'.format(r_value))
print('Resistivity : {:.4e} ohm.m'.format(rho))
print('conductivity: {:.4e} S/m'.format(sigma))

if r_value <= 0.90 & r_value > 0.70:
    print('\n\n')
    print('''/!\\ given the R value you might no be in the presence of a ohmic
          behaviour, hence the results might no be trustworthy /!\\''')
    plt.style.use('seaborn-whitegrid')
    plt.plot(L, R)
    plt.xlabel('Length')
    plt.ylabel('Resistance (ohm)')
    plt.show()
if r_value <= 0.70:
    print('\n\n')
    print('''/!\\ given the R value you are not in the presence of a ohmic
          behaviour, hence the results are not trustworthy /!\\''')
    plt.style.use('seaborn-whitegrid')
    plt.plot(L, R)
    plt.show()
plt.savefig('resistance_length-Graph.png')
