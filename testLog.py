
"""
Logging for testGimpPDB
"""

from stats import TestStats


import logging

# logger for this plugin.  GimpFu has its own logger
logger = logging.getLogger('testGimpPDB')

# TODO make the level come from the command line or the environment
logger.setLevel(logging.DEBUG)
#logger.setLevel(logging.INFO)
#logger.setLevel(logging.WARNING)

# create file handler which logs even debug messages
#fh = logging.FileHandler('spam.log')
#fh.setLevel(logging.DEBUG)
# create console handler with same log level
ch = logging.StreamHandler()
# possible levels are DEBUG, INFO, WARNING, ERROR, CRITICAL
ch.setLevel(logging.DEBUG)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
#fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
#logger.addHandler(fh)
logger.addHandler(ch)




class TestLog:

    '''
    This logs tests.

    The test plugin may also log for debuggging itself.
    '''

    failSummary = []
    excludedSummary = []

    @classmethod
    def sayEnd(cls, message):
        logger.info("End test: " + message)
        # print white space or marker after a test
        logger.info("^^^^^")


    @classmethod
    def appendToFailSummary(cls, message):
        TestLog.failSummary.append(message)

    @classmethod
    def sayExcluded(cls, didExclude, name, reason=None):
        if didExclude:
            TestStats.sample("excluded")
            cls.say(f"Excluded {name}")
            TestLog.excludedSummary.append(name)
        else:
            TestStats.sample("not excluded")
            cls.say(f"Not excluded {name}")


    @classmethod
    def say(cls, message):
        ''' Info interspersed in standard log (usually console) '''

        logger.info(message)

        ''' wrapper of warnings.warn() that fixpoints the parameters. '''
        # stacklevel=2 means print two lines, including caller's info
        #warnings.warn(message, DeprecationWarning, stacklevel=2)


    @classmethod
    def summarize(cls):
        print("=================================")
        print("testGimpPDB excluded procedures:")
        for line in TestLog.excludedSummary:
            print(line)
        print("=================================")

        if not TestLog.failSummary:
            result = False
        else:
            print("=================================")
            print("testGimpPDB summary of failures:")
            print("")

            for line in TestLog.failSummary:
                print(line)
            print("")
            print("end of testGimpPDB summary of failures.")
            print("=================================")
            print("")
            result = True
        return result
