# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Oct 23 2019)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

from subsync.gui.components.streamlist import StreamList
from subsync.gui.components.choicelang import ChoiceLang
from subsync.gui.components.choiceenc import ChoiceCharEnc
import wx
import wx.xrc


###########################################################################
## Class OpenWin
###########################################################################

class OpenWin ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"Select stream"), pos = wx.DefaultPosition, size = wx.Size( 620,480 ), style = wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.RESIZE_BORDER )

		self.SetSizeHints( wx.Size( 440,480 ), wx.DefaultSize )

		bSizer1 = wx.BoxSizer( wx.VERTICAL )

		self.m_panelMain = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		fgSizer14 = wx.FlexGridSizer( 0, 1, 0, 0 )
		fgSizer14.AddGrowableCol( 0 )
		fgSizer14.AddGrowableRow( 3 )
		fgSizer14.SetFlexibleDirection( wx.BOTH )
		fgSizer14.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText1 = wx.StaticText( self.m_panelMain, wx.ID_ANY, _(u"Input file:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )

		fgSizer14.Add( self.m_staticText1, 0, wx.EXPAND|wx.TOP|wx.RIGHT|wx.LEFT, 5 )

		fgSizer1 = wx.FlexGridSizer( 1, 0, 0, 0 )
		fgSizer1.AddGrowableCol( 0 )
		fgSizer1.AddGrowableRow( 0 )
		fgSizer1.SetFlexibleDirection( wx.BOTH )
		fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_textPath = wx.TextCtrl( self.m_panelMain, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY )
		fgSizer1.Add( self.m_textPath, 0, wx.EXPAND|wx.BOTTOM|wx.LEFT, 5 )

		self.m_buttonOpen = wx.BitmapButton( self.m_panelMain, wx.ID_OPEN, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|0 )

		self.m_buttonOpen.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_FILE_OPEN, wx.ART_BUTTON ) )
		fgSizer1.Add( self.m_buttonOpen, 0, wx.EXPAND|wx.BOTTOM|wx.RIGHT|wx.LEFT, 5 )


		fgSizer14.Add( fgSizer1, 0, wx.EXPAND, 5 )

		self.m_staticText2 = wx.StaticText( self.m_panelMain, wx.ID_ANY, _(u"Select stream:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )

		fgSizer14.Add( self.m_staticText2, 0, wx.TOP|wx.RIGHT|wx.LEFT|wx.EXPAND, 5 )

		self.m_listStreams = StreamList( self.m_panelMain, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_ALIGN_LEFT|wx.LC_REPORT|wx.LC_SINGLE_SEL )
		fgSizer14.Add( self.m_listStreams, 0, wx.ALL|wx.EXPAND, 5 )

		fgSizer2 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer2.AddGrowableCol( 1 )
		fgSizer2.SetFlexibleDirection( wx.BOTH )
		fgSizer2.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText3 = wx.StaticText( self.m_panelMain, wx.ID_ANY, _(u"Language:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )

		fgSizer2.Add( self.m_staticText3, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 5 )

		m_choiceLangChoices = []
		self.m_choiceLang = ChoiceLang( self.m_panelMain, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choiceLangChoices, 0 )
		self.m_choiceLang.SetSelection( 0 )
		fgSizer2.Add( self.m_choiceLang, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_staticText4 = wx.StaticText( self.m_panelMain, wx.ID_ANY, _(u"Character encoding:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText4.Wrap( -1 )

		fgSizer2.Add( self.m_staticText4, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 5 )

		m_choiceEncodingChoices = []
		self.m_choiceEncoding = ChoiceCharEnc( self.m_panelMain, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choiceEncodingChoices, 0 )
		self.m_choiceEncoding.SetSelection( 0 )
		self.m_choiceEncoding.Enable( False )

		fgSizer2.Add( self.m_choiceEncoding, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		self.m_staticText5 = wx.StaticText( self.m_panelMain, wx.ID_ANY, _(u"Audio channels:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText5.Wrap( -1 )

		fgSizer2.Add( self.m_staticText5, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 5 )

		fgSizer3 = wx.FlexGridSizer( 1, 0, 0, 0 )
		fgSizer3.AddGrowableCol( 0 )
		fgSizer3.AddGrowableRow( 0 )
		fgSizer3.SetFlexibleDirection( wx.BOTH )
		fgSizer3.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_textChannels = wx.TextCtrl( self.m_panelMain, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY )
		self.m_textChannels.Enable( False )

		fgSizer3.Add( self.m_textChannels, 0, wx.TOP|wx.BOTTOM|wx.LEFT|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )

		self.m_buttonSelectChannels = wx.Button( self.m_panelMain, wx.ID_ANY, _(u"Select"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_buttonSelectChannels.Enable( False )

		fgSizer3.Add( self.m_buttonSelectChannels, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )


		fgSizer2.Add( fgSizer3, 1, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )


		fgSizer14.Add( fgSizer2, 1, wx.EXPAND, 5 )

		self.m_staticline8 = wx.StaticLine( self.m_panelMain, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		fgSizer14.Add( self.m_staticline8, 0, wx.EXPAND |wx.ALL, 5 )

		fgSizer4 = wx.FlexGridSizer( 1, 0, 0, 0 )
		fgSizer4.SetFlexibleDirection( wx.BOTH )
		fgSizer4.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_buttonCancel = wx.Button( self.m_panelMain, wx.ID_CANCEL, _(u"Cancel"), wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer4.Add( self.m_buttonCancel, 0, wx.ALL, 5 )

		self.m_buttonOk = wx.Button( self.m_panelMain, wx.ID_OK, _(u"OK"), wx.DefaultPosition, wx.DefaultSize, 0 )

		self.m_buttonOk.SetDefault()
		fgSizer4.Add( self.m_buttonOk, 0, wx.ALL, 5 )


		fgSizer14.Add( fgSizer4, 1, wx.ALIGN_RIGHT, 5 )


		self.m_panelMain.SetSizer( fgSizer14 )
		self.m_panelMain.Layout()
		fgSizer14.Fit( self.m_panelMain )
		bSizer1.Add( self.m_panelMain, 1, wx.EXPAND |wx.ALL, 5 )


		self.SetSizer( bSizer1 )
		self.Layout()

		# Connect Events
		self.m_buttonOpen.Bind( wx.EVT_BUTTON, self.onButtonOpenClick )
		self.m_listStreams.Bind( wx.EVT_LEFT_DCLICK, self.onListStreamsDClick )
		self.m_listStreams.Bind( wx.EVT_LIST_ITEM_DESELECTED, self.onListStreamsSelect )
		self.m_listStreams.Bind( wx.EVT_LIST_ITEM_SELECTED, self.onListStreamsSelect )
		self.m_choiceLang.Bind( wx.EVT_CHOICE, self.onChoiceLangChoice )
		self.m_choiceEncoding.Bind( wx.EVT_CHOICE, self.onChoiceEncChoice )
		self.m_buttonSelectChannels.Bind( wx.EVT_BUTTON, self.onButtonSelectChannelsClick )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def onButtonOpenClick( self, event ):
		event.Skip()

	def onListStreamsDClick( self, event ):
		event.Skip()

	def onListStreamsSelect( self, event ):
		event.Skip()


	def onChoiceLangChoice( self, event ):
		event.Skip()

	def onChoiceEncChoice( self, event ):
		event.Skip()

	def onButtonSelectChannelsClick( self, event ):
		event.Skip()


