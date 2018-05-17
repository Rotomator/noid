print "NOID pipeline initializing..."


import nuke
import noid


nukeMenu= nuke.menu("Nuke")
noidMenu= nukeMenu.addMenu("NOID")
noidMenu.addCommand("Set Current Task", "")
noidMenu.addSeparator()
noidMenu.addCommand("Increment", "")


import LensDistort.LensDistort_3de