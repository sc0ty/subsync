# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Dec  3 2017)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc


###########################################################################
## Class AboutWin
###########################################################################

class AboutWin ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"About"), pos = wx.DefaultPosition, size = wx.DefaultSize, style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_panelMain = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		fgSizer1 = wx.FlexGridSizer( 0, 1, 0, 0 )
		fgSizer1.AddGrowableCol( 0 )
		fgSizer1.AddGrowableRow( 0 )
		fgSizer1.SetFlexibleDirection( wx.BOTH )
		fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		fgSizer2 = wx.FlexGridSizer( 1, 0, 0, 0 )
		fgSizer2.AddGrowableCol( 0 )
		fgSizer2.AddGrowableCol( 1 )
		fgSizer2.AddGrowableRow( 0 )
		fgSizer2.SetFlexibleDirection( wx.BOTH )
		fgSizer2.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_bitmapLogo = wx.StaticBitmap( self.m_panelMain, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer2.Add( self.m_bitmapLogo, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5 )
		
		fgSizer3 = wx.FlexGridSizer( 0, 1, 0, 0 )
		fgSizer3.SetFlexibleDirection( wx.BOTH )
		fgSizer3.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText5 = wx.StaticText( self.m_panelMain, wx.ID_ANY, _(u"Subtitle\nSpeech\nSynchronizer"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText5.Wrap( -1 )
		self.m_staticText5.SetFont( wx.Font( 24, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )
		
		fgSizer3.Add( self.m_staticText5, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		self.m_textVersion = wx.StaticText( self.m_panelMain, wx.ID_ANY, _(u"custom build"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textVersion.Wrap( -1 )
		fgSizer3.Add( self.m_textVersion, 0, wx.BOTTOM|wx.RIGHT|wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		fgSizer2.Add( fgSizer3, 1, wx.EXPAND|wx.LEFT, 5 )
		
		
		fgSizer1.Add( fgSizer2, 1, wx.EXPAND, 50 )
		
		
		fgSizer1.Add( ( 0, 10), 1, wx.EXPAND, 5 )
		
		self.m_staticText10 = wx.StaticText( self.m_panelMain, wx.ID_ANY, _(u"This is an automatic movie subtitle synchronization tool.\nSynchronization is done by listening to the audio track, translating it if necessary.\nIt could also use another subtitle as a reference.\n\nAuthor: Michał Szymaniak"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText10.Wrap( -1 )
		fgSizer1.Add( self.m_staticText10, 0, wx.ALL, 5 )
		
		
		fgSizer1.Add( ( 0, 10), 1, wx.EXPAND, 5 )
		
		self.m_staticline1 = wx.StaticLine( self.m_panelMain, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		fgSizer1.Add( self.m_staticline1, 0, wx.EXPAND|wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		fgSizer3 = wx.FlexGridSizer( 1, 0, 0, 0 )
		fgSizer3.AddGrowableCol( 2 )
		fgSizer3.SetFlexibleDirection( wx.BOTH )
		fgSizer3.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_buttonLicense = wx.Button( self.m_panelMain, wx.ID_ANY, _(u"License"), wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer3.Add( self.m_buttonLicense, 0, wx.ALL, 5 )
		
		self.m_buttonCredits = wx.Button( self.m_panelMain, wx.ID_ANY, _(u"Credits"), wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer3.Add( self.m_buttonCredits, 0, wx.ALL, 5 )
		
		self.m_buttonWebsite = wx.Button( self.m_panelMain, wx.ID_ANY, _(u"Website"), wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer3.Add( self.m_buttonWebsite, 0, wx.ALL, 5 )
		
		
		fgSizer3.Add( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.m_buttonClose = wx.Button( self.m_panelMain, wx.ID_OK, _(u"Close"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_buttonClose.SetDefault() 
		fgSizer3.Add( self.m_buttonClose, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		
		fgSizer1.Add( fgSizer3, 1, wx.EXPAND, 5 )
		
		
		self.m_panelMain.SetSizer( fgSizer1 )
		self.m_panelMain.Layout()
		fgSizer1.Fit( self.m_panelMain )
		bSizer1.Add( self.m_panelMain, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
		bSizer1.Fit( self )
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.m_buttonLicense.Bind( wx.EVT_BUTTON, self.onButtonLicenseClick )
		self.m_buttonCredits.Bind( wx.EVT_BUTTON, self.onButtonCreditsClick )
		self.m_buttonWebsite.Bind( wx.EVT_BUTTON, self.onButtonWebsiteClick )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onButtonLicenseClick( self, event ):
		event.Skip()
	
	def onButtonCreditsClick( self, event ):
		event.Skip()
	
	def onButtonWebsiteClick( self, event ):
		event.Skip()
	

