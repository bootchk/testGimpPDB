

from testLog import TestLog
from stats import TestStats
from permute import Permute
from procedureCategory import ProcedureCategory




"""
functions to generate param strings for PDB procedures

param strings will be eval'ed
"""



def appendParameter(paramString, parameter):
    # trailing comma will be OK to Python
    result = paramString + parameter + ','
    return result






def generateParamString(procName, inParamList,  image, drawable):
    """
    Generate a string of the form '(foo,)' or '()'
    Returns None for unhandled types (an error)
    """
    # TODO why GParam and GimpParam ??
    result = "("

    # If we are eval'ing in GimpFu context (see elsewhere)
    # omit the first parameter, the run mode
    if ProcedureCategory.doesGimpFuHideRunMode(procName):
        startParam = 1
    else:
        startParam = 0

    for aType in inParamList[startParam:]:
        if aType == "GimpParamString" or aType == "GParamString" :
            # often the name of an item
            result = appendParameter(result, '"foo"')
        elif aType == "GParamInt" :
            result = appendParameter(result, Permute.int())
        elif aType == "GParamUInt" :
            # TODO this does not suffice.  Change gimpfu to cast to GParamUint
            result = appendParameter(result, Permute.int())
        elif aType == "GParamUChar" :
            # GParamUChar usually used as an int-valued enum, often True/False
            # TODO this does not suffice.  Change gimpfu to cast to GParamUint
            result = appendParameter(result, Permute.int())
        elif aType == "GParamDouble" :
            result = appendParameter(result, Permute.float())
        elif aType == "GParamBoolean" :
            # bool is int ??
            result = appendParameter(result, Permute.int())
        elif aType == "GimpParamItem" :
            # Item is superclass of Drawable, etc.
            # Use a convenient one
            result = appendParameter(result, 'drawable')
        elif aType == "GParamEnum" or aType == "GimpParamEnum" :
            # Sometimes run_mode e.g. for Internal  gimp-file-load-layers
            # enums are ints
            # TODO an interactive mode of testing
            # 1 is NONINTERACTIVE
            result = appendParameter(result, '1')
        elif aType == "GimpParamImage" :
            # reference a symbol in Python context at time of eval
            result = appendParameter(result, 'image')
        elif aType == "GimpParamDrawable" :
            # reference a symbol in Python context at time of eval
            result = appendParameter(result, 'drawable')
        elif aType == "GimpParamLayer" :
            # reference a symbol in Python context at time of eval
            # assert drawable is-a Layer
            result = appendParameter(result, 'drawable')
        elif aType == "GimpParamRGB" :
            # a 3-tuple suffices, GimpFu marshals to a Gimp.RGB
            result = appendParameter(result, '(12, 13, 14)')
        elif aType == "GimpParamUnit" :
            # call out to Gimp for a defined constant
            # result = appendParameter(result, 'Gimp.Unit.UNIT_PIXEL')
            # int works?
            # TODO should we permute out of the range of the enum type?
            result = appendParameter(result, Permute.int())
        elif aType == "GimpParamFloatArray" :
            # a 4-tuple often suffices
            # TODO  prefixed with len ?? result = appendParameter(result, '4, (1.0, 1.0, 5.0, 5.0)')
            result = appendParameter(result, '(1.0, 1.0, 5.0, 5.0)')
        elif aType == "GimpParamUInt8Array" :
            # a 4-tuple often suffices e.g. gimp-image-set-colormap
            result = appendParameter(result, '(1, 2, 3, 4)')
        elif aType == "GimpParamVectors" :
            # refer to test harness object
            result = appendParameter(result, 'fooVectors')
        elif aType == "GParamObject" :
            # Usually a GFile
            # refer to test harness object
            result = appendParameter(result, 'fooFile')
        elif aType == "GimpParamObjectArray" :
            """
            Usually an array of Gimp.Drawable.
            The signature of many procedures changed in 3.0 to take: n_drawables, drawables
            Refer to "drawable", since GimpFu will convert to GimpParamDrawableArray automatically.
            However, this depends on the int for n_drawables being 1.
            """
            # assert drawable is a wrapped GimpFu Adapter
            #print(f"Drawable: {drawable}")  # DEBUG unwrapped
            result = appendParameter(result, 'drawable')

        # TODO more types
        # GimpParamParasite
        # GimpParamUInt8Array 10
        # GimpParamChannel 12
        # GimpParamUnit 13
        # GimpParamVectors 23
        # GimpParamDisplay 2
        # GimpParamStringArray
        else:
            # some type we don't handle, omit test
            TestStats.sample("omit for param type")
            TestStats.sample(f"omit for param type: {aType}")

            TestLog.say(f"unhandled type {aType} for {procName}")
            return ""

    result = result + ')'
    # assert result is '()' or of the form '(foo,)'
    return result
