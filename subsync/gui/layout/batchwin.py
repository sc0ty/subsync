# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Oct 23 2019)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

from subsync.gui.components.batchlist import BatchList
from subsync.gui.components.choicelang import ChoiceLang
from subsync.gui.components.popups import PopupInfoButton
import wx
import wx.xrc


###########################################################################
## Class BatchWin
###########################################################################

class BatchWin ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"Batch Processing"), pos = wx.DefaultPosition, size = wx.Size( 900,600 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.Size( 900,500 ), wx.DefaultSize )

		bSizer1 = wx.BoxSizer( wx.VERTICAL )

		self.m_panelMain = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		fgSizer1 = wx.FlexGridSizer( 0, 1, 0, 0 )
		fgSizer1.AddGrowableCol( 0 )
		fgSizer1.AddGrowableRow( 0 )
		fgSizer1.SetFlexibleDirection( wx.BOTH )
		fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_items = BatchList( self.m_panelMain, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_ICON )
		fgSizer1.Add( self.m_items, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_panelSettings = wx.Panel( self.m_panelMain, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		fgSizer2 = wx.FlexGridSizer( 0, 1, 0, 0 )
		fgSizer2.AddGrowableCol( 0 )
		fgSizer2.SetFlexibleDirection( wx.BOTH )
		fgSizer2.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		fgSizer3 = wx.FlexGridSizer( 1, 0, 0, 0 )
		fgSizer3.SetFlexibleDirection( wx.BOTH )
		fgSizer3.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_buttonAdd = wx.Button( self.m_panelSettings, wx.ID_ANY, _(u"Add"), wx.DefaultPosition, wx.DefaultSize, 0 )

		self.m_buttonAdd.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_NORMAL_FILE, wx.ART_BUTTON ) )
		fgSizer3.Add( self.m_buttonAdd, 0, wx.ALL, 5 )

		self.m_buttonRemove = wx.Button( self.m_panelSettings, wx.ID_ANY, _(u"Remove"), wx.DefaultPosition, wx.DefaultSize, 0 )

		self.m_buttonRemove.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_DELETE, wx.ART_BUTTON ) )
		self.m_buttonRemove.Enable( False )

		fgSizer3.Add( self.m_buttonRemove, 0, wx.ALL, 5 )

		self.m_buttonStreamSel = wx.Button( self.m_panelSettings, wx.ID_ANY, _(u"Select stream"), wx.DefaultPosition, wx.DefaultSize, 0 )

		self.m_buttonStreamSel.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_HELP_SETTINGS, wx.ART_BUTTON ) )
		self.m_buttonStreamSel.Enable( False )

		fgSizer3.Add( self.m_buttonStreamSel, 0, wx.ALL, 5 )

		self.m_buttonOutSel = wx.Button( self.m_panelSettings, wx.ID_ANY, _(u"Select output"), wx.DefaultPosition, wx.DefaultSize, 0 )

		self.m_buttonOutSel.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_HELP_SETTINGS, wx.ART_BUTTON ) )
		self.m_buttonOutSel.Enable( False )

		fgSizer3.Add( self.m_buttonOutSel, 0, wx.ALL, 5 )

		self.m_buttonAutoSort = wx.Button( self.m_panelSettings, wx.ID_ANY, _(u"Auto sort"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_buttonAutoSort.Enable( False )

		fgSizer3.Add( self.m_buttonAutoSort, 0, wx.ALL, 5 )


		fgSizer2.Add( fgSizer3, 1, wx.EXPAND, 5 )

		self.m_staticline1 = wx.StaticLine( self.m_panelSettings, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		fgSizer2.Add( self.m_staticline1, 0, wx.EXPAND |wx.ALL, 5 )

		fgSizer4 = wx.FlexGridSizer( 0, 4, 0, 0 )
		fgSizer4.AddGrowableCol( 2 )
		fgSizer4.SetFlexibleDirection( wx.BOTH )
		fgSizer4.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_textLang = wx.StaticText( self.m_panelSettings, wx.ID_ANY, _(u"Language:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textLang.Wrap( -1 )

		fgSizer4.Add( self.m_textLang, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.RIGHT|wx.LEFT, 5 )


		fgSizer4.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		m_choiceLangChoices = []
		self.m_choiceLang = ChoiceLang( self.m_panelSettings, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choiceLangChoices, 0 )
		self.m_choiceLang.SetSelection( 0 )
		self.m_choiceLang.Enable( False )

		fgSizer4.Add( self.m_choiceLang, 0, wx.ALIGN_CENTER_VERTICAL|wx.EXPAND|wx.TOP|wx.RIGHT|wx.LEFT, 5 )


		fgSizer4.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.m_textMaxDistLabel = wx.StaticText( self.m_panelSettings, wx.ID_ANY, _(u"Max adjustment:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textMaxDistLabel.Wrap( -1 )

		fgSizer4.Add( self.m_textMaxDistLabel, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.RIGHT|wx.LEFT, 5 )

		self.m_buttonMaxDistInfo = PopupInfoButton( self.m_panelSettings, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|0|wx.BORDER_NONE )

		self.m_buttonMaxDistInfo.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_TIP, wx.ART_BUTTON ) )
		fgSizer4.Add( self.m_buttonMaxDistInfo, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_sliderMaxDist = wx.Slider( self.m_panelSettings, wx.ID_ANY, 30, 5, 180, wx.DefaultPosition, wx.Size( -1,-1 ), wx.SL_HORIZONTAL )
		fgSizer4.Add( self.m_sliderMaxDist, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND|wx.TOP|wx.RIGHT|wx.LEFT, 5 )

		self.m_textMaxDist = wx.StaticText( self.m_panelSettings, wx.ID_ANY, _(u"999 min"), wx.DefaultPosition, wx.DefaultSize, wx.ST_NO_AUTORESIZE )
		self.m_textMaxDist.Wrap( -1 )

		fgSizer4.Add( self.m_textMaxDist, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.RIGHT|wx.LEFT, 5 )

		self.m_textEffortLabel = wx.StaticText( self.m_panelSettings, wx.ID_ANY, _(u"Effort:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textEffortLabel.Wrap( -1 )

		fgSizer4.Add( self.m_textEffortLabel, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		self.m_buttonEffortInfo = PopupInfoButton( self.m_panelSettings, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|0|wx.BORDER_NONE )

		self.m_buttonEffortInfo.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_TIP, wx.ART_BUTTON ) )
		fgSizer4.Add( self.m_buttonEffortInfo, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

		self.m_sliderEffort = wx.Slider( self.m_panelSettings, wx.ID_ANY, 50, 0, 100, wx.DefaultPosition, wx.Size( -1,-1 ), wx.SL_HORIZONTAL )
		fgSizer4.Add( self.m_sliderEffort, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND|wx.ALL, 5 )

		self.m_textEffort = wx.StaticText( self.m_panelSettings, wx.ID_ANY, _(u"0.50"), wx.DefaultPosition, wx.DefaultSize, wx.ST_NO_AUTORESIZE )
		self.m_textEffort.Wrap( -1 )

		fgSizer4.Add( self.m_textEffort, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		fgSizer2.Add( fgSizer4, 1, wx.EXPAND, 5 )


		self.m_panelSettings.SetSizer( fgSizer2 )
		self.m_panelSettings.Layout()
		fgSizer2.Fit( self.m_panelSettings )
		fgSizer1.Add( self.m_panelSettings, 0, wx.EXPAND, 5 )

		self.m_panelProgress = wx.Panel( self.m_panelMain, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_panelProgress.Hide()

		fgSizer5 = wx.FlexGridSizer( 0, 1, 0, 0 )
		fgSizer5.AddGrowableCol( 0 )
		fgSizer5.SetFlexibleDirection( wx.BOTH )
		fgSizer5.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_panelSyncDone = wx.Panel( self.m_panelProgress, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_panelSyncDone.Hide()

		fgSizer6 = wx.FlexGridSizer( 0, 1, 0, 0 )
		fgSizer6.AddGrowableCol( 0 )
		fgSizer6.SetFlexibleDirection( wx.BOTH )
		fgSizer6.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		fgSizer7 = wx.FlexGridSizer( 1, 0, 0, 0 )
		fgSizer7.SetFlexibleDirection( wx.BOTH )
		fgSizer7.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_buttonEditFailed = wx.Button( self.m_panelSyncDone, wx.ID_ANY, _(u"Edit failed tasks"), wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer7.Add( self.m_buttonEditFailed, 0, wx.ALL, 5 )

		self.m_buttonEditAll = wx.Button( self.m_panelSyncDone, wx.ID_ANY, _(u"Edit all tasks"), wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer7.Add( self.m_buttonEditAll, 0, wx.ALL, 5 )

		self.m_buttonEditNew = wx.Button( self.m_panelSyncDone, wx.ID_ANY, _(u"New synchronization"), wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer7.Add( self.m_buttonEditNew, 0, wx.ALL, 5 )


		fgSizer6.Add( fgSizer7, 1, wx.EXPAND, 5 )

		self.m_staticline2 = wx.StaticLine( self.m_panelSyncDone, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		fgSizer6.Add( self.m_staticline2, 0, wx.EXPAND |wx.ALL, 5 )


		self.m_panelSyncDone.SetSizer( fgSizer6 )
		self.m_panelSyncDone.Layout()
		fgSizer6.Fit( self.m_panelSyncDone )
		fgSizer5.Add( self.m_panelSyncDone, 1, wx.EXPAND, 5 )

		fgSizer8 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer8.AddGrowableCol( 1 )
		fgSizer8.SetFlexibleDirection( wx.BOTH )
		fgSizer8.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_textStatus = wx.StaticText( self.m_panelProgress, wx.ID_ANY, _(u"Status:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textStatus.Wrap( -1 )

		fgSizer8.Add( self.m_textStatus, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT|wx.ALL, 5 )

		fgSizer9 = wx.FlexGridSizer( 1, 0, 0, 0 )
		fgSizer9.SetFlexibleDirection( wx.BOTH )
		fgSizer9.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_bitmapStatus = wx.StaticBitmap( self.m_panelProgress, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_bitmapStatus.Hide()

		fgSizer9.Add( self.m_bitmapStatus, 0, wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.BOTTOM|wx.LEFT, 5 )

		self.m_textStatusVal = wx.StaticText( self.m_panelProgress, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textStatusVal.Wrap( -1 )

		fgSizer9.Add( self.m_textStatusVal, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )


		fgSizer8.Add( fgSizer9, 1, wx.EXPAND, 5 )

		self.m_textCurrentProgress = wx.StaticText( self.m_panelProgress, wx.ID_ANY, _(u"Current file:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textCurrentProgress.Wrap( -1 )

		fgSizer8.Add( self.m_textCurrentProgress, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT|wx.TOP|wx.RIGHT|wx.LEFT, 5 )

		self.m_gaugeCurrentProgress = wx.Gauge( self.m_panelProgress, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL )
		self.m_gaugeCurrentProgress.SetValue( 0 )
		fgSizer8.Add( self.m_gaugeCurrentProgress, 0, wx.ALIGN_CENTER_VERTICAL|wx.EXPAND|wx.TOP|wx.RIGHT|wx.LEFT, 5 )

		self.m_textTotalProgress = wx.StaticText( self.m_panelProgress, wx.ID_ANY, _(u"Total progress:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textTotalProgress.Wrap( -1 )

		fgSizer8.Add( self.m_textTotalProgress, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 5 )

		self.m_gaugeTotalProgress = wx.Gauge( self.m_panelProgress, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL )
		self.m_gaugeTotalProgress.SetValue( 0 )
		fgSizer8.Add( self.m_gaugeTotalProgress, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )


		fgSizer5.Add( fgSizer8, 1, wx.EXPAND, 5 )


		self.m_panelProgress.SetSizer( fgSizer5 )
		self.m_panelProgress.Layout()
		fgSizer5.Fit( self.m_panelProgress )
		fgSizer1.Add( self.m_panelProgress, 1, wx.EXPAND |wx.ALL, 5 )

		self.m_staticline3 = wx.StaticLine( self.m_panelMain, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		fgSizer1.Add( self.m_staticline3, 0, wx.EXPAND |wx.ALL, 5 )

		fgSizer10 = wx.FlexGridSizer( 1, 0, 0, 0 )
		fgSizer10.SetFlexibleDirection( wx.BOTH )
		fgSizer10.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_buttonClose = wx.Button( self.m_panelMain, wx.ID_CLOSE, _(u"Close"), wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer10.Add( self.m_buttonClose, 1, wx.ALL|wx.EXPAND, 5 )

		self.m_buttonStop = wx.Button( self.m_panelMain, wx.ID_STOP, _(u"Stop"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_buttonStop.Hide()

		fgSizer10.Add( self.m_buttonStop, 1, wx.ALL|wx.EXPAND, 5 )

		self.m_buttonStart = wx.Button( self.m_panelMain, wx.ID_OK, _(u"Start"), wx.DefaultPosition, wx.DefaultSize, 0 )

		self.m_buttonStart.SetDefault()
		self.m_buttonStart.Enable( False )

		fgSizer10.Add( self.m_buttonStart, 1, wx.ALL|wx.EXPAND, 5 )


		fgSizer1.Add( fgSizer10, 0, wx.ALIGN_RIGHT, 5 )


		self.m_panelMain.SetSizer( fgSizer1 )
		self.m_panelMain.Layout()
		fgSizer1.Fit( self.m_panelMain )
		bSizer1.Add( self.m_panelMain, 1, wx.EXPAND, 5 )


		self.SetSizer( bSizer1 )
		self.Layout()
		self.m_menubar = wx.MenuBar( 0 )
		self.m_menuFile = wx.Menu()
		self.m_menuItemNew = wx.MenuItem( self.m_menuFile, wx.ID_ANY, _(u"&New")+ u"\t" + u"CTRL+N", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuItemNew.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_NEW, wx.ART_MENU ) )
		self.m_menuFile.Append( self.m_menuItemNew )

		self.m_menuFile.AppendSeparator()

		self.m_menuItemAddAuto = wx.MenuItem( self.m_menuFile, wx.ID_ANY, _(u"&Add files (auto sort)")+ u"\t" + u"CTRL+O", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuItemAddAuto.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_NORMAL_FILE, wx.ART_MENU ) )
		self.m_menuFile.Append( self.m_menuItemAddAuto )

		self.m_menuItemAddSubs = wx.MenuItem( self.m_menuFile, wx.ID_ANY, _(u"Add &subtitles")+ u"\t" + u"F3", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuItemAddSubs.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_NORMAL_FILE, wx.ART_MENU ) )
		self.m_menuFile.Append( self.m_menuItemAddSubs )

		self.m_menuItemAddRefs = wx.MenuItem( self.m_menuFile, wx.ID_ANY, _(u"Add &references")+ u"\t" + u"F4", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuItemAddRefs.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_NORMAL_FILE, wx.ART_MENU ) )
		self.m_menuFile.Append( self.m_menuItemAddRefs )

		self.m_menuItemAddFolder = wx.MenuItem( self.m_menuFile, wx.ID_ANY, _(u"Add &folder")+ u"\t" + u"F2", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuItemAddFolder.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_FOLDER, wx.ART_MENU ) )
		self.m_menuFile.Append( self.m_menuItemAddFolder )

		self.m_menuFile.AppendSeparator()

		self.m_menuItemImport = wx.MenuItem( self.m_menuFile, wx.ID_ANY, _(u"&Import list")+ u"\t" + u"F9", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuItemImport.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_FILE_OPEN, wx.ART_MENU ) )
		self.m_menuFile.Append( self.m_menuItemImport )

		self.m_menuItemExport = wx.MenuItem( self.m_menuFile, wx.ID_ANY, _(u"&Export list")+ u"\t" + u"F10", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuItemExport.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_FILE_SAVE, wx.ART_MENU ) )
		self.m_menuFile.Append( self.m_menuItemExport )

		self.m_menuFile.AppendSeparator()

		self.m_menuItemClose = wx.MenuItem( self.m_menuFile, wx.ID_ANY, _(u"&Close"), wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuItemClose.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_QUIT, wx.ART_MENU ) )
		self.m_menuFile.Append( self.m_menuItemClose )

		self.m_menubar.Append( self.m_menuFile, _(u"&File") )

		self.m_menuEdit = wx.Menu()
		self.m_menuItemAutoSort = wx.MenuItem( self.m_menuEdit, wx.ID_ANY, _(u"Au&to sort")+ u"\t" + u"CTRL+S", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuEdit.Append( self.m_menuItemAutoSort )
		self.m_menuItemAutoSort.Enable( False )

		self.m_menuItemRemove = wx.MenuItem( self.m_menuEdit, wx.ID_ANY, _(u"&Remove")+ u"\t" + u"DELETE", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuItemRemove.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_DELETE, wx.ART_MENU ) )
		self.m_menuEdit.Append( self.m_menuItemRemove )
		self.m_menuItemRemove.Enable( False )

		self.m_menuEdit.AppendSeparator()

		self.m_menuItemSelectAll = wx.MenuItem( self.m_menuEdit, wx.ID_ANY, _(u"Select &all")+ u"\t" + u"CTRL+A", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuEdit.Append( self.m_menuItemSelectAll )

		self.m_menuItemSelectSubs = wx.MenuItem( self.m_menuEdit, wx.ID_ANY, _(u"Select all &subtitles")+ u"\t" + u"CTRL+1", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuEdit.Append( self.m_menuItemSelectSubs )

		self.m_menuItemSelectRefs = wx.MenuItem( self.m_menuEdit, wx.ID_ANY, _(u"Select all &references")+ u"\t" + u"CTRL+2", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuEdit.Append( self.m_menuItemSelectRefs )

		self.m_menuItemSelectOuts = wx.MenuItem( self.m_menuEdit, wx.ID_ANY, _(u"Select all o&utputs")+ u"\t" + u"CTRL+3", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuEdit.Append( self.m_menuItemSelectOuts )

		self.m_menuEdit.AppendSeparator()

		self.m_menuItemStreamSel = wx.MenuItem( self.m_menuEdit, wx.ID_ANY, _(u"Set &input stream")+ u"\t" + u"F5", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuEdit.Append( self.m_menuItemStreamSel )
		self.m_menuItemStreamSel.Enable( False )

		self.m_menuItemOutSel = wx.MenuItem( self.m_menuEdit, wx.ID_ANY, _(u"Set &output location")+ u"\t" + u"F6", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuEdit.Append( self.m_menuItemOutSel )

		self.m_menuItemProps = wx.MenuItem( self.m_menuEdit, wx.ID_ANY, _(u"&Propeties")+ u"\t" + u"F8", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuItemProps.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_HELP_SETTINGS, wx.ART_MENU ) )
		self.m_menuEdit.Append( self.m_menuItemProps )
		self.m_menuItemProps.Enable( False )

		self.m_menubar.Append( self.m_menuEdit, _(u"&Edit") )

		self.m_menuHelp = wx.Menu()
		self.m_menuItemAbout = wx.MenuItem( self.m_menuHelp, wx.ID_ABOUT, _(u"&About"), wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuHelp.Append( self.m_menuItemAbout )

		self.m_menubar.Append( self.m_menuHelp, _(u"&Help") )

		self.SetMenuBar( self.m_menubar )


		# Connect Events
		self.Bind( wx.EVT_CLOSE, self.onClose )
		self.m_choiceLang.Bind( wx.EVT_CHOICE, self.onChoiceLangChoice )
		self.m_sliderMaxDist.Bind( wx.EVT_SCROLL, self.onSliderMaxDistScroll )
		self.m_sliderEffort.Bind( wx.EVT_SCROLL, self.onSliderEffortScroll )
		self.m_buttonEditFailed.Bind( wx.EVT_BUTTON, self.onButtonEditFailedClick )
		self.m_buttonEditAll.Bind( wx.EVT_BUTTON, self.onButtonEditAllClick )
		self.m_buttonEditNew.Bind( wx.EVT_BUTTON, self.onButtonEditNewClick )
		self.m_buttonClose.Bind( wx.EVT_BUTTON, self.onButtonCloseClick )
		self.m_buttonStop.Bind( wx.EVT_BUTTON, self.onButtonStopClick )
		self.m_buttonStart.Bind( wx.EVT_BUTTON, self.onButtonStartClick )
		self.Bind( wx.EVT_MENU, self.onMenuNewClick, id = self.m_menuItemNew.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuAddFolderClick, id = self.m_menuItemAddFolder.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuImportClick, id = self.m_menuItemImport.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuExportClick, id = self.m_menuItemExport.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuPropsClick, id = self.m_menuItemProps.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuAboutClick, id = self.m_menuItemAbout.GetId() )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def onClose( self, event ):
		event.Skip()

	def onChoiceLangChoice( self, event ):
		event.Skip()

	def onSliderMaxDistScroll( self, event ):
		event.Skip()

	def onSliderEffortScroll( self, event ):
		event.Skip()

	def onButtonEditFailedClick( self, event ):
		event.Skip()

	def onButtonEditAllClick( self, event ):
		event.Skip()

	def onButtonEditNewClick( self, event ):
		event.Skip()

	def onButtonCloseClick( self, event ):
		event.Skip()

	def onButtonStopClick( self, event ):
		event.Skip()

	def onButtonStartClick( self, event ):
		event.Skip()

	def onMenuNewClick( self, event ):
		event.Skip()

	def onMenuAddFolderClick( self, event ):
		event.Skip()

	def onMenuImportClick( self, event ):
		event.Skip()

	def onMenuExportClick( self, event ):
		event.Skip()

	def onMenuPropsClick( self, event ):
		event.Skip()

	def onMenuAboutClick( self, event ):
		event.Skip()


