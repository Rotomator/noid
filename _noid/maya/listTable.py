from PySide import QtCore, QtGui


''' _listTable_model '''
''' ============================================================================================================================ '''
class _listTable_model(QtCore.QAbstractTableModel) :
    ''' __init__ '''
    ''' ------------------------------------------------------------------------------------------------------------------------ '''
    def __init__(self, table, headers, parent= None, *args) :
        self.m_table= table
        self.m_headers= headers

        QtCore.QAbstractTableModel.__init__(self, parent, *args)

    ''' columnCount, rowCount '''
    ''' ------------------------------------------------------------------------------------------------------------------------ '''
    def columnCount(self, parent= QtCore.QModelIndex()) : return len(self.m_headers)
    def rowCount(self, parent= QtCore.QModelIndex()) : return self.m_table.rowCount()

    ''' data '''
    ''' ------------------------------------------------------------------------------------------------------------------------ '''
    def data(self, index, role) :
        if index.isValid() :
            if role == QtCore.Qt.ForegroundRole : return self.m_table.fgColor(index.column(), index.row())
            elif role == QtCore.Qt.BackgroundRole : return self.m_table.bgColor(index.column(), index.row())
            elif role == QtCore.Qt.DisplayRole : return self.m_table.data(index.column(), index.row())

        return None

    ''' headerData '''
    ''' ------------------------------------------------------------------------------------------------------------------------ '''
    def headerData(self, section, orientation, role= QtCore.Qt.DisplayRole) :
        if role == QtCore.Qt.DisplayRole and orientation == QtCore.Qt.Horizontal :
            return self.m_headers[section]

        return None


''' _listTable '''
''' ============================================================================================================================ '''
class _listTable(QtGui.QTableView) :
    ''' __init__ '''
    ''' ------------------------------------------------------------------------------------------------------------------------ '''
    def __init__(self, headers, parent= None) :
        self.m_model= _listTable_model(self, headers)

        ''' create table '''
        QtGui.QTableView.__init__(self, parent)
        self.setModel(self.m_model)
        self.setFrameStyle(QtGui.QFrame.NoFrame)
        self.setShowGrid(False)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)

        ''' rows size '''
        header= self.verticalHeader()
        header.setVisible(False)
        header.setResizeMode(QtGui.QHeaderView.Fixed)
        header.setDefaultSectionSize(24)

        ''' columns size '''
        header= self.horizontalHeader()
        for i in range(0, self.m_model.columnCount()) :
            header.setResizeMode(i, QtGui.QHeaderView.Stretch)

    ''' setFixed '''
    ''' ------------------------------------------------------------------------------------------------------------------------ '''
    def setFixed(self, columnIdx) : self.horizontalHeader().setResizeMode(columnIdx, QtGui.QHeaderView.Fixed)

    ''' setWidth '''
    ''' ------------------------------------------------------------------------------------------------------------------------ '''
    def setWidth(self, columnIdx, width) :
        self.horizontalHeader().setResizeMode(columnIdx, QtGui.QHeaderView.Fixed)
        self.setColumnWidth(columnIdx, width)

    ''' update '''
    ''' ------------------------------------------------------------------------------------------------------------------------ '''
    def update(self) :
        self.m_model.reset()

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
