#
#
# 3DE4.script.name:	Import Agisoft Calibration...
#
# 3DE4.script.version:	v0.1
#
# 3DE4.script.gui:	Main Window::3DE4::File::Import
# 3DE4.script.gui:	Object Browser::Context Menu Scene
# 3DE4.script.gui:	Object Browser::Context Menu Camera
# 3DE4.script.gui:	Object Browser::Context Menu Cameras
# 3DE4.script.gui:	Object Browser::Context Menu PGroup
# 3DE4.script.gui:  Main Window::NOID::Scripts:Calib
# 3DE4.script.gui:  Main Window::NOID::Scripts:All

#
#
# 3DE4.script.comment:	Import Agisoft Calibration from a .calib file.
#
#

#
# main script...

c	= tde4.getCurrentCamera()
pg	= tde4.getCurrentPGroup()

if c != None and pg != None:
	width	= tde4.getCameraImageWidth(c)
	height	= tde4.getCameraImageHeight(c)
	cn		= tde4.getCameraName(c)
	pgn		= tde4.getPGroupName(pg)
	nf		= tde4.getCameraNoFrames(c)
	cnl		= (cn + ' (' + str(nf) + ' frames)')
	pgt		= tde4.getPGroupType(pg)
	pgi 	= (pgn + ' (' + pgt + ')')
	l		= tde4.getCameraLens(c)
	ln		= tde4.getLensName(l)

	req	= tde4.createCustomRequester()
	tde4.addFileWidget(req,"file_browser","Filename...","*.calib")
	tde4.addSeparatorWidget(req, "sep" "file_browser")
	tde4.addTextFieldWidget(req,"help1","","Sequence :")
	tde4.setWidgetSensitiveFlag(req, "help1", 0)
	tde4.addOptionMenuWidget(req,"importSeq","","Import calibration sequence","Keep current sequence")
	tde4.addTextFieldWidget(req,"activeCam","Current Sequence",cnl)
	tde4.addTextFieldWidget(req,"activePg","Current Point Group",pgi)
	tde4.setWidgetBGColor(req, "activePg", .3, .3, .3)
	tde4.setWidgetSensitiveFlag(req, "activePg", 0)
	tde4.setWidgetBGColor(req, "activeCam", .3, .3, .3)
	tde4.setWidgetSensitiveFlag(req, "activeCam", 0)
	tde4.addTextFieldWidget(req,"activeLens","Current Lens",ln)
	tde4.setWidgetBGColor(req, "activeLens", .3, .3, .3)
	tde4.setWidgetSensitiveFlag(req, "activeLens", 0)
	tde4.addSeparatorWidget(req, "sep" "activeLens")
	tde4.addTextFieldWidget(req,"help2","","Mesh :")
	tde4.setWidgetSensitiveFlag(req, "help2", 0)
	tde4.addOptionMenuWidget(req,"keepMeshs","","Keep existing and import if possible","Delete existing and import if possible")
	tde4.addOptionMenuWidget(req,"modelColor","","White color","Black color")
	tde4.addSeparatorWidget(req, "sep" "modelColor")
	tde4.addTextFieldWidget(req,"help3","","Options :")
	tde4.setWidgetSensitiveFlag(req, "help3", 0)
	tde4.addOptionMenuWidget(req,"deletePoints","","Delete existing calib tracks","Don't delete existing calib tracks")
	tde4.addOptionMenuWidget(req,"groupPoints","","Group points","Don't group points")
	tde4.addOptionMenuWidget(req,"hidePoints","","Hide points","Don't hide points")
	tde4.addOptionMenuWidget(req,"disblePf","","Disable pointGroup postfilter","Don't disable pointGroup postfilter")
	tde4.addOptionMenuWidget(req,"replaceFocal","","Import focal curve","Focal is fixed")

	ret	= tde4.postCustomRequester(req,"Import Agisoft Calib...",900,530,"Ok","Cancel")

	if ret == 1:
		path = tde4.getWidgetValue(req,"file_browser")
		if path!=None:
			dat			= open(path,"r")
			check		= dat.readline().split('\n')[0]
			sceneName	= dat.next().split('\n')[0]
			rezXY		= dat.next().split('\n')[0]
			rezX		= int(rezXY.split(' ')[0])
			rezY		= int(rezXY.split(' ')[1])
			duration	= dat.next().split('\n')[0]
			minF		= int(duration.split(' ')[0])
			maxF		= int(duration.split(' ')[1])
			offset		= int(duration.split(' ')[2])
			duration	= maxF - minF + 1
			seq			= dat.next().split('\n')[0]
			lens		= dat.next().split('\n')[0]
			tracks		= dat.next().split('\n')[0]
			surveys		= dat.next().split('\n')[0]
			focal		= dat.next().split('\n')[0]
			obj			= dat.next().split('\n')[0]

			seqManage = tde4.getWidgetValue(req,"importSeq")
			if seqManage == 1 :
				nf = int(duration)

			if int(duration) <= nf :
				if '#3de_calib' in check:

					#import calib
					if seqManage == 1 :

						#create new lens
						l = tde4.createLens()

						#create sequence
						c			= tde4.createCamera("SEQUENCE")
						tde4.setCameraLens(c,l)
						seqName		= seq.split('/')[-1]
						seqPath 	= seq.replace(seqName, '\ ').split(' ')[0]
						seqPrefix 	= seqName.split('_')[0]
						seqExt 		= seqName.split('.')[-1]
						seqNiceName	= (seqPrefix + '_####.' + seqExt)
						seqPath		= (seqPath + seqNiceName)

						tde4.setCameraPath(c,seqPath)
						tde4.setCameraName(c,sceneName)
						tde4.setCameraSequenceAttr(c,int(minF),int(maxF),1)
						#tde4.setCameraFocalLengthMode(c,"FOCAL_DYNAMIC")

						tde4.setCameraImageWidth(c,rezX)
						tde4.setCameraImageHeight(c,rezY)

						width	= tde4.getCameraImageWidth(c)
						height	= tde4.getCameraImageHeight(c)

					#lens
					def readCurve(f,curve):
						tde4.deleteAllCurveKeys(curve)
						string	= f.readline()
						n		= int(string)
						for i in range(n):
							string	= f.readline()
							para	= string.split()
							k		= tde4.createCurveKey(curve,[float(para[0]),float(para[1])])
							tde4.setCurveKeyTangent1(curve,k,[float(para[2]),float(para[3])])
							tde4.setCurveKeyTangent2(curve,k,[float(para[4]),float(para[5])])
							tde4.setCurveKeyMode(curve,k,para[6])

					f = open(lens,"r")
					if not f.closed:

						name	= f.readline()
						name	= name.strip()
						name	= (sceneName + "_" + name)
						tde4.setLensName(l,name)

						string	= f.readline()
						para	= string.split()
						fl		= float(para[2])
						tde4.setLensFocalLength(l,fl)
						tde4.setLensFilmAspect(l,float(para[3]))
						tde4.setLensLensCenterX(l,float(para[4]))
						tde4.setLensLensCenterY(l,float(para[5]))
						tde4.setLensFBackWidth(l,float(para[0]))
						tde4.setLensPixelAspect(l,float(para[6]))
						tde4.setLensFBackHeight(l,float(para[1]))

						string = f.readline()
						string = string.strip()
						if string[0]=='0' or string[0]=='1': tde4.setLensDynamicDistortionFlag(l,int(string))
						else: tde4.setLensDynamicDistortionMode(l,string)

						model = f.readline()
						model = model.strip()
						tde4.setLensLDModel(l,model)

						dyndist	= tde4.getLensDynamicDistortionMode(l)
						tde4.setLensDynamicDistortionMode(l,"DISTORTION_STATIC")
						para	= ""
						while para != "<end_of_file>":
							para = f.readline()
							para = para.strip()

							if para != "<end_of_file>":
								string = f.readline()
								string = string.strip()
								d = float(string)
								tde4.setLensLDAdjustableParameter(l,para,fl,100.0,d)
								curve = tde4.getLensLDAdjustableParameterCurve(l,para)
								readCurve(f,curve)
						tde4.setLensDynamicDistortionMode(l,dyndist)

						f.close
					else:
						tde4.postQuestionRequester("Import Agisoft Calibration...","Error, couldn't open file.","Ok")

					#focal
					setFl = tde4.getWidgetValue(req,"replaceFocal")
					if setFl == 1:
						def readFocal(f,curve):
							string	= f.readline()
							if string!="":
								n	= int(string)
								tde4.deleteAllCurveKeys(curve)
								for i in range(n):
									string	= f.readline()
									para	= string.split()
									k	= tde4.createCurveKey(curve,[float(para[0]),float(para[1])])
									tde4.setCurveKeyTangent1(curve,k,[float(para[2]),float(para[3])])
									tde4.setCurveKeyTangent2(curve,k,[float(para[4]),float(para[5])])
									tde4.setCurveKeyMode(curve,k,para[6])

						f = open(focal,"r")
						if not f.closed:
							curve = tde4.getCameraZoomCurve(c)
							readFocal(f,curve)
							tde4.setCameraFocalLengthMode(c,"FOCAL_DYNAMIC")
						else:
							tde4.postQuestionRequester("Import Agisoft Calibration...","Error, couldn't open file.","Ok")

					#delete existing calib points
					doDelete = tde4.getWidgetValue(req,"deletePoints")
					if doDelete == 1:
						setList = tde4.getSetList(pg)
						for set in setList:
							setName	= tde4.getSetName(pg,set)
							if 'calib' in setName:
								tde4.deleteSet(pg,set)
						pointList = tde4.getPointList(pg)
						for point in pointList:
							pointName = tde4.getPointName(pg,point)
							if 'agisoft' in pointName:
								tde4.deletePoint(pg,point)

					#surveys
					f	= open(surveys,"r")
					if not f.closed:
						for lines in f:
							a	= lines.split()
							p	= tde4.createPoint(pg)
							tde4.setPointName(pg,p,a[0])
							tde4.setPointSurveyMode(pg,p,"SURVEY_EXACT")
							tde4.setPointSurveyPosition3D(pg,p,[float(a[1]),float(a[2]),float(a[3])])
						f.close()
					else:
						tde4.postQuestionRequester("Import Survey Textfile...","Error, couldn't open file.","Ok")

					# tracks
					f	= open(tracks,"r")
					if not f.closed:
						string	= f.readline()
						n	= int(string)
						for i in range(n):
							name	= f.readline()
							name	= name.strip()
							p		= tde4.findPointByName(pg,name)
							tde4.setPointName(pg,p,name)
							string	= f.readline()
							color	= int(string)
							tde4.setPointColor2D(pg,p,color)
							l = []
							for j in range(nf): l.append([-1.0,-1.0])
							string 	= f.readline()
							n0 		= int(string)
							for j in range(n0):
								string	= f.readline()
								line	= string.split()
								l[int(line[0])-1] = [float(line[1])/width,float(line[2])/height]
							tde4.setPointPosition2DBlock(pg,p,c,1,l)
						f.close()
					else:
						tde4.postQuestionRequester("Import Agisoft Calibration...","Error, couldn't open file.","Ok")

					#group #hide
					doGroup 	= tde4.getWidgetValue(req,"groupPoints")
					hidePoints 	= tde4.getWidgetValue(req,"hidePoints")
					name		= (sceneName + "_calib")
					s			= tde4.createSet(pg)
					tde4.setSetName(pg,s,name)
					toGroup	= tde4.getPointList(pg)
					toHide	= tde4.getPointList(pg)
					for p in toGroup:
						name = tde4.getPointName(pg,p)
						if "agisoft" in name:
							if doGroup == 1:
								tde4.setPointSet(pg,p,s)
							if hidePoints == 1:
								tde4.setPointHideFlag(pg,p,1)

					#postfilter
					setPf = tde4.getWidgetValue(req,"disblePf")
					if setPf == 1:
						tde4.setPGroupPostfilterMode(pg,"POSTFILTER_OFF")

					#obj
					if obj != 'NoObj':
						meshClean = tde4.getWidgetValue(req,"keepMeshs")
						if meshClean == 2:
							meshList = tde4.get3DModelList(pg)
							if meshList >=1:
								for current in meshList:
									tde4.delete3DModel(pg,current)
						mC = tde4.getWidgetValue(req,"modelColor")
						if mC == 2:
							mC = 0
						meshName = obj.split('/')[-1].split('.')[0]
						newMesh = tde4.create3DModel(pg,10000)
						tde4.set3DModelName(pg,newMesh,meshName)
						tde4.importOBJ3DModel(pg,newMesh,obj)
						tde4.set3DModelColor(pg,newMesh,mC,mC,mC,0.1)
						tde4.set3DModelReferenceFlag(pg,newMesh,1)
						tde4.set3DModelSurveyFlag(pg,newMesh,1)
						tde4.set3DModelRenderingFlags(pg,newMesh,0,1,0)

					tde4.setCurrentCamera(c)
					tde4.updateGUI()

					#confirm window
					pgName = (sceneName + '_pgroup#1')
					tde4.setPGroupName(pg,pgName)
					pgn	= tde4.getPGroupName(pg)

					if setPf == 1:
						tde4.postQuestionRequester("Import Agisoft Calibration...","Postfilter of " + pgn + " is disabled\nExecute Calc / Calc All From Scratch...","Ok")
					else:
						tde4.postQuestionRequester("Import Agisoft Calibration...","Execute Calc / Calc All From Scratch...","Ok")

				else:
					tde4.postQuestionRequester("Import Agisoft Calibration...","Error, Not a calibration file.","Ok")
			else:
				tde4.postQuestionRequester("Import Agisoft Calibration...","Error, Too much frames in selected calibration file.","Ok")
		else:
			tde4.postQuestionRequester("Import Agisoft Calibration...","Error, couldn't open file.","Ok")
else:
	tde4.postQuestionRequester("Import Agisoft Calibration...","There is no current Point Group, or no Camera.","Ok")
