"""
Understands what procedures are not easily testable
for various reasons.
"""
from procedureCategory import ProcedureCategory


def isProcedureSpecialCase(procName):
    """
    Special cases.
    Some open windows, impeding lights-out testing.
    We *can* test them interactively, optionally.  TODO

    Others are known bad actors, usually they hang or take too long.
    """
    return procName in (
       # TODO why are these excluded?
       "plug-in-animationplay",
       "python-fu-console",
       # ??? These are opening windows despite run mode NONINTERACTIVE ???
       # TODO explore whether that is a bug
       "plug-in-script-fu-console",
       "plug-in-script-fu-text-console",
       "plug-in-unit-editor",
       "plug-in-screenshot",
       "plug-in-metadata-viewer",
       # Hang, with many Gtk errors
       "plug-in-metadata-editor",
       "plug-in-plug-in-details",
       # Hang, without error messages
       "script-fu-ripply-anim",
       # Don't call the script-fu interpreter.  It has no documented params?
       "extension-script-fu",
       # temporary, crashes in gimp-display-new ???
       "script-fu-font-map",
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
        )



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
       # counterproductive to abort gimp
       or (procName in ("gimp-quit"))
       # opens a dialog that locks GUI
       or (procName in ("plug-in-busy-dialog"))
       # more special cases
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
