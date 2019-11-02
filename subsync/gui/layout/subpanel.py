# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Oct 23 2019)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

from subsync.gui.components.choicelang import ChoiceLang
import wx
import wx.xrc


###########################################################################
## Class SubtitlePanel
###########################################################################

class SubtitlePanel ( wx.Panel ):

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( -1,-1 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		fgSizer2 = wx.FlexGridSizer( 1, 0, 0, 0 )
		fgSizer2.AddGrowableCol( 0 )
		fgSizer2.AddGrowableRow( 0 )
		fgSizer2.SetFlexibleDirection( wx.BOTH )
		fgSizer2.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_textSubPath = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY )
		self.m_textSubPath.SetMinSize( wx.Size( 380,-1 ) )

		fgSizer2.Add( self.m_textSubPath, 0, wx.EXPAND|wx.BOTTOM|wx.RIGHT|wx.LEFT, 5 )

		m_choiceSubLangChoices = []
		self.m_choiceSubLang = ChoiceLang( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choiceSubLangChoices, 0 )
		self.m_choiceSubLang.SetSelection( 0 )
		fgSizer2.Add( self.m_choiceSubLang, 0, wx.EXPAND|wx.BOTTOM, 5 )

		self.m_buttonSubOpen = wx.BitmapButton( self, wx.ID_OPEN, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|0 )

		self.m_buttonSubOpen.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_FILE_OPEN, wx.ART_BUTTON ) )
		fgSizer2.Add( self.m_buttonSubOpen, 0, wx.EXPAND|wx.BOTTOM|wx.RIGHT|wx.LEFT, 5 )


		self.SetSizer( fgSizer2 )
		self.Layout()
		fgSizer2.Fit( self )

		# Connect Events
		self.m_choiceSubLang.Bind( wx.EVT_CHOICE, self.onChoiceSubLang )
		self.m_buttonSubOpen.Bind( wx.EVT_BUTTON, self.onButtonSubOpenClick )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def onChoiceSubLang( self, event ):
		event.Skip()

	def onButtonSubOpenClick( self, event ):
		event.Skip()


