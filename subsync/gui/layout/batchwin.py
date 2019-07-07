# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Dec  3 2017)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

from subsync.gui.components.multicolview import MultiColumnView
from subsync.gui.components.choicelang import ChoiceLang
from subsync.gui.components.choiceenc import ChoiceCharEnc
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
		fgSizer1.AddGrowableRow( 1 )
		fgSizer1.SetFlexibleDirection( wx.BOTH )
		fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		fgSizer2 = wx.FlexGridSizer( 0, 3, 0, 0 )
		fgSizer2.AddGrowableCol( 0 )
		fgSizer2.AddGrowableCol( 1 )
		fgSizer2.AddGrowableCol( 2 )
		fgSizer2.SetFlexibleDirection( wx.VERTICAL )
		fgSizer2.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_textSubs = wx.StaticText( self.m_panelMain, wx.ID_ANY, _(u"Subtitles:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textSubs.Wrap( -1 )
		self.m_textSubs.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )
		
		fgSizer2.Add( self.m_textSubs, 0, wx.TOP|wx.RIGHT|wx.LEFT|wx.EXPAND, 5 )
		
		self.m_textRefs = wx.StaticText( self.m_panelMain, wx.ID_ANY, _(u"References:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textRefs.Wrap( -1 )
		self.m_textRefs.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )
		
		fgSizer2.Add( self.m_textRefs, 0, wx.TOP|wx.RIGHT|wx.LEFT|wx.EXPAND, 5 )
		
		self.m_textOuts = wx.StaticText( self.m_panelMain, wx.ID_ANY, _(u"Outputs:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textOuts.Wrap( -1 )
		self.m_textOuts.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )
		
		fgSizer2.Add( self.m_textOuts, 0, wx.TOP|wx.RIGHT|wx.LEFT|wx.EXPAND, 5 )
		
		self.m_toolBarSub = wx.ToolBar( self.m_panelMain, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TB_HORIZONTAL ) 
		self.m_toolSubAdd = self.m_toolBarSub.AddLabelTool( wx.ID_ANY, _(u"Add files"), wx.ArtProvider.GetBitmap( wx.ART_PLUS, wx.ART_TOOLBAR ), wx.NullBitmap, wx.ITEM_NORMAL, _(u"Add files"), wx.EmptyString, None ) 
		
		self.m_toolSubRemove = self.m_toolBarSub.AddLabelTool( wx.ID_ANY, _(u"Remove files"), wx.ArtProvider.GetBitmap( wx.ART_MINUS, wx.ART_TOOLBAR ), wx.NullBitmap, wx.ITEM_NORMAL, _(u"Remove files"), wx.EmptyString, None ) 
		
		self.m_toolSubSelStream = self.m_toolBarSub.AddLabelTool( wx.ID_ANY, _(u"Select stream"), wx.ArtProvider.GetBitmap( wx.ART_LIST_VIEW, wx.ART_TOOLBAR ), wx.NullBitmap, wx.ITEM_NORMAL, _(u"Select stream"), wx.EmptyString, None ) 
		
		self.m_toolBarSub.Realize() 
		
		fgSizer2.Add( self.m_toolBarSub, 0, wx.EXPAND, 5 )
		
		self.m_toolBarRef = wx.ToolBar( self.m_panelMain, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TB_HORIZONTAL ) 
		self.m_toolRefAdd = self.m_toolBarRef.AddLabelTool( wx.ID_ANY, _(u"Add files"), wx.ArtProvider.GetBitmap( wx.ART_PLUS, wx.ART_TOOLBAR ), wx.NullBitmap, wx.ITEM_NORMAL, _(u"Add files"), wx.EmptyString, None ) 
		
		self.m_toolRefRemove = self.m_toolBarRef.AddLabelTool( wx.ID_ANY, _(u"Remove files"), wx.ArtProvider.GetBitmap( wx.ART_MINUS, wx.ART_TOOLBAR ), wx.NullBitmap, wx.ITEM_NORMAL, _(u"Remove files"), wx.EmptyString, None ) 
		
		self.m_toolRefSelStream = self.m_toolBarRef.AddLabelTool( wx.ID_ANY, _(u"Select stream"), wx.ArtProvider.GetBitmap( wx.ART_LIST_VIEW, wx.ART_TOOLBAR ), wx.NullBitmap, wx.ITEM_NORMAL, _(u"Select stream"), wx.EmptyString, None ) 
		
		self.m_toolBarRef.Realize() 
		
		fgSizer2.Add( self.m_toolBarRef, 0, wx.EXPAND, 5 )
		
		self.m_toolBarOut = wx.ToolBar( self.m_panelMain, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TB_HORIZONTAL ) 
		self.m_toolOutPattern = self.m_toolBarOut.AddLabelTool( wx.ID_ANY, _(u"Set file names"), wx.ArtProvider.GetBitmap( wx.ART_LIST_VIEW, wx.ART_TOOLBAR ), wx.NullBitmap, wx.ITEM_NORMAL, _(u"Set file names"), wx.EmptyString, None ) 
		
		self.m_toolBarOut.Realize() 
		
		fgSizer2.Add( self.m_toolBarOut, 0, wx.EXPAND, 5 )
		
		
		fgSizer1.Add( fgSizer2, 1, wx.EXPAND, 5 )
		
		self.m_items = MultiColumnView( self.m_panelMain, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.FULL_REPAINT_ON_RESIZE|wx.VSCROLL )
		self.m_items.SetScrollRate( 5, 5 )
		self.m_items.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )
		self.m_items.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
		
		fgSizer1.Add( self.m_items, 1, wx.EXPAND|wx.BOTTOM|wx.RIGHT|wx.LEFT, 5 )
		
		fgSizer3 = wx.FlexGridSizer( 1, 0, 0, 0 )
		fgSizer3.AddGrowableCol( 1 )
		fgSizer3.SetFlexibleDirection( wx.BOTH )
		fgSizer3.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_textSelectedLabel = wx.StaticText( self.m_panelMain, wx.ID_ANY, _(u"selected:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textSelectedLabel.Wrap( -1 )
		fgSizer3.Add( self.m_textSelectedLabel, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL|wx.ALIGN_RIGHT, 5 )
		
		self.m_textSelected = wx.TextCtrl( self.m_panelMain, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY )
		fgSizer3.Add( self.m_textSelected, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )
		
		self.m_buttonSelStream = wx.Button( self.m_panelMain, wx.ID_ANY, _(u"Select Stream"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_buttonSelStream.Enable( False )
		
		fgSizer3.Add( self.m_buttonSelStream, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		fgSizer1.Add( fgSizer3, 1, wx.EXPAND, 5 )
		
		fgSizer4 = wx.FlexGridSizer( 0, 1, 0, 0 )
		fgSizer4.AddGrowableCol( 0 )
		fgSizer4.SetFlexibleDirection( wx.BOTH )
		fgSizer4.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_panelSettings = wx.Panel( self.m_panelMain, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		fgSizer5 = wx.FlexGridSizer( 0, 3, 0, 0 )
		fgSizer5.AddGrowableCol( 2 )
		fgSizer5.SetFlexibleDirection( wx.BOTH )
		fgSizer5.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		fgSizer6 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer6.AddGrowableCol( 1 )
		fgSizer6.SetFlexibleDirection( wx.BOTH )
		fgSizer6.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_textLang = wx.StaticText( self.m_panelSettings, wx.ID_ANY, _(u"Language:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textLang.Wrap( -1 )
		fgSizer6.Add( self.m_textLang, 0, wx.TOP|wx.RIGHT|wx.LEFT|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		m_choiceLangChoices = []
		self.m_choiceLang = ChoiceLang( self.m_panelSettings, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choiceLangChoices, 0 )
		self.m_choiceLang.SetSelection( 0 )
		self.m_choiceLang.Enable( False )
		
		fgSizer6.Add( self.m_choiceLang, 0, wx.ALIGN_CENTER_VERTICAL|wx.EXPAND|wx.TOP|wx.RIGHT|wx.LEFT, 5 )
		
		self.m_textEnc = wx.StaticText( self.m_panelSettings, wx.ID_ANY, _(u"Character encoding:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textEnc.Wrap( -1 )
		fgSizer6.Add( self.m_textEnc, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT|wx.ALL, 5 )
		
		m_choiceEncChoices = []
		self.m_choiceEnc = ChoiceCharEnc( self.m_panelSettings, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choiceEncChoices, 0 )
		self.m_choiceEnc.SetSelection( 0 )
		self.m_choiceEnc.Enable( False )
		
		fgSizer6.Add( self.m_choiceEnc, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		
		fgSizer5.Add( fgSizer6, 1, wx.EXPAND, 5 )
		
		self.m_staticline3 = wx.StaticLine( self.m_panelSettings, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
		fgSizer5.Add( self.m_staticline3, 0, wx.EXPAND |wx.ALL, 5 )
		
		fgSizer7 = wx.FlexGridSizer( 0, 4, 0, 0 )
		fgSizer7.AddGrowableCol( 2 )
		fgSizer7.SetFlexibleDirection( wx.BOTH )
		fgSizer7.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_textMaxDistLabel = wx.StaticText( self.m_panelSettings, wx.ID_ANY, _(u"Max adjustment:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textMaxDistLabel.Wrap( -1 )
		fgSizer7.Add( self.m_textMaxDistLabel, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.RIGHT|wx.LEFT, 5 )
		
		self.m_buttonMaxDistInfo = PopupInfoButton( self.m_panelSettings, wx.ID_ANY, wx.ArtProvider.GetBitmap( wx.ART_TIP, wx.ART_BUTTON ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|wx.NO_BORDER )
		fgSizer7.Add( self.m_buttonMaxDistInfo, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )
		
		self.m_sliderMaxDist = wx.Slider( self.m_panelSettings, wx.ID_ANY, 30, 5, 180, wx.DefaultPosition, wx.DefaultSize, wx.SL_HORIZONTAL )
		fgSizer7.Add( self.m_sliderMaxDist, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND|wx.TOP|wx.RIGHT|wx.LEFT, 5 )
		
		self.m_textMaxDist = wx.StaticText( self.m_panelSettings, wx.ID_ANY, _(u"999 min"), wx.DefaultPosition, wx.DefaultSize, wx.ST_NO_AUTORESIZE )
		self.m_textMaxDist.Wrap( -1 )
		fgSizer7.Add( self.m_textMaxDist, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.RIGHT|wx.LEFT, 5 )
		
		self.m_textEffortLabel = wx.StaticText( self.m_panelSettings, wx.ID_ANY, _(u"Effort:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textEffortLabel.Wrap( -1 )
		fgSizer7.Add( self.m_textEffortLabel, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		self.m_buttonEffortInfo = PopupInfoButton( self.m_panelSettings, wx.ID_ANY, wx.ArtProvider.GetBitmap( wx.ART_TIP, wx.ART_BUTTON ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|wx.NO_BORDER )
		fgSizer7.Add( self.m_buttonEffortInfo, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5 )
		
		self.m_sliderEffort = wx.Slider( self.m_panelSettings, wx.ID_ANY, 50, 0, 100, wx.DefaultPosition, wx.DefaultSize, wx.SL_HORIZONTAL )
		fgSizer7.Add( self.m_sliderEffort, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND|wx.ALL, 5 )
		
		self.m_textEffort = wx.StaticText( self.m_panelSettings, wx.ID_ANY, _(u"0.50"), wx.DefaultPosition, wx.DefaultSize, wx.ST_NO_AUTORESIZE )
		self.m_textEffort.Wrap( -1 )
		fgSizer7.Add( self.m_textEffort, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		fgSizer5.Add( fgSizer7, 1, wx.EXPAND, 5 )
		
		
		self.m_panelSettings.SetSizer( fgSizer5 )
		self.m_panelSettings.Layout()
		fgSizer5.Fit( self.m_panelSettings )
		fgSizer4.Add( self.m_panelSettings, 0, wx.EXPAND, 5 )
		
		self.m_panelDrop = wx.Panel( self.m_panelMain, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_panelDrop.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
		self.m_panelDrop.Hide()
		
		bSizer8 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_textDrop = wx.StaticText( self.m_panelDrop, wx.ID_ANY, _(u"Drop files here to sort subtitles and references automatically"), wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE|wx.ST_ELLIPSIZE_MIDDLE )
		self.m_textDrop.Wrap( -1 )
		self.m_textDrop.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )
		
		bSizer8.Add( self.m_textDrop, 0, wx.ALL|wx.EXPAND, 20 )
		
		
		self.m_panelDrop.SetSizer( bSizer8 )
		self.m_panelDrop.Layout()
		bSizer8.Fit( self.m_panelDrop )
		fgSizer4.Add( self.m_panelDrop, 1, wx.EXPAND |wx.ALL, 5 )
		
		self.m_panelProgress = wx.Panel( self.m_panelMain, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_panelProgress.Hide()
		
		fgSizer9 = wx.FlexGridSizer( 0, 1, 0, 0 )
		fgSizer9.AddGrowableCol( 0 )
		fgSizer9.AddGrowableRow( 0 )
		fgSizer9.SetFlexibleDirection( wx.BOTH )
		fgSizer9.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_textStatus = wx.StaticText( self.m_panelProgress, wx.ID_ANY, _(u"Initializing..."), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textStatus.Wrap( -1 )
		fgSizer9.Add( self.m_textStatus, 0, wx.TOP|wx.RIGHT|wx.LEFT, 5 )
		
		self.m_gaugeProgress = wx.Gauge( self.m_panelProgress, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL )
		self.m_gaugeProgress.SetValue( 0 ) 
		fgSizer9.Add( self.m_gaugeProgress, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticline2 = wx.StaticLine( self.m_panelProgress, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		fgSizer9.Add( self.m_staticline2, 0, wx.EXPAND |wx.ALL, 5 )
		
		fgSizer10 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer10.AddGrowableCol( 0 )
		fgSizer10.AddGrowableCol( 1 )
		fgSizer10.SetFlexibleDirection( wx.BOTH )
		fgSizer10.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		fgSizer11 = wx.FlexGridSizer( 0, 1, 0, 0 )
		fgSizer11.AddGrowableCol( 0 )
		fgSizer11.SetFlexibleDirection( wx.BOTH )
		fgSizer11.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		fgSizer12 = wx.FlexGridSizer( 1, 0, 0, 0 )
		fgSizer12.AddGrowableCol( 2 )
		fgSizer12.AddGrowableRow( 0 )
		fgSizer12.SetFlexibleDirection( wx.BOTH )
		fgSizer12.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_bitmapTick = wx.StaticBitmap( self.m_panelProgress, wx.ID_ANY, wx.ArtProvider.GetBitmap( wx.ART_TICK_MARK, wx.ART_MENU ), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_bitmapTick.Hide()
		
		fgSizer12.Add( self.m_bitmapTick, 0, wx.EXPAND|wx.TOP|wx.LEFT, 5 )
		
		self.m_bitmapCross = wx.StaticBitmap( self.m_panelProgress, wx.ID_ANY, wx.ArtProvider.GetBitmap( wx.ART_CROSS_MARK, wx.ART_MENU ), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_bitmapCross.Hide()
		
		fgSizer12.Add( self.m_bitmapCross, 0, wx.TOP|wx.LEFT, 5 )
		
		self.m_textFileStatus = wx.StaticText( self.m_panelProgress, wx.ID_ANY, _(u"Initializing..."), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textFileStatus.Wrap( -1 )
		fgSizer12.Add( self.m_textFileStatus, 0, wx.TOP|wx.RIGHT|wx.LEFT, 5 )
		
		
		fgSizer11.Add( fgSizer12, 1, wx.EXPAND, 5 )
		
		self.m_gaugeFileProgress = wx.Gauge( self.m_panelProgress, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL )
		self.m_gaugeFileProgress.SetValue( 0 ) 
		fgSizer11.Add( self.m_gaugeFileProgress, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		fgSizer10.Add( fgSizer11, 1, wx.EXPAND, 5 )
		
		self.m_panelError = wx.Panel( self.m_panelProgress, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_panelError.Hide()
		
		fgSizer13 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer13.AddGrowableCol( 1 )
		fgSizer13.AddGrowableRow( 0 )
		fgSizer13.SetFlexibleDirection( wx.BOTH )
		fgSizer13.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_bitmapErrorIcon = wx.StaticBitmap( self.m_panelError, wx.ID_ANY, wx.ArtProvider.GetBitmap( wx.ART_WARNING, wx.ART_CMN_DIALOG ), wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer13.Add( self.m_bitmapErrorIcon, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT|wx.TOP|wx.BOTTOM|wx.LEFT, 5 )
		
		fgSizer14 = wx.FlexGridSizer( 0, 1, 0, 0 )
		fgSizer14.AddGrowableCol( 0 )
		fgSizer14.AddGrowableRow( 0 )
		fgSizer14.AddGrowableRow( 1 )
		fgSizer14.SetFlexibleDirection( wx.BOTH )
		fgSizer14.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_textErrorMsg = wx.StaticText( self.m_panelError, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textErrorMsg.Wrap( -1 )
		fgSizer14.Add( self.m_textErrorMsg, 0, wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.RIGHT|wx.LEFT, 5 )
		
		self.m_textErrorDetails = wx.StaticText( self.m_panelError, wx.ID_ANY, _(u"[details]"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textErrorDetails.Wrap( -1 )
		self.m_textErrorDetails.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_HIGHLIGHT ) )
		
		fgSizer14.Add( self.m_textErrorDetails, 0, wx.ALIGN_CENTER_VERTICAL|wx.BOTTOM|wx.RIGHT|wx.LEFT, 5 )
		
		
		fgSizer13.Add( fgSizer14, 1, wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )
		
		
		self.m_panelError.SetSizer( fgSizer13 )
		self.m_panelError.Layout()
		fgSizer13.Fit( self.m_panelError )
		fgSizer10.Add( self.m_panelError, 0, wx.ALIGN_BOTTOM|wx.EXPAND|wx.LEFT, 20 )
		
		
		fgSizer9.Add( fgSizer10, 1, wx.EXPAND, 5 )
		
		
		self.m_panelProgress.SetSizer( fgSizer9 )
		self.m_panelProgress.Layout()
		fgSizer9.Fit( self.m_panelProgress )
		fgSizer4.Add( self.m_panelProgress, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		fgSizer1.Add( fgSizer4, 1, wx.EXPAND, 5 )
		
		self.m_staticline1 = wx.StaticLine( self.m_panelMain, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		fgSizer1.Add( self.m_staticline1, 0, wx.EXPAND |wx.ALL, 5 )
		
		fgSizer15 = wx.FlexGridSizer( 1, 0, 0, 0 )
		fgSizer15.SetFlexibleDirection( wx.BOTH )
		fgSizer15.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_buttonMenu = wx.Button( self.m_panelMain, wx.ID_ANY, _(u"Menu"), wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT )
		self.m_menu = wx.Menu()
		self.m_menuItemImportList = wx.MenuItem( self.m_menu, wx.ID_ANY, _(u"Import file list"), wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu.Append( self.m_menuItemImportList )
		
		self.m_menuItemExportList = wx.MenuItem( self.m_menu, wx.ID_ANY, _(u"Export file list"), wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu.Append( self.m_menuItemExportList )
		
		self.m_menu.AppendSeparator()
		
		self.m_menuItemClearList = wx.MenuItem( self.m_menu, wx.ID_ANY, _(u"Clear file list"), wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu.Append( self.m_menuItemClearList )
		
		self.m_buttonMenu.Bind( wx.EVT_RIGHT_DOWN, self.m_buttonMenuOnContextMenu ) 
		
		fgSizer15.Add( self.m_buttonMenu, 1, wx.ALL|wx.EXPAND, 5 )
		
		self.m_buttonClose = wx.Button( self.m_panelMain, wx.ID_CLOSE, _(u"Close"), wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer15.Add( self.m_buttonClose, 1, wx.ALL|wx.EXPAND, 5 )
		
		self.m_buttonStart = wx.Button( self.m_panelMain, wx.ID_OK, _(u"Start"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_buttonStart.SetDefault() 
		self.m_buttonStart.Enable( False )
		
		fgSizer15.Add( self.m_buttonStart, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		fgSizer1.Add( fgSizer15, 0, wx.ALIGN_RIGHT, 5 )
		
		
		self.m_panelMain.SetSizer( fgSizer1 )
		self.m_panelMain.Layout()
		fgSizer1.Fit( self.m_panelMain )
		bSizer1.Add( self.m_panelMain, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
		self.m_menuItems = wx.Menu()
		self.m_menuItemsRemove = wx.MenuItem( self.m_menuItems, wx.ID_ANY, _(u"Remove"), wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuItems.Append( self.m_menuItemsRemove )
		
		self.m_menuItemsProps = wx.MenuItem( self.m_menuItems, wx.ID_ANY, _(u"Properties"), wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuItems.Append( self.m_menuItemsProps )
		
		self.Bind( wx.EVT_RIGHT_DOWN, self.BatchWinOnContextMenu ) 
		
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.Bind( wx.EVT_CLOSE, self.onClose )
		self.Bind( wx.EVT_TOOL, self.onSubAddClick, id = self.m_toolSubAdd.GetId() )
		self.Bind( wx.EVT_TOOL, self.onSubRemoveClick, id = self.m_toolSubRemove.GetId() )
		self.Bind( wx.EVT_TOOL, self.onSubSelStreamClick, id = self.m_toolSubSelStream.GetId() )
		self.Bind( wx.EVT_TOOL, self.onRefAddClick, id = self.m_toolRefAdd.GetId() )
		self.Bind( wx.EVT_TOOL, self.onRefRemoveClick, id = self.m_toolRefRemove.GetId() )
		self.Bind( wx.EVT_TOOL, self.onRefSelStreamClick, id = self.m_toolRefSelStream.GetId() )
		self.Bind( wx.EVT_TOOL, self.onOutPatternClick, id = self.m_toolOutPattern.GetId() )
		self.m_items.Bind( wx.EVT_LEFT_DCLICK, self.onItemsLeftDClick )
		self.m_buttonSelStream.Bind( wx.EVT_BUTTON, self.onButtonSelStreamClick )
		self.m_choiceLang.Bind( wx.EVT_CHOICE, self.onChoiceLangChoice )
		self.m_choiceEnc.Bind( wx.EVT_CHOICE, self.onChoiceEncChoice )
		self.m_sliderMaxDist.Bind( wx.EVT_SCROLL, self.onSliderMaxDistScroll )
		self.m_sliderEffort.Bind( wx.EVT_SCROLL, self.onSliderEffortScroll )
		self.m_textErrorDetails.Bind( wx.EVT_LEFT_UP, self.onTextErrorDetailsClick )
		self.m_buttonMenu.Bind( wx.EVT_BUTTON, self.onButtonMenuClick )
		self.Bind( wx.EVT_MENU, self.onMenuItemImportListClick, id = self.m_menuItemImportList.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuItemExportListClick, id = self.m_menuItemExportList.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuItemClearListClick, id = self.m_menuItemClearList.GetId() )
		self.m_buttonClose.Bind( wx.EVT_BUTTON, self.onButtonCloseClick )
		self.m_buttonStart.Bind( wx.EVT_BUTTON, self.onButtonStartClick )
		self.Bind( wx.EVT_MENU, self.onMenuItemsRemoveClick, id = self.m_menuItemsRemove.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuItemsPropsClick, id = self.m_menuItemsProps.GetId() )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onClose( self, event ):
		event.Skip()
	
	def onSubAddClick( self, event ):
		event.Skip()
	
	def onSubRemoveClick( self, event ):
		event.Skip()
	
	def onSubSelStreamClick( self, event ):
		event.Skip()
	
	def onRefAddClick( self, event ):
		event.Skip()
	
	def onRefRemoveClick( self, event ):
		event.Skip()
	
	def onRefSelStreamClick( self, event ):
		event.Skip()
	
	def onOutPatternClick( self, event ):
		event.Skip()
	
	def onItemsLeftDClick( self, event ):
		event.Skip()
	
	def onButtonSelStreamClick( self, event ):
		event.Skip()
	
	def onChoiceLangChoice( self, event ):
		event.Skip()
	
	def onChoiceEncChoice( self, event ):
		event.Skip()
	
	def onSliderMaxDistScroll( self, event ):
		event.Skip()
	
	def onSliderEffortScroll( self, event ):
		event.Skip()
	
	def onTextErrorDetailsClick( self, event ):
		event.Skip()
	
	def onButtonMenuClick( self, event ):
		event.Skip()
	
	def onMenuItemImportListClick( self, event ):
		event.Skip()
	
	def onMenuItemExportListClick( self, event ):
		event.Skip()
	
	def onMenuItemClearListClick( self, event ):
		event.Skip()
	
	def onButtonCloseClick( self, event ):
		event.Skip()
	
	def onButtonStartClick( self, event ):
		event.Skip()
	
	def onMenuItemsRemoveClick( self, event ):
		event.Skip()
	
	def onMenuItemsPropsClick( self, event ):
		event.Skip()
	
	def m_buttonMenuOnContextMenu( self, event ):
		self.m_buttonMenu.PopupMenu( self.m_menu, event.GetPosition() )
		
	def BatchWinOnContextMenu( self, event ):
		self.PopupMenu( self.m_menuItems, event.GetPosition() )
		

