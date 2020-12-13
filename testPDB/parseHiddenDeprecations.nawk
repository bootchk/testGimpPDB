# parse a dump of the pdb, into a list of deprecations

# lloyd konneker Dec 2020

# invoke   nawk -f parseHiddenDeprecations.nawk pdb2_99.dump  > hidden.deprecations

# Input
# A text file dump of the pdb.

# Output
# a file, each line of format oldName => newName



# !!! strip, not replace with space
function stripQuotes(text) {
  gsub("\"", "", text)
  return text
}

function stripSingleQuotes(text) {
  gsub("'", "", text)
  return text
}


# There are several kinds of notations
# Not sure where they flow from.
# Possibly some from pdb/groups/foo.pdb, in various inconsistent forms
# Possibly some from app/pdb/gimp-pdb-compat.c

# gimp-vectors-to-selection: second and third line Deprecated: use 'foo'
# script-fu-selection-round  second and third line "This procedure is deprecated! Use 'script-fu-selection-rounded-rectangle' instead."

# gimp-get-icon-theme-dir: fifth line  Deprecated: There is no replacement for this procedure.
# gimp-edit-fill:          fifth line  Deprecated: Use .

/\(register-procedure / {
   deprecated = $2
   # hidden deprecatee is on a following line

   # skip
   getline
   getline
   # assert on third line

   if (match($0, /.*is deprecated/)) {
      deprecatee = $6
      print stripQuotes(deprecated),"=>",stripSingleQuotes(deprecatee)
   }
   if (match($0, /Deprecated: Use/)) {
      deprecatee = $3
      print stripQuotes(deprecated),"=>",stripSingleQuotes(deprecatee)
   }

   # !!! Some on fifth line
   getline
   getline
   #print "Fifth line", $0
   if (match($0, /Deprecated: Use/)) {
      # split on single quote
      if (split($0, array, "''")) {
        # print "Matched appended.", array[1]
        deprecatee = array[1]
        print stripQuotes(deprecated),"=>",stripSingleQuotes(deprecatee)
      }
   }

   next
}
