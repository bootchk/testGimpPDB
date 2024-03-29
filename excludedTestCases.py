"""
Understands what procedures are not easily testable
for various reasons.
"""
from procedureCategory import ProcedureCategory

from testLog import TestLog


def isProcedureInteractivePopup(procName):
    """
    Open dialogs to return a user choice, enter event loop, impeding lights-out testing.

    e.g. gimp-brushes-popup
    """
    # TODO this might be too loose, could omit some procedures that should be tested
    return procName.find("popup") > -1



def isProcedureInteractive(procName):
    """
    Open windows, enter event loop, impeding lights-out testing.

    TODO We *can* test them interactively, optionally.
    Add a control to this plugin.

    Plugins take a parameter runmode, they should respect NONINTERACTIVE.
    But some don't seem to.
    So exclude any that we know open windows.

    TODO not respecting runmode is a bug?
    """
    return procName in (

        "plug-in-animationplay",

        "python-fu-console",
        "plug-in-script-fu-console",
        "plug-in-script-fu-text-console",
        "plug-in-unit-editor",
        "plug-in-screenshot",
        "plug-in-metadata-viewer",
        # Appears in Help>Procedure Browser.
        # Duplicates the Browse button in Python Console???  Duplicate code??
        "plug-in-dbbrowser",
        # Hang, with many Gtk errors
        "plug-in-metadata-editor",
        "plug-in-plug-in-details",

        # Has a GUI.
        # Can't be used NON-INTERACTIVE, since no parameters that specify operations
        "plug-in-gfig",

        # Has a GUI.
        # For complete testing of ScriptFu dialog.
        # Best tested individually outside of testGimpPDB
        # The only SF plugin that uses a GimpParamChannel parameter,
        # which is not currently supported by testGimpPDB (or even by GIMP?)
        "script-fu-test-sphere",

        # Don't call the script-fu interpreter.
        # Not actually a GUI, but it is tested by calling scripts themselves
        "extension-script-fu",

        # opens a dialog that locks GUI
        "plug-in-busy-dialog",
        # same as gimp_clone, but tries to open a dialog?
        "gimp-clone-default",
       )


