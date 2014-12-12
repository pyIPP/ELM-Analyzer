# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Feb 26 2014)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class videoPanel
###########################################################################

class videoPanel ( wx.Panel ):
    
    def __init__( self, parent ):
        wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 800,600 ), style = wx.TAB_TRAVERSAL )
        font = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        font.SetPointSize(10)
        m_superSizer = wx.BoxSizer( wx.HORIZONTAL )

###Panel is ordered:
       ##############                        super
       #     #      #           leftMain       -           rightMain
       #     #      #    leftVideo - leftSub   |    rightVideo  - rightSub
       #     #      #
       ##############
       #     #      #
       ##############

##Left: #############################################
#Main/Video:
        m_leftMainSizer         = wx.BoxSizer( wx.VERTICAL )
        #self.m_leftMainPanel    = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        #m_leftMainSizer         = wx.BoxSizer( wx.VERTICAL )       
        #self.m_leftMainPanel    = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        #leftVideoSizer          = wx.BoxSizer( wx.VERTICAL )
        #self.m_leftMainPanel.SetSizer( leftVideoSizer )
        #self.m_leftMainPanel.Layout()
        #leftVideoSizer.Fit( self.m_leftMainPanel )
#Sub:
        leftSubSizer            = wx.BoxSizer( wx.HORIZONTAL )
        self.m_startTime        = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
        self.m_stopTime         = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
        self.m_ELMButtonLeft    = wx.Button( self, wx.ID_ANY, u"search ELMs", wx.DefaultPosition, wx.DefaultSize, 0 )
        boxStartTime            = wx.BoxSizer( wx.VERTICAL )
        boxStopTime             = wx.BoxSizer( wx.VERTICAL )
        self.m_textStartTime    = wx.StaticText(self, label='Start H-mode: ')
        self.m_textStopTime     = wx.StaticText(self, label='End H-mode: ')
        self.m_textStartTime.SetFont(font)
        self.m_textStopTime.SetFont(font)

        boxStartTime.Add(self.m_textStartTime,flag=wx.RIGHT, border=8)
        boxStartTime.Add(self.m_startTime, 0, wx.ALIGN_CENTER | wx.ALL , 5)
        leftSubSizer.Add(boxStartTime, 1, wx.EXPAND, 5 )

        boxStopTime.Add(self.m_textStopTime,flag=wx.RIGHT, border=8)
        boxStopTime.Add(self.m_stopTime, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        leftSubSizer.Add(boxStopTime, 1, wx.EXPAND, 5 )

        leftSubSizer.Add(self.m_ELMButtonLeft, 0, wx.ALIGN_CENTER | wx.ALL, 5)
#Main:

        #m_leftMainSizer.Add( self.m_leftMainPanel, 10, wx.EXPAND |wx.ALL, 5 )
        m_leftMainSizer.Add( leftSubSizer, 1, wx.EXPAND, 5 )

##Right: ###############################################
#Main/video:
        self.m_rightMainSizer   = wx.BoxSizer( wx.VERTICAL )
        #self.m_rightMainPanel   = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        #rightVideoSizer         = wx.BoxSizer( wx.VERTICAL )
        #self.m_rightMainPanel.SetSizer( rightVideoSizer )
        #self.m_rightMainPanel.Layout()
        #rightVideoSizer.Fit( self.m_rightMainPanel )

#Sub:        
        rightSubSizer           = wx.BoxSizer( wx.HORIZONTAL )
        self.m_previousButton   = wx.Button( self, wx.ID_ANY, u"prev Frame", wx.DefaultPosition, wx.DefaultSize, 0 )
        rightSubSizer.Add(self.m_previousButton, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        
        self.m_videoSlider      = wx.Slider( self, wx.ID_ANY, 50, 0, 100, wx.DefaultPosition, wx.DefaultSize, wx.SL_HORIZONTAL )
        rightSubSizer.Add( self.m_videoSlider, 10, wx.ALIGN_CENTER|wx.ALL, 5 )

        self.m_nextButton       = wx.Button( self, wx.ID_ANY, u"next Frame", wx.DefaultPosition, wx.DefaultSize, 0 )
        rightSubSizer.Add(self.m_nextButton, 0, wx.ALIGN_CENTER | wx.ALL , 5)

        self.m_nextELMButton    = wx.Button( self, wx.ID_ANY, u"next ELM", wx.DefaultPosition, wx.DefaultSize, 0 )
        rightSubSizer.Add(self.m_nextELMButton, 0, wx.ALIGN_CENTER | wx.ALL , 5)

        self.m_textCurrentTime  = wx.StaticText(self, label='Current Time: ')
        self.m_textCurrentTime.SetFont(font)
        
        self.m_currentTime      = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )

        boxCurrentTime          = wx.BoxSizer( wx.VERTICAL )

        boxCurrentTime.Add(self.m_textCurrentTime,flag= wx.Right, border=8)
        boxCurrentTime.Add(self.m_currentTime, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        rightSubSizer.Add(boxCurrentTime, 1, wx.EXPAND, 5 )

        rightSubSizer.Add( self.m_currentTime, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
#Main:        
        #self.m_rightMainSizer.Add( self.m_rightMainPanel, 10, wx.EXPAND |wx.ALL, 5 )
        self.m_rightMainSizer.Add( rightSubSizer, 1, wx.EXPAND, 5 )


##SUPER (the main sizer): #####################################################

        #self.m_leftMainPanel.SetBackgroundColour("red")
        #self.m_rightMainPanel.SetBackgroundColour("blue")

        m_superSizer.Add( m_leftMainSizer, 1, wx.EXPAND, 5)
        m_superSizer.Add( self.m_rightMainSizer, 1, wx.EXPAND, 5)

        self.SetSizer( m_superSizer )
        self.Layout()
    
    def __del__( self ):
        pass
    

###########################################################################
## Class mainFrame
###########################################################################

class mainFrame ( wx.Frame ):
    
    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"ELM Profiles", pos = wx.DefaultPosition, size = wx.Size( 1600,768 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
        
        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        
        self.m_statusBar               = self.CreateStatusBar( 1, wx.ST_SIZEGRIP, wx.ID_ANY )
        self.m_menuBar                 = wx.MenuBar( 0 )
        self.m_fileMenu                = wx.Menu()
        self.m_fileMenuOpen            = wx.MenuItem( self.m_fileMenu, wx.ID_ANY, u"&Open", wx.EmptyString, wx.ITEM_NORMAL )
        self.m_fileMenu.AppendItem( self.m_fileMenuOpen )
        self.m_fileMenuClose           = wx.MenuItem(self.m_fileMenu, wx.ID_ANY, u"C&lose", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_fileMenu.AppendItem( self.m_fileMenuClose )
        
        self.m_fileMenu.AppendSeparator()
        
        self.m_fileMenuExit            = wx.MenuItem( self.m_fileMenu, wx.ID_ANY, u"E&xit", wx.EmptyString, wx.ITEM_NORMAL )
        self.m_fileMenu.AppendItem( self.m_fileMenuExit )
        
        self.m_menuBar.Append( self.m_fileMenu, u"F&ile" ) 
        
        self.m_viewMenu                = wx.Menu()

        self.m_menuOrientation         = wx.Menu()
        self.m_menuOrientationReverseX = wx.MenuItem( self.m_menuOrientation, wx.ID_ANY, u"Reverse X", wx.EmptyString, wx.ITEM_CHECK )
        self.m_menuOrientation.AppendItem( self.m_menuOrientationReverseX )

        self.m_viewMenu.AppendSubMenu( self.m_menuOrientation, u"Orientation" )
        
        self.m_menuBar.Append( self.m_viewMenu, u"&View" ) 

        self.m_editMenu                = wx.Menu()
        self.m_editMenuSaveImage       = wx.MenuItem(self.m_editMenu, wx.ID_ANY, u"Save &Image", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_editMenuSavePositions   = wx.MenuItem(self.m_editMenu, wx.ID_ANY, u"S&ave Stripes", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_editMenuSaveELMProfile  = wx.MenuItem(self.m_editMenu, wx.ID_ANY, u"S&ave ELM Profile", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_editMenu.AppendItem(self.m_editMenuSavePositions)
        self.m_editMenu.AppendItem(self.m_editMenuSaveImage)
        self.m_editMenu.AppendItem(self.m_editMenuSaveELMProfile)
        self.m_editMenuSavePositions.Enable(False)

        self.m_menuBar.Append(self.m_editMenu, u'&Edit')
        
        self.m_helpMenu                = wx.Menu()
        self.m_helpMenuAbout           = wx.MenuItem( self.m_helpMenu, wx.ID_ANY, u"A&bout", wx.EmptyString, wx.ITEM_NORMAL )
        self.m_helpMenu.AppendItem( self.m_helpMenuAbout )
        
        self.m_menuBar.Append( self.m_helpMenu, u"H&elp" ) 
        
        self.SetMenuBar( self.m_menuBar )
        
        m_videoSizer                   = wx.BoxSizer( wx.VERTICAL )
        
        self.SetSizer( m_videoSizer )
        self.Layout()
        
        self.Centre( wx.BOTH )
    
    def __del__( self ):
        pass
    

###########################################################################
## Class openVideoDialog
###########################################################################

class openVideoDialog ( wx.Dialog ):
    
    def __init__( self, parent ):
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Open", pos = wx.DefaultPosition, size = wx.Size( 192,104 ), style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER )
        
        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        
        mainSizer                         = wx.BoxSizer( wx.VERTICAL )
        
        bSizer3                           = wx.BoxSizer( wx.HORIZONTAL )
        
        m_pulseNumberChoiceChoices        = []
        self.m_pulseNumberChoice          = wx.ComboBox( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, m_pulseNumberChoiceChoices, wx.CB_DROPDOWN|wx.CB_SORT )
        bSizer3.Add( self.m_pulseNumberChoice, 1, wx.ALIGN_CENTER|wx.ALL|wx.EXPAND, 5 )
        
        
        mainSizer.Add( bSizer3, 1, wx.EXPAND, 5 )
        
        buttonSizer                       = wx.BoxSizer( wx.HORIZONTAL )
        
        self.m_okButton                   = wx.Button( self, wx.ID_OK, u"O&k", wx.DefaultPosition, wx.DefaultSize, 0 )
        buttonSizer.Add( self.m_okButton, 1, wx.ALL|wx.EXPAND, 5 )
        
        self.m_cancelButton               = wx.Button( self, wx.ID_CANCEL, u"C&ancel", wx.DefaultPosition, wx.DefaultSize, 0 )
        buttonSizer.Add( self.m_cancelButton, 1, wx.ALIGN_CENTER|wx.ALL|wx.EXPAND, 5 )
        
        
        mainSizer.Add( buttonSizer, 1, wx.ALIGN_CENTER|wx.EXPAND, 5 )
        
        
        self.SetSizer( mainSizer )
        self.Layout()
        
        self.Centre( wx.BOTH )
    
    def __del__( self ):
        pass

