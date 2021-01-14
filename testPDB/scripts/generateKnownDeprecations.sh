# generateKnownDeprecations.sh
gawk -f parsePDBCompat.nawk ~/v*G*/gimp/app/pdb/gimp-pdb-compat.c | sort > known.deprecations
gawk '{ print $1}' known.deprecations > knownDeprecated
gawk '{ print $3}' known.deprecations | sort | uniq > knownDeprecatees
