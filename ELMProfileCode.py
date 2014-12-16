import wx
import matplotlib
import matplotlib.pyplot
import matplotlib.backends.backend_wxagg
import matplotlib.axes
import matplotlib.image
import matplotlib.cm
import ELMProfileCore
import IRCam
import myObject
import os
import time
import ir
from bisect import bisect_right
import scipy.misc
import numpy
import SigELM
        
class videoPopUp(wx.Menu):
    def __init__(self):
        wx.Menu.__init__(self, 'Image Menu')

class videoPanel(ELMProfileCore.videoPanel):
    def __init__(self, parent):
        ELMProfileCore.videoPanel.__init__(self, parent)
        self.figLeft    = matplotlib.pyplot.Figure()
        self.canLeft    = matplotlib.backends.backend_wxagg.FigureCanvasWxAgg(self, -1, self.figLeft)
        self.imLeft     = self.figLeft.add_subplot(111)
        self.imLeft.set_xlabel('Time [s]', fontsize=20, family='serif')
        self.imLeft.set_ylabel(r'Total Heat Flux $\left[ \frac{\mathrm{MW}}{ \mathrm{m}}\right]$', fontsize=20, family='serif')
        self.imLeft.set_xlim(0,10)
        self.imLeft.set_ylim(0,100)
        self.plotLeft   = self.imLeft.plot(numpy.linspace(0,10,100), 40*numpy.ones(100))
        videoSizerLeft  = self.m_leftMainSizer  #self.GetSizer().GetItem(0).GetSizer()
        videoSizerLeft.Prepend(self.canLeft, 10, wx.ALL | wx.EXPAND, 5)
        self.canLeft.draw()
        self.canLeft.mpl_connect('button_press_event', self.onClick)
        self.xValues    = []
        self.timeValues = []
        self.xDummy     = []
        self.yDummy     = []
        self.sepPos     = []
        self.sepDummy   = numpy.nan
        self.searchLocalMaxRange = 5
        self.figure     = matplotlib.pyplot.Figure()
        self.canvas     = matplotlib.backends.backend_wxagg.FigureCanvasWxAgg(self, -1, self.figure)
        self.image      = self.figure.add_subplot(111)
        self.image.set_xlabel('Target Location [mm]', fontsize=20, family='serif')
        self.image.set_ylabel(r'Heat Flux $\left[ \frac{\mathrm{MW}}{ \mathrm{m}^{2}}\right]$', fontsize=20, family='serif')
        self.image.set_xlim(0,100)
        self.image.set_ylim(0,10)
        self.reverseX   = 1
        try:
            testFrame       = myObject.myObject('/afs/ipp-garching.mpg.de/home/m/mfai/workspace/pyElmStriations/program/testFrameCoordinates')
            self.plot       = self.image.plot(testFrame.x[::self.reverseX], testFrame.y)
        except:
            self.plot       = self.image.plot([0,1],[0,1])
        self.lineSep = self.image.axvline(self.sepDummy)
        videoSizerRight     = self.m_rightMainSizer
        videoSizerRight.Prepend(self.canvas, 10, wx.ALL | wx.EXPAND, 5)
        self.canvas.draw()
        self.canvas.mpl_connect('button_press_event', self.onClick)
        self.currentFrame = 0
        self.m_videoSlider.Disable()
        self.m_previousButton.Disable()
        self.m_nextButton.Disable()
        self.m_ELMButtonLeft.Disable()
        self.m_nextELMButton.Disable()
        self.Bind(wx.EVT_SLIDER,     self.OnSlider,   self.m_videoSlider    ) 
        self.Bind(wx.EVT_TEXT_ENTER, self.OnSetTime,  self.m_currentTime    )
        self.Bind(wx.EVT_BUTTON,     self.OnPrevious, self.m_previousButton )
        self.Bind(wx.EVT_BUTTON,     self.OnNext,     self.m_nextButton     )
        self.Bind(wx.EVT_BUTTON,     self.FindELMs,   self.m_ELMButtonLeft  )
        self.Bind(wx.EVT_BUTTON,     self.NextELM,    self.m_nextELMButton  )

    def clear(self):
        try:
            del self.video
        except Exception, Error:
            pass
        try:
            self.plot.pop(0).remove()
        except:
            pass
        try:
            self.plotLeft.pop(0).remove()
        except:
            pass
        try:
            testFrame       = myObject.myObject('/afs/ipp-garching.mpg.de/home/m/mfai/workspace/pyElmStriations/program/testFrameCoordinates')
            self.plot       = self.image.plot(testFrame.x[::self.reverseX], testFrame.y)
        except:
            self.plot       = self.image.plot([0,1],[0,1])
        self.sepDummy = numpy.nan
        self.plotLeft       = self.imLeft.plot(numpy.linspace(0,10,100), 40*numpy.ones(100))
        self.imLeft.set_xlim(0,10)
        self.imLeft.set_ylim(0,100)
        self.image.set_xlim(0,100)
        self.image.set_ylim(0,10)
        self.m_videoSlider.Disable()
        self.m_previousButton.Disable()
        self.m_nextButton.Disable()
        self.canvas.draw()
        self.canLeft.draw()


    def onClick(self, event):
        if event.button==1 and event.key=='shift':
            ix = event.xdata
            self.sepDummy = ix
        elif event.button==1 and event.key!= 'shift':
            ix, iy = event.xdata, event.ydata
            try:
                tempXLoc      = numpy.abs(self.video.location-ix/1.0e3).argmin()
                tempXstart    = (tempXLoc-self.searchLocalMaxRange) if (tempXLoc-self.searchLocalMaxRange)>0 else 0
                tempXstop     = (tempXLoc+self.searchLocalMaxRange) if (tempXLoc+self.searchLocalMaxRange)<self.video.location.size else -1
                locIndex      = self.video.data[self.currentFrame][tempXstart:tempXstop].argmax() + tempXLoc -self.searchLocalMaxRange
                xLocalMax     = self.video.location[locIndex]*1.0e3
                yLocalMax     = self.video.data[self.currentFrame][locIndex]/1.0e6
                self.xDummy.append(xLocalMax)
                self.yDummy.append(yLocalMax)
            except:
                self.xDummy.append(ix)
                self.yDummy.append(iy)
        elif event.button==3:
            if len(self.xDummy)>0:
                del self.xDummy[-1]
                del self.yDummy[-1]
        try:
            self.point.pop(0).remove()
        except:
            pass
        self.point = self.image.plot(self.xDummy,self.yDummy,'ro', ms=12)
        self.lineSep.set_xdata(self.sepDummy)
        self.canvas.draw()



    def setVideo(self, video, name=''):
        self.video        = video
        self.m_videoSlider.SetRange(0, self.video.time.size -1)
        self.m_videoSlider.SetValue(0)
        self.m_nextELMButton.Disable()
        self.m_videoSlider.Enable()
        self.m_previousButton.Enable()
        self.m_nextButton.Enable()
        self.m_ELMButtonLeft.Enable()
        self.name         = name
        self.heatIntegral = scipy.integrate.trapz(self.video.data, self.video.location)/1.0e6
        self.imLeft.set_xlim(self.video.time[0], self.video.time[-1])
        self.imLeft.set_ylim(self.heatIntegral.min(), self.heatIntegral.max())
        try:
            self.plotLeft.pop(0).remove()
        except:
            pass
        try:
            self.plotLeftELMs.pop(0).remove()
        except:
            pass
        try:
            self.imLeft.lines[-1].remove()
        except:
            pass
        self.plotLeft = self.imLeft.plot(self.video.time, self.heatIntegral, 'r', lw=2)
        self.lineLeft = self.imLeft.axvline(0)
        self.setFrame(0)

    def saveImage(self, filename):
        self.figure.savefig(filename)

    def setFrame(self, index):
        try:
            if index >= 0 and index < self.video.data.shape[0]:
                temp =  self.video.data[index]/1.0e6
                self.xValues.append(self.xDummy)
                self.timeValues.append(self.video.time[self.currentFrame])
                self.sepPos.append(self.sepDummy)
                self.plot.pop(0).remove()
                try:
                    self.point.pop(0).remove()
                except:
                    pass
                self.xDummy              = []
                self.yDummy              = []
                self.sepDummy            = numpy.nan
                self.lineSep.set_xdata(self.sepDummy)
                self.image.set_xlim(self.video.location[0]*1.0e3, self.video.location[-1]*1.0e3)
                self.image.set_ylim(temp.min(), temp.max()+0.5)
                self.currentFrame        = index
                self.plot                = self.image.plot(self.video.location[::self.reverseX]*1.0e3, temp, 'k', lw=4)
                self.m_currentTime.Value = '%f' % self.video.time[index]
                self.canvas.draw()
                self.lineLeft.set_xdata(self.video.time[index])
                self.canLeft.draw()
        except Exception, Error:
            print Error

    def setReverseX(self, value):
        if value==True:
            self.reverseX = -1
        else:
            self.reverseX = 1
        self.setFrame(self.currentFrame)


    def OnSlider(self, event):
        self.setFrame(self.m_videoSlider.Value)

    def OnSetTime(self, event):
        time = float(self.m_currentTime.Value)
        index = numpy.abs(self.video.time-time).argmin()
        self.m_videoSlider.Value = index
        self.setFrame(index)

    def OnPrevious(self, event):
        self.setFrame(self.currentFrame - 1)

    def OnNext(self, event):
        self.setFrame(self.currentFrame + 1)

    def FindELMs(self, event):
        timeStart              = float(self.m_startTime.Value)
        timeStop               = float(self.m_stopTime.Value)
        sigTemp                = SigELM.SigELM(self.video.time, self.heatIntegral)
        print 'searching ELMs'
        self.ELMS              = sigTemp.FindELMs(timeStart, timeStop)
        print '%d' %self.ELMS.max.size
        if self.ELMS.max.size>0:
            self.m_nextELMButton.Enable()
            self.plotLeftELMs  = self.imLeft.plot(self.video.time[self.ELMS.max], self.heatIntegral[self.ELMS.max], 'bo', ms=5)
            self.canLeft.draw()

    def NextELM(self, event):
        try:
            temp                 = bisect_right(self.ELMS.begin, self.currentFrame)
            index                = self.ELMS.begin[temp]
        except:
            index                = self.currentFrame
        self.m_videoSlider.Value = index
        self.setFrame(index)


