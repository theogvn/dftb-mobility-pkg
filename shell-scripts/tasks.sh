#!/bin/bash
echo "starting all tasks"
./setgeom.sh
./run_contact.sh
./run_transport.sh
# ./data_analysis
echo "all tasks are done"
