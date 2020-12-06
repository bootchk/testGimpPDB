# parse a dump of the pdb, into PDB procedure signatures

# Input is a text file dump of the pdb.
# You can created such a file:
# Open the GIMP Python Console (Filters>Development>Python>Console)
# >import gimpfu
# >pdb.gimp_procedural_db_dump("filename")
# (seems broken in Gimp 2.8)
# (Since V3 gimp_pdb_dump)
# (Might be a plugin of another name: pdb.dump_to_file("filename"))

# Output is two files:
# 1) a JSON file (many lines per PDB procedure)  to stdout
# 2) a file  (each line a type signature for a PDB procedure), to gimpPDBSignatures.txt

# invoke   nawk -f parsePDBTxt.nawk pdb.txt >pdb.json

# TODO !!! The JSON has an extra comma after the last procedure
# You must manually delete it

# lloyd konneker May 2020




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
  print "initTypeTranslations"

  # Single use GIMP_PDB_COLORARRAY only gimp-palette-get-colors

  # Types in 2.10.20 obsolete in 3.0 ??  Not always convergent
  # GIMP_PDB_INT8 ?
  # GIMP_PDB_INT16 ?

  # Divergent Types
  # Some INT32 => Boolean
  # Some INT32 for run mode => GParamEnum

  # Some GIMP_PDB_INT8 => Boolean
  # Some GIMP_PDB_INT8 => pixelel color?

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
  typeTranslations["GIMP_PDB_DRAWABLE"] = "GParamDrawable"
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

function translateType(type) {
  # assert type is stripQuotes, no leading or trailing whitespace

  # since type is a string, this should print: -GIMP_PDB_STRING-
  #print "-" type "-"

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






# captures signature in associative array <signatures>

function captureTypeSig(type) {
  translatedType = translateType(stripQuotes(type))
  signatures[currentProc] = signatures[currentProc]  " " translatedType
}

function appendToSignature(text) {
  # text must have spaces, else string concatenation will run them together.
  signatures[currentProc] = signatures[currentProc] text
}



function captureProcNameSig(name) {
  name = stripQuotes(name)
  signatures[name] = name " : "
}






# translates to JSON
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

  translatedType = translateType(stripQuotes(type))

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



function closeProc() {
  closeProcJSON()
}

function openParamSet(inOut) {
   # just JSON
   # key, and start list
   print indent "\""  inOut  "\": ["
}

function closeParamSet(shouldAddComma) {
   # signature
   if (shouldAddComma == "true") {
    appendToSignature(" => ")
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

function captureType(shouldPrefixComma) {
  # capture arg type on second following line
  # it is already quoted
  getline; getline
  type = $1

  captureTypeSig(stripQuotes(type))
  captureTypeJSON(type, shouldPrefixComma)
}








BEGIN {
  print "begin"
  initTypeTranslations()
  print typeTranslations["GIMP_PDB_STRING"]

  state = "null"
  openProcSet()
  indent = "   "
}

END {
  closeProcSet()

  # write signatures to separate file
  for (key in signatures) { print signatures[key] > "gimpPDBSignatures.txt" }
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
