# parse a comm of the pdb, finding procedures possibly newly deprecated

# lloyd konneker May 2020

# invoke   gawk -f parseNewDeprecations.nawk col1.txt >signatureChanges.txt

# invocation as a pipe:
# comm -23 pdb2_10.txt.sig pdb2_99.txt.sig | gawk -f parseNewDeprecations.nawk >signatureChanges.txt

# Input
# A text file from running comm on two .txt.sig getting the first column
# (the signatures that are in first version and not in second version.)
# comm -23 pdb2_10.txt.sig pdb2_99.txt.sig > temp.txt

# Output:
# a txt file
# where each line is one name of a procedure not in PDB V3
# and not already documented as deprecated in app/pdb/gimp-pdb-compat.c

# Use case
# To produce a document describing possible new deprecations

# !!! Some may have replacements that are not documented.
# Requires human post-processing



BEGIN {
  # read known deprecations into an associative array
  while ((getline  < "deprecations.txt") > 0) {
     # keyed by old name, value the new name
     # $2 is "=>" in deprecations.txt
     deprecations[$1] = $3
  }
}


# performed on every line
{
  if ( $1 in deprecations ) {
     # known deprecation
     print $1, "=>", deprecations[$1]
  }
  else {
     print "New dep", $1
  }
}
