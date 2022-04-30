# parse a list of internal procedures in the pdb

# To compare with libgimp/gimp.def, which is Windows file showing exports

# !!! It parses a json, not a dump

# invoke   nawk -f parseInternalProcs.nawk   pdb2_99.dump.json  >pdb_internal_procs
# sort libgimp/gimp.def > temp2
# comm -3 temp temp2


# lloyd konneker May 2020


# procedure records start with a quoted name at beginning of line
/^"/ {
   # we found a procedure
   # print $0
   # $0 is "foo":
   name = $0

   # remove quotes and trailing colon
   gsub("\"", "", name)
   gsub(":", "", name)
   # translate - to _, since gimp.def has _
   gsub("-", "_", name)

   # buffer name to be output later
   }

/"type"/ {
  # we found a type field
  type = $2
  gsub("\"", "", type)
  if (type == "Internal") {
    # crux: print name of procedures of type Internal
    print name
    }
  }
