# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Dec  3 2017)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

from subsync.gui.components.choicelang import ChoiceCustomLang
from subsync.gui.components.iconlist import IconList
import wx
import wx.xrc


###########################################################################
## Class StreamSelectionWin
###########################################################################

class StreamSelectionWin ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"Select streams"), pos = wx.DefaultPosition, size = wx.Size( 800,600 ), style = wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.RESIZE_BORDER )
		
		self.SetSizeHints( wx.Size( 600,480 ), wx.DefaultSize )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_panel1 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		fgSizer1 = wx.FlexGridSizer( 0, 1, 0, 0 )
		fgSizer1.AddGrowableCol( 0 )
		fgSizer1.AddGrowableRow( 1 )
		fgSizer1.SetFlexibleDirection( wx.BOTH )
		fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		fgSizer3 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer3.AddGrowableCol( 1 )
		fgSizer3.AddGrowableRow( 0 )
		fgSizer3.AddGrowableRow( 1 )
		fgSizer3.SetFlexibleDirection( wx.BOTH )
		fgSizer3.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_textSelType = wx.StaticText( self.m_panel1, wx.ID_ANY, _(u"Select stream by type:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textSelType.Wrap( -1 )
		fgSizer3.Add( self.m_textSelType, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 5 )
		
		m_choiceSelTypeChoices = [ _(u"auto"), _(u"subtitle/text"), _(u"audio") ]
		self.m_choiceSelType = wx.Choice( self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choiceSelTypeChoices, 0 )
		self.m_choiceSelType.SetSelection( 0 )
		fgSizer3.Add( self.m_choiceSelType, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_textSelLang = wx.StaticText( self.m_panel1, wx.ID_ANY, _(u"Select stream by language:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textSelLang.Wrap( -1 )
		fgSizer3.Add( self.m_textSelLang, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 5 )
		
		m_choiceSelLangChoices = []
		self.m_choiceSelLang = ChoiceCustomLang( self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choiceSelLangChoices, 0 )
		self.m_choiceSelLang.SetSelection( 0 )
		fgSizer3.Add( self.m_choiceSelLang, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_textSelTitle = wx.StaticText( self.m_panel1, wx.ID_ANY, _(u"Select stream by title:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textSelTitle.Wrap( -1 )
		fgSizer3.Add( self.m_textSelTitle, 0, wx.ALL|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		m_choiceSelTitleChoices = []
		self.m_choiceSelTitle = wx.Choice( self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choiceSelTitleChoices, 0 )
		self.m_choiceSelTitle.SetSelection( 0 )
		fgSizer3.Add( self.m_choiceSelTitle, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )
		
		
		fgSizer1.Add( fgSizer3, 1, wx.EXPAND, 5 )
		
		self.m_items = IconList( self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_ALIGN_LEFT|wx.LC_NO_HEADER|wx.LC_NO_SORT_HEADER|wx.LC_REPORT )
		fgSizer1.Add( self.m_items, 0, wx.ALL|wx.EXPAND, 5 )
		
		fgSizer4 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer4.AddGrowableCol( 1 )
		fgSizer4.SetFlexibleDirection( wx.BOTH )
		fgSizer4.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_bitmapTick = wx.StaticBitmap( self.m_panel1, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer4.Add( self.m_bitmapTick, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )
		
		self.m_textTickInfo = wx.StaticText( self.m_panel1, wx.ID_ANY, _(u"files with matching streams"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textTickInfo.Wrap( -1 )
		fgSizer4.Add( self.m_textTickInfo, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		self.m_bitmapCross = wx.StaticBitmap( self.m_panel1, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer4.Add( self.m_bitmapCross, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )
		
		self.m_textCrossInfo = wx.StaticText( self.m_panel1, wx.ID_ANY, _(u"files without matching streams"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textCrossInfo.Wrap( -1 )
		fgSizer4.Add( self.m_textCrossInfo, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		
		fgSizer1.Add( fgSizer4, 1, wx.EXPAND, 5 )
		
		self.m_staticline1 = wx.StaticLine( self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		fgSizer1.Add( self.m_staticline1, 0, wx.EXPAND |wx.ALL, 5 )
		
		fgSizer2 = wx.FlexGridSizer( 1, 0, 0, 0 )
		fgSizer2.SetFlexibleDirection( wx.BOTH )
		fgSizer2.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_buttonCancel = wx.Button( self.m_panel1, wx.ID_CANCEL, _(u"Cancel"), wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer2.Add( self.m_buttonCancel, 0, wx.ALL, 5 )
		
		self.m_buttonOK = wx.Button( self.m_panel1, wx.ID_OK, _(u"OK"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_buttonOK.SetDefault() 
		fgSizer2.Add( self.m_buttonOK, 0, wx.ALL, 5 )
		
		
		fgSizer1.Add( fgSizer2, 1, wx.ALIGN_RIGHT, 5 )
		
		
		self.m_panel1.SetSizer( fgSizer1 )
		self.m_panel1.Layout()
		fgSizer1.Fit( self.m_panel1 )
		bSizer1.Add( self.m_panel1, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.m_choiceSelType.Bind( wx.EVT_CHOICE, self.onSelChange )
		self.m_choiceSelLang.Bind( wx.EVT_CHOICE, self.onSelChange )
		self.m_choiceSelTitle.Bind( wx.EVT_CHOICE, self.onSelChange )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onSelChange( self, event ):
		event.Skip()
	
	
	

