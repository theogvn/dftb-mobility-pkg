#!/usr/bin/env python3

import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

# ____________________________________________________________________________ #
# ------------------------------ display info -------------------------------- #
print('''
# ============================================================================ #
#  Package for performing resistivity calculation with DFTB+ and results of    #
#  resistance package output                                                   #
#  Developed by                                                                #
#    T. Giverne, Bordeaux University Institute of Technology, _France_         #
#    N. A. Nebogatikova**, Novosibirsk State University (NSU), _Russia_        #
#                                                                              #
#  Optimized for graphene                                                      #
#                                                                              #
#  See the LICENSE file for terms of usage and distribution.                   #
#  https://github.com/theogvn/dftb-mobility-pkg                                #
# ============================================================================ #

''')

# ____________________________________________________________________________ #
# ------------------------------ loading data ------------------------------- #
resistance_content = np.loadtxt('resistance_out.dat')
# L_val, R, T, meanTrans
L = resistance_content[:, 0]
R = resistance_content[:, 1]
T = resistance_content[:, 2]
Trans = resistance_content[:, 3]

regress = stats.linregress(L, R)  # (L, R)[0]
print('regress: ', regress)
rho = regress[0]
r_value = regress[2]
sigma = 1/rho

# ____________________________________________________________________________ #
# ------------------------------ display results ----------------------------- #
print('R value     : {:.4}\n'.format(r_value))
print('Resistivity : {:.4e} ohm.m'.format(rho))
print('conductivity: {:.4e} S/m'.format(sigma))

if r_value <= 0.90 and r_value > 0.70:
    print('\n\n')
    print('''/!\\ given the R value you might no be in the presence of a ohmic
          behaviour, hence the results might no be trustworthy /!\\''')
    plt.style.use('seaborn-whitegrid')
    plt.plot(L, R, '+', markeredgewidth=1.6, markersize=8)
    plt.xlabel('Length')
    plt.ylabel('Resistance (ohm)')

    # plotting linregress
    x1, y1 = min(L), min(L)*rho + regress[1]
    x2, y2 = max(L), max(L)*rho + regress[1]
    plt.axline((x1, y1), (x2, y2), ls='--', color='gray', lw=0.8,
               label="linear regression")
    plt.legend()

if r_value <= 0.70:
    print('\n\n')
    print('''/!\\ given the R value you are not in the presence of a ohmic
    behaviour, hence the results are not trustworthy /!\\''')
    plt.style.use('seaborn-whitegrid')
    plt.plot(L, R)
    plt.show()
plt.savefig('resistance_length-Graph.png')
