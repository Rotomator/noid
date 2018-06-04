import os
import time
import nuke

import noid_utils as nut
import rrSubmit_Nuke_5


def batch() :
    node= nuke.thisNode()
    #nodeName= node["name"].value()
    #print "<"+nodeName+">"

    #node= nuke.toNode(nodeName)
    #if node == None :
    #    return
    #path= os.path.dirname(nuke.filename(node)) +"/rr/" +name +"_rr" +time.strftime('%y%m%d-%H%M%S',time.localtime())+".nk"
    #path= node["file"].value()
    #print path
    #scene= "//storc/diskc/NOID/_rr/nuke/_rr_" +nodeName +"_" +nut.dateTimeStr() +".nk"
    #print scene
    #write= nodeName

    #nut.createFolder(os.path.dirname(scene))
    #nuke.scriptSaveAs(scene)

    rrSubmit_Nuke_5.rrSubmit_Nuke_5(node)
    #toBatch.batchNk(scene= scene, path= path, write= write, nukeVersion='10.5')
