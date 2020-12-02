


"""
Plugin that tests Gimp PDB.

Test calling procedures in PDB.
Some procedures are omitted.

Test via GimpFu

Goals:
- stress test GimpFu
- find crashes in Gimp

Parameters to PDB procedures are arbitrary.

Tests do NOT test semantics:
- don't know the expected result,
- mostly that a procedure should not crash

FUTURE more fuzzy: pass edge case values
"""

import gi
from gi.repository import GObject
from gi.repository import Gio   # Gio.File

import time

from gimpfu import *

from proceduresDB import ProceduresDB
from excludedTestCases import *
from procedureCategory import ProcedureCategory
from userFilter import UserFilter
from testHarness import *
from params import *
from testLog import TestLog
from stats import TestStats



# Plugin is not i18n ???
gettext.install("gimp30-python", gimp.locale_directory)

# global improvised data assigned by generateGlobalFooParameters()
fooFile=None
fooVectors=None


def testProcHavingNoParams(procName):
     evalCatchingExceptions(procName, "()")


def evalCatchingExceptions(procName, params, image=None, drawable=None):
    # not all pdb procedures use the current image and Drawable
    # They are passed so they are in scope when we eval

    """
    form a GimpFu statement.
    Since this is GimpFu plugin, any calls to other plugins
    will be run-mode noninteractive.
    """
    newName = procName.replace("-", "_")
    testStmt = "pdb." + newName + params

    # Log start of test so we know what test hangs (takes too long time)
    TestLog.say(f"Begin test: {testStmt}")
    try:
        eval(testStmt)

    except Exception as err:
        """
        An exception here emanates from faulty Gimpfu code.
        Since Gimpfu catches and proceeds past exceptions while doing
        its own eval of author source.
        That is, GimpFu will log exceptions that the tested procedure throws.
        """
        TestStats.sample("GimpFu exception", str(err) )
        TestLog.say(f"exception in Gimpfu code: {err} for test: {testStmt}")

    # Log end of test, with weak result.
    # get the pdb status, it is a weak form of pass/fail
    error_str = Gimp.get_pdb().get_last_error()
    TestLog.say(f"End test, PDB status: {error_str}")
    if error_str != "success":
        TestStats.sample("fail", error_str)
        TestLog.sayFail(f"Fail: {testStmt}, PDB status: {error_str}")
    else:
        TestStats.sample("pass")

    # TODO stronger form of pass, test effects are as expected


def testProcHavingStringParam(procName):
    # TODO get an appropriate name of an existing object, by parsing the procname
    evalCatchingExceptions(procName, '("foo")')



"""
OLD
def testPluginWith3Params():
    # Since in GimpFu, no need to pass run mode
    if len(inParamList)==3:
        TestLog.say(f"test plugin: {procName}")
        evalCatchingExceptions(procName, '(image, drawable)', image, drawable)
    else:
        TestLog.say(f"omit test plugin: {procName}")
"""



def testProcThatIsPlugin(procName, inParamList, image, drawable):
    """
    Since we are in gimpFu, no need to provide first parameter "mode":
    gimpFu will insert value sorta RUN-NONINTERACTIVE
    """

    # hack off the run mode from formal params
    inParamList.pop(0)

    paramString = generateParamString(procName, inParamList,  image, drawable)
    if paramString:
        evalCatchingExceptions(procName, paramString, image, drawable)
        result = True
    else:
        result = False




def testGeneralProc(procName, inParamList,  image, drawable):

    paramString = generateParamString(procName, inParamList,  image, drawable)
    if paramString:
        evalCatchingExceptions(procName, paramString, image, drawable)
        result = True
    else:
        result = False

    # success means we tested it, not that it succeeded
    return result




def testProcGivenInParams(procName, inParamList,  image, drawable):
    """
    Dispatch on various flavors of procedure signature.
    """
    if not len(inParamList):
        TestLog.say(f"No in params: {procName}")
        testProcHavingNoParams(procName)
    elif (len(inParamList) == 1) and inParamList[0] == "GimpParamString":
        testProcHavingStringParam(procName)
    elif ProcedureCategory.isPlugin(procName):
        testProcThatIsPlugin(procName, inParamList,  image, drawable)
    elif testGeneralProc(procName, inParamList,  image, drawable):
        pass
    else:
        # Omitted: unhandled signature or unhandled parameter type or is interactive
        TestLog.say(f"Omitting test of {procName}")




def testAProc(procName, paramsDict,  image, drawable):
    # We don't care about the out params
    # not len(paramsDict["out"]
    testProcGivenInParams(procName, paramsDict["in"], image, drawable)


