# generateNew.sh
gawk '{ print $3}' undocumentedDeprecations.data > undocumentedDeprecatees
sort -o undocumentedDeprecatees undocumentedDeprecatees
comm -23 added undocumentedDeprecatees > new
