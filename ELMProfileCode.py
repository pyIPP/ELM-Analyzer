import wx
import matplotlib
import matplotlib.pyplot
import matplotlib.backends.backend_wxagg
import matplotlib.axes
import matplotlib.image
import matplotlib.cm
import ELMProfileCore
import IRCam
import ModelES3
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
        self.figLeft = matplotlib.pyplot.Figure()
        self.canLeft = matplotlib.backends.backend_wxagg.FigureCanvasWxAgg(self, -1, self.figLeft)
        self.imLeft  = self.figLeft.add_subplot(111)
        self.imLeft.set_xlabel('Time [s]', fontsize=20, family='serif')
        self.imLeft.set_ylabel(r'Total Heat Flux $\left[ \frac{\mathrm{MW}}{ \mathrm{m}}\right]$', fontsize=20, family='serif')
        self.imLeft.set_xlim(0,10)
        self.imLeft.set_ylim(0,100)
        self.plotLeft = self.imLeft.plot(numpy.linspace(0,10,100), 40*numpy.ones(100))
        videoSizerLeft = self.m_leftPanel.GetSizer()
        videoSizerLeft.Add(self.canLeft, 1, wx.ALL | wx.EXPAND, 5)
        self.canLeft.draw()
        self.canLeft.mpl_connect('button_press_event', self.onClick)
        self.xValues= []
        self.timeValues = []
        self.xDummy = []
        self.yDummy = []
        self.figure = matplotlib.pyplot.Figure()
        self.canvas = matplotlib.backends.backend_wxagg.FigureCanvasWxAgg(self, -1, self.figure)
        self.image = self.figure.add_subplot(111)
        self.image.set_xlabel('Target Location [mm]', fontsize=20, family='serif')
        self.image.set_ylabel(r'Heat Flux $\left[ \frac{\mathrm{MW}}{ \mathrm{m}^{2}}\right]$', fontsize=20, family='serif')
        self.image.set_xlim(0,100)
        self.image.set_ylim(0,10)
        self.reverseX = 1
        self.plot = self.image.plot(numpy.linspace(0,100,1000)[::self.reverseX], ModelES3.ModelES3(numpy.array([30,10,10,2.5,0]),numpy.linspace(0,100,1000)))
#        videoSizer = self.m_mainPanel.GetSizer()
        videoSizer = self.m_leftPanel.GetSizer()    #wrong but otherwise it does not work! should be on left panel!
        videoSizer.Add(self.canvas, 1, wx.ALL | wx.EXPAND, 5)
        self.canvas.draw()
        self.canvas.mpl_connect('button_press_event', self.onClick)
        self.currentFrame = 0
        self.m_videoSlider.Disable()
        self.m_previousButton.Disable()
        self.m_nextButton.Disable()
        self.m_ELMButtonLeft.Disable()
        self.m_nextELMButton.Disable()
        self.Bind(wx.EVT_SLIDER, self.OnSlider, self.m_videoSlider)
        self.Bind(wx.EVT_TEXT_ENTER, self.OnSetTime, self.m_currentTime)
        self.Bind(wx.EVT_BUTTON, self.OnPrevious, self.m_previousButton)
        self.Bind(wx.EVT_BUTTON, self.OnNext, self.m_nextButton)
        self.Bind(wx.EVT_BUTTON, self.FindELMs, self.m_ELMButtonLeft)
        self.Bind(wx.EVT_BUTTON, self.NextELM, self.m_nextELMButton)

    def clear(self):
        try:
            del self.video
        except Exception, Error:
            pass
        try:
            self.plot.pop(0).remove()
        except:
            pass
        self.plot = self.image.plot(numpy.linspace(0,100,1000)[::self.reverseX], ModelES3.ModelES3(numpy.array([30,10,10,2.5,0]),numpy.linspace(0,100,1000)))
        self.image.set_xlim(0,100)
        self.image.set_ylim(0,10)
        self.m_videoSlider.Disable()
        self.m_previousButton.Disable()
        self.m_nextButton.Disable()
        self.canvas.draw()


    def onClick(self, event):
        if event.button==1:
            ix, iy = event.xdata, event.ydata
            print 'x = %d, y = %d'%(ix, iy*1.0e6)
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
        self.point = self.image.plot(self.xDummy,self.yDummy,'ro')
        self.canvas.draw()



    def setVideo(self, video, name=''):
        self.video = video
        self.m_videoSlider.SetRange(0, self.video.time.size -1)
        self.m_videoSlider.SetValue(0)
        self.m_nextELMButton.Disable()
        self.m_videoSlider.Enable()
        self.m_previousButton.Enable()
        self.m_nextButton.Enable()
        self.m_ELMButtonLeft.Enable()
        self.name = name
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

