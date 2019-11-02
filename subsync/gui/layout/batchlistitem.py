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
## Class BatchListItem
###########################################################################

class BatchListItem ( wx.Panel ):

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( -1,-1 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		fgSizer1 = wx.FlexGridSizer( 1, 0, 0, 0 )
		fgSizer1.AddGrowableCol( 1 )
		fgSizer1.AddGrowableRow( 0 )
		fgSizer1.SetFlexibleDirection( wx.BOTH )
		fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_bitmapIcon = wx.StaticBitmap( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_bitmapIcon.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )

		fgSizer1.Add( self.m_bitmapIcon, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL|wx.RESERVE_SPACE_EVEN_IF_HIDDEN, 5 )

		fgSizer2 = wx.FlexGridSizer( 0, 1, 0, 0 )
		fgSizer2.AddGrowableCol( 0 )
		fgSizer2.SetFlexibleDirection( wx.BOTH )
		fgSizer2.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_textName = wx.StaticText( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ST_ELLIPSIZE_END )
		self.m_textName.Wrap( -1 )

		self.m_textName.SetFont( wx.Font( 10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Sans" ) )

		fgSizer2.Add( self.m_textName, 0, wx.ALIGN_BOTTOM|wx.EXPAND|wx.RESERVE_SPACE_EVEN_IF_HIDDEN|wx.TOP|wx.RIGHT|wx.LEFT, 5 )

		fgSizer3 = wx.FlexGridSizer( 1, 0, 0, 0 )
		fgSizer3.AddGrowableCol( 2 )
		fgSizer3.AddGrowableRow( 0 )
		fgSizer3.SetFlexibleDirection( wx.BOTH )
		fgSizer3.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_bitmapStatus = wx.StaticBitmap( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.Size( 16,16 ), 0 )
		self.m_bitmapStatus.Hide()

		fgSizer3.Add( self.m_bitmapStatus, 0, wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.BOTTOM|wx.LEFT, 5 )

		self.m_textErrors = wx.StaticText( self, wx.ID_ANY, _(u"[errors]"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textErrors.Wrap( -1 )

		self.m_textErrors.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, True, wx.EmptyString ) )
		self.m_textErrors.Hide()

		fgSizer3.Add( self.m_textErrors, 0, wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.BOTTOM|wx.LEFT, 5 )

		self.m_textDetails = wx.StaticText( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ST_ELLIPSIZE_END )
		self.m_textDetails.Wrap( -1 )

		fgSizer3.Add( self.m_textDetails, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL|wx.EXPAND|wx.RESERVE_SPACE_EVEN_IF_HIDDEN, 5 )


		fgSizer2.Add( fgSizer3, 1, wx.EXPAND, 5 )


		fgSizer1.Add( fgSizer2, 1, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )


		self.SetSizer( fgSizer1 )
		self.Layout()
		fgSizer1.Fit( self )

	def __del__( self ):
		pass


