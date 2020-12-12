# generateKnownDeprecations.sh
gawk -f parsePDBCompat.nawk ~/v*G*/gimp/app/pdb/gimp-pdb-compat.c > known.deprecations
sort -o known.deprecations known.deprecations
gawk '{ print $1}' known.deprecations > knownDeprecated
