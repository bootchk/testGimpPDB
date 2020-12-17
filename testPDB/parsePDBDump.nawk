# parse a dump of the pdb, into signatures of two forms: json and plain text

# lloyd konneker May 2020

# invoke   nawk -f parsePDBDump.nawk pdb2_99.dump >pdb2_99.json
# (or gawk: nawk is a synonym usually.  But not the original awk.)

# Input
# A text file dump of the pdb.
# You can created such a file:
# Open the GIMP Python Console (Filters>Development>Python>Console)
# >import gimpfu
# >pdb.gimp_procedural_db_dump("filename")
# (seems broken in Gimp 2.8)
# (Since V3 gimp_pdb_dump)
# (Might be a plugin of another name: pdb.dump_to_file("filename"))

# Output:
# 1) a JSON file (many lines per PDB procedure)  to stdout
# 2) a plain text file  (each line a type signature for a PDB procedure), to gimpPDBSignatures.signatures

# Signature format
# Fields separated by OFS i.e. space
# I.E. somewhat lisp-like, no commas
# name ( type ... ) => type ...
# name, open paren, one or more types, close paren, "=>", one or more types

# Unification/translation:
# For signatures, unifies type terms into canonical type terms
# I.E. translates GIMP v2 terms into v3 terms
# (or even some more unified terms)

# TODO !!! The JSON has an extra comma after the last procedure
# You must manually delete it

# Use cases

# 1) the json can be used to drive test programs
# Alternatively you can query the PDB, but that might be harder

# 2) to compare signatures of different versions of GIMP PDB

# First get a clean install, without custom plugins (which may appear in diffs)
# a. dump the pdb(s) in two versions of GIMP
# b. nawk this script on both versions
# c. Use  command "comm", or "diff"
# >comm pdb2_10.txt.sig pdb2_99.txt.sig | more


# c. OLD sort both signature files NEW this script sorts the signature
# >sort *Sig*2_99* >sorted2_99
# >sort *Sig*2_10* >sorted2_10
# >comm sorted2_99 sorted2_10 | more

# You can use "sed -i s/GParamEnum/GParamInt/" file to do more unification?



# Implementation notes

# Implements a small state machine

# note that both the input and the JSON do not omit empty containers
# e.g. a list of out params always, even if list is empty

# !!! strings in the input have quote characters, be careful to strip as necessary



# !!! strip, not replace with space
function stripQuotes(text) {
  gsub("\"", "", text)
  return text
}



# Translate gimp types v2 to v3
# use associative array


function initTypeTranslations() {
  #print "initTypeTranslations"

  # Single use GIMP_PDB_COLORARRAY only gimp-palette-get-colors

  # Types in 2.10.20 obsolete in 3.0 ??  Not always convergent
  # GIMP_PDB_INT8 ?
  # GIMP_PDB_INT16 ?

  # Divergent Types
  # Some INT32 => Boolean
  # Some INT32 for run mode => GParamEnum

  # Some GIMP_PDB_INT8 => Boolean
  # Some GIMP_PDB_INT8 => pixelel color?
  # Some GIMP_PDB_INT8 => colormap index, i.e. GimpParamUChar

  # Types in 3.0 not present in 2.10.20
  # GParamBoolean (no GIMP_PDB_BOOL in 2.10.20)
  # GParamEnum

  # Not sure this is correct?
  typeTranslations["GIMP_PDB_INT16"]  = "GParamInt"
  # !!! Since divergent, most frequent translation
  typeTranslations["GIMP_PDB_INT32"]  = "GParamInt"
  typeTranslations["GIMP_PDB_FLOAT"]  = "GParamFloat"
  typeTranslations["GIMP_PDB_DOUBLE"] = "GParamDouble"
  typeTranslations["GIMP_PDB_STRING"] = "GParamString"
  # !!! Since divergent, most frequent translation
  typeTranslations["GIMP_PDB_INT8"]    = "GParamBoolean"

  typeTranslations["GIMP_PDB_IMAGE"]    = "GimpParamImage"
  typeTranslations["GIMP_PDB_DRAWABLE"] = "GimpParamDrawable"
  typeTranslations["GIMP_PDB_LAYER"]    = "GimpParamLayer"
  typeTranslations["GIMP_PDB_ITEM"]     = "GimpParamItem"
  typeTranslations["GIMP_PDB_CHANNEL"]  = "GimpParamChannel"

  typeTranslations["GIMP_PDB_INT8ARRAY"]  = "GimpParamInt8Array"
  typeTranslations["GIMP_PDB_UINT8ARRAY"] = "GimpParamUInt8Array"
  typeTranslations["GIMP_PDB_INT32ARRAY"] = "GimpParamInt32Array"
  typeTranslations["GIMP_PDB_FLOATARRAY"] = "GimpParamFloatArray"
  typeTranslations["GIMP_PDB_STRINGARRAY"] = "GimpParamStringArray"
  typeTranslations["GIMP_PDB_COLORARRAY"] = "GimpParamRGBArray"

  typeTranslations["GIMP_PDB_COLOR"]      = "GimpParamRGB"
  typeTranslations["GIMP_PDB_VECTORS"]    = "GimpParamVectors"
  typeTranslations["GIMP_PDB_PARASITE"]   = "GimpParamParasite"
  typeTranslations["GIMP_PDB_SELECTION"]  = "GimpParamSelection"
  typeTranslations["GIMP_PDB_DISPLAY"]    = "GimpParamDisplay"
}

