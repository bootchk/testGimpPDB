
"""
Plugin that tests procedures in Gimp PDB.
By calling them with improvised parameters.

Filtering, i.e. categories of stats:
First, user can choose subsets, "user filtered" or "user unfiltered"
Then, we predefine "excluded" sets that:
 - cannot be tested: interactive
 - or should not be tested: not worth testing, we know they work
Then:
   "called"
   "uncalled": bugs or limitations in this plugin may throw, preventing call,
Then:
   Gimpfu can throw, "GimpFu exception"
   "pass"
   "fail".

Interpreting "fail"
1) Many "fail" mean this plugin doesn't understand semantics,
i.e. improvization is dumb.  E.G. PDB result like: "out of range"
2) PDB result: "execution error" is hard to interpret.
It means that the procedure lacks good error message, does not give specifics.

Stats:
procedures in PDB: count of registered PDB procedures
procedures in PDB = user filtered + user unfiltered
user unfiltered = excluded + unexcluded
unexcluded = called + uncalled
called = pass + fail + GimpFu exception

Test via GimpFu, which affects how this is coded
(relying on GimpFu to promote parameters to a needed type.)

Goals:
- stress test GimpFu
- find crashes in Gimp

Improvised parameters to PDB procedures are arbitrary but not random (yet.)

Tests do NOT test semantics:
- don't know the expected result,
- mostly that a procedure should not crash

FUTURE more fuzzy: pass edge case values
"""

