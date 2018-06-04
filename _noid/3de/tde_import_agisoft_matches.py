#
#
# 3DE4.script.name:	Import Agisoft Matches...
#
# 3DE4.script.version:	v0.1
#
# 3DE4.script.gui:	Main Window::3DE4::File::Import
# 3DE4.script.gui:  Main Window::NOID::Scripts:Calib
# 3DE4.script.gui:  Main Window::NOID::Scripts:All

#
#
# 3DE4.script.comment:	Imports Agisoft matches from .dat file
#
#


#
# agisoft translator...

def translateAgiTo3de(inFile, outFile):
    f = open(inFile, 'r')
    o = open(outFile, 'w')

    frameDict = {}
    oFrame = 0
    for line in f:
        line = line.split()
        # If the line starts with '-99' skip
        if line[0] == '-99':
            continue
        # If the line starts with 'C' it's a frame number
        if line[0].startswith('C'):
            oFrame += 1
            frame = oFrame
            frameDict[frame] = {}
            continue
        # frameDict[frame].append(line)
        frameDict[frame][int(line[0])] = [line[1], line[2]]

    frameNum = len(frameDict.keys())
    trackNum = 0

    for frame in frameDict.keys():
        if len(frameDict[frame].keys()) > trackNum:
            trackNum = len(frameDict[frame].keys())

    # Rearrange the information for 3DE
    trackDict = {}
    for trackID in range(trackNum):
        trackDict[trackID] = {}
        for frame in frameDict.keys():
            if trackID in frameDict[frame].keys():
                trackDict[trackID][frame] =  frameDict[frame][trackID]

    # Writing the file
    o.write(str(trackNum)+'\n')

    for trackID in sorted(trackDict.keys()):
        o.write(str('%05d' % (trackID+1))+'\n')
        o.write('0\n')
        trackedFrames = len(trackDict[trackID].keys())
        o.write(str(trackedFrames)+'\n')
        for frame in sorted(trackDict[trackID].keys()):
            o.write(str(frame)+' ')
            o.write(' '.join(trackDict[trackID][frame])+'\n')

    f.close()
    o.close()

#
# main script...