# OLD not used
function initTypeUnifications() {
  #print "initTypeUnifications"
  typeUnifications["GParamInt"]      = "Int"
  typeUnifications["GParamFloat"]    = "Float"
  typeUnifications["GParamString"]   = "String"
  typeUnifications["GParamDouble"]   = "Double"
  typeUnifications["GParamBoolean"]  = "Boolean"

  typeUnifications["GParamDrawable"] = "Drawable"
  typeUnifications["GParamImage"]    = "Image"
}



function translateTypeV2ToV3(type) {
  # assert type is quoted string, no leading or trailing whitespace

  # since type is a string, this should print: -"GIMP_PDB_STRING"-
  #print "-" type "-"

  type = stripQuotes(type)

  if (type in typeTranslations ) {
    translatedType = typeTranslations[type]
    # print type "translated to" translatedType
    return translatedType
    }
  else {
     #print "not translated:" type
     return type
     }
}



# Unify: use more generic, abstract type name
# Types have different names in GIMP and the native language
# This abstracts those differences.

function unifyType(type) {
  # assert type is unquoted string, no leading or trailing whitespace

  # since type is a string, this should print: -"GIMP_PDB_STRING"-
  #print "-" type "-"

  # elide prefixes: GParam, GimpParam
  gsub("GParam", "", type)
  gsub("GimpParam", "", type)


  # unify double type to float
  # GIMP V2 used only ...Float, V3 used  both ...Float and ...Double
  gsub("Double", "Float", type)

  # unify UInt type to Int
  # GIMP V2 used Int types
  # V3 uses UInt
  gsub("UInt", "Int", type)

  type = unifyShortType(type)

  return type
}

# unify range limited int types
function unifyShortType(type) {

  # Choice here, according to what you want to accomplish
  # Unify to Int gives fewer differences
  # Unify to Short shows differences where type is newly clarified
  unifiedType = "Int"
  # unifiedType = "Short"

  # unify an enum type to the underlying type in C
  # GIMP V2 used ...Int, V3 used ...Enum
  gsub("Enum", unifiedType, type)

  # unify Boolean type to Short
  # GIMP V2 used Int with annotations (TRUE or FALSE)
  # V3 used Boolean
  gsub("Boolean",unifiedType, type)

  # unify Unit type to Short
  # GIMP V2 used Int types
  # V3 uses GimpParamUnit i.e. Gimp.Unit
  gsub("Unit", unifiedType, type)

  # unify UChar type to Short
  # GIMP V2 used Int types
  # V3 uses GimpParamUChar
  gsub("UChar", unifiedType, type)

  return type
}

# OLD code

#  if (type in typeUnifications ) {
#    result = typeUnifications[type]
#    # print type "unified to" result
#    }
#  else {
#     #print "not unified:" type
#     result = type
#     }
#  return result







# captures plain text signature in associative array <signatures>

function captureTypeSig(type) {
  # assert type is quoted string like "GimpParamInt" or "GIMP_PDB_INT"

  translatedType = translateTypeV2ToV3(type)

  unifiedType = unifyType(translatedType)

  # append
  # NOT suffix with comma.  Thats conventional notation.  OFS ","
  signatures[currentProc] = signatures[currentProc] OFS unifiedType
}

function appendToSignature(text) {
  # text must have spaces, else string concatenation will run them together.
  signatures[currentProc] = signatures[currentProc] text
}

function captureProcNameSig(name) {
  name = stripQuotes(name)
  # Use conventional notation: parens
  signatures[name] = name OFS "("
}

function closeParamsSig() {
  signatures[currentProc] = signatures[currentProc] OFS ")" OFS "=>"
}
# signature
#if (shouldAddComma == "true") {
#appendToSignature(") => ")
#}


# !!! If you use @ind_str_asc, the sorted order does not quite agree
# with the sorted order of the 'sort' and 'comm' commands
# @val_str_asc does, i.e. sort on the values, not the keys
# The values are the signatures, which contain the keys
# ??? Why don't the sort orders agree ???

