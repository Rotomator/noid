# 3DE4.script.name:	\\ Load NOID Disks...
# 3DE4.script.version:	v0.1
# 3DE4.script.gui:  Main Window::NOID::Scripts:All
# 3DE4.script.gui:  Main Window::NOID::Scripts:
# 3DE4.script.comment:	Load NOID Disks...


def _loadCgevDisks():
	req	= tde4.createCustomRequester()
	tde4.addTextFieldWidget(req,"line1","","Load Disks :")
	tde4.setWidgetSensitiveFlag(req, "line1", 0)
	tde4.addTextFieldWidget(req,"line2","","Clic Ok when browser window appears:")
	tde4.setWidgetSensitiveFlag(req, "line2", 0)
	tde4.addSeparatorWidget(req, "sep" "line2")
	tde4.addToggleWidget(req,"sa","stora/diska",0)
	tde4.addToggleWidget(req,"sb","storb/diskb",0)
	tde4.addToggleWidget(req,"sc","storc/diskc",0)
	tde4.addToggleWidget(req,"sd","stord/diskd",0)
	tde4.addToggleWidget(req,"se","store/diske",0)
	tde4.addToggleWidget(req,"sf","storf/diskf",0)
	tde4.addToggleWidget(req,"sg","storg/diskg",0)
	tde4.addToggleWidget(req,"sw","storw/diskw",0)
	tde4.addToggleWidget(req,"sz","storz/diskz",0)
	ret	= tde4.postCustomRequester(req,"Load NOID Disks...",350,0,"Ok","Cancel")
	if ret == 1:
		la = tde4.getWidgetValue(req,"sa")
		lb = tde4.getWidgetValue(req,"sb")
		lc = tde4.getWidgetValue(req,"sc")
		ld = tde4.getWidgetValue(req,"sd")
		le = tde4.getWidgetValue(req,"se")
		lf = tde4.getWidgetValue(req,"sf")
		lg = tde4.getWidgetValue(req,"sg")
		lw = tde4.getWidgetValue(req,"sw")
		lz = tde4.getWidgetValue(req,"sz")
		if la == 1:
			stora = '\\\\stora\diska\\'
			_req = tde4.postFileRequester_copy('Load stora', '*.x', stora)
		if lb == 1:
			storb = '\\\\storb\diskb\\'
			_req = tde4.postFileRequester_copy('Load storb', '*.x', storb)
		if lc == 1:
			storc = '\\\\storc\diskc\\'
			_req = tde4.postFileRequester_copy('Load storc', '*.x', storc)
		if ld == 1:
			stord = '\\\\stord\diskd\\'
			_req = tde4.postFileRequester_copy('Load stord', '*.x', stord)
		if le == 1:
			store = '\\\\store\diske\\'
			_req = tde4.postFileRequester_copy('Load store', '*.x', store)
		if lf == 1:
			storf = '\\\\storf\diskf\\'
			_req = tde4.postFileRequester_copy('Load storf', '*.x', storf)
		if lg == 1:
			storg = '\\\\storg\diskg\\'
			_req = tde4.postFileRequester_copy('Load storg', '*.x', storg)
		if lw == 1:
			storw = '\\\\storw\diskw\\'
			_req = tde4.postFileRequester_copy('Load storw', '*.x', storw)
		if lz == 1:
			storz = '\\\\storz\diskz\\'
			_req = tde4.postFileRequester_copy('Load storz', '*.x', storz)
_loadCgevDisks()
