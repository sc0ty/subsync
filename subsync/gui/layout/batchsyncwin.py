# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Dec  3 2017)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

from subsync.gui.components.iconlist import IconList
import wx
import wx.xrc


###########################################################################
## Class BatchSyncWin
###########################################################################

class BatchSyncWin ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"Batch Synchronization"), pos = wx.DefaultPosition, size = wx.Size( 800,600 ), style = wx.CAPTION|wx.CLOSE_BOX|wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.MINIMIZE_BOX|wx.RESIZE_BORDER )
		
		self.SetSizeHints( wx.Size( 600,480 ), wx.DefaultSize )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_panel1 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		fgSizer1 = wx.FlexGridSizer( 0, 1, 0, 0 )
		fgSizer1.AddGrowableCol( 0 )
		fgSizer1.AddGrowableRow( 2 )
		fgSizer1.SetFlexibleDirection( wx.BOTH )
		fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		fgSizer2 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer2.AddGrowableCol( 1 )
		fgSizer2.SetFlexibleDirection( wx.BOTH )
		fgSizer2.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_textCurrentProgress = wx.StaticText( self.m_panel1, wx.ID_ANY, _(u"Current file:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textCurrentProgress.Wrap( -1 )
		fgSizer2.Add( self.m_textCurrentProgress, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_gaugeCurrentProgress = wx.Gauge( self.m_panel1, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL )
		self.m_gaugeCurrentProgress.SetValue( 0 ) 
		fgSizer2.Add( self.m_gaugeCurrentProgress, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_textTotalProgress = wx.StaticText( self.m_panel1, wx.ID_ANY, _(u"Total progress:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textTotalProgress.Wrap( -1 )
		fgSizer2.Add( self.m_textTotalProgress, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_gaugeTotalProgress = wx.Gauge( self.m_panel1, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL )
		self.m_gaugeTotalProgress.SetValue( 0 ) 
		fgSizer2.Add( self.m_gaugeTotalProgress, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )
		
		
		fgSizer1.Add( fgSizer2, 1, wx.EXPAND, 5 )
		
		self.m_textEta = wx.StaticText( self.m_panel1, wx.ID_ANY, _(u"Initializing..."), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textEta.Wrap( -1 )
		fgSizer1.Add( self.m_textEta, 0, wx.ALL, 5 )
		
		self.m_items = IconList( self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_ALIGN_LEFT|wx.LC_NO_HEADER|wx.LC_NO_SORT_HEADER|wx.LC_REPORT|wx.LC_SINGLE_SEL )
		fgSizer1.Add( self.m_items, 0, wx.ALL|wx.EXPAND, 5 )
		
		fgSizer3 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer3.SetFlexibleDirection( wx.BOTH )
		fgSizer3.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_textStatusTitle = wx.StaticText( self.m_panel1, wx.ID_ANY, _(u"status:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textStatusTitle.Wrap( -1 )
		fgSizer3.Add( self.m_textStatusTitle, 0, wx.RIGHT|wx.LEFT|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		fgSizer4 = wx.FlexGridSizer( 1, 0, 0, 0 )
		fgSizer4.SetFlexibleDirection( wx.BOTH )
		fgSizer4.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_bitmapTick = wx.StaticBitmap( self.m_panel1, wx.ID_ANY, wx.ArtProvider.GetBitmap( wx.ART_TICK_MARK, wx.ART_MENU ), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_bitmapTick.Hide()
		
		fgSizer4.Add( self.m_bitmapTick, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )
		
		self.m_bitmapCross = wx.StaticBitmap( self.m_panel1, wx.ID_ANY, wx.ArtProvider.GetBitmap( wx.ART_CROSS_MARK, wx.ART_MENU ), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_bitmapCross.Hide()
		
		fgSizer4.Add( self.m_bitmapCross, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )
		
		self.m_textStatus = wx.StaticText( self.m_panel1, wx.ID_ANY, _(u"-"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textStatus.Wrap( -1 )
		fgSizer4.Add( self.m_textStatus, 0, wx.RIGHT|wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_textErrorTitle = wx.StaticText( self.m_panel1, wx.ID_ANY, _(u"errors"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textErrorTitle.Wrap( -1 )
		self.m_textErrorTitle.SetForegroundColour( wx.Colour( 255, 0, 0 ) )
		self.m_textErrorTitle.Hide()
		
		fgSizer4.Add( self.m_textErrorTitle, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.LEFT, 5 )
		
		self.m_textErrorDetails = wx.StaticText( self.m_panel1, wx.ID_ANY, _(u"[show]"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textErrorDetails.Wrap( -1 )
		self.m_textErrorDetails.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_HIGHLIGHT ) )
		self.m_textErrorDetails.Hide()
		
		fgSizer4.Add( self.m_textErrorDetails, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 5 )
		
		
		fgSizer3.Add( fgSizer4, 1, wx.EXPAND, 5 )
		
		self.m_textPointsTitle = wx.StaticText( self.m_panel1, wx.ID_ANY, _(u"points:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textPointsTitle.Wrap( -1 )
		fgSizer3.Add( self.m_textPointsTitle, 0, wx.RIGHT|wx.LEFT|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_textPoints = wx.StaticText( self.m_panel1, wx.ID_ANY, _(u"-"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textPoints.Wrap( -1 )
		fgSizer3.Add( self.m_textPoints, 0, wx.RIGHT|wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_textCorrelationTitle = wx.StaticText( self.m_panel1, wx.ID_ANY, _(u"correlation:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textCorrelationTitle.Wrap( -1 )
		fgSizer3.Add( self.m_textCorrelationTitle, 0, wx.RIGHT|wx.LEFT|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_textCorrelation = wx.StaticText( self.m_panel1, wx.ID_ANY, _(u"-"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textCorrelation.Wrap( -1 )
		fgSizer3.Add( self.m_textCorrelation, 0, wx.RIGHT|wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_textFormulaTitle = wx.StaticText( self.m_panel1, wx.ID_ANY, _(u"formula:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textFormulaTitle.Wrap( -1 )
		fgSizer3.Add( self.m_textFormulaTitle, 0, wx.RIGHT|wx.LEFT|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_textFormula = wx.StaticText( self.m_panel1, wx.ID_ANY, _(u"-"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textFormula.Wrap( -1 )
		fgSizer3.Add( self.m_textFormula, 0, wx.RIGHT|wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_textMaxChangeTitle = wx.StaticText( self.m_panel1, wx.ID_ANY, _(u"max change:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textMaxChangeTitle.Wrap( -1 )
		fgSizer3.Add( self.m_textMaxChangeTitle, 0, wx.BOTTOM|wx.RIGHT|wx.LEFT|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_textMaxChange = wx.StaticText( self.m_panel1, wx.ID_ANY, _(u"-"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textMaxChange.Wrap( -1 )
		fgSizer3.Add( self.m_textMaxChange, 0, wx.BOTTOM|wx.RIGHT|wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		fgSizer1.Add( fgSizer3, 1, wx.EXPAND, 5 )
		
		self.m_staticline1 = wx.StaticLine( self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		fgSizer1.Add( self.m_staticline1, 0, wx.EXPAND |wx.ALL, 5 )
		
		fgSizer5 = wx.FlexGridSizer( 1, 0, 0, 0 )
		fgSizer5.SetFlexibleDirection( wx.BOTH )
		fgSizer5.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_buttonFixFailed = wx.Button( self.m_panel1, wx.ID_OK, _(u"Fix failed"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_buttonFixFailed.Hide()
		
		fgSizer5.Add( self.m_buttonFixFailed, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )
		
		self.m_buttonClose = wx.Button( self.m_panel1, wx.ID_CANCEL, _(u"Close"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_buttonClose.Hide()
		
		fgSizer5.Add( self.m_buttonClose, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )
		
		self.m_buttonStop = wx.Button( self.m_panel1, wx.ID_STOP, _(u"Stop"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_buttonStop.SetDefault() 
		fgSizer5.Add( self.m_buttonStop, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )
		
		
		fgSizer1.Add( fgSizer5, 1, wx.ALIGN_RIGHT, 5 )
		
		
		self.m_panel1.SetSizer( fgSizer1 )
		self.m_panel1.Layout()
		fgSizer1.Fit( self.m_panel1 )
		bSizer1.Add( self.m_panel1, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.Bind( wx.EVT_CLOSE, self.onClose )
		self.m_items.Bind( wx.EVT_LIST_ITEM_SELECTED, self.onItemsSelected )
		self.m_textErrorDetails.Bind( wx.EVT_LEFT_UP, self.onTextErrorDetailsClick )
		self.m_buttonFixFailed.Bind( wx.EVT_BUTTON, self.onButtonFixFailedClick )
		self.m_buttonStop.Bind( wx.EVT_BUTTON, self.onButtonStopClick )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onClose( self, event ):
		event.Skip()
	
	def onItemsSelected( self, event ):
		event.Skip()
	
	def onTextErrorDetailsClick( self, event ):
		event.Skip()
	
	def onButtonFixFailedClick( self, event ):
		event.Skip()
	
	def onButtonStopClick( self, event ):
		event.Skip()
	

