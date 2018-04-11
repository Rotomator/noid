from PySide import QtCore, QtGui


''' _infoTable_model '''
''' ============================================================================================================================ '''
class _infoTable_model(QtCore.QAbstractTableModel) :
    ''' __init__ '''
    ''' ------------------------------------------------------------------------------------------------------------------------ '''
    def __init__(self, table, headers, parent= None, *args) :
        self.m_table= table
        self.m_headers= headers

        QtCore.QAbstractTableModel.__init__(self, parent, *args)

    ''' rowCount, columnCount '''
    ''' ------------------------------------------------------------------------------------------------------------------------ '''
    def columnCount(self, parent= QtCore.QModelIndex()) : return 1
    def rowCount(self, parent= QtCore.QModelIndex()) : return len(self.m_headers)

    ''' data '''
    ''' ------------------------------------------------------------------------------------------------------------------------ '''
    def data(self, index, role) :
        if index.isValid() and role == QtCore.Qt.DisplayRole :
            return self.m_table.data(index.row())

        return None

    ''' headerData '''
    ''' ------------------------------------------------------------------------------------------------------------------------ '''
    def headerData(self, section, orientation, role= QtCore.Qt.DisplayRole) :
        if role == QtCore.Qt.DisplayRole and orientation == QtCore.Qt.Vertical :
            return self.m_headers[section]

        return None


''' _infoTable '''
''' ============================================================================================================================ '''
class _infoTable(QtGui.QTableView) :
    ''' __init__ '''
    ''' ------------------------------------------------------------------------------------------------------------------------ '''
    def __init__(self, headers, parent= None) :
        self.m_model= _infoTable_model(self, headers)

        ''' create table '''
        QtGui.QTableView.__init__(self, parent)
        self.setModel(self.m_model)
        self.setSizePolicy(QtGui.QSizePolicy.Policy.Minimum, QtGui.QSizePolicy.Policy.Fixed)
        #self.verticalScrollBar().setDisabled(True)
        #self.horizontalScrollBar().setDisabled(True)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        self.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        #self.setHeight(24*len(headers))
        #self.setMinimumHeight(24*len(headers))
        self.setShowGrid(False)

        ''' rows size '''
        header= self.verticalHeader()
        header.setResizeMode(QtGui.QHeaderView.Fixed)
        header.setDefaultSectionSize(24)
        header.setStyleSheet("::section{background-color:#2b2b2b;}")

        ''' columns size '''
        header= self.horizontalHeader()
        header.setVisible(False)
        header.setResizeMode(0, QtGui.QHeaderView.Stretch)


    ''' sizeHint '''
    ''' ------------------------------------------------------------------------------------------------------------------------ '''
    def sizeHint(self) :
        h= self.verticalHeader().sectionSize(0)
        return QtCore.QSize(0, h*len(self.m_model.m_headers)+4)


    ''' update '''
    ''' ------------------------------------------------------------------------------------------------------------------------ '''
    def update(self) :
        self.m_model.reset()

    ''' data '''
    ''' ------------------------------------------------------------------------------------------------------------------------ '''
    def data(self, idx) : return None
