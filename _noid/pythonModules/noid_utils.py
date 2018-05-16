import os
import time
import datetime


''' createFolder '''
''' -----------------------------------------------------------------------------------------------------------------------------'''
def createFolder(folder) :
    if not os.path.exists(folder) :
        os.makedirs(folder)


''' folderExists '''
''' -----------------------------------------------------------------------------------------------------------------------------'''
def folderExists(folder) :
    return os.path.exists(folder)


''' elapsedTimeStr '''
''' -----------------------------------------------------------------------------------------------------------------------------'''
def elapsedTimeStr(t) :
    dt= datetime.datetime.now()-t
    minutes= dt.seconds/60
    hours= minutes/60

    if dt.days :
        if dt.days == 1 : return "Yesterday"
        return "{} days ago".format(dt.days)

    if hours :
        if hours == 1 : return "1 hour ago"
        return "{} hours ago".format(hours)

    if minutes :
        if minutes == 1 : return "1 minute ago"
        return "{} minutes ago".format(minutes)

    if dt.seconds < 1 : return "< 1 second ago"
    elif dt.seconds == 1 : return "1 second ago"
    return "{} seconds ago".format(dt.seconds)

''' dateTimeStr '''
''' -----------------------------------------------------------------------------------------------------------------------------'''
def dateTimeStr():
    '''
    return a formatted date
    '''
    date = time.strftime("%y%m%d%H%M%S", time.gmtime())  # YYMMDDhhmmss
    return date
