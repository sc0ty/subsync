# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Oct 23 2019)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc


###########################################################################
## Class ChannelsWin
###########################################################################

class ChannelsWin ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"Audio channels"), pos = wx.DefaultPosition, size = wx.DefaultSize, style = wx.DEFAULT_DIALOG_STYLE )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer1 = wx.BoxSizer( wx.VERTICAL )

		self.m_panel1 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		fgSizer1 = wx.FlexGridSizer( 0, 1, 0, 0 )
		fgSizer1.SetFlexibleDirection( wx.BOTH )
		fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText1 = wx.StaticText( self.m_panel1, wx.ID_ANY, _(u"Select audio channels to listen to:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )

		fgSizer1.Add( self.m_staticText1, 0, wx.ALL, 5 )

		self.m_radioAuto = wx.RadioButton( self.m_panel1, wx.ID_ANY, _(u"auto select"), wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.m_radioAuto, 0, wx.EXPAND|wx.ALL, 5 )

		self.m_radioAllChannels = wx.RadioButton( self.m_panel1, wx.ID_ANY, _(u"all channels"), wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.m_radioAllChannels, 0, wx.EXPAND|wx.BOTTOM|wx.RIGHT|wx.LEFT, 5 )

		self.m_radioCustom = wx.RadioButton( self.m_panel1, wx.ID_ANY, _(u"custom selection"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_radioCustom.Enable( False )

		fgSizer1.Add( self.m_radioCustom, 0, wx.EXPAND|wx.BOTTOM|wx.RIGHT|wx.LEFT, 5 )

		self.m_panelCustom = wx.Panel( self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		fgSizer3 = wx.FlexGridSizer( 0, 1, 0, 0 )
		fgSizer3.SetFlexibleDirection( wx.BOTH )
		fgSizer3.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )


		self.m_panelCustom.SetSizer( fgSizer3 )
		self.m_panelCustom.Layout()
		fgSizer3.Fit( self.m_panelCustom )
		fgSizer1.Add( self.m_panelCustom, 1, wx.EXPAND|wx.RIGHT|wx.LEFT, 20 )

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
		bSizer1.Fit( self )

		self.Centre( wx.BOTH )

		# Connect Events
		self.m_radioAuto.Bind( wx.EVT_RADIOBUTTON, self.onRadioButtonToggle )
		self.m_radioAllChannels.Bind( wx.EVT_RADIOBUTTON, self.onRadioButtonToggle )
		self.m_radioCustom.Bind( wx.EVT_RADIOBUTTON, self.onRadioButtonToggle )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def onRadioButtonToggle( self, event ):
		event.Skip()




