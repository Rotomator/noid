#
#
# 3DE4.script.name:	Duplicate Selected Lens Keep Width...
#
# 3DE4.script.version:	v0.1
#
# 3DE4.script.gui:	Object Browser::Edit
# 3DE4.script.gui:	Object Browser::Context Menu Lens
# 3DE4.script.gui:	Object Browser::Context Menu Lenses
# 3DE4.script.gui:  Main Window::NOID::Scripts:Lens
# 3DE4.script.gui:  Main Window::NOID::Scripts:All

#
# 3DE4.script.comment:	Creates a copy of the currently selected lens.

# Update :
#	New name = name + '_1' and increment
#	Set film width fixed
#	Duplicate multiple lens
#

ls	= tde4.getLensList(1)

if len(ls) >= 1:
	for l0 in ls:
		l	= tde4.createLens()
		name	= tde4.getLensName(l0)
		num = name.split('_')[-1]
		if num.isdigit() == True:
			numInt = int(num)
			numInt += 1
			name = (name.replace(num, '') + str(numInt))
		else:
			name	= name+"_1"
		tde4.setLensName(l,name)

		fl	= tde4.getLensFocalLength(l0)
		tde4.setLensFocalLength(l,fl)

		focus	= tde4.getLensFocus(l0)
		tde4.setLensFocus(l,focus)

		d	= tde4.getLensFilmAspect(l0)
		tde4.setLensFilmAspect(l,d)

		d	= tde4.getLensLensCenterX(l0)
		tde4.setLensLensCenterX(l,d)

		d	= tde4.getLensLensCenterY(l0)
		tde4.setLensLensCenterY(l,d)

		d	= tde4.getLensPixelAspect(l0)
		tde4.setLensPixelAspect(l,d)

		d	= tde4.getLensFBackHeight(l0)
		tde4.setLensFBackHeight(l,d)

		d	= tde4.getLensFBackWidth(l0)
		tde4.setLensFBackWidth(l,d)

		dmode	= tde4.getLensDynamicDistortionMode(l0)
		tde4.setLensDynamicDistortionMode(l0,"DISTORTION_STATIC")

		model	= tde4.getLensLDModel(l0)
		tde4.setLensLDModel(l,model)

		n	= tde4.getLDModelNoParameters(model)
		for i in range(0,n):
			para	= tde4.getLDModelParameterName(model,i)
			type	= tde4.getLDModelParameterType(model,para)
			if type=="LDP_DOUBLE_ADJUST":
				d	= tde4.getLensLDAdjustableParameter(l0,para,fl,focus)
				tde4.setLensLDAdjustableParameter(l,para,fl,focus,d)

				c0	= tde4.getLensLDAdjustableParameterCurve(l0,para)
				c	= tde4.getLensLDAdjustableParameterCurve(l,para)

				klist	= tde4.getCurveKeyList(c0,0)
				for k0 in klist:
					mode	= tde4.getCurveKeyMode(c0,k0)
					fixed	= tde4.getCurveKeyFixedXFlag(c0,k0)
					cv	= tde4.getCurveKeyPosition(c0,k0)
					t0	= tde4.getCurveKeyTangent1(c0,k0)
					t1	= tde4.getCurveKeyTangent2(c0,k0)
					k	= tde4.createCurveKey(c,cv)
					tde4.setCurveKeyMode(c,k,mode)
					tde4.setCurveKeyFixedXFlag(c,k,fixed)
					tde4.setCurveKeyTangent1(c,k,t0)
					tde4.setCurveKeyTangent2(c,k,t1)

				n	= tde4.getLensNo2DLUTSamples(l0,para)
				for i in range(n):
					v	= tde4.getLens2DLUTSample(l0,para,i)
					tde4.addLens2DLUTSample(l,para,v[0],v[1],v[2])


		tde4.setLensDynamicDistortionMode(l,dmode)
		tde4.setLensDynamicDistortionMode(l0,dmode)