def isProcedureSpecialCase(procName):
    """
    Special cases.
    Known bad actors, usually they hang or take too long.
    """
    result = procName in (

       # don't test example plugins
       # TODO goat-exercise-python is not canonically named python-fu-goat..
       "goat-exercise-lua",
       "goat-exercise-python",
       "plug-in-goat-exercise-vala",
       "plug-in-goat-exercise-c",

       # temporary procedures, author Itkin
       "gimp-palette-export-text",
       "gimp-palette-export-css",
       "gimp-palette-export-java",
       "gimp-palette-export-php",
       "gimp-palette-export-python",

       # TODO why excluding this?
       "file-print-gtk",
       # help, author ???
       "gimp-help-using-web",
       "gimp-help-using-photography",
       "gimp-help-concepts-usage",
       "gimp-help-using-selections",
       "gimp-help-concepts-paths",
       "gimp-help-using-simpleobjects",
       "gimp-help-using-fileformats",
       "gimp-help-using-docks",
       # Spawn a browser, which could be tested, does not stop test.
       # This one takes a URL parameter, but also throws missing run-mode
       # since we pass runmode to every 'plug-in-'
       "plug-in-web-browser",

       # Bookmarks.  Authors Henrik Brix Andersen or Roman Joost or A. Prokoudine
       # These all use plug-in-web-browser, and Gimp throws "operation not supported"
       # meaning they cannot be called procedurally
       "gimp-online-main-web-site",
       "gimp-online-docs-web-site",
       "gimp-online-developer-web-site",
       "gimp-online-wiki",
       "gimp-online-bugs-features",
       "gimp-online-roadmap",
       # gimp-web

       # Not to be used in production, for GIMP developers only
       "gimp-debug-timer-start",    # should succeed
       "gimp-debug-timer-end",      # fails if no timer started

       #Exclude some pdb management functions.
       #We know they work??
       #For setters, we would need to improvise a proc to mess with.
       #We do test "gimp-pdb-set-data" and "gimp-pdb-get-data" and "gimp-pdb-get-data-size",
       #and e.g. query
       "gimp-pdb-set-proc-attribution",
       "gimp-pdb-get-proc-attribution",
       "gimp-pdb-set-proc-documentation",
       "gimp-pdb-get-proc-documentation",
       "gimp-pdb-set-proc-menu-label",
       "gimp-pdb-get-proc-menu-label",
       "gimp-pdb-add-proc-menu-path",
       "gimp-pdb-get-proc-menu-paths",
       "gimp-pdb-set-proc-icon",
       "gimp-pdb-set-proc-image-types",
       "gimp-pdb-get-proc-image-types",
       "gimp-pdb-get-proc-info",
       "gimp-pdb-get-proc-argument",
       "gimp-pdb-get-proc-return-value",

       "gimp-pdb-set-file-proc-thumbnail-loader",
       "gimp-pdb-set-file-proc-handles-remote",
       "gimp-pdb-set-file-proc-handles-raw",
       "gimp-pdb-set-file-proc-mime-types",
       "gimp-pdb-set-file-proc-priority",
       "gimp-pdb-set-file-proc-save-handler",
       "gimp-pdb-set-file-proc-load-handler",

       # Cannot be called from any plugin, only from app, it crashes
       "script-fu-refresh",

       # Excluded ordinary ScriptFu scripts
       # Hangs, without error messages
       "script-fu-ripply-anim",
       # temporary, crashes in gimp-display-new ???

       # Error: car: argument 1 must be: pair
       # "script-fu-font-map",

       # April 2020 crashing GIMP,
       # scriptfu-WARNING **: 15:04:27.278: PDB procedure returned NULL GIMP object or non-GIMP object.
       # TODO retest, may not be this procedure's fault
       # April 2022, calls plug-in-tile with wrong arg types
       # April 2022 unbound variable foo  ???
       # This requires two layers anyway: foreground with alpha, and background
       #"script-fu-burn-in-anim",

       # Crash gimp core assertion item_is_attached
       # Not reproducible when run by itself? Only crashes when testing all SF scripts
       # ?? GIMP-CRITICAL: file ../gimp/app/gegl/gimp-babl.c: line 1091 (gimp_babl_format): should not be reached
       # "script-fu-drop-shadow",

        # Procedures that take a long time.
        "script-fu-erase-rows",
        "script-fu-erase-nth-rows",

        # Don't use a """ """ above, it ends the tuple???
        )
    TestLog.say(f"Exclude {procName} {result}")
    return result



def shouldTestProcedure(procName):
    """ Decides to NOT test certain procedures.

    Generally, any that prevent lights-out testing.
    Reasons:
    - infinite recursion
    - quitting
    - interactive, open windows and hang test waiting on user Input
    - delete test objects (they should be run last)
    - special cases
    """

    isExcluded =  (
       # procedures that delete improvised resources
       ProcedureCategory.isDeleting(procName)
       # self, infinite recursion
       or (procName in ("python-fu-test-gimp-pdb"))
       # another plugin that tests Gimp, should be called separately
       or (procName in ("python-fu-test-export-import"))
       # is type "PLUGIN" but takes no run mode, a very special case
       or (procName in ("python-fu-eval"))
       # counterproductive to abort gimp
       or (procName in ("gimp-quit"))
       or (isProcedureInteractive(procName))
       or (isProcedureInteractivePopup(procName))
       or (isProcedureSpecialCase(procName))
    )
    return not isExcluded

    # We will test load/save if user requests it.
    # But better to use plugin testGimpExportImport
    # OLD if isLoadSave(procName):





# Not used?
def printPDBError(testStmt):
    """
    testGimpPDB is-a GimpFu plugin, so pdb is defined,
    but get_last_error() is not *in* the PDB, only a method of the pdb.
    Hence we call Gimp.get_pdb().

    PDB is stateful on errors so we can get the last error until we call the next PDB procedure.

    error_str = Gimp.get_pdb().get_last_error()
    print(f"Error string from pdb procedure execution: {error_str}")
    if error_str != 'success':
    """

    """
    GimpFu continues past exceptions on PDB procedures.
    also has already printed an error like "Error: Gimp PDB execution error: <foo>"
    But that mechanism doesn't print the stmt.
    """
    print(f"Error executing {testStmt}")
