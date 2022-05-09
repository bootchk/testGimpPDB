

from testLog import TestLog
from stats import TestStats
from cycle import Cycle
from procedureCategory import ProcedureCategory
from specialParams import SpecialParams

from pdb import PDB



"""
functions to generate param strings for PDB procedures

param strings will be eval'ed
"""



def appendParameter(paramString, parameter):
    # trailing comma will be OK to Python
    result = paramString + parameter + ','
    return result


"""
Before 2.99.10,
gimp-pdb-dump was printing the type of the GParam
instead of the inner type
i.e. GimpParamInt instead of gint.
"""

def improviseParmStringForType(aType):
    """
    Return a string that is an example of the given type.

    Some examples change from call to call.
    Some examples are fixed.

    Some examples are literals.
    Some are names of vars that will be in scope when the call is evaluated,
    where a value is improvised into the variable.
    """
    if aType == "gchararray":
        # "GimpParamString" or aType == "GParamString" :
        # often the name of an item but formerly sometimes a filename or dirname
        # and sometimes a quoted numeric like "1" which scriptfu strips of quotes?
        result = Cycle.str()
    elif aType == "gint" or aType == "guint":
        # "GParamInt"
        """
        Special case, to handle multilayer
        """
        result = Cycle.int()
    elif aType == "guchar":
        # "GParamUChar" :
        # GParamUChar usually used as an int-valued enum, often True/False
        # TODO this does not suffice.  Change gimpfu to cast to GParamUint
        result = Cycle.int()
    elif aType == "gdouble":
        # "GParamDouble"
        result = Cycle.float()
    elif aType == "gboolean":
        # GParamBoolean" :
        # bool is int ??
        result = Cycle.int()
    elif aType == "GimpItem":
        # "GimpParamItem" :
        # Item is superclass of Drawable, etc.
        # Use a convenient one, i.e. drawable
        # reference a symbol in Python context at time of eval
        result = 'drawable' # name of a var
        # TODO change name of all improvised vars to fooDrawable
    elif aType == "GimpRunMode":
        # "GParamEnum" or aType == "GimpParamEnum" :
        # Sometimes run_mode e.g. for Internal  gimp-file-load-layers
        # enums are ints
        # TODO an interactive mode of testing
        # 1 is NONINTERACTIVE
        result = '1'
    elif aType == "GimpImage":
        # "GimpParamImage" :
        # reference a symbol in Python context at time of eval
        result = 'image'
    elif aType == "GimpDrawable":
        # "GimpParamDrawable"
        # reference a symbol in Python context at time of eval
        result = 'drawable'
    elif aType == "GimpLayer":
        # "GimpParamLayer" :
        # reference a symbol in Python context at time of eval
        # assert drawable is-a Layer
        result = 'drawable'
    elif aType == "GimpRGB" :
        # "GimpParamRGB"
        # a 3-tuple suffices, GimpFu marshals to a Gimp.RGB
        result = '(12, 13, 14)' # literal
    elif aType == "GimpUnit" :
        # "GimpParamUnit"
        # call out to Gimp for a defined constant
        # result = 'Gimp.Unit.UNIT_PIXEL')
        # int works? The int is often 1, and most enums have 1 in range
        # TODO should we cycle out of the range of the enum type?
        # TODO just always use '1'
        result = Cycle.int()
    elif aType == "GimpFloatArray" :
        # "GimpParamFloatArray"
        # a 4-tuple often suffices
        # TODO  prefixed with len ?? result = '4, (1.0, 1.0, 5.0, 5.0)')
        result = '(1.0, 1.0, 5.0, 5.0)'
    elif aType == "GimpUint8Array" :
        # "GimpParamUInt8Array"
        # a 4-tuple often suffices e.g. gimp-image-set-colormap
        result = '(1, 2, 3, 4)'
    elif aType == "GimpVectors" :
        # "GimpParamVectors"
        # refer to test harness object
        # reference a symbol in Python context at time of eval
        result = 'fooVectors'
    elif aType == "GimpObject" :
        # "GParamObject"
        # Before 2.99.10, usually a GFile
        # Arbitrarily refer to a drawable
        # reference a symbol in Python context at time of eval
        result = 'drawable'
    elif aType == "GFile" :
        # Since 2.99.10, usually a GFile
        # reference a symbol in Python context at time of eval
        # TODO just return a double quoted string for a filename
        result = 'fooFile'
    elif aType == "GimpObjectArray" :
        # "GimpParamObjectArray"
        """
        Usually an array of Gimp.Drawable.
        The signature of many procedures changed in 3.0 to take: n_drawables, drawables
        Refer to "drawable", since GimpFu will convert to GimpParamDrawableArray automatically.
        However, this depends on the int for n_drawables being 1.
        """
        # assert drawable is a wrapped GimpFu Adapter
        #print(f"Drawable: {drawable}")  # DEBUG unwrapped
        result = 'drawable'
    elif aType == "GimpOrientationType" :
        # See above re enums
        result = '1'

    # TODO more types
    # GimpParamParasite
    # GimpParamUInt8Array 10
    # GimpParamChannel 12
    # GimpParamDisplay 2

    # TODO GStrv formerly GimpParamStringArray
    # No PDB procedures that we test take a GStrv

    else:
        # some type we don't handle, omit test
        TestStats.sample("omit for param type")
        TestStats.sample(f"omit for param type: {aType}")

        TestLog.say(f"improviseParmStringForType: unhandled type {aType}")
        return ""

    return result




def generateParamString(procName, inParamList,  image, drawable):
    """
    Generate a string of the form '(foo,)' or '()'
    The string denotes parameters.
    It will be evaled in Python.
    Returns None for unhandled types (an error)
    """

    result = SpecialParams.get(procName)
    if result:
        return result
    # else generate param string dynamically

    # TODO why GParam and GimpParam ??
    result = "("

    # If we are eval'ing in GimpFu context (see elsewhere)
    # omit the first parameter, the run mode
    if ProcedureCategory.doesGimpFuHideRunMode(procName):
        startParam = 1
    else:
        startParam = 0

    argIndex = startParam
    for aType in inParamList[startParam:]:

        """
        Use the default, more likely to succeed.
        Especially for num_drawables param, which we don't want to fuzz.
        """
        improvisedParmString = PDB.default_value_for_procname_arg(procName, argIndex)
        print(improvisedParmString)

        if improvisedParmString == "None":
            improvisedParmString = improviseParmStringForType(aType)

        # trailing comma will be OK to Python
        result = result + improvisedParmString + ','
        argIndex += 1


    result = result + ')'
    # assert result is '()' or of the form '(foo,)'
    return result
