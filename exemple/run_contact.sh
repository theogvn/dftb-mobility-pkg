#!/bin/bash
echo "Starting contacts"
for i in 1 2 5 20 50
do
  cd length$i
  echo "  source contact for n°$i"
  #dftb+ | tee output_source.log
  sed -i '' -e 's/contactId = "source"/contactId\ =\ "drain"/g' dftb_in.hsd
  sed -i '' -e 's/\#ReadInitialCharges/ReadInitialCharges/g' dftb_in.hsd
  echo "  drain contact for n°$i"
  #dftb+ | tee output_drain.log
  cd ..
done
echo -e "contacts done\n"