function writeSignatureFile() {
  filename = FILENAME ".signatures"

  # traverse sorted by key
  # use predefined scanning order function
  PROCINFO["sorted_in"] = "@val_str_asc"

  for (key in signatures) { print signatures[key] > filename }
}





# captures signature in JSON
# JSON is dict[name] of dict[inParams list[types], outParams list[types]]

function captureProcNameJSON(name) {
  # start new json record
  print name ":"

  # json record is a dictionary of attributes
  # keyed by type: and then dicts of params, keyed by "in" and "out"
  print indent "{"
}

function captureProcTypeJSON(type) {
  # type is quoted string
  print indent "\"type\":" type ","
}

function closeProcJSON() {
  # close dict of params
  # comma between procs
  print indent "},"
  # don't close ProcSet    print "}"
}

# JSON does not allow trailing commas, JSON5 does
function captureTypeJSON(type, shouldPrefixComma) {
  # TODO these are formal param types

  # ??? Do we really want to translate types for the JSON?
  # It will mess up test programs that use the original type strings
  # translatedType = translateTypeV2ToV3(type)
  translatedType = type

  # types are in a comma delimited list
  if (shouldPrefixComma == "true") {
    print indent indent ", " translatedType
  }
  else {
    print indent indent translatedType
  }
}



# chooses or doubles up on format of output
# JSON is written immediately, signature is dumped at END


# signature list has no open and close delimiter, only json
function openProcSet() { print "{" }
function closeProcSet() { print "}" }


function captureProcName(name) {
  captureProcNameSig(name)
  captureProcNameJSON(name)
}

function captureProcType(type) {
  # signature not have proc type
  # print "type is" type
  captureProcTypeJSON(type)
}

function captureType(shouldPrefixComma) {
  # capture arg type on second following line
  # it is already quoted
  getline; getline
  type = $1

  captureTypeSig(type)
  captureTypeJSON(type, shouldPrefixComma)
}


function closeProc() {
  closeProcJSON()
}

function openParamSet(inOut) {
   # just JSON
   # key, and start list
   print indent "\""  inOut  "\": ["
}

function closeParamSet(shouldAddComma) {
  # shouldAddComma means the param set is not empty
  if (shouldAddComma == "true") {
    closeParamsSig()
  }

   # JSON
   # close list
   if (shouldAddComma == "true") {
    print indent indent "],"
   }
   else {
    print indent indent "]"
   }
}










BEGIN {
  # print "begin"
  initTypeTranslations()
  initTypeUnifications()
  # print typeTranslations["GIMP_PDB_STRING"]

  state = "null"
  openProcSet()
  indent = "   "
}

END {
  closeProcSet()
  writeSignatureFile()
}

/\(register-procedure / {
   captureProcName($2)

   # Capture attributes of procedure
   currentProc = stripQuotes($2)

   # procedure type is on the sixth quoted string

   # skip forward five quotes strings
   for (counter = 5; counter >= 0; counter--) {
     # Not checking for read errors.
     getline
     # while first word not starts with quote char
     # print $1
     while ( ! match($1, /\"/) ) {
       getline
     }
   }

   # assert on sixth quoted string


   # capture the whole record, a string with spaces e.g. "Gimp Plug-In"
   captureProcType($0)

   state = "proc"
   next
   }

# match opening left paren (except for the left paren in "(register-procedure" )
# since parens can be anywhere, match beginning of line and whitespace

/^\s*\(/ {
   switch ( state )  {

     # !!! State:null is handled above, matching "(register-procedure"

     case "proc":
        state = "inParamSet"
        openParamSet("in")
        break

     case "inParamSet":
        state = "inParam"
        captureType("false")
        break
      case "outParamSet":
         state = "outParam"
         captureType()
         break

      case "afterInParam":
        state = "inParam"
        captureType("true")
        break
      case "afterOutParam":
        state = "outParam"
        captureType("true")
        break

      case "afterInParamSet":
        openParamSet("out")
        state = "outParamSet"
        break
      case "afterOutParamSet":
        print "Parse error: open paren after out params"
        break

      default:
        print "found open paren in unknown state " state
   }
   next
}

# match closing right paren

/^\s*\)/ {
   switch ( state )  {
     case "proc":
        print "Parse error"
        break

     case "inParam":
        state = "afterInParam"
        break
      case "outParam":
         state = "afterOutParam"
         break

     case "afterInParam":
        state = "afterInParamSet"
        closeParamSet("true")
        break
      case "afterOutParam":
         state = "afterOutParamSet"
         closeParamSet("false")
         break

       case "inParamSet":
         state = "afterInParamSet"
         closeParamSet("true")
         break
       case "outParamSet":
          state = "afterOutParamSet"
          closeParamSet("false")
          break

        case "afterOutParamSet":
        case "afterInParamSet":
          closeProc()
          state = "null"
          break
        default:
          print "found close paren in unknown state: " state
  }
   next
}
