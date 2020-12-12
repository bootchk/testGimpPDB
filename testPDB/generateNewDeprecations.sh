# generateNewDeprecations.sh
# output stream is newDeprecations, each line of form "earlyName  => lateName"
comm -3 pdb2_10.txt.sig  pdb2_99.txt.sig | gawk -f parseSignatureChanges.nawk >signaturesChanged.txt
comm -23 pdb2_10.txt.sig  pdb2_99.txt.sig | gawk '{ print $1}' > removedOrSignatureChanged.txt
comm -23 removedOrSignatureChanged.txt signaturesChanged.txt > removedOrDeprecated.txt
gawk -f parsePDBCompat.nawk ~/v*G*/gimp/app/pdb/gimp-pdb-compat.c > deprecations.txt
gawk '{ print $1}' deprecations.txt > deprecated.txt
comm -23 removedOrDeprecated.txt deprecated.txt
