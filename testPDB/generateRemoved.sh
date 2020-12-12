# generateRemoved.sh
sh generateNewDeprecations.sh > newDeprecations.txt
nawk '{ print $1}' undocumentedDeprecations > undocumentedDeprecated.txt
sort -o undocumentedDeprecated.txt undocumentedDeprecated.txt
comm -23  newDeprecations.txt  undocumentedDeprecated.txt
