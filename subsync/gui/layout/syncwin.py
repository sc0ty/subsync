# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Oct 23 2019)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc


###########################################################################
## Class SyncWin
###########################################################################

class SyncWin ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"Synchronization"), pos = wx.DefaultPosition, size = wx.DefaultSize, style = wx.DEFAULT_DIALOG_STYLE )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer1 = wx.BoxSizer( wx.VERTICAL )

		self.m_panelMain = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		fgSizer2 = wx.FlexGridSizer( 0, 1, 0, 0 )
		fgSizer2.AddGrowableCol( 0 )
		fgSizer2.AddGrowableRow( 4 )
		fgSizer2.SetFlexibleDirection( wx.BOTH )
		fgSizer2.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_textStatus = wx.StaticText( self.m_panelMain, wx.ID_ANY, _(u"Initializing..."), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textStatus.Wrap( -1 )

		fgSizer2.Add( self.m_textStatus, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_gaugeProgress = wx.Gauge( self.m_panelMain, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL )
		self.m_gaugeProgress.SetValue( 0 )
		self.m_gaugeProgress.SetMinSize( wx.Size( 320,-1 ) )

		fgSizer2.Add( self.m_gaugeProgress, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_panelError = wx.Panel( self.m_panelMain, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_panelError.Hide()

		fgSizer3 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer3.AddGrowableCol( 1 )
		fgSizer3.AddGrowableRow( 0 )
		fgSizer3.SetFlexibleDirection( wx.BOTH )
		fgSizer3.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_bitmapErrorIcon = wx.StaticBitmap( self.m_panelError, wx.ID_ANY, wx.ArtProvider.GetBitmap( wx.ART_WARNING, wx.ART_CMN_DIALOG ), wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer3.Add( self.m_bitmapErrorIcon, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT|wx.TOP|wx.BOTTOM|wx.LEFT, 5 )

		fgSizer4 = wx.FlexGridSizer( 0, 1, 0, 0 )
		fgSizer4.AddGrowableCol( 0 )
		fgSizer4.AddGrowableRow( 0 )
		fgSizer4.AddGrowableRow( 1 )
		fgSizer4.SetFlexibleDirection( wx.BOTH )
		fgSizer4.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_textErrorMsg = wx.StaticText( self.m_panelError, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textErrorMsg.Wrap( -1 )

		fgSizer4.Add( self.m_textErrorMsg, 0, wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.RIGHT|wx.LEFT, 5 )

		self.m_textErrorDetails = wx.StaticText( self.m_panelError, wx.ID_ANY, _(u"[details]"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textErrorDetails.Wrap( -1 )

		self.m_textErrorDetails.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_HIGHLIGHT ) )

		fgSizer4.Add( self.m_textErrorDetails, 0, wx.ALIGN_CENTER_VERTICAL|wx.BOTTOM|wx.RIGHT|wx.LEFT, 5 )


		fgSizer3.Add( fgSizer4, 1, wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )


		self.m_panelError.SetSizer( fgSizer3 )
		self.m_panelError.Layout()
		fgSizer3.Fit( self.m_panelError )
		fgSizer2.Add( self.m_panelError, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )

		fgSizer5 = wx.FlexGridSizer( 1, 0, 0, 0 )
		fgSizer5.AddGrowableCol( 2 )
		fgSizer5.AddGrowableRow( 0 )
		fgSizer5.SetFlexibleDirection( wx.BOTH )
		fgSizer5.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_bitmapTick = wx.StaticBitmap( self.m_panelMain, wx.ID_ANY, wx.ArtProvider.GetBitmap( wx.ART_TICK_MARK, wx.ART_MENU ), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_bitmapTick.Hide()

		fgSizer5.Add( self.m_bitmapTick, 0, wx.EXPAND|wx.TOP|wx.BOTTOM|wx.LEFT, 5 )

		self.m_bitmapCross = wx.StaticBitmap( self.m_panelMain, wx.ID_ANY, wx.ArtProvider.GetBitmap( wx.ART_CROSS_MARK, wx.ART_MENU ), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_bitmapCross.Hide()

		fgSizer5.Add( self.m_bitmapCross, 0, wx.TOP|wx.BOTTOM|wx.LEFT, 5 )

		self.m_textSync = wx.StaticText( self.m_panelMain, wx.ID_ANY, _(u"Synchronization: 0 points"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textSync.Wrap( -1 )

		fgSizer5.Add( self.m_textSync, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_textShowDetails = wx.StaticText( self.m_panelMain, wx.ID_ANY, _(u"[show more]"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textShowDetails.Wrap( -1 )

		self.m_textShowDetails.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_HIGHLIGHT ) )

		fgSizer5.Add( self.m_textShowDetails, 0, wx.ALL|wx.EXPAND, 5 )


		fgSizer2.Add( fgSizer5, 1, wx.EXPAND|wx.TOP, 5 )

		self.m_panelDetails = wx.Panel( self.m_panelMain, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_panelDetails.Hide()

		fgSizer61 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer61.AddGrowableCol( 0 )
		fgSizer61.AddGrowableRow( 0 )
		fgSizer61.SetFlexibleDirection( wx.BOTH )
		fgSizer61.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		fgSizer16 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer16.AddGrowableCol( 0 )
		fgSizer16.AddGrowableCol( 1 )
		fgSizer16.AddGrowableRow( 0 )
		fgSizer16.SetFlexibleDirection( wx.BOTH )
		fgSizer16.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_textElapsedTimeTitle = wx.StaticText( self.m_panelDetails, wx.ID_ANY, _(u"elapsed time:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textElapsedTimeTitle.Wrap( -1 )

		fgSizer16.Add( self.m_textElapsedTimeTitle, 0, wx.TOP|wx.RIGHT|wx.LEFT|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_textElapsedTime = wx.StaticText( self.m_panelDetails, wx.ID_ANY, _(u"-"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textElapsedTime.Wrap( -1 )

		fgSizer16.Add( self.m_textElapsedTime, 0, wx.TOP|wx.RIGHT|wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_textCorrelationTitle = wx.StaticText( self.m_panelDetails, wx.ID_ANY, _(u"correlation:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textCorrelationTitle.Wrap( -1 )

		fgSizer16.Add( self.m_textCorrelationTitle, 0, wx.RIGHT|wx.LEFT|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_textCorrelation = wx.StaticText( self.m_panelDetails, wx.ID_ANY, _(u"-"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textCorrelation.Wrap( -1 )

		fgSizer16.Add( self.m_textCorrelation, 0, wx.RIGHT|wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_textFormulaTitle = wx.StaticText( self.m_panelDetails, wx.ID_ANY, _(u"formula:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textFormulaTitle.Wrap( -1 )

		fgSizer16.Add( self.m_textFormulaTitle, 0, wx.RIGHT|wx.LEFT|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_textFormula = wx.StaticText( self.m_panelDetails, wx.ID_ANY, _(u"-"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textFormula.Wrap( -1 )

		fgSizer16.Add( self.m_textFormula, 0, wx.RIGHT|wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_textMaxChangeTitle = wx.StaticText( self.m_panelDetails, wx.ID_ANY, _(u"max change:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textMaxChangeTitle.Wrap( -1 )

		fgSizer16.Add( self.m_textMaxChangeTitle, 0, wx.BOTTOM|wx.RIGHT|wx.LEFT|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_textMaxChange = wx.StaticText( self.m_panelDetails, wx.ID_ANY, _(u"-"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textMaxChange.Wrap( -1 )

		fgSizer16.Add( self.m_textMaxChange, 0, wx.BOTTOM|wx.RIGHT|wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5 )


		fgSizer61.Add( fgSizer16, 1, wx.RIGHT|wx.LEFT, 5 )

		self.m_textHideDetails = wx.StaticText( self.m_panelDetails, wx.ID_ANY, _(u"[hide]"), wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
		self.m_textHideDetails.Wrap( -1 )

		self.m_textHideDetails.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_HIGHLIGHT ) )

		fgSizer61.Add( self.m_textHideDetails, 0, wx.ALIGN_BOTTOM|wx.LEFT|wx.RIGHT|wx.TOP, 5 )


		self.m_panelDetails.SetSizer( fgSizer61 )
		self.m_panelDetails.Layout()
		fgSizer61.Fit( self.m_panelDetails )
		fgSizer2.Add( self.m_panelDetails, 1, wx.EXPAND|wx.RIGHT|wx.LEFT, 5 )

		self.m_textInitialSyncInfo = wx.StaticText( self.m_panelMain, wx.ID_ANY, _(u"Initial synchronization is done.\nYou could save subtitles already.\nIf they don't match, wait for a better result."), wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL )
		self.m_textInitialSyncInfo.Wrap( -1 )

		self.m_textInitialSyncInfo.Hide()

		fgSizer2.Add( self.m_textInitialSyncInfo, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL, 10 )

		self.m_staticline1 = wx.StaticLine( self.m_panelMain, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		fgSizer2.Add( self.m_staticline1, 0, wx.EXPAND |wx.ALL, 5 )

		fgSizer6 = wx.FlexGridSizer( 1, 0, 0, 0 )
		fgSizer6.SetFlexibleDirection( wx.BOTH )
		fgSizer6.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_buttonDebugMenu = wx.Button( self.m_panelMain, wx.ID_ANY, _(u"Debug"), wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT )
		self.m_buttonDebugMenu.Hide()

		self.m_menuDebug = wx.Menu()
		self.m_menuItemEnableSave = wx.MenuItem( self.m_menuDebug, wx.ID_ANY, _(u"Enable save button"), wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuDebug.Append( self.m_menuItemEnableSave )

		self.m_menuDebug.AppendSeparator()

		self.m_menuItemDumpSubWords = wx.MenuItem( self.m_menuDebug, wx.ID_ANY, _(u"Dump subtitle words"), wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuDebug.Append( self.m_menuItemDumpSubWords )

		self.m_menuItemDumpRefWords = wx.MenuItem( self.m_menuDebug, wx.ID_ANY, _(u"Dump reference words"), wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuDebug.Append( self.m_menuItemDumpRefWords )

		self.m_menuDebug.AppendSeparator()

		self.m_menuItemDumpAllSyncPoints = wx.MenuItem( self.m_menuDebug, wx.ID_ANY, _(u"Dump all synchronization points"), wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuDebug.Append( self.m_menuItemDumpAllSyncPoints )

		self.m_menuItemDumpUsedSyncPoints = wx.MenuItem( self.m_menuDebug, wx.ID_ANY, _(u"Dump used synchronization points"), wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuDebug.Append( self.m_menuItemDumpUsedSyncPoints )

		self.m_buttonDebugMenu.Bind( wx.EVT_RIGHT_DOWN, self.m_buttonDebugMenuOnContextMenu )

		fgSizer6.Add( self.m_buttonDebugMenu, 1, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_buttonClose = wx.Button( self.m_panelMain, wx.ID_CANCEL, _(u"Close"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_buttonClose.Hide()

		fgSizer6.Add( self.m_buttonClose, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )

		self.m_buttonStop = wx.Button( self.m_panelMain, wx.ID_STOP, _(u"Stop"), wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer6.Add( self.m_buttonStop, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )

		self.m_buttonSave = wx.Button( self.m_panelMain, wx.ID_SAVE, _(u"Save"), wx.DefaultPosition, wx.DefaultSize, 0 )

		self.m_buttonSave.SetDefault()
		self.m_buttonSave.Enable( False )

		fgSizer6.Add( self.m_buttonSave, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )


		fgSizer2.Add( fgSizer6, 1, wx.ALIGN_RIGHT, 5 )


		self.m_panelMain.SetSizer( fgSizer2 )
		self.m_panelMain.Layout()
		fgSizer2.Fit( self.m_panelMain )
		bSizer1.Add( self.m_panelMain, 1, wx.EXPAND |wx.ALL, 5 )


		self.SetSizer( bSizer1 )
		self.Layout()
		bSizer1.Fit( self )

		self.Centre( wx.BOTH )

		# Connect Events
		self.Bind( wx.EVT_CLOSE, self.onClose )
		self.m_textErrorDetails.Bind( wx.EVT_LEFT_UP, self.onTextErrorDetailsClick )
		self.m_textShowDetails.Bind( wx.EVT_LEFT_UP, self.onTextShowDetailsClick )
		self.m_textHideDetails.Bind( wx.EVT_LEFT_UP, self.onTextHideDetailsClick )
		self.m_buttonDebugMenu.Bind( wx.EVT_BUTTON, self.onButtonDebugMenuClick )
		self.Bind( wx.EVT_MENU, self.onMenuItemEnableSaveClick, id = self.m_menuItemEnableSave.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuItemDumpSubWordsClick, id = self.m_menuItemDumpSubWords.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuItemDumpRefWordsClick, id = self.m_menuItemDumpRefWords.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuItemDumpAllSyncPointsClick, id = self.m_menuItemDumpAllSyncPoints.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuItemDumpUsedSyncPointsClick, id = self.m_menuItemDumpUsedSyncPoints.GetId() )
		self.m_buttonStop.Bind( wx.EVT_BUTTON, self.onButtonStopClick )
		self.m_buttonSave.Bind( wx.EVT_BUTTON, self.onButtonSaveClick )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def onClose( self, event ):
		event.Skip()

	def onTextErrorDetailsClick( self, event ):
		event.Skip()

	def onTextShowDetailsClick( self, event ):
		event.Skip()

	def onTextHideDetailsClick( self, event ):
		event.Skip()

	def onButtonDebugMenuClick( self, event ):
		event.Skip()

	def onMenuItemEnableSaveClick( self, event ):
		event.Skip()

	def onMenuItemDumpSubWordsClick( self, event ):
		event.Skip()

	def onMenuItemDumpRefWordsClick( self, event ):
		event.Skip()

	def onMenuItemDumpAllSyncPointsClick( self, event ):
		event.Skip()

	def onMenuItemDumpUsedSyncPointsClick( self, event ):
		event.Skip()

	def onButtonStopClick( self, event ):
		event.Skip()

	def onButtonSaveClick( self, event ):
		event.Skip()

	def m_buttonDebugMenuOnContextMenu( self, event ):
		self.m_buttonDebugMenu.PopupMenu( self.m_menuDebug, event.GetPosition() )


