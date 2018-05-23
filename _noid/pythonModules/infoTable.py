try:
    from PySide2 import QtCore as core, QtGui as gui, QtWidgets as widgets
except ImportError:
    from PySide import QtCore as core, QtGui as gui
    widgets= gui
    core.QItemSelectionModel= gui.QItemSelectionModel
    widgets.QHeaderView.setSectionResizeMode= widgets.QHeaderView.setResizeMode


''' _infoTable_model '''
''' ============================================================================================================================ '''
class _infoTable_model(core.QAbstractTableModel) :
    ''' __init__ '''
    ''' ------------------------------------------------------------------------------------------------------------------------ '''
    def __init__(self, table, headers, parent= None, *args) :
        self.m_table= table
        self.m_headers= headers

        core.QAbstractTableModel.__init__(self, parent, *args)

    ''' rowCount, columnCount '''
    ''' ------------------------------------------------------------------------------------------------------------------------ '''
    def columnCount(self, parent= core.QModelIndex()) : return 1
    def rowCount(self, parent= core.QModelIndex()) : return len(self.m_headers)

    ''' data '''
    ''' ------------------------------------------------------------------------------------------------------------------------ '''
    def data(self, index, role) :
        if index.isValid() and role == core.Qt.DisplayRole :
            return self.m_table.data(index.row())

        return None

    ''' headerData '''
    ''' ------------------------------------------------------------------------------------------------------------------------ '''
    def headerData(self, section, orientation, role= core.Qt.DisplayRole) :
        if role == core.Qt.DisplayRole and orientation == core.Qt.Vertical :
            return self.m_headers[section]

        return None


''' _infoTable '''
''' ============================================================================================================================ '''
class _infoTable(widgets.QTableView) :
    ''' __init__ '''
    ''' ------------------------------------------------------------------------------------------------------------------------ '''
    def __init__(self, headers, parent= None) :
        self.m_model= _infoTable_model(self, headers)

        ''' create table '''
        widgets.QTableView.__init__(self, parent)
        self.setModel(self.m_model)
        self.setSizePolicy(widgets.QSizePolicy.Policy.Minimum, widgets.QSizePolicy.Policy.Fixed)
        #self.verticalScrollBar().setDisabled(True)
        #self.horizontalScrollBar().setDisabled(True)
        self.setFocusPolicy(core.Qt.NoFocus)
        self.setSelectionMode(widgets.QAbstractItemView.NoSelection)
        self.setEditTriggers(widgets.QAbstractItemView.NoEditTriggers)
        #self.setHeight(24*len(headers))
        #self.setMinimumHeight(24*len(headers))
        self.setShowGrid(False)

        ''' rows size '''
        header= self.verticalHeader()
        header.setSectionResizeMode(widgets.QHeaderView.Fixed)
        header.setDefaultSectionSize(24)
        header.setStyleSheet("::section{background-color:#2b2b2b;}")

        ''' columns size '''
        header= self.horizontalHeader()
        header.setVisible(False)
        header.setSectionResizeMode(0, widgets.QHeaderView.Stretch)


    ''' sizeHint '''
    ''' ------------------------------------------------------------------------------------------------------------------------ '''
    def sizeHint(self) :
        h= self.verticalHeader().sectionSize(0)
        return core.QSize(0, h*len(self.m_model.m_headers)+4)


    ''' update '''
    ''' ------------------------------------------------------------------------------------------------------------------------ '''
    def update(self) :
        #self.m_model.reset()
        self.m_model.beginResetModel()
        self.m_model.endResetModel()

    ''' data '''
    ''' ------------------------------------------------------------------------------------------------------------------------ '''
    def data(self, idx) : return None
