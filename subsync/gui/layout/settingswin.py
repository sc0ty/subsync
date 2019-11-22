# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Oct 23 2019)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

from subsync.gui.components.choicelang import ChoiceGuiLang
from subsync.gui.components.choiceenc import ChoiceCharEnc
import wx
import wx.xrc


###########################################################################
## Class SettingsWin
###########################################################################

class SettingsWin ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"Settings"), pos = wx.DefaultPosition, size = wx.DefaultSize, style = wx.DEFAULT_DIALOG_STYLE )

		self.SetSizeHints( wx.Size( -1,-1 ), wx.DefaultSize )

		bSizer1 = wx.BoxSizer( wx.VERTICAL )

		self.m_panelMain = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		fgSizer3 = wx.FlexGridSizer( 0, 1, 0, 0 )
		fgSizer3.AddGrowableCol( 0 )
		fgSizer3.AddGrowableRow( 0 )
		fgSizer3.SetFlexibleDirection( wx.BOTH )
		fgSizer3.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_notebook = wx.Notebook( self.m_panelMain, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_panelGeneral = wx.Panel( self.m_notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		fgSizer4 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer4.AddGrowableCol( 1 )
		fgSizer4.SetFlexibleDirection( wx.BOTH )
		fgSizer4.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText1 = wx.StaticText( self.m_panelGeneral, wx.ID_ANY, _(u"Language:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )

		fgSizer4.Add( self.m_staticText1, 0, wx.ALL|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5 )

		m_languageChoices = []
		self.m_language = ChoiceGuiLang( self.m_panelGeneral, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_languageChoices, 0 )
		self.m_language.SetSelection( 0 )
		fgSizer4.Add( self.m_language, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )

		self.m_staticText2 = wx.StaticText( self.m_panelGeneral, wx.ID_ANY, _(u"Output encoding:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )

		fgSizer4.Add( self.m_staticText2, 0, wx.ALL|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5 )

		m_outputCharEncChoices = []
		self.m_outputCharEnc = ChoiceCharEnc( self.m_panelGeneral, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_outputCharEncChoices, 0 )
		self.m_outputCharEnc.SetSelection( 0 )
		fgSizer4.Add( self.m_outputCharEnc, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )

		self.m_staticText3 = wx.StaticText( self.m_panelGeneral, wx.ID_ANY, _(u"Output filename:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )

		fgSizer4.Add( self.m_staticText3, 0, wx.ALL|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_appendLangCode = wx.CheckBox( self.m_panelGeneral, wx.ID_ANY, _(u"append language code"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_appendLangCode.SetValue(True)
		fgSizer4.Add( self.m_appendLangCode, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_textUpdates = wx.StaticText( self.m_panelGeneral, wx.ID_ANY, _(u"Updates:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textUpdates.Wrap( -1 )

		fgSizer4.Add( self.m_textUpdates, 0, wx.ALL|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_autoUpdate = wx.CheckBox( self.m_panelGeneral, wx.ID_ANY, _(u"download updates automatically"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_autoUpdate.SetValue(True)
		fgSizer4.Add( self.m_autoUpdate, 0, wx.ALIGN_CENTER_VERTICAL|wx.EXPAND|wx.ALL, 5 )


		fgSizer4.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.m_askForUpdate = wx.CheckBox( self.m_panelGeneral, wx.ID_ANY, _(u"ask for update on exit"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_askForUpdate.SetValue(True)
		fgSizer4.Add( self.m_askForUpdate, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )

		self.m_staticText14 = wx.StaticText( self.m_panelGeneral, wx.ID_ANY, _(u"Show popups:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText14.Wrap( -1 )

		fgSizer4.Add( self.m_staticText14, 0, wx.ALL|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_showLanguageNotSelectedPopup1 = wx.CheckBox( self.m_panelGeneral, wx.ID_ANY, _(u"language not selected"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_showLanguageNotSelectedPopup1.SetValue(True)
		fgSizer4.Add( self.m_showLanguageNotSelectedPopup1, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )


		fgSizer4.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.m_showOverwriteExistingFilesConfirmPopup = wx.CheckBox( self.m_panelGeneral, wx.ID_ANY, _(u"confirm file overwrite (in batch mode)"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_showOverwriteExistingFilesConfirmPopup.SetValue(True)
		fgSizer4.Add( self.m_showOverwriteExistingFilesConfirmPopup, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )


		self.m_panelGeneral.SetSizer( fgSizer4 )
		self.m_panelGeneral.Layout()
		fgSizer4.Fit( self.m_panelGeneral )
		self.m_notebook.AddPage( self.m_panelGeneral, _(u"General"), True )
		self.m_panelSynchro = wx.Panel( self.m_notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		fgSizer5 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer5.AddGrowableCol( 1 )
		fgSizer5.SetFlexibleDirection( wx.BOTH )
		fgSizer5.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText4 = wx.StaticText( self.m_panelSynchro, wx.ID_ANY, _(u"Max points distance:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText4.Wrap( -1 )

		fgSizer5.Add( self.m_staticText4, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT|wx.ALL, 5 )

		self.m_maxPointDist = wx.SpinCtrlDouble( self.m_panelSynchro, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 1000, 2, 0.01 )
		self.m_maxPointDist.SetDigits( 2 )
		fgSizer5.Add( self.m_maxPointDist, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )

		self.m_staticText5 = wx.StaticText( self.m_panelSynchro, wx.ID_ANY, _(u"Min points no:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText5.Wrap( -1 )

		fgSizer5.Add( self.m_staticText5, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 5 )

		self.m_minPointsNo = wx.SpinCtrl( self.m_panelSynchro, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 1000, 20 )
		fgSizer5.Add( self.m_minPointsNo, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )

		self.m_staticText6 = wx.StaticText( self.m_panelSynchro, wx.ID_ANY, _(u"Min word length (letters):"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText6.Wrap( -1 )

		fgSizer5.Add( self.m_staticText6, 0, wx.ALL|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_minWordLen = wx.SpinCtrl( self.m_panelSynchro, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 1000, 5 )
		fgSizer5.Add( self.m_minWordLen, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )

		self.m_staticText7 = wx.StaticText( self.m_panelSynchro, wx.ID_ANY, _(u"Min words similarity:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText7.Wrap( -1 )

		fgSizer5.Add( self.m_staticText7, 0, wx.ALL|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_minWordsSim = wx.SpinCtrlDouble( self.m_panelSynchro, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 1, 0.6, 0.01 )
		self.m_minWordsSim.SetDigits( 2 )
		fgSizer5.Add( self.m_minWordsSim, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )

		self.m_staticText8 = wx.StaticText( self.m_panelSynchro, wx.ID_ANY, _(u"Min correlation factor:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText8.Wrap( -1 )

		fgSizer5.Add( self.m_staticText8, 0, wx.ALL|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_minCorrelation = wx.SpinCtrlDouble( self.m_panelSynchro, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 1, 0.9999, 1e-08 )
		self.m_minCorrelation.SetDigits( 4 )
		fgSizer5.Add( self.m_minCorrelation, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )

		self.m_staticText9 = wx.StaticText( self.m_panelSynchro, wx.ID_ANY, _(u"Min speech recognition score:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText9.Wrap( -1 )

		fgSizer5.Add( self.m_staticText9, 0, wx.ALL|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_minWordProb = wx.SpinCtrlDouble( self.m_panelSynchro, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 1, 0.3, 0.01 )
		self.m_minWordProb.SetDigits( 2 )
		fgSizer5.Add( self.m_minWordProb, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_staticText10 = wx.StaticText( self.m_panelSynchro, wx.ID_ANY, _(u"Extractor jobs no:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText10.Wrap( -1 )

		fgSizer5.Add( self.m_staticText10, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 5 )

		fgSizer9 = wx.FlexGridSizer( 1, 2, 0, 0 )
		fgSizer9.AddGrowableCol( 1 )
		fgSizer9.AddGrowableRow( 0 )
		fgSizer9.SetFlexibleDirection( wx.BOTH )
		fgSizer9.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_checkAutoJobsNo = wx.CheckBox( self.m_panelSynchro, wx.ID_ANY, _(u"auto"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_checkAutoJobsNo.SetValue(True)
		fgSizer9.Add( self.m_checkAutoJobsNo, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_jobsNo = wx.SpinCtrl( self.m_panelSynchro, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 1, 1000, 4 )
		self.m_jobsNo.Enable( False )

		fgSizer9.Add( self.m_jobsNo, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )


		fgSizer5.Add( fgSizer9, 1, wx.EXPAND, 5 )


		self.m_panelSynchro.SetSizer( fgSizer5 )
		self.m_panelSynchro.Layout()
		fgSizer5.Fit( self.m_panelSynchro )
		self.m_notebook.AddPage( self.m_panelSynchro, _(u"Synchronization"), False )
		self.m_panelDebug = wx.Panel( self.m_notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		fgSizer6 = wx.FlexGridSizer( 0, 1, 0, 0 )
		fgSizer6.AddGrowableCol( 0 )
		fgSizer6.AddGrowableRow( 4 )
		fgSizer6.SetFlexibleDirection( wx.BOTH )
		fgSizer6.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_debugOptions = wx.CheckBox( self.m_panelDebug, wx.ID_ANY, _(u"enable advanced debug options"), wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer6.Add( self.m_debugOptions, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		fgSizer14 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer14.AddGrowableCol( 1 )
		fgSizer14.SetFlexibleDirection( wx.BOTH )
		fgSizer14.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText11 = wx.StaticText( self.m_panelDebug, wx.ID_ANY, _(u"Logging level:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText11.Wrap( -1 )

		fgSizer14.Add( self.m_staticText11, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		m_choiceLogLevelChoices = [ _(u"all"), _(u"debug"), _(u"info"), _(u"warning"), _(u"error"), _(u"critical") ]
		self.m_choiceLogLevel = wx.Choice( self.m_panelDebug, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choiceLogLevelChoices, 0 )
		self.m_choiceLogLevel.SetSelection( 3 )
		fgSizer14.Add( self.m_choiceLogLevel, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		fgSizer6.Add( fgSizer14, 1, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )

		fgSizer7 = wx.FlexGridSizer( 1, 3, 0, 0 )
		fgSizer7.AddGrowableCol( 1 )
		fgSizer7.AddGrowableRow( 0 )
		fgSizer7.SetFlexibleDirection( wx.BOTH )
		fgSizer7.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_checkLogToFile = wx.CheckBox( self.m_panelDebug, wx.ID_ANY, _(u"log to file"), wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer7.Add( self.m_checkLogToFile, 0, wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.BOTTOM|wx.LEFT, 5 )

		self.m_textLogFilePath = wx.TextCtrl( self.m_panelDebug, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textLogFilePath.Enable( False )

		fgSizer7.Add( self.m_textLogFilePath, 0, wx.ALIGN_CENTER_VERTICAL|wx.EXPAND|wx.TOP|wx.BOTTOM|wx.LEFT, 5 )

		self.m_buttonLogFileSelect = wx.BitmapButton( self.m_panelDebug, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|0 )

		self.m_buttonLogFileSelect.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_FILE_OPEN, wx.ART_BUTTON ) )
		self.m_buttonLogFileSelect.Enable( False )

		fgSizer7.Add( self.m_buttonLogFileSelect, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		fgSizer6.Add( fgSizer7, 1, wx.EXPAND|wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_staticText12 = wx.StaticText( self.m_panelDebug, wx.ID_ANY, _(u"Filter out logs from modules (one per line):"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText12.Wrap( -1 )

		fgSizer6.Add( self.m_staticText12, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_textLogBlacklist = wx.TextCtrl( self.m_panelDebug, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE )
		fgSizer6.Add( self.m_textLogBlacklist, 0, wx.EXPAND|wx.BOTTOM|wx.RIGHT|wx.LEFT, 5 )


		self.m_panelDebug.SetSizer( fgSizer6 )
		self.m_panelDebug.Layout()
		fgSizer6.Fit( self.m_panelDebug )
		self.m_notebook.AddPage( self.m_panelDebug, _(u"Debug"), False )

		fgSizer3.Add( self.m_notebook, 1, wx.EXPAND|wx.ALL, 5 )

		fgSizer8 = wx.FlexGridSizer( 1, 0, 0, 0 )
		fgSizer8.SetFlexibleDirection( wx.BOTH )
		fgSizer8.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_buttonRestoreDefaults = wx.Button( self.m_panelMain, wx.ID_DEFAULT, _(u"Restore defaults"), wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer8.Add( self.m_buttonRestoreDefaults, 0, wx.ALL, 5 )

		self.m_buttonCancel = wx.Button( self.m_panelMain, wx.ID_CANCEL, _(u"Cancel"), wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer8.Add( self.m_buttonCancel, 0, wx.ALL, 5 )

		self.m_buttonOk = wx.Button( self.m_panelMain, wx.ID_OK, _(u"OK"), wx.DefaultPosition, wx.DefaultSize, 0 )

		self.m_buttonOk.SetDefault()
		fgSizer8.Add( self.m_buttonOk, 0, wx.ALL, 5 )


		fgSizer3.Add( fgSizer8, 1, wx.ALIGN_RIGHT, 5 )


		self.m_panelMain.SetSizer( fgSizer3 )
		self.m_panelMain.Layout()
		fgSizer3.Fit( self.m_panelMain )
		bSizer1.Add( self.m_panelMain, 1, wx.EXPAND |wx.ALL, 5 )


		self.SetSizer( bSizer1 )
		self.Layout()
		bSizer1.Fit( self )

		self.Centre( wx.BOTH )

		# Connect Events
		self.m_checkAutoJobsNo.Bind( wx.EVT_CHECKBOX, self.onCheckAutoJobsNoCheck )
		self.m_checkLogToFile.Bind( wx.EVT_CHECKBOX, self.onCheckLogToFileCheck )
		self.m_buttonLogFileSelect.Bind( wx.EVT_BUTTON, self.onButtonLogFileSelectClick )
		self.m_buttonRestoreDefaults.Bind( wx.EVT_BUTTON, self.onButtonRestoreDefaultsClick )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def onCheckAutoJobsNoCheck( self, event ):
		event.Skip()

	def onCheckLogToFileCheck( self, event ):
		event.Skip()

	def onButtonLogFileSelectClick( self, event ):
		event.Skip()

	def onButtonRestoreDefaultsClick( self, event ):
		event.Skip()