c	= tde4.getCurrentCamera()
pg	= tde4.getCurrentPGroup()
if c!=None and pg!=None:
	frames	= tde4.getCameraNoFrames(c)
	width	= tde4.getCameraImageWidth(c)
	height	= tde4.getCameraImageHeight(c)
	l	= tde4.getCameraLens(c)
	film_aspect	= tde4.getLensFilmAspect(l)

	req	= tde4.createCustomRequester()
	tde4.addFileWidget(req,"file_browser","Filename...","*.dat")
	tde4.addTextFieldWidget(req,"agisoft_fx","Agisoft fx","3664.68")
	tde4.addTextFieldWidget(req,"fx_help","","Enter Agisoft fx value (in Agisoft/Tools/Camera Calibration...)")
	tde4.setWidgetBGColor(req, "fx_help", 0.25, 0.25, 0.25)
	tde4.setWidgetSensitiveFlag(req, "fx_help", 0)
	tde4.addSeparatorWidget(req, "sep" "fx_help")
	tde4.addTextFieldWidget(req,"point_prefix","Add point prefix","agisoft_")
	tde4.setWidgetBGColor(req, "point_prefix", 0.1, 0.1, 0.1)
	tde4.addTextFieldWidget(req,"point_weight","Point weight","0.05")
	tde4.setWidgetBGColor(req, "point_weight", 0.1, 0.1, 0.1)
	tde4.addSeparatorWidget(req, "sep" "Point weight")
	tde4.addTextFieldWidget(req,"color_2d","Point color 2d","Grey")
	tde4.setWidgetBGColor(req, "color_2d", 0, 0, 0)
	tde4.setWidgetSensitiveFlag(req, "color_2d", 0)
	tde4.addTextFieldWidget(req,"color_3d","Point color 2d","Grey")
	tde4.setWidgetBGColor(req, "color_3d", 0, 0, 0)
	tde4.setWidgetSensitiveFlag(req, "color_3d", 0)
	tde4.addSeparatorWidget(req, "sep" "color_3d")
	tde4.addTextFieldWidget(req,"rezX","Image resolution X",str(width))
	tde4.setWidgetBGColor(req, "rezX", 0, 0, 0)
	tde4.setWidgetSensitiveFlag(req, "rezX", 0)
	tde4.addTextFieldWidget(req,"rezY","Image resolution Y",str(height))
	tde4.setWidgetBGColor(req, "rezY", 0, 0, 0)
	tde4.setWidgetSensitiveFlag(req, "rezY", 0)
	tde4.addTextFieldWidget(req,"filmA","Film aspect",str(film_aspect))
	tde4.setWidgetBGColor(req, "filmA", 0, 0, 0)
	tde4.setWidgetSensitiveFlag(req, "filmA", 0)
	tde4.addSeparatorWidget(req, "sep" "Image resolution Y")
	tde4.addToggleWidget(req, "prog_win","Show progress window", 1)
	tde4.addOptionMenuWidget(req,"mode_menu","","Always Create New Points","Replace Existing Points If Possible")
	tde4.setWidgetBGColor(req, "mode_menu", 0.1, 0.1, 0.1)

	ret	= tde4.postCustomRequester(req,"Import Agisoft matches from .dat file...",600,420,"Ok","Cancel")
	if ret==1:
		create_new = tde4.getWidgetValue(req,"mode_menu")
		path	= tde4.getWidgetValue(req,"file_browser")
		outFile	= path.split(".")
		outFile[1]	= "3dedat"
		outFile	= ".".join(outFile)
		agifx	= tde4.getWidgetValue(req,"agisoft_fx")
		point_prefix	= tde4.getWidgetValue(req,"point_prefix")
		point_weight	= tde4.getWidgetValue(req,"point_weight")
		Ox	= float(agifx)/200
		Oy	= Ox/film_aspect
		Rx	= float(tde4.getWidgetValue(req,"rezX"))
		Ry	= float(tde4.getWidgetValue(req,"rezY"))
		prog_win	= int(tde4.getWidgetValue(req,"prog_win"))

		translateAgiTo3de(path, outFile)

		if path!=None:
			#
			# main block...

			f	= open(outFile,"r")
			if not f.closed:
				string	= f.readline()
				n	= int(string)
				poffset	= 25
				np	= n/poffset
				updateFrame	= 1
				if prog_win==1:
					tde4.postProgressRequesterAndContinue("Importing Matches...","Translating finished",n,"")
				for i in range(n):
					name	= f.readline()
					name	= name.strip()
					name	= point_prefix+name
					p	= tde4.findPointByName(pg,name)
					if create_new==1 or p==None: p = tde4.createPoint(pg)
					tde4.setPointName(pg,p,name)
					tde4.setPointWeight(pg,p,float(point_weight))

					string	= f.readline()
					color	= 6
					tde4.setPointColor2D(pg,p,color)
					tde4.setPointColor3D(pg,p,color)

					l	= []
					for j in range(frames): l.append([-1.0,-1.0])
					string	= f.readline()
					n0	= int(string)
					for j in range(n0):
						string	= f.readline()
						line	= string.split()
						x_value	= float(line[1])
						y_value	= float(line[2])
						x_value	= ((x_value+Ox)*Rx)/(Ox*2)
						y_value	= ((y_value+Oy)*Ry)/(Oy*2)
						l[int(line[0])-1] = [x_value/width,y_value/height]
					tde4.setPointPosition2DBlock(pg,p,c,1,l)
					if prog_win==1:
						frame	= i+1
						if frame == updateFrame+np:
							tde4.updateProgressRequester(frame, "Creating 3de track : "+name)
							updateFrame	= frame
				f.close()
			else:
				tde4.postQuestionRequester("Import Agisoft matches from .dat file...","Error, couldn't open file.","Ok")

			# end main block...
			#
else:
	tde4.postQuestionRequester("Import Agisoft matches from .dat file...","There is no current Point Group or Camera.","Ok")




