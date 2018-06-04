#
#
# 3DE4.script.name:	Delete Unused Lens...
#
# 3DE4.script.version:	v0.1
#
# 3DE4.script.gui:	Object Browser::Edit
# 3DE4.script.gui:	Object Browser::Context Menu Lens
# 3DE4.script.gui:	Object Browser::Context Menu Lenses
# 3DE4.script.gui:  Main Window::NOID::Scripts:Lens
# 3DE4.script.gui:  Main Window::NOID::Scripts:All

#
# 3DE4.script.comment:	Delete unused lens...


def deleteUnusedLens():
	camList 	= tde4.getCameraList()
	lensList 	= tde4.getLensList(0)
	lensDel 	= 0
	if len(camList) > 0:
		usedLensList = []
		for cam in camList:
			lens = tde4.getCameraLens(cam)
			if lens not in usedLensList:
				usedLensList.append(lens)
		for currentLens in lensList:
			if currentLens not in usedLensList:
				lensDel = 1
				name = tde4.getLensName(currentLens)
				tde4.deleteLens(currentLens)
				print (name + ' > deleted...')
		if lensDel == 0:
			print ('No unused lens...')
deleteUnusedLens()