def testSingleProc(procName, image, drawable):
    """ For a wild procName, i.e. possibly entered by user """
    """
    So testing is from a known base, test on a copy of original image
    Note there is no undo() operation in the PDB, to undo the previous test.
    Alternatively, use the same image over and over, but errors will be different?
    """
    testImage = pdb.gimp_image_duplicate(image)
    testDrawable = pdb.gimp_image_get_active_drawable(testImage)

    # Not testing undo. Disable it for speed.
    pdb.gimp_image_undo_disable(testImage)

    # pass procName, its dictionary of attributes
    try:
        testAProc(procName, ProceduresDB.attributeDictionary(procName),  testImage, testDrawable)
    except KeyError:
        message = f"Failed to find procedure in PDB: {procName}, use hyphens?"
        TestLog.say(message)
        pdb.gimp_message(message)


    # delete test image or undo changes made by procedure
    pdb.gimp_image_delete(testImage)


def testProcs(image, drawable):
    """ Iterate over procedures, testing them.

    TODO sort so that procedures that delete global test data come last?

    Setup each test in various contexts e.g. a test image.
    """
    testedCount = 0

    for procName in ProceduresDB.sortedNames():

        # print(procName)
        TestStats.sample("procedures in PDB")

        if UserFilter.userWantsTest(procName):

            # Exclude certain procs
            if not shouldTestProcedure(procName):
                TestStats.sample("omit bad actor")
                TestLog.say(f"omit bad actor: {procName}")
                continue
            else:
                TestStats.sample("tested procedures")

            testSingleProc(procName, image, drawable)

            # Temporary
            testedCount += 1
            if testedCount > 100:
                return





def plugin_main(image, drawable,
      shouldTestScriptFu, shouldTestPythonFu, shouldTestCPlugin,
      shouldTestExportImport, shouldTestTemporary, shouldTestOther,
      oneToTest):
    """
    """

    # Generate named resources in Gimp
    generateFooGimpData(drawable)

    # generate named globals for various parameters
    generateGlobalFooParameters(image, drawable)

    # Not testing undo.  Disable it for speed.
    pdb.gimp_image_undo_disable(image)

    # Success on many tested procedures depends on existence of certain things
    # Person running the test should also insure:
    # selection in image
    # strokes in image

    ProceduresDB.read()

    UserFilter.setChoices(shouldTestScriptFu, shouldTestPythonFu, shouldTestCPlugin,
         shouldTestExportImport, shouldTestTemporary, shouldTestOther)

    if oneToTest :
        logger.debug(f"tested {oneToTest}")
        testSingleProc(oneToTest, image, drawable)
        # to allow for possible GUI to be seen, short delay
        time.sleep(5)  # seconds
    else:
        # run set of tests
        testProcs(image, drawable)

        # TODO cleanup any excess test data and stuff generated by tested procedures
        # Otherwise, they accumulate in Gimp settings
        # Alternative, delete gimp config/settings regularly

        TestStats.summarize()
        TestLog.summarize()

        # regex for procedure_type as given from PDBBrowser
        #count, names = pdb.gimp_pdb_query("","","","","","","Internal GIMP procedure")
        # pdb.query_procedures("","","","","","","","","","")
        #print(count)




register(
    "python-fu-test-gimp-pdb",
    "Test Gimp PDB",
    "Test Gimp PDB procedures by calling them with improvised arguments.",
    "Lloyd Konneker",
    "Copyright 2020 Lloyd Konneker",
    "2020",
    N_("Test Gimp PDB..."),  # menu item
    "*", # image types: blank means don't care but no image param
    [(PF_IMAGE,  "i", _("_Image"), None),
     (PF_DRAWABLE, "d", _("_Drawable"), None),
     (PF_TOGGLE, "shouldTestScriptFu", "ScriptFu procedures?", 1),
     (PF_TOGGLE, "shouldTestPythonFu", "PythonFu procedures?", 1),
     (PF_TOGGLE, "shouldTestCPlugin", "C Plugin procedures?", 1),
     (PF_TOGGLE, "shouldTestExportImport", "Export/Import procedures?", 1),
     (PF_TOGGLE, "shouldTestTemporary", "Temporary procedures?", 1),
     (PF_TOGGLE, "shouldTestOther", "Other (Internal, etc.) procedures?", 1),
     (PF_STRING, "oneToTest", "Test one:", ""),
    ],
    [], # No return value
    plugin_main,
    menu=N_("<Image>/Test"), # menupath
    domain=("gimp30-python", gimp.locale_directory))

TestLog.say(f"Starting")
main()
