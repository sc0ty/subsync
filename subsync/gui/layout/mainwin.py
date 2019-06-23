# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Dec  3 2017)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

from subsync.gui.subpanel import SubPanel
from subsync.gui.subpanel import RefPanel
import wx
import wx.xrc


###########################################################################
## Class MainWin
###########################################################################

class MainWin ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"Subtitle Speech Synchronizer"), pos = wx.DefaultPosition, size = wx.Size( -1,-1 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL, name = u"Subtitle Speech Synchronizer" )
		
		self.SetSizeHints( wx.Size( -1,-1 ), wx.DefaultSize )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_panelMain = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer2 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_panel2 = wx.Panel( self.m_panelMain, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		fgSizer1 = wx.FlexGridSizer( 0, 1, 0, 0 )
		fgSizer1.AddGrowableCol( 0 )
		fgSizer1.AddGrowableRow( 5 )
		fgSizer1.SetFlexibleDirection( wx.BOTH )
		fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText3 = wx.StaticText( self.m_panel2, wx.ID_ANY, _(u"Subtitles:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )
		fgSizer1.Add( self.m_staticText3, 0, wx.EXPAND|wx.TOP|wx.RIGHT|wx.LEFT, 5 )
		
		self.m_panelSub = SubPanel( self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		fgSizer1.Add( self.m_panelSub, 1, wx.EXPAND |wx.ALL, 5 )
		
		self.m_staticText31 = wx.StaticText( self.m_panel2, wx.ID_ANY, _(u"References (your video):"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText31.Wrap( -1 )
		fgSizer1.Add( self.m_staticText31, 0, wx.TOP|wx.RIGHT|wx.LEFT|wx.EXPAND, 5 )
		
		self.m_panelRef = RefPanel( self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		fgSizer1.Add( self.m_panelRef, 1, wx.EXPAND |wx.ALL, 5 )
		
		fgSizer5 = wx.FlexGridSizer( 1, 0, 0, 0 )
		fgSizer5.AddGrowableCol( 1 )
		fgSizer5.AddGrowableRow( 0 )
		fgSizer5.SetFlexibleDirection( wx.BOTH )
		fgSizer5.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText32 = wx.StaticText( self.m_panel2, wx.ID_ANY, _(u"Max adjustment"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText32.Wrap( -1 )
		fgSizer5.Add( self.m_staticText32, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_sliderMaxDist = wx.Slider( self.m_panel2, wx.ID_ANY, 30, 5, 180, wx.DefaultPosition, wx.DefaultSize, wx.SL_HORIZONTAL )
		fgSizer5.Add( self.m_sliderMaxDist, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		self.m_textMaxDist = wx.StaticText( self.m_panel2, wx.ID_ANY, _(u"999 min"), wx.DefaultPosition, wx.DefaultSize, wx.ST_NO_AUTORESIZE )
		self.m_textMaxDist.Wrap( -1 )
		fgSizer5.Add( self.m_textMaxDist, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT|wx.ALL|wx.EXPAND|wx.FIXED_MINSIZE, 5 )
		
		
		fgSizer1.Add( fgSizer5, 1, wx.EXPAND|wx.TOP|wx.BOTTOM, 5 )
		
		
		fgSizer1.Add( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.m_staticline1 = wx.StaticLine( self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		fgSizer1.Add( self.m_staticline1, 0, wx.EXPAND |wx.ALL, 5 )
		
		fgSizer8 = wx.FlexGridSizer( 1, 0, 0, 0 )
		fgSizer8.SetFlexibleDirection( wx.BOTH )
		fgSizer8.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_buttonMenu = wx.Button( self.m_panel2, wx.ID_ANY, _(u"Menu"), wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT )
		self.m_menu = wx.Menu()
		self.m_menuItemBatchProcessing = wx.MenuItem( self.m_menu, wx.ID_ANY, _(u"Batch processing"), wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu.Append( self.m_menuItemBatchProcessing )
		
		self.m_menu.AppendSeparator()
		
		self.m_menuItemSettings = wx.MenuItem( self.m_menu, wx.ID_PROPERTIES, _(u"Settings"), wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu.Append( self.m_menuItemSettings )
		
		self.m_menu.AppendSeparator()
		
		self.m_menuItemCheckUpdate = wx.MenuItem( self.m_menu, wx.ID_ANY, _(u"Check for updates"), wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu.Append( self.m_menuItemCheckUpdate )
		
		self.m_menuItemAbout = wx.MenuItem( self.m_menu, wx.ID_ABOUT, _(u"About"), wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu.Append( self.m_menuItemAbout )
		
		self.m_buttonMenu.Bind( wx.EVT_RIGHT_DOWN, self.m_buttonMenuOnContextMenu ) 
		
		fgSizer8.Add( self.m_buttonMenu, 1, wx.ALL|wx.EXPAND, 5 )
		
		self.m_buttonClose = wx.Button( self.m_panel2, wx.ID_CLOSE, _(u"Close"), wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer8.Add( self.m_buttonClose, 1, wx.ALL|wx.EXPAND, 5 )
		
		self.m_buttonStart = wx.Button( self.m_panel2, wx.ID_OK, _(u"Start"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_buttonStart.SetDefault() 
		fgSizer8.Add( self.m_buttonStart, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		fgSizer1.Add( fgSizer8, 1, wx.ALIGN_RIGHT, 5 )
		
		
		self.m_panel2.SetSizer( fgSizer1 )
		self.m_panel2.Layout()
		fgSizer1.Fit( self.m_panel2 )
		bSizer2.Add( self.m_panel2, 1, wx.EXPAND|wx.ALL, 5 )
		
		
		self.m_panelMain.SetSizer( bSizer2 )
		self.m_panelMain.Layout()
		bSizer2.Fit( self.m_panelMain )
		bSizer1.Add( self.m_panelMain, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
		bSizer1.Fit( self )
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.Bind( wx.EVT_CLOSE, self.onClose )
		self.m_sliderMaxDist.Bind( wx.EVT_SCROLL, self.onSliderMaxDistScroll )
		self.m_buttonMenu.Bind( wx.EVT_BUTTON, self.onButtonMenuClick )
		self.Bind( wx.EVT_MENU, self.onMenuItemBatchProcessingClick, id = self.m_menuItemBatchProcessing.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuItemSettingsClick, id = self.m_menuItemSettings.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuItemCheckUpdateClick, id = self.m_menuItemCheckUpdate.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuItemAboutClick, id = self.m_menuItemAbout.GetId() )
		self.m_buttonClose.Bind( wx.EVT_BUTTON, self.onButtonCloseClick )
		self.m_buttonStart.Bind( wx.EVT_BUTTON, self.onButtonStartClick )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onClose( self, event ):
		event.Skip()
	
	def onSliderMaxDistScroll( self, event ):
		event.Skip()
	
	def onButtonMenuClick( self, event ):
		event.Skip()
	
	def onMenuItemBatchProcessingClick( self, event ):
		event.Skip()
	
	def onMenuItemSettingsClick( self, event ):
		event.Skip()
	
	def onMenuItemCheckUpdateClick( self, event ):
		event.Skip()
	
	def onMenuItemAboutClick( self, event ):
		event.Skip()
	
	def onButtonCloseClick( self, event ):
		event.Skip()
	
	def onButtonStartClick( self, event ):
		event.Skip()
	
	def m_buttonMenuOnContextMenu( self, event ):
		self.m_buttonMenu.PopupMenu( self.m_menu, event.GetPosition() )
		