class openVideoDialog(ELMProfileCore.openVideoDialog):
    def __init__(self, parent):
        ELMProfileCore.openVideoDialog.__init__(self, parent)

    def getSelection(self):
        return int(self.m_pulseNumberChoice.Value)

    def getVideo(self):
        pulseNumber = self.getSelection()
        return IRCam.heatFluxProfiles(pulseNumber)


class mainFrame(ELMProfileCore.mainFrame):
    def __init__(self, parent):
        ELMProfileCore.mainFrame.__init__(self, parent)
        self.Bind(wx.EVT_MENU, self.OnOpen, self.m_fileMenuOpen)
        self.Bind(wx.EVT_MENU, self.OnClose, self.m_fileMenuClose)
        self.Bind(wx.EVT_MENU, self.OnExit, self.m_fileMenuExit)
        self.Bind(wx.EVT_MENU, self.OnAbout, self.m_helpMenuAbout)
        self.Bind(wx.EVT_MENU, self.OnSaveImage, self.m_editMenuSaveImage)
        self.Bind(wx.EVT_MENU, self.OnSavePositions, self.m_editMenuSavePositions)
        self.Bind(wx.EVT_MENU, self.OnSaveELMProfile, self.m_editMenuSaveELMProfile)
        self.Bind(wx.EVT_MENU, self.OnReverseX, self.m_menuOrientationReverseX)
        self.Bind(wx.EVT_MENU, self.OnChangeRange, self.m_editMenuChangeRange)
        videoSizer = self.GetSizer()
        self.m_videoPanel = videoPanel(self)
        videoSizer.Add(self.m_videoPanel, 1, wx.ALL | wx.EXPAND, 5)


    def OnOpen(self, event):
        dialog = openVideoDialog(self)
        dialog.Show(True)
        if dialog.ShowModal()==wx.ID_OK:
            dialog.Show(False)
            pulseNumber = dialog.getSelection()
            self.shotNumber = pulseNumber
            self.m_statusBar.SetStatusText('Loading pulse %(pulseNumber)d' % locals())
            self.m_videoPanel.setVideo(dialog.getVideo())
            self.m_statusBar.SetStatusText('')
            self.m_editMenuSavePositions.Enable(True)

        dialog.Destroy()

    def OnClose(self, event):
        self.m_videoPanel.clear()

    def OnExit(self, event):
        self.Close(True)

    def OnReverseX(self, event):
        self.m_videoPanel.setReverseX(event.IsChecked())

    def OnAbout(self, event):
        info = wx.AboutDialogInfo()
        info.SetName('ELM Profiles')
        info.SetDevelopers(['Michael Faitsch'])
        info.SetDescription('Program to view IR ELM Profiles')
        info.SetVersion('0.1')
        wx.AboutBox(info)

    def OnSavePositions(self, event):
        tempSave            = myObject.myObject()
        tempSave.shotNumber = self.shotNumber
        tempSave.time       = self.m_videoPanel.timeValues
        tempSave.xValues    = self.m_videoPanel.xValues
        tempSave.sepPos     = self.m_videoPanel.sepPos
        tempSave.elmsStart  = self.ELMS.begin
        tempSave.elmsStop   = self.ELMS.end
        tempSave.elmsMax    = self.ELMS.max
        files               = [x for x in os.listdir('/afs/ipp-garching.mpg.de/home/m/mfai/workspace/pyElmStriations/program/ELM_Stribes') if str(tempSave.shotNumber) in x]
        tempEdition         = [int(x.split('-')[1].replace('.elmstribes','')) for x in files]
        edition             = ir.editions(tempSave.shotNumber, tempEdition).nextEdition
        saveString          = '/afs/ipp-garching.mpg.de/home/m/mfai/workspace/pyElmStriations/program/ELM_Stribes/%d-%d.elmstribes' % (tempSave.shotNumber, edition)
        tempSave.save(saveString)
        print 'Saved!'

    def OnSaveImage(self, event):
        dialog = wx.FileDialog(self, u'Save Image', '', '', 'EPS Image (*.eps)|*.eps', wx.FD_SAVE)
        if dialog.ShowModal() == wx.ID_OK:
            self.m_videoPanel.saveImage(dialog.GetPath())
        dialog.Destroy()

    def OnSaveELMProfile(self, event):
        saveString = '/afs/ipp-garching.mpg.de/home/m/mfai/workspace/pyElmStriations/program/ELM_Profiles/ELMProfile%d-%5.3f.eps' % (self.shotNumber,self.m_videoPanel.video.time[self.m_videoPanel.currentFrame] )
        self.m_videoPanel.saveImage(saveString)

    def OnChangeRange(self, event):
        dialog = openVideoDialog(self)
        if dialog.ShowModal()==wx.ID_OK:
            dialog.Show(False)
            self.m_videoPanel.searchLocalMaxRange = numpy.int32(dialog.getSelection())



