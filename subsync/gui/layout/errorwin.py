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
## Class ErrorWin
###########################################################################

class ErrorWin ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"Error"), pos = wx.DefaultPosition, size = wx.DefaultSize, style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		
		bSizer2 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_panelMain = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		fgSizer2 = wx.FlexGridSizer( 0, 1, 0, 0 )
		fgSizer2.SetFlexibleDirection( wx.BOTH )
		fgSizer2.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		fgSizer1 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer1.SetFlexibleDirection( wx.BOTH )
		fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_bitmapIcon = wx.StaticBitmap( self.m_panelMain, wx.ID_ANY, wx.ArtProvider.GetBitmap( wx.ART_WARNING, wx.ART_MESSAGE_BOX ), wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.m_bitmapIcon, 0, wx.ALL, 5 )
		
		fgSizer3 = wx.FlexGridSizer( 0, 1, 0, 0 )
		fgSizer3.SetFlexibleDirection( wx.BOTH )
		fgSizer3.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_textMsg = wx.StaticText( self.m_panelMain, wx.ID_ANY, _(u"Error"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textMsg.Wrap( -1 )
		self.m_textMsg.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
		
		fgSizer3.Add( self.m_textMsg, 0, wx.ALL, 5 )
		
		self.m_textDetails = wx.StaticText( self.m_panelMain, wx.ID_ANY, _(u"[details]"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textDetails.Wrap( -1 )
		self.m_textDetails.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_HIGHLIGHT ) )
		
		fgSizer3.Add( self.m_textDetails, 0, wx.BOTTOM|wx.RIGHT|wx.LEFT, 5 )
		
		self.m_panelFields = wx.Panel( self.m_panelMain, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_panelFields.Hide()
		
		bSizer3 = wx.BoxSizer( wx.VERTICAL )
		
		
		self.m_panelFields.SetSizer( bSizer3 )
		self.m_panelFields.Layout()
		bSizer3.Fit( self.m_panelFields )
		fgSizer3.Add( self.m_panelFields, 0, wx.EXPAND|wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		
		fgSizer1.Add( fgSizer3, 0, 0, 5 )
		
		
		fgSizer2.Add( fgSizer1, 1, wx.EXPAND, 5 )
		
		self.m_button1 = wx.Button( self.m_panelMain, wx.ID_OK, _(u"OK"), wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer2.Add( self.m_button1, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		
		self.m_panelMain.SetSizer( fgSizer2 )
		self.m_panelMain.Layout()
		fgSizer2.Fit( self.m_panelMain )
		bSizer2.Add( self.m_panelMain, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		self.SetSizer( bSizer2 )
		self.Layout()
		bSizer2.Fit( self )
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.m_textDetails.Bind( wx.EVT_LEFT_UP, self.onTextDetailsClick )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onTextDetailsClick( self, event ):
		event.Skip()
	

