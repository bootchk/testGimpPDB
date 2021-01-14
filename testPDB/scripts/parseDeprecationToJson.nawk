# Creates json dictionary of deprecations of PDB procedures.

# Input of form: foo => bar
# Output of form: "foo" : "bar",
# where foo and bar are PDB procedure names

# IOW creates text suitable to be cut and pasted into either a JSON or Python dictionary
# !!!! Not sorted on name

# lloyd konneker Jan 2021

# Invoke:
# cd scripts
# gawk -f parseDeprecationToJson.nawk ../sourceData/undocumentedDeprecations.data > ../undocumentDeprecations.json


{
# Input
# $1            $2  $3
# unquotedname  =>  unquotedname2


# Output
# "unquotedname" : "unquotedname2" ,

# Not columnar output
# print "\""   $1  "\" : \""   $3   "\","

# Columnar output
# Concatenate quotes around $1,$3 and then print in columns with : and ,
printf ("%-40s : %-40s ,\n", "\"" $1 "\"", "\"" $3 "\"" )
}
