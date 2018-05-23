# 3DE4.script.name:    loading cgev
# 3DE4.script.version:    v0.0.2
# 3DE4.script.gui:    Main Window::NOID
# 3DE4.script.comment:    load NOID pipeline
# 3DE4.script.startup: true
# 3DE4.script.hide: true
# v150625 0914
import time

import tde4

import scramble

from PySide import QtGui

from cgev.common import log

from cgev.pipeline.process import IssueReporter

tde4.projectPath = ""
tde4.addFileWidget_copy = tde4.addFileWidget


def addFileWidget_cgev(requester_id, widget_name, label, filter_pattern,
                       default_path=""):
    if default_path != "":
        return tde4.addFileWidget_copy(requester_id, widget_name, label,
                                       filter_pattern, default_path)
    else:
        return tde4.addFileWidget_copy(requester_id, widget_name, label,
                                       filter_pattern, tde4.projectPath)

tde4.addFileWidget = addFileWidget_cgev
tde4.postFileRequester_copy = tde4.postFileRequester


def postFileRequester_cgev(label, filter_pattern, default_path=""):
    if default_path != "":
        return tde4.postFileRequester_copy(label, filter_pattern, default_path)
    else:
        return tde4.postFileRequester_copy(label, filter_pattern,
                                           tde4.projectPath)

tde4.postFileRequester = postFileRequester_cgev


@IssueReporter.reportIssue(raiseException=True)
def tdeStartup():
    log.info('TDE STARTUP')
    stamp = time.time()

    import cgev.pipeline.process.start
    from cgev.tde.prefs import loadPrefs

    loadPrefs()

    tde4.updateGUI()

    log.info('TDE STARTUP DONE (%d seconds)' % (time.time() - stamp))


def tdeExecuteModal(original_function):
    def new_function(*args, **kwargs):
        tde4.postProgressRequesterAndContinue("loading...",
                                              "loading...", 100, "wait...")
        original_function(*args, **kwargs)
        tde4.unpostProgressRequester()
    return new_function

tde4.executeModal = tdeExecuteModal

tdeStartup()

try:
    app = QtGui.QApplication.instance()
    if not app:
        app = QtGui.QApplication(list())
except Exception as e:
    log.error('Failed to load QT Application : {0}', e)
