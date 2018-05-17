try:
    from PySide2 import QtCore as core, QtGui as gui, QtWidgets as widgets
except ImportError:
    from PySide import QtCore as core, QtGui as gui
    widgets= gui
    core.QItemSelectionModel= gui.QItemSelectionModel
    widgets.QHeaderView.setSectionResizeMode= widgets.QHeaderView.setResizeMode


''' _listTable_model '''
''' ============================================================================================================================ '''
class _listTable_model(core.QAbstractTableModel) :
    ''' __init__ '''
    ''' ------------------------------------------------------------------------------------------------------------------------ '''
    def __init__(self, table, headers, parent= None, *args) :
        self.m_table= table
        self.m_headers= headers

        core.QAbstractTableModel.__init__(self, parent, *args)

    ''' columnCount, rowCount '''
    ''' ------------------------------------------------------------------------------------------------------------------------ '''
    def columnCount(self, parent= core.QModelIndex()) : return len(self.m_headers)
    def rowCount(self, parent= core.QModelIndex()) : return self.m_table.rowCount()

    ''' data '''
    ''' ------------------------------------------------------------------------------------------------------------------------ '''
    def data(self, index, role) :
        if index.isValid() :
            if role == core.Qt.ForegroundRole : return self.m_table.fgColor(index.column(), index.row())
            elif role == core.Qt.BackgroundRole : return self.m_table.bgColor(index.column(), index.row())
            elif role == core.Qt.DisplayRole : return self.m_table.data(index.column(), index.row())

        return None

    ''' headerData '''
    ''' ------------------------------------------------------------------------------------------------------------------------ '''
    def headerData(self, section, orientation, role= core.Qt.DisplayRole) :
        if role == core.Qt.DisplayRole and orientation == core.Qt.Horizontal :
            return self.m_headers[section]

        return None


''' _listTable '''
''' ============================================================================================================================ '''
class _listTable(widgets.QTableView) :
    ''' __init__ '''
    ''' ------------------------------------------------------------------------------------------------------------------------ '''
    def __init__(self, headers, parent= None) :
        self.m_model= _listTable_model(self, headers)

        ''' create table '''
        widgets.QTableView.__init__(self, parent)
        self.setModel(self.m_model)
        self.setFrameStyle(widgets.QFrame.NoFrame)
        self.setShowGrid(False)
        self.setFocusPolicy(core.Qt.NoFocus)
        self.setEditTriggers(widgets.QAbstractItemView.NoEditTriggers)
        self.setSelectionBehavior(widgets.QAbstractItemView.SelectRows)
        self.setSelectionMode(widgets.QAbstractItemView.SingleSelection)

        ''' rows size '''
        header= self.verticalHeader()
        header.setVisible(False)
        header.setSectionResizeMode(widgets.QHeaderView.Fixed)
        header.setDefaultSectionSize(24)

        ''' columns size '''
        header= self.horizontalHeader()
        for i in range(0, self.m_model.columnCount()) :
            header.setSectionResizeMode(i, widgets.QHeaderView.Stretch)

    ''' setFixed '''
    ''' ------------------------------------------------------------------------------------------------------------------------ '''
    def setFixed(self, columnIdx) : self.horizontalHeader().setSectionResizeMode(columnIdx, widgets.QHeaderView.Fixed)

    ''' setWidth '''
    ''' ------------------------------------------------------------------------------------------------------------------------ '''
    def setWidth(self, columnIdx, width) :
        self.horizontalHeader().setSectionResizeMode(columnIdx, widgets.QHeaderView.Fixed)
        self.setColumnWidth(columnIdx, width)

    ''' update '''
    ''' ------------------------------------------------------------------------------------------------------------------------ '''
    def update(self) :
        #self.m_model.reset()
        self.m_model.beginResetModel()
        self.m_model.endResetModel()

    ''' columnCount, rowCount '''
    ''' ------------------------------------------------------------------------------------------------------------------------ '''
    #def columnCount(self) : return 0
    def rowCount(self) : return 0

    ''' headerData '''
    ''' ------------------------------------------------------------------------------------------------------------------------ '''
    #def headerData(self, columnIdx) : return None

    ''' data '''
    ''' ------------------------------------------------------------------------------------------------------------------------ '''
    def data(self, columnIdx, rowIdx) : return None

    ''' fgColor '''
    ''' ------------------------------------------------------------------------------------------------------------------------ '''
    def fgColor(self, columnIdx, rowIdx) : return None

    ''' bgColor '''
    ''' ------------------------------------------------------------------------------------------------------------------------ '''
    def bgColor(self, columnIdx, rowIdx) : return None
