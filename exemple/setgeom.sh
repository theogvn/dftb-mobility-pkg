#!/bin/bash
echo "setting up all geometry"
for i in 1 2 5 20 50 # number of PL in each system
do
  mkdir length$i
  cd length$i
  repeatgen ../*_init.gen 2 3 2 > pl.gen
  buildwire pl.gen 1 $i | tee dftb_in.hsd
  #create the right dftb_in.hsd file
  sed -i '' -e '1,3d' dftb_in.hsd
  (echo -e " Geometry = GenFormat {\n <<< 'Ordered_pl.gen'\n }\n" && cat dftb_in.hsd && cat ../contact_hamiltonian_settings.hsd) > tmp.hsd && mv tmp.hsd dftb_in.hsd
  gen2xyz Ordered_pl.gen
  cd ..
done
echo -e "setgeom done\n"
