#!/usr/bin/env python
# =============================================================================#
#  Package for performing mobility calculation from DFTB+ output               #
#  Made by Bordeaux University Institute of Technology (IUT), France and       #
#  Novosibirsk State University (NSU), Russia                                  #
#  T. Giverne, Bordeaux IUT    N. A. Nebogatikova, NSU                         #
#                                                                              #
#  Optimized for graphene                                                      #
#                                                                              #
#  See the LICENSE file for terms of usage and distribution.                   #
# =============================================================================#

import argparse
import numpy as np
import matplotlib.pyplot as plt

# ______________________________________________________________________________
# ----------------------- Parsing ----------------------------------------------

# ----------------------- Setting parser args ----------------------------------
parser = argparse.ArgumentParser(
    description='''Compute electon mobility from DOS and electrical resistivity
                by integration of the product of DOS and Fermi-Dirac
                distribution over the conduction band energy (E > E fermi).
                Integration with trapeze methode.''')
parser.add_argument('-T', '--Temperature', dest='temperature',
                    type=float, default=300,
                    help='set temperature in K to compute electon mobility '
                    '(default: 300 K)')
parser.add_argument('-bias', '-volume', '-surface', '-lenght', dest='bias',
                    type=float, default=1,
                    help='bias for normalizing DOS')
parser.add_argument('-Ef', '--fermi-energy',
                    dest='E_fermi', type=float, default=None,
                    help='fermi energy in eV (is required) | starts integration'
                    ' at this value')
parser.add_argument('-rho', '--resistivity', dest='resistivity', type=float,
                    default=None,
                    help='resistivity of the material in ohm.cm (is required)')
parser.add_argument('-verbose', action='store_true',
                    default='false', dest='verbose',
                    help='show additional information')
parser.add_argument('-graph', action='store_true',
                    default='False', dest='graph',
                    help='show graphs')
parser.add_argument('-AllOccupiedStates', action='store_true',
                    default='false', dest='all_occupied_states',
                    help='integer on whole energy and gives the number of '
                    'valence electrons, bias is then ignored')
args = parser.parse_args()

# ----------------------- Checking for errors ----------------------------------
ErrorFlag = False
if args.E_fermi is None:
    print('Error you must set a Fermi energy\
     -h for help')
    ErrorFlag = True
if args.resistivity is None:
    print('Error you must set a resistivity\
      -h for help')
    ErrorFlag = True
if ErrorFlag:
    exit()
if args.temperature == 0:
    args.temperature = 1e-10

# ______________________________________________________________________________
# ----------------------- setting the ploting space ----------------------------
plt.style.use('seaborn-whitegrid')
Fig, (ax1, ax2, ax3) = plt.subplots(1, 3)

# ______________________________________________________________________________
# ----------------------- Loading data -----------------------------------------

# ----------------------- From DOS ---------------------------------------------
dos = np.loadtxt('dos.dat')
dos_E = dos[:, 0]
dos_val = dos[:, 1]
h = round(abs(dos_E[0]-dos_E[1]), 2)

# ----------------------- Physical parameters ----------------------------------
rho = np.float64(args.resistivity)      # Resistivity in ohm.cm ________________
E_fermi = args.E_fermi                  # Fermis Energy in eV __________________
T = args.temperature                    # Temperature in K _____________________

k_B = np.float64(8.617333262145e-05)  # Boltzman constant eV/K _________________
e = np.float64(1.602176634e-19)       # elementary charge in C _________________
kT = np.float64(k_B * T)              # saving k_B * T _________________________

# ______________________________________________________________________________
# ----------------------- Setting the values for the abscice axis --------------
xx = []
[xx.append(E-E_fermi) for E in dos_E]

# ______________________________________________________________________________
# ----------------------- Normalizing DOS values -------------------------------
bias = args.bias  # 1e25
if args.all_occupied_states is not True:
    for i in range(len(dos_val)):
        dos_val[i] = dos_val[i]/bias  # possibly going from e/eV/nm3 -> e/eV/cm3

# ______________________________________________________________________________
# ----------------------- Setting plot for normalized values -------------------
ax1.plot(xx, dos_val)
ax1.set(ylabel='DOS (g(E))', xlabel='E-Ef (eV)')

# ______________________________________________________________________________
# ----------------------- Printing complementary information -------------------
if args.verbose is True:
    print('kT    : ', kT, ' eV')
    print('Ef/kT : ', E_fermi/kT)
    print('step  : ', h)

# ______________________________________________________________________________
# ----------------------- Computing Fermi-Dirac distribution -------------------
f = []
for E in dos_E:
    denominator = 1 + np.exp((E - E_fermi)/kT)
    y = 1/denominator
    f.append(y)

# ----------------------- Setting plot for Fermi-Dirac distribution ------------
ax2.plot(xx, f, color='red')
ax2.set(ylabel='F-D distribution (f(E)) at {} K'.format(round(T)),
        xlabel='E - Ef (eV)',  xlim=[-1, 1])

# ______________________________________________________________________________
# ----------------------- Computing DOS * F-D distribution ---------------------
to_be_integered = []
for i in range(len(dos_val)):
    to_be_integered.append(dos_val[i] * f[i])

# ______________________________________________________________________________
# ----------------------- Integration module using trapeze method --------------
s = 0.0
nChargeCarrier = 0.0
flag = 0
integerded = []
xx2 = []
for i in range(len(to_be_integered)):
    if args.all_occupied_states is True:
        s += to_be_integered[i]
    else:
        if xx[i] == 0:
            flag = i
        if xx[i] > 0:
            s += to_be_integered[i]

nChargeCarrier = 2*((h/2)*(to_be_integered[0] + 2*s + to_be_integered[-1]))
if args.verbose:
    print('lower integration limit: ', dos_E[flag], ' eV')

# ----------------------- Setting plot for DOS * F-D distribution --------------
ax3.plot(xx, to_be_integered, color='purple')
ax3.set(ylabel=r'$g(E)\cdot f(E)$', xlabel="E - Ef (eV)")

# ----------------------- Computing mobility -----------------------------------
mobility = 1/(e * nChargeCarrier * rho)

# ______________________________________________________________________________
# ----------------------- Printing resuslt -------------------------------------
print('\nTemperature :    {:.0f} K '.format(T))
print('Ef          :    {:.2f} eV'.format(E_fermi))
print('Resistivity :    {:.2e} ohm.cm'.format(rho))
print('DOS bias    :    {:.2e}'.format(bias))

if args.all_occupied_states is True:
    print('\nnumber of valence electons in the tested system : {:.0f}'.format(
        nChargeCarrier))
else:
    print('\n######################## RESULTS ################################')
    print('charge carrier density :  {:.4e} (cm-3 ?)'.format(nChargeCarrier))
    print('mobility               :  {:.4e} cm2/(V.s)'.format(mobility))

    FileOutput = open('mobility.dat', 'w')
    FileOutput.write('#carrierDensity    mobility\n')
    FileOutput.write(
        '{:.4e} cm-3    {:.4e} cm2/(V.s)'.format(nChargeCarrier, mobility))

if args.graph is True:
    plt.show()
# ------------------------------- The End --------------------------------------