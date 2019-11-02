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
## Class OutputPatternWin
###########################################################################

class OutputPatternWin ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"Output file names"), pos = wx.DefaultPosition, size = wx.DefaultSize, style = wx.DEFAULT_DIALOG_STYLE )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer1 = wx.BoxSizer( wx.VERTICAL )

		self.m_panel1 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		fgSizer1 = wx.FlexGridSizer( 0, 1, 0, 0 )
		fgSizer1.SetFlexibleDirection( wx.BOTH )
		fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_radioPredef = wx.RadioButton( self.m_panel1, wx.ID_ANY, _(u"predefined names:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_radioPredef.SetValue( True )
		fgSizer1.Add( self.m_radioPredef, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		self.m_panelPredef = wx.Panel( self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		gbSizer1 = wx.GridBagSizer( 0, 0 )
		gbSizer1.SetFlexibleDirection( wx.BOTH )
		gbSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText1 = wx.StaticText( self.m_panelPredef, wx.ID_ANY, _(u"Output directory:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )

		gbSizer1.Add( self.m_staticText1, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 2 ), wx.TOP|wx.RIGHT|wx.LEFT, 5 )

		self.m_radioFolderRef = wx.RadioButton( self.m_panelPredef, wx.ID_ANY, _(u"same as reference file"), wx.DefaultPosition, wx.DefaultSize, wx.RB_GROUP )
		self.m_radioFolderRef.SetValue( True )
		gbSizer1.Add( self.m_radioFolderRef, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 2 ), wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_radioFolderSub = wx.RadioButton( self.m_panelPredef, wx.ID_ANY, _(u"same as input subtitles"), wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer1.Add( self.m_radioFolderSub, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 2 ), wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_radioFolderCustom = wx.RadioButton( self.m_panelPredef, wx.ID_ANY, _(u"select custom folder"), wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer1.Add( self.m_radioFolderCustom, wx.GBPosition( 3, 0 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_buttonFolderCustom = wx.BitmapButton( self.m_panelPredef, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|0 )

		self.m_buttonFolderCustom.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_FILE_OPEN, wx.ART_BUTTON ) )
		self.m_buttonFolderCustom.Enable( False )

		gbSizer1.Add( self.m_buttonFolderCustom, wx.GBPosition( 3, 1 ), wx.GBSpan( 1, 1 ), wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.LEFT, 5 )

		self.m_staticText2 = wx.StaticText( self.m_panelPredef, wx.ID_ANY, _(u"File name:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )

		gbSizer1.Add( self.m_staticText2, wx.GBPosition( 0, 3 ), wx.GBSpan( 1, 1 ), wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.RIGHT|wx.LEFT, 5 )

		self.m_radioFileRef = wx.RadioButton( self.m_panelPredef, wx.ID_ANY, _(u"same as reference file"), wx.DefaultPosition, wx.DefaultSize, wx.RB_GROUP )
		self.m_radioFileRef.SetValue( True )
		gbSizer1.Add( self.m_radioFileRef, wx.GBPosition( 1, 3 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_radioFileSub = wx.RadioButton( self.m_panelPredef, wx.ID_ANY, _(u"same as input subtitles"), wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer1.Add( self.m_radioFileSub, wx.GBPosition( 2, 3 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_checkFileAppendLang = wx.CheckBox( self.m_panelPredef, wx.ID_ANY, _(u"append language code"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_checkFileAppendLang.SetValue(True)
		gbSizer1.Add( self.m_checkFileAppendLang, wx.GBPosition( 3, 3 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_checkFileAppendStreamNo = wx.CheckBox( self.m_panelPredef, wx.ID_ANY, _(u"append stream number"), wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer1.Add( self.m_checkFileAppendStreamNo, wx.GBPosition( 4, 3 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_staticText3 = wx.StaticText( self.m_panelPredef, wx.ID_ANY, _(u"File type:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )

		gbSizer1.Add( self.m_staticText3, wx.GBPosition( 0, 4 ), wx.GBSpan( 1, 1 ), wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.RIGHT|wx.LEFT, 5 )

		self.m_radioTypeSrt = wx.RadioButton( self.m_panelPredef, wx.ID_ANY, _(u"SubRIP"), wx.DefaultPosition, wx.DefaultSize, wx.RB_GROUP )
		self.m_radioTypeSrt.SetValue( True )
		gbSizer1.Add( self.m_radioTypeSrt, wx.GBPosition( 1, 4 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_radioTypeSsa = wx.RadioButton( self.m_panelPredef, wx.ID_ANY, _(u"Sub Station Alpha"), wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer1.Add( self.m_radioTypeSsa, wx.GBPosition( 2, 4 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_radioTypeAss = wx.RadioButton( self.m_panelPredef, wx.ID_ANY, _(u"Advanced SSA"), wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer1.Add( self.m_radioTypeAss, wx.GBPosition( 3, 4 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		self.m_panelPredef.SetSizer( gbSizer1 )
		self.m_panelPredef.Layout()
		gbSizer1.Fit( self.m_panelPredef )
		fgSizer1.Add( self.m_panelPredef, 1, wx.EXPAND|wx.RIGHT|wx.LEFT, 20 )

		self.m_staticline2 = wx.StaticLine( self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		fgSizer1.Add( self.m_staticline2, 0, wx.EXPAND |wx.ALL, 5 )

		self.m_radioCustom = wx.RadioButton( self.m_panel1, wx.ID_ANY, _(u"custom names:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.m_radioCustom, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_panelCustom = wx.Panel( self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		fgSizer3 = wx.FlexGridSizer( 0, 1, 0, 0 )
		fgSizer3.AddGrowableCol( 0 )
		fgSizer3.SetFlexibleDirection( wx.BOTH )
		fgSizer3.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		fgSizer4 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer4.AddGrowableCol( 1 )
		fgSizer4.SetFlexibleDirection( wx.BOTH )
		fgSizer4.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText1 = wx.StaticText( self.m_panelCustom, wx.ID_ANY, _(u"pattern:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )

		fgSizer4.Add( self.m_staticText1, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 5 )

		self.m_textPattern = wx.TextCtrl( self.m_panelCustom, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer4.Add( self.m_textPattern, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )


		fgSizer3.Add( fgSizer4, 1, wx.EXPAND, 5 )

		gbSizer2 = wx.GridBagSizer( 0, 0 )
		gbSizer2.SetFlexibleDirection( wx.BOTH )
		gbSizer2.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText4 = wx.StaticText( self.m_panelCustom, wx.ID_ANY, _(u"{sub_path}"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText4.Wrap( -1 )

		self.m_staticText4.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

		gbSizer2.Add( self.m_staticText4, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.RIGHT|wx.LEFT, 5 )

		self.m_staticText5 = wx.StaticText( self.m_panelCustom, wx.ID_ANY, _(u"{ref_path}"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText5.Wrap( -1 )

		self.m_staticText5.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

		gbSizer2.Add( self.m_staticText5, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.RIGHT|wx.LEFT, 5 )

		self.m_staticText6 = wx.StaticText( self.m_panelCustom, wx.ID_ANY, _(u"subtitle/reference file full path"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText6.Wrap( -1 )

		gbSizer2.Add( self.m_staticText6, wx.GBPosition( 0, 2 ), wx.GBSpan( 1, 1 ), wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.RIGHT|wx.LEFT, 5 )

		self.m_staticText7 = wx.StaticText( self.m_panelCustom, wx.ID_ANY, _(u"{sub_no}"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText7.Wrap( -1 )

		self.m_staticText7.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

		gbSizer2.Add( self.m_staticText7, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ), wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.RIGHT|wx.LEFT, 5 )

		self.m_staticText8 = wx.StaticText( self.m_panelCustom, wx.ID_ANY, _(u"{ref_no}"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText8.Wrap( -1 )

		self.m_staticText8.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

		gbSizer2.Add( self.m_staticText8, wx.GBPosition( 1, 1 ), wx.GBSpan( 1, 1 ), wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.RIGHT|wx.LEFT, 5 )

		self.m_staticText9 = wx.StaticText( self.m_panelCustom, wx.ID_ANY, _(u"subtitle/reference stream number"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText9.Wrap( -1 )

		gbSizer2.Add( self.m_staticText9, wx.GBPosition( 1, 2 ), wx.GBSpan( 1, 1 ), wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.RIGHT|wx.LEFT, 5 )

		self.m_staticText10 = wx.StaticText( self.m_panelCustom, wx.ID_ANY, _(u"{sub_lang}"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText10.Wrap( -1 )

		self.m_staticText10.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

		gbSizer2.Add( self.m_staticText10, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 1 ), wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.RIGHT|wx.LEFT, 5 )

		self.m_staticText11 = wx.StaticText( self.m_panelCustom, wx.ID_ANY, _(u"{ref_lang}"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText11.Wrap( -1 )

		self.m_staticText11.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

		gbSizer2.Add( self.m_staticText11, wx.GBPosition( 2, 1 ), wx.GBSpan( 1, 1 ), wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.RIGHT|wx.LEFT, 5 )

		self.m_staticText12 = wx.StaticText( self.m_panelCustom, wx.ID_ANY, _(u"subtitle/reference language"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText12.Wrap( -1 )

		gbSizer2.Add( self.m_staticText12, wx.GBPosition( 2, 2 ), wx.GBSpan( 1, 1 ), wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.RIGHT|wx.LEFT, 5 )

		self.m_staticText13 = wx.StaticText( self.m_panelCustom, wx.ID_ANY, _(u"{sub_name}"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText13.Wrap( -1 )

		self.m_staticText13.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

		gbSizer2.Add( self.m_staticText13, wx.GBPosition( 3, 0 ), wx.GBSpan( 1, 1 ), wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.RIGHT|wx.LEFT, 5 )

		self.m_staticText14 = wx.StaticText( self.m_panelCustom, wx.ID_ANY, _(u"{ref_name}"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText14.Wrap( -1 )

		self.m_staticText14.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

		gbSizer2.Add( self.m_staticText14, wx.GBPosition( 3, 1 ), wx.GBSpan( 1, 1 ), wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.RIGHT|wx.LEFT, 5 )

		self.m_staticText15 = wx.StaticText( self.m_panelCustom, wx.ID_ANY, _(u"file name (without path and extension)"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText15.Wrap( -1 )

		gbSizer2.Add( self.m_staticText15, wx.GBPosition( 3, 2 ), wx.GBSpan( 1, 1 ), wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.RIGHT|wx.LEFT, 5 )

		self.m_staticText16 = wx.StaticText( self.m_panelCustom, wx.ID_ANY, _(u"{sub_dir}"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText16.Wrap( -1 )

		self.m_staticText16.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

		gbSizer2.Add( self.m_staticText16, wx.GBPosition( 4, 0 ), wx.GBSpan( 1, 1 ), wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.RIGHT|wx.LEFT, 5 )

		self.m_staticText17 = wx.StaticText( self.m_panelCustom, wx.ID_ANY, _(u"{ref_dir}"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText17.Wrap( -1 )

		self.m_staticText17.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

		gbSizer2.Add( self.m_staticText17, wx.GBPosition( 4, 1 ), wx.GBSpan( 1, 1 ), wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.RIGHT|wx.LEFT, 5 )

		self.m_staticText18 = wx.StaticText( self.m_panelCustom, wx.ID_ANY, _(u"directory path"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText18.Wrap( -1 )

		gbSizer2.Add( self.m_staticText18, wx.GBPosition( 4, 2 ), wx.GBSpan( 1, 1 ), wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.RIGHT|wx.LEFT, 5 )

		self.m_staticText19 = wx.StaticText( self.m_panelCustom, wx.ID_ANY, _(u"{if:<field>:<value>}"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText19.Wrap( -1 )

		self.m_staticText19.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

		gbSizer2.Add( self.m_staticText19, wx.GBPosition( 5, 0 ), wx.GBSpan( 1, 2 ), wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.RIGHT|wx.LEFT, 5 )

		self.m_staticText20 = wx.StaticText( self.m_panelCustom, wx.ID_ANY, _(u"if <field> is set, append <value>"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText20.Wrap( -1 )

		gbSizer2.Add( self.m_staticText20, wx.GBPosition( 5, 2 ), wx.GBSpan( 1, 1 ), wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.RIGHT|wx.LEFT, 5 )

		self.m_staticText21 = wx.StaticText( self.m_panelCustom, wx.ID_ANY, _(u"{if_not:<field>:<value>}"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText21.Wrap( -1 )

		self.m_staticText21.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

		gbSizer2.Add( self.m_staticText21, wx.GBPosition( 6, 0 ), wx.GBSpan( 1, 2 ), wx.ALL, 5 )

		self.m_staticText22 = wx.StaticText( self.m_panelCustom, wx.ID_ANY, _(u"if <field> is not set, append <value>"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText22.Wrap( -1 )

		gbSizer2.Add( self.m_staticText22, wx.GBPosition( 6, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )


		fgSizer3.Add( gbSizer2, 1, wx.EXPAND, 5 )


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

		self.m_buttonOK = wx.Button( self.m_panel1, wx.ID_ANY, _(u"OK"), wx.DefaultPosition, wx.DefaultSize, 0 )

		self.m_buttonOK.SetDefault()
		fgSizer2.Add( self.m_buttonOK, 0, wx.ALL, 5 )


		fgSizer1.Add( fgSizer2, 1, wx.ALIGN_RIGHT, 5 )


		self.m_panel1.SetSizer( fgSizer1 )
		self.m_panel1.Layout()
		fgSizer1.Fit( self.m_panel1 )
		bSizer1.Add( self.m_panel1, 1, wx.EXPAND|wx.ALL, 5 )


		self.SetSizer( bSizer1 )
		self.Layout()
		bSizer1.Fit( self )

		self.Centre( wx.BOTH )

		# Connect Events
		self.m_radioPredef.Bind( wx.EVT_RADIOBUTTON, self.onModeSel )
		self.m_radioFolderRef.Bind( wx.EVT_RADIOBUTTON, self.onNameSel )
		self.m_radioFolderSub.Bind( wx.EVT_RADIOBUTTON, self.onNameSel )
		self.m_radioFolderCustom.Bind( wx.EVT_RADIOBUTTON, self.onNameSel )
		self.m_buttonFolderCustom.Bind( wx.EVT_BUTTON, self.onButtonFolderCustomClick )
		self.m_radioFileRef.Bind( wx.EVT_RADIOBUTTON, self.onNameSel )
		self.m_radioFileSub.Bind( wx.EVT_RADIOBUTTON, self.onNameSel )
		self.m_checkFileAppendLang.Bind( wx.EVT_CHECKBOX, self.onNameSel )
		self.m_checkFileAppendStreamNo.Bind( wx.EVT_CHECKBOX, self.onNameSel )
		self.m_radioTypeSrt.Bind( wx.EVT_RADIOBUTTON, self.onNameSel )
		self.m_radioTypeSsa.Bind( wx.EVT_RADIOBUTTON, self.onNameSel )
		self.m_radioTypeAss.Bind( wx.EVT_RADIOBUTTON, self.onNameSel )
		self.m_radioCustom.Bind( wx.EVT_RADIOBUTTON, self.onModeSel )
		self.m_buttonOK.Bind( wx.EVT_BUTTON, self.onButtonOkClick )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def onModeSel( self, event ):
		event.Skip()

	def onNameSel( self, event ):
		event.Skip()



	def onButtonFolderCustomClick( self, event ):
		event.Skip()









	def onButtonOkClick( self, event ):
		event.Skip()


