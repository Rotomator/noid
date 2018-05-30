import os
import time
import nuke

import noid_utils as nut
import toBatch


def batch() :
    node= nuke.thisNode()
    nodeName= node["name"].value()
    #print "<"+nodeName+">"

    #node= nuke.toNode(nodeName)
    #if node == None :
    #    return
    #path= os.path.dirname(nuke.filename(node)) +"/rr/" +name +"_rr" +time.strftime('%y%m%d-%H%M%S',time.localtime())+".nk"
    out= node["file"].value()
    print out
    path= "//storc/diskc/_rr/nuke/" +nodeName +"_rr" +nut.dateTimeStr() +".nk"
    print path
    #nut.createFolder(os.path.dirname(path))
    #nuke.scriptSaveAs(path)
    #toBatch.batchNk(scene= path, path= )
