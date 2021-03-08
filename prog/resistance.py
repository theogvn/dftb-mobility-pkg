#!/usr/bin/env python3

import argparse
import numpy as np
import matplotlib.pyplot as plt

# ______________________________________________________________________________
# ------------------------ Display info -------------------------------------- #
print('''
# ============================================================================ #
#  Package for performing resistance calculation with DFTB+                    #
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
# ----------------------- Parsing -------------------------------------------- #

# ----------------------- Setting parser arguments --------------------------- #
parser = argparse.ArgumentParser(
    description='Compute electrical resistivity by integration of'
                ' the product of the average transmission and Fermi-Dirac '
                'distribution derivative.'
                'Integration is compute with the trapeze methode')
parser.add_argument('-T', '--Temperature', dest='temperature',
                    type=float, default=298,
                    help='set temperature in K to compute electon mobility'
                    '(default: 298 K)')
parser.add_argument('-Ef', '--fermi-energy',
                    dest='E_fermi', type=float, default=None,
                    help='fermi energy in eV (is required) | starts integration'
                    ' at this value')
parser.add_argument('-normalizer', dest='normalizer',
                    type=float, default=1,
                    help='set a normalizer for DOS value (default: 1)')
parser.add_argument('-L', dest='length_pl', nargs=2, default=None, type=str,
                    help='''length of the pl along the transport direction
                             syntax : <value> <unit> (default: None)
                             (is required)''')
parser.add_argument('-npl', dest='num_pl', default=None, type=str,
                    help='number of pl in the device (default: None)'
                    ' (is required)')
parser.add_argument('-graph', action='store_true',
                    default='false', dest='graph',
                    help='show graph')
args = parser.parse_args()

# ----------------------- Checking for errors -------------------------------- #
ErrorFlag = False
if args.E_fermi is None:
    print('Error you must set a Fermi energy')
    ErrorFlag = True
if args.normalizer is None:
    print('Error you must set a normalizer')
    ErrorFlag = True
if None in args.length_pl:
    print('''Error you must set a value and unit for the length of the pl along
             the transport direction''')
    ErrorFlag = True
if args.num_pl is None:
    print('Error you must set the number of pl in your device')
    ErrorFlag = True
if ErrorFlag:
    print('-h for help')
    exit()
if args.temperature == 0:
    args.temperature = 1e-10
# ____________________________________________________________________________ #
# ----------------------- setting the ploting space -------------------------- #
plt.style.use('seaborn-whitegrid')
Fig, (ax1, ax2) = plt.subplots(1, 2)

# ____________________________________________________________________________ #
# ----------------------- Loading data --------------------------------------- #

# ----------------------- From Transmisson ----------------------------------- #
transmission = np.loadtxt('transmission.dat')
trans_E = transmission[:, 0]
trans_val = transmission[:, 1]
h = round(abs(trans_E[0]-trans_E[1]), 2)

# ----------------------- Physical parameters -------------------------------- #
normalizer = args.normalizer  # 15.598e-8*8.5961e-8# atm nb   # area in m^2 __ #
E_fermi = args.E_fermi                # Fermis Energy in eV __________________ #
T = args.temperature                  # Temperature in K _____________________ #

L_val = float(args.length_pl[0]) * int(args.num_pl)
L_unit = args.length_pl[1]

k_B = np.float64(8.617333262145e-05)  # Boltzman constant eV/K _______________ #
kT = np.float64(k_B * T)              # saving k_B * T _______________________ #

# ____________________________________________________________________________ #
# ----------------------- Setting the values for the abscice axis ------------ #
xx = []
[xx.append(E-E_fermi) for E in trans_E]

# ____________________________________________________________________________ #
# ----------------------- Computing average transmission --------------------- #
meanTrans = np.mean(trans_val)

# ____________________________________________________________________________ #
# ----------------------- Computing F-D distribution derivative -------------- #
df = []
for E in trans_E:
    expo = np.exp((E-E_fermi)/kT)
    y = expo/(kT*(1+expo)**2)
    df.append(y)

# ----------------------- Setting plot for F-D distribution derivative ------- #
ax1.plot(xx, df, color='red')
ax1.set(ylabel=f'F-D distribution derivative (df/dE) at {round(T)} K',
        xlabel='E - Ef (eV)')

# ____________________________________________________________________________ #
# ----------------------- Computing <T> * df/dE ------------------------------ #
tobeInteger = []
for i in range(len(trans_val)):
    tobeInteger.append(meanTrans * df[i])

# ----------------------- Setting plot for <T> * df/dE ----------------------- #
ax2.plot(xx, tobeInteger, color='purple')
ax2.set(ylabel=r'$\langle\mathcal{T}\rangle\cdot\frac{df}{dE}$',
        xlabel="E - Ef (eV)")

# ____________________________________________________________________________ #
# ----------------------- Integration module using trapeze method ------------ #
s = 0.0
G = 0.0
for i in range(len(tobeInteger)):
    s += tobeInteger[i]
G = (h/2)*(tobeInteger[0] + 2*s + tobeInteger[-1])

# ----------------------- Computing restistance ------------------------------ #
R = 1/G

# ____________________________________________________________________________ #
# ----------------------- Printing resuslt ----------------------------------- #
print('')
print('#'*35, 'RESULTS', '#'*36)
print('Mean transmission : {:.4e}'.format(meanTrans))
print('\nLength      : {:.4e} {}'.format(L_val, L_unit))
print('Resistance  : {:.4e} ohm'.format(R))
print('Conductance : {:.4e} S'.format(G))

FileOutput = open('../dataAnalysisResults/resistance_out.dat', 'a')
FileOutput.write("{:.4e}    {:.4e}    {:.4e}    {:.4e}".format(
    L_val, R, T, meanTrans))
plt.savefig(f'../dataAnalysisResults/transmissionGraph_{L_val}{L_unit}.png')
if args.graph is True:
    plt.show()
# ------------------------------- The End ------------------------------------ #
