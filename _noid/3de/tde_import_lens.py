#
#
# 3DE4.script.name:	Import Lens Keep Width...
#
# 3DE4.script.version:	v0.1
#
# 3DE4.script.gui:	Main Window::3DE4::File::Import
# 3DE4.script.gui:	Object Browser::Context Menu Lens
# 3DE4.script.gui:	Object Browser::Context Menu Lenses
# 3DE4.script.gui:  Main Window::NOID::Scripts:Lens
# 3DE4.script.gui:  Main Window::NOID::Scripts:All
#
# 3DE4.script.comment:	Import Lens Keep Width...
#
#


#
# funktions...

def readCurve(f,curve):
	tde4.deleteAllCurveKeys(curve)
	string	= f.readline()
	n	= int(string)
	for i in range(n):
		string	= f.readline()
		para	= string.split()
		k	= tde4.createCurveKey(curve,[float(para[0]),float(para[1])])
		tde4.setCurveKeyTangent1(curve,k,[float(para[2]),float(para[3])])
		tde4.setCurveKeyTangent2(curve,k,[float(para[4]),float(para[5])])
		tde4.setCurveKeyMode(curve,k,para[6])


#
# main script...

req	= tde4.createCustomRequester()
tde4.addFileWidget(req,"file_browser","Filename...","*.txt")
ls	= tde4.getLensList(1)
if len(ls)==1:
	tde4.addOptionMenuWidget(req,"mode_menu","","Create New Lens","Replace Selected Lens")
else:	tde4.addOptionMenuWidget(req,"mode_menu","","Create New Lens")
ret	= tde4.postCustomRequester(req,"Import Lens...",500,0,"Ok","Cancel")

if ret==1:
	path	= tde4.getWidgetValue(req,"file_browser")
	if path!=None:
		f	= open(path,"r")
		if not f.closed:
			new_lens	= tde4.getWidgetValue(req,"mode_menu")
			if (new_lens==1): l = tde4.createLens()
			else: l = ls[0]

			name	= f.readline()
			name	= name.strip()
			tde4.setLensName(l,name)

			string	= f.readline()
			para	= string.split()
			fl	= float(para[2])
			tde4.setLensFocalLength(l,fl)
			tde4.setLensFilmAspect(l,float(para[3]))
			tde4.setLensLensCenterX(l,float(para[4]))
			tde4.setLensLensCenterY(l,float(para[5]))
			tde4.setLensFBackHeight(l,float(para[1]))
			tde4.setLensFBackWidth(l,float(para[0]))
			tde4.setLensPixelAspect(l,float(para[6]))

			string	= f.readline()
			string	= string.strip()
			if string[0]=='0' or string[0]=='1': tde4.setLensDynamicDistortionFlag(l,int(string))
			else: tde4.setLensDynamicDistortionMode(l,string)

			model	= f.readline()
			model	= model.strip()
			tde4.setLensLDModel(l,model)

			dyndist	= tde4.getLensDynamicDistortionMode(l)
			tde4.setLensDynamicDistortionMode(l,"DISTORTION_STATIC")
			para	= ""
			while para!="<end_of_file>":
				para	= f.readline()
				para	= para.strip()

				if para!="<end_of_file>":
					string	= f.readline()
					string	= string.strip()
					d	= float(string)
					tde4.setLensLDAdjustableParameter(l,para,fl,100.0,d)
					curve	= tde4.getLensLDAdjustableParameterCurve(l,para)
					readCurve(f,curve)
			tde4.setLensDynamicDistortionMode(l,dyndist)

			string	= f.readline()
			string	= string.strip()
			if string=="<begin_2dlut_samples>":
				para	= ""
				while para!="<end_2dlut_samples>":
					para	= f.readline()
					para	= para.strip()

					if para!="<end_2dlut_samples>":
						string	= f.readline()
						string	= string.strip()
						n	= int(string)
						for i in range(n):
							string	= f.readline()
							string	= string.split()
							focal	= float(string[0])
							focus	= float(string[1])
							v	= float(string[2])
							tde4.addLens2DLUTSample(l,para,focal,focus,v)

			f.close
		else:
			tde4.postQuestionRequester("Import Lens...","Error, couldn't open file.","Ok")


tde4.deleteCustomRequester(req)