"""
This is the help string:

If you enter into "Test one" box, the other buttons are moot.
Enter the name of a procedure with hyphens i.e. "script-fu-set-cmap"

Repeated tests may clutter GIMP resources and lead to unexplained crashes.
Occasionally delete ~/.config/GIMP/2.99, and restart GIMP (which will create it fresh.)

You can test with iterated improvisation of parameters.
Currently, not in the GUI, instead uncommment in the code:
Cycle.turnOnCycling()

Use a small image for faster testing.
However, that is an edge case: some scripts have meth bugs for small images.

A new image (say all white) can be used, but might be harder to visually interpret results.
Other images may test harder?
If you know a procedure has requirements on the image (rare?)
you may start a test with a suitable image.
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
from params import generateParamString
from drawables import generateDrawableAproposToProc
from testLog import TestLog
from stats import TestStats
from cycle import Cycle



# This plugin is not i18n ???
# gettext.install("gimp30-python", gimp.locale_directory())

# global improvised data assigned by improviseGlobalFooParameters()
fooFile=None
fooVectors=None



def omit(procName):
    TestLog.say(f"Omit: {procName}")
    TestStats.sample("omit")




# TODO form a statement that assigns results, and print results
def formGimpFuStatement(procName, paramString):
    """
    Since this is GimpFu plugin,
    and GimpFu hides runmode,
    any calls to other plugins using the "pdb.name(args)" form will be run-mode noninteractive.
    We have already omitted run mode arg from paramString.

    Alternatively, we can execute using Gimp.get_pdb().run_procedure(),
    and then pass the run mode, e.g. to test interactively
    """
    newName = procName.replace("-", "_")
    result = "pdb." + newName + paramString
    return result


def evalCatchingExceptions(procName, params, image=None, drawable=None):
    # not all pdb procedures use the current image and Drawable
    # They are passed so they are in scope when we eval

    testStmt = formGimpFuStatement(procName, params)

    # Log start of test so we know what test hangs (takes too long time)
    TestLog.say(f"Begin test: {testStmt}")
    TestLog.say(f"Test image: {image.filename}")
    TestLog.say(f"Test drawable: {drawable.name}")
    startTime = time.time()
    try:
        eval(testStmt)

    except Exception as err:
        """
        An exception here can be:
           - fault in Gimpfu itself
           - fault in the string submitted to eval
           - when procedure under test (PUT) is a Python plugin:
               - again fault in GimpFu
               - fault in PUT code (exceptions that the tested procedure throws.
        """
        TestStats.sample("GimpFu exception", str(err) )
        TestLog.say(f"exception in Gimpfu code: {err} for test: {testStmt}")
        return "Exception"

    # get the pdb status, it is a weak form of pass/fail
    # is "success" or something else
    error_str = Gimp.get_pdb().get_last_error()

    # Elapsed time from wall clock.  Process time would only be for this plugin, not the unit under test
    endTime = time.time()

    TestLog.say(f"End call, PDB status: {error_str}, elapsed time: {endTime - startTime}")
    return error_str

'''
OLD
def testProcHavingStringParam(procName):
    # TODO get an appropriate name of an existing object, by parsing the procName
    evalCatchingExceptions(procName, '("foo")')



def testPluginWith3Params():
    # Since in GimpFu, no need to pass run mode
    if len(inParamList)==3:
        TestLog.say(f"test plugin: {procName}")
        evalCatchingExceptions(procName, '(image, drawable)', image, drawable)
    else:
        TestLog.say(f"omit: {procName}")



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
    return result
'''




def callProcWithParams(procName, paramString, image, drawable):
    return evalCatchingExceptions(procName, paramString, image, drawable)



def testGeneralProc(procName, inParamList,  image, drawable):
    """
    Iterate, generating permutations of param values and calling until it succeeds.

    Log the result
    """
    # We can start each test with the same permutation
    # # ??? See cycle.py, we don't really have this: Permute.reset()
    for iteration in range(3): # TODO magic
        TestLog.say(f"Iteration {iteration} of improvising params.")

        paramString = generateParamString(procName, inParamList,  image, drawable)
        # ??? See cycle.py, we don't really have this: Permute.advance()

        if not paramString:
            TestLog.say(f"Not call, could not improvise params: {procName}")
            TestStats.sample("uncalled")
            return
        call_result = callProcWithParams(procName, paramString, image, drawable)
        TestStats.sample("calls")

        if call_result == "success":
            TestStats.sample("pass")
            TestLog.sayEnd("Pass, procedure returned success.")
            return
        elif call_result == "exception":
            # could be exception in GimpFu, not always in GIMP
            TestStats.sample("exception")
            TestLog.sayEnd("Exception")
            return
        else:
            # Failed, but not exception.
            # Brute force fuzz: for various error messages, try again  with permuted parameters
            if call_result.find("out of range") > -1:
                pass
            elif call_result.find("execution error") > -1:
                # often a poor error message from the procedure itself that means: out of range
                pass
            else:
                # a call_result that we don't iterate on
                # Usually one of the parameters that we don't permute is not valid.
                break

        # hack.  If tester does not want to iterate
        # WIP restructure this.
        # For now, just suffer many iterations.
        #if Cycle.shouldCycle():
        #    break

    # Exhausted attempts without passing, or a call_result that we don't iterate on
    TestStats.sample("fail", call_result)
    TestLog.sayEnd("Fail, procedure returned an error.")
    TestLog.appendToFailSummary(f"Call: {procName} params: {paramString}, PDB status: {call_result}")







'''
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
        omit(procName)
'''



# TODO this layer is of little use???
# The test should also test that out params are the proper type?
def testAProc(procName, paramsDict,  image, drawable):
    # We don't care about the out params
    # not len(paramsDict["out"]
    # OLD testProcGivenInParams(procName, paramsDict["in"], image, drawable)
    testGeneralProc(procName, paramsDict["in"], image, drawable)

"""
Return an image and drawable suitable for the tested procedure.
The original image is not touched.
The tested image is a duplicate.
However, the tested drawable may be added, when the tested procedure
wants a type of layer that the original might not have.

!!! Note that the tested layer must be attached to the tested image.
The tested image may have the same name i.e. "[Untitled]" when the original has not been saved.
"""
def getImageCopy(originalImage, procName):
    testImage = pdb.gimp_image_duplicate(originalImage)
    # print(f"Original: {originalImage.filename}, duplicated image: {testImage.filename}")
    testDrawable = generateDrawableAproposToProc(procName, testImage)
    return testImage, testDrawable


def testSingleProc(procName, image, drawable):
    """
    Bracket test with disabling undo
    For a wild procName, i.e. possibly entered by user.

    Image, drawable should be a a copy of known base image, the one the user submitted.
    Note there is no undo() operation in the PDB, to undo the previous test.
    Alternatively, use the same image over and over, but errors will be different?
    """

    # Not testing undo. Disable it for speed.
    pdb.gimp_image_undo_disable(image)

    # pass procName, its dictionary of attributes
    try:
        attributes = ProceduresDB.attributeDictionary(procName)
    except KeyError:
        message = f"Failed to find procedure in local copy of PDB: {procName}, use hyphens?"
        TestLog.say(message)
        pdb.gimp_message(message)
    try:
        testAProc(procName, attributes,  image, drawable)
    except:
        message = f"Failed to test procedure: {procName}, database flaw?"
        TestLog.say(message)
        pdb.gimp_message(message)


    # Caller may delete test image or undo changes made by procedure



def testProcs(image, drawable):
    """ Iterate over procedures, testing them.

    TODO sort so that procedures that delete global test data come last?

    Setup each test in various contexts e.g. a test image.
    """
    testedCount = 0
    TestStats.preload()


    for procName in ProceduresDB.sortedNames():

        # print(procName)
        TestStats.sample("procedures in PDB")

        if UserFilter.userWantsTest(procName):
            TestStats.sample("user unfiltered")

            # Exclude certain procs
            if not shouldTestProcedure(procName):
                TestLog.sayExcluded(True, procName)
            else:
                TestLog.sayExcluded(False, procName)
                #TestStats.sample("unexcluded")
                # Test a copy
                testImage, testDrawable = getImageCopy(image, procName)
                testSingleProc(procName, testImage, testDrawable)

                """
                Delete the copy.
                testGimpPDB itself does not leave any images,
                but the called procedures may create new images and resources (e.g. brush)
                Also, testGimpPDB may leave generated test resources (e.g. brush.)
                """
                pdb.gimp_image_delete(testImage)


            # Temporary
            testedCount += 1
            if testedCount > 100:
                return
        else:
            TestStats.sample("user filtered")






def plugin_main(image, drawable,
      shouldTestScriptFu, shouldTestPythonFu, shouldTestCPlugin,
      shouldTestExportImport, shouldTestOther,
      oneToTest,
      shouldTestTemporary, shouldFuzz):
    """
    """

    """
    Uncomment this to test more stochastically.
    You can also futz with the ranges in cycle.py to test even harder.
    """

    if shouldFuzz:
        Cycle.turnOnCycling()

    # Generate named resources in Gimp
    generateFooGimpData(drawable)

    global fooVectors
    global fooFile
    fooVectors, fooFile = improviseFooParameters(image, drawable)
    assert fooVectors is not None
    # assert these are now in scope for eval()

    # Not testing undo.  Disable it for speed.
    pdb.gimp_image_undo_disable(image)

    # Success on many tested procedures depends on existence of certain things
    # Person running the test should also insure:
    # selection in image
    # strokes in image

    # Choose one
    # ProceduresDB.readFromJSON()
    ProceduresDB.readFromGimp()

    UserFilter.setChoices(shouldTestScriptFu, shouldTestPythonFu, shouldTestCPlugin,
         shouldTestExportImport, shouldTestTemporary, shouldTestOther)

    if oneToTest :
        TestLog.say(f"Testing single procedure: {oneToTest}")
        # !!! Note we are testing on the original image
        testImage, testDrawable = image, drawable
        # Alternatively test a copy: testImage, testDrawable = getImageCopy(image, oneToTest)

        testSingleProc(oneToTest, testImage, testDrawable)

        # to allow for possible GUI to be seen, short delay
        time.sleep(5)  # seconds
        TestLog.summarize()
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
     (PF_TOGGLE, "shouldTestOther", "Other (Internal, etc.) procedures?", 1),
     (PF_STRING, "oneToTest", "Test one:", ""),
     (PF_TOGGLE, "shouldTestTemporary", "Temporary procedures?", 1),
     (PF_TOGGLE, "shouldFuzz", "Fuzz till succeed?", 1),
    ],
    [], # No return value
    plugin_main,
    menu=N_("<Image>/Test"), # menupath
    domain=("gimp30-python", gimp.locale_directory))

TestLog.say(f"Starting")
main()
