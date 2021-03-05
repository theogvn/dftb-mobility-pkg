#!/bin/bash
echo "starting data analysis"
mkdir dataAnalysisResults
for i in 1 2 5 20 50
do
  cd length$i
  resistance -T 300 -Ef 2.43 -L 0.1855199285e+01 aa -npl $i
  cd ..
done
cd dataAnalysisResults
resistivity
cd ..
echo -e "data analysis done\n"
