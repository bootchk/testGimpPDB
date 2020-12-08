
# Creates list of deprecations of PDB procedures.

# Output of form "foo => bar zed"
# where foo and bar are PDB procedure names and zed is a version of Gimp or "forever".
# Not sorted, use >sort -i deprecations.txt > deprecations.txt

# Input should be always app/pdb/gimp-pdb-compat.c

# lloyd konneker May 2020

# Invoke:
# gawk -f parsePDBCompat.nawk <some prefix>app/pdb/gimp-pdb-compat.c > deprecations.txt


# !!! strip, not replace with space
function stripQuotes(text) {
  gsub("\"", "", text)
  return text
}

function stripTrailingComma(text) {
  gsub(",", "", text)
  return text
}

BEGIN {
  Since = "forever"
}

/since/ {
  # 4th field is a version
  Since = $4
  # OLD
   # print
   # a = $0
   # strip leading stuff
   #result = gensub(/\/\*  deprecations since */, "", "g", a)
   # strip trailing stuff
   #result = gensub(/\*\//, "", "g", result)
   #print result,"*"
   # Since = result
}

# a line {gimp-.*, gimp-.*} is a deprecation
/gimp-.*gimp-/ {

   print stripTrailingComma(stripQuotes($2)), "=>", stripQuotes($3), Since
}
