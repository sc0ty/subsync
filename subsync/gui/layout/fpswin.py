# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Dec  3 2017)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

from subsync.gui.combofps import ComboFps
import wx
import wx.xrc


###########################################################################
## Class FpsWin
###########################################################################

class FpsWin ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"FPS"), pos = wx.DefaultPosition, size = wx.DefaultSize, style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_panel1 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		fgSizer1 = wx.FlexGridSizer( 0, 1, 0, 0 )
		fgSizer1.SetFlexibleDirection( wx.BOTH )
		fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText1 = wx.StaticText( self.m_panel1, wx.ID_ANY, _(u"Select output subtitles framerate:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )
		fgSizer1.Add( self.m_staticText1, 0, wx.ALL, 5 )
		
		bSizer2 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_radioRef = wx.RadioButton( self.m_panel1, wx.ID_ANY, _(u"same as reference file"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.m_radioRef, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_radioSub = wx.RadioButton( self.m_panel1, wx.ID_ANY, _(u"same as input subtitles"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.m_radioSub, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		fgSizer2 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer2.SetFlexibleDirection( wx.BOTH )
		fgSizer2.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_radioCustom = wx.RadioButton( self.m_panel1, wx.ID_ANY, _(u"custom value:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer2.Add( self.m_radioCustom, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		m_comboFpsChoices = []
		self.m_comboFps = ComboFps( self.m_panel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, m_comboFpsChoices, wx.CB_SORT )
		fgSizer2.Add( self.m_comboFps, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		
		bSizer2.Add( fgSizer2, 1, wx.EXPAND, 5 )
		
		
		fgSizer1.Add( bSizer2, 1, wx.EXPAND, 5 )
		
		self.m_staticline1 = wx.StaticLine( self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		fgSizer1.Add( self.m_staticline1, 0, wx.EXPAND |wx.ALL, 5 )
		
		fgSizer3 = wx.FlexGridSizer( 1, 0, 0, 0 )
		fgSizer3.SetFlexibleDirection( wx.BOTH )
		fgSizer3.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_buttonCancel = wx.Button( self.m_panel1, wx.ID_CANCEL, _(u"Cancel"), wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer3.Add( self.m_buttonCancel, 0, wx.ALL, 5 )
		
		self.m_buttonOK = wx.Button( self.m_panel1, wx.ID_OK, _(u"OK"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_buttonOK.SetDefault() 
		fgSizer3.Add( self.m_buttonOK, 0, wx.ALL, 5 )
		
		
		fgSizer1.Add( fgSizer3, 1, wx.ALIGN_RIGHT, 5 )
		
		
		self.m_panel1.SetSizer( fgSizer1 )
		self.m_panel1.Layout()
		fgSizer1.Fit( self.m_panel1 )
		bSizer1.Add( self.m_panel1, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
		bSizer1.Fit( self )
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.m_radioRef.Bind( wx.EVT_RADIOBUTTON, self.onRadioRefClick )
		self.m_radioSub.Bind( wx.EVT_RADIOBUTTON, self.onRadioSubClick )
		self.m_radioCustom.Bind( wx.EVT_RADIOBUTTON, self.onRadioCustomClick )
		self.m_comboFps.Bind( wx.EVT_LEFT_UP, self.onComboFpsClick )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onRadioRefClick( self, event ):
		event.Skip()
	
	def onRadioSubClick( self, event ):
		event.Skip()
	
	def onRadioCustomClick( self, event ):
		event.Skip()
	
	def onComboFpsClick( self, event ):
		event.Skip()
	

