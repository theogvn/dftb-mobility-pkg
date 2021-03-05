#!/bin/bash
echo "starting transport"
for i in 1 2 5 20 50
do
  cd length$i
  # setup the dftb_in.hsd for Transport
  cat dftb_in.hsd > dftb_in_contacts.hsd # duplicate dftb_in file
  transport_file_editor
  #dftb+ | tee output_transport
  cd ..
done
echo -e "transport done\n"