#    def saveImage(self, filename):
#        self.figure.savefig(filename)

    def setFrame(self, index):
        try:
            if index >= 0 and index < self.video.data.shape[0]:
                temp =  self.video.data[index]/1.0e6
                self.plot.pop(0).remove()
                try:
                    self.point.pop(0).remove()
                except:
                    pass

                self.xDummy = []
                self.yDummy = []
                self.image.set_xlim(self.video.location[0]*1.0e3, self.video.location[-1]*1.0e3)
                self.image.set_ylim(temp.min(), temp.max()+0.5)
                self.currentFrame = index
                self.plot = self.image.plot(self.video.location[::self.reverseX]*1.0e3, temp, 'k', lw=4)
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
        self.xValues.append(self.xDummy)
        self.timeValues.append(self.video.time[self.currentFrame])

    def FindELMs(self, event):
        timeStart = float(self.m_startTime.Value)
        timeStop = float(self.m_stopTime.Value)
        sigTemp = SigELM.SigELM(self.video.time, self.heatIntegral)
        print 'searching ELMs'
        self.ELMS = sigTemp.FindELMs(timeStart, timeStop)
        print '%d' %self.ELMS.max.size
        if self.ELMS.max.size>0:
            self.m_nextELMButton.Enable()
            self.plotLeftELMs = self.imLeft.plot(self.video.time[self.ELMS.max], self.heatIntegral[self.ELMS.max], 'bo', ms=5)
            self.canLeft.draw()

    def NextELM(self, event):
        try:
            temp = bisect_right(self.ELMS.begin, self.currentFrame)
            index = self.ELMS.begin[temp]
        except:
            index = self.currentFrame
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
#        self.Bind(wx.EVT_MENU, self.OnSaveImage, self.m_editMenuSaveImage)
        self.Bind(wx.EVT_MENU, self.OnSavePositions, self.m_editMenuSavePositions)
        self.Bind(wx.EVT_MENU, self.OnReverseX, self.m_menuOrientationReverseX)
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

    def OnVideoPanelRightClick(self, event):
        print 'Right Click'

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
        tempSave = myObject.myObject()
        tempSave.shotNumber = self.shotNumber
        tempSave.time = self.m_videoPanel.timeValues
        tempSave.xValues = self.m_videoPanel.xValues
        tempSave.elmsStart = self.ELMS.begin
        tempSave.elmsStop  = self.ELMS.end
        tempSave.elmsMax   = self.ELMS.max
        files = [x for x in os.listdir('/afs/ipp-garching.mpg.de/home/m/mfai/workspace/pyElmStriations/program/ELM_Stribes') if str(tempSave.shotNumber) in x]
        tempEdition = [int(x.split('-')[1].replace('.elmstribes','')) for x in files]
        edition = ir.editions(tempSave.shotNumber, tempEdition).nextEdition
        saveString = 'ELM_Stribes/%d-%d.elmstribes' % (tempSave.shotNumber, edition)
        tempSave.save(saveString)
        print 'Saved!'
