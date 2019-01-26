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
## Class DownloadWin
###########################################################################

class DownloadWin ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"Downloading"), pos = wx.DefaultPosition, size = wx.DefaultSize, style = wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.RESIZE_BORDER )
		
		self.SetSizeHints( wx.Size( -1,-1 ), wx.DefaultSize )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_panelMain = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		fgSizer2 = wx.FlexGridSizer( 0, 1, 0, 0 )
		fgSizer2.AddGrowableCol( 0 )
		fgSizer2.AddGrowableRow( 1 )
		fgSizer2.SetFlexibleDirection( wx.BOTH )
		fgSizer2.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_textName = wx.StaticText( self.m_panelMain, wx.ID_ANY, _(u"Download"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textName.Wrap( -1 )
		fgSizer2.Add( self.m_textName, 0, wx.EXPAND|wx.RIGHT|wx.LEFT, 5 )
		
		self.m_gaugeProgress = wx.Gauge( self.m_panelMain, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL )
		self.m_gaugeProgress.SetValue( 0 ) 
		self.m_gaugeProgress.SetMinSize( wx.Size( 340,-1 ) )
		
		fgSizer2.Add( self.m_gaugeProgress, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_textDetails = wx.StaticText( self.m_panelMain, wx.ID_ANY, _(u"processing..."), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textDetails.Wrap( -1 )
		fgSizer2.Add( self.m_textDetails, 0, wx.EXPAND|wx.RIGHT|wx.LEFT, 5 )
		
		self.m_line = wx.StaticLine( self.m_panelMain, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		fgSizer2.Add( self.m_line, 0, wx.EXPAND|wx.TOP|wx.RIGHT|wx.LEFT, 10 )
		
		fgSizer81 = wx.FlexGridSizer( 1, 0, 0, 0 )
		fgSizer81.SetFlexibleDirection( wx.BOTH )
		fgSizer81.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_buttonCancel = wx.Button( self.m_panelMain, wx.ID_CANCEL, _(u"Cancel"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_buttonCancel.SetDefault() 
		fgSizer81.Add( self.m_buttonCancel, 0, wx.ALL, 5 )
		
		
		fgSizer2.Add( fgSizer81, 1, wx.ALIGN_RIGHT|wx.TOP|wx.RIGHT|wx.LEFT, 5 )
		
		
		self.m_panelMain.SetSizer( fgSizer2 )
		self.m_panelMain.Layout()
		fgSizer2.Fit( self.m_panelMain )
		bSizer1.Add( self.m_panelMain, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
		bSizer1.Fit( self )
		
		self.Centre( wx.BOTH )
	
	def __del__( self ):
		pass
	

