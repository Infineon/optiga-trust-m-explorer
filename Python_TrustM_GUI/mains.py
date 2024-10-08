import wx
import tab1_general as t1
import tab2_crypto as t2
import tab3_provider as t3
import tab4_protected as t4
import tab5_storage as t5
import misc_dialogs as misc
import shell_util as exec_cmd
import images as img
import subprocess
import config
#import wx.lib.inspection
import os

class MainFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title="Main Window", style=(wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX)))
        self.SetBackgroundColour(wx.WHITE)
        # Set Font for frame, so all buttons will inherit this, so it saves time
        main_menu_font = wx.Font(16, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.SetFont(main_menu_font)

        # Create all the button widgets first
        self.button1 = wx.Button(self, -1, 'General Features')
        self.button2 = wx.Button(self, -1, 'Cryptographic Functions')
        self.button3 = wx.Button(self, -1, 'OpenSSL-Provider')
        self.button4 = wx.Button(self, -1, 'Protected Update', size = wx.Size(367, -1))
        self.button5 = wx.Button(self, -1, 'Secure Storage', size = wx.Size(367, -1))
        # Title screen widget setup
        # "\xe2\x84\xa2" represents the Trademark symbol in UTF-8 for Python 2.x, will not display properly on Windows (or Python 3.x)
        title_screen = wx.StaticText(self, -1, style=wx.ALIGN_CENTER, label="OPTIGA"+ u"\u1d40\u1d39"+ " TRUST M Explorer")
        font = wx.Font(28, wx.ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        title_screen.SetFont(font)
        
        #TrustM Image
        trustm_image = wx.Image(config.IMAGEPATH + "/images/chipp.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        trustm_image = wx.StaticBitmap(self, -1, trustm_image)

        # IFX Logo
        ifx_image = wx.Image(config.IMAGEPATH + "/images/250px-Infineon-Logo.png", wx.BITMAP_TYPE_PNG)
        ifx_image = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(ifx_image))   
        
        # General logo
        tab1_image = wx.Image(config.IMAGEPATH + "/images/setup.png", wx.BITMAP_TYPE_PNG)
        tab1_image = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(tab1_image))

        # Crypto logo
        tab2_image = wx.Image(config.IMAGEPATH + "/images/crypto.png", wx.BITMAP_TYPE_PNG)
        tab2_image = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(tab2_image))

        # Provider logo
        tab3_image = wx.Image(config.IMAGEPATH + "/images/provider.png", wx.BITMAP_TYPE_PNG)
        tab3_image = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(tab3_image))
        
        # Protected logo
        tab4_image = wx.Image(config.IMAGEPATH + "/images/protected.png", wx.BITMAP_TYPE_PNG)
        tab4_image = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(tab4_image))
        
        # Secure Storage logo
        tab5_image = wx.Image(config.IMAGEPATH + "/images/policy.png", wx.BITMAP_TYPE_PNG)
        tab5_image = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(tab5_image))

        # declare the sizers
        mainsizer = wx.BoxSizer(wx.VERTICAL)
        horisizer = wx.BoxSizer(wx.HORIZONTAL)
        horisizer2 = wx.BoxSizer(wx.HORIZONTAL)
        gdsizer1 = wx.GridSizer(rows=2, cols=3, vgap=0, hgap=0)
        gdsizer2 = wx.GridSizer(rows=2, cols=2, vgap=0, hgap=0)
        
        # add the widgets to the sizers (add row by row)
        horisizer.Add(trustm_image, 0)
        horisizer.AddSpacer(150)
        horisizer.Add(title_screen, 0, wx.CENTRE)
        horisizer.AddSpacer(150)
        horisizer.Add(ifx_image, 0, wx.ALIGN_CENTRE, 10)
        
        horisizer2.AddSpacer(1278)

        gdsizer1.Add(tab1_image, 0, wx.ALIGN_CENTRE | wx.TOP, 5)
        gdsizer1.Add(tab2_image, 0, wx.ALIGN_CENTRE | wx.TOP, 5)
        gdsizer1.Add(tab3_image, 0, wx.ALIGN_CENTRE | wx.TOP, 5)

        gdsizer1.Add(self.button1, 1, wx.EXPAND | wx.ALL, 30)
        gdsizer1.Add(self.button2, 1, wx.EXPAND | wx.ALL, 30)
        gdsizer1.Add(self.button3, 1, wx.EXPAND | wx.ALL, 30)

        gdsizer2.Add(tab4_image, 0, wx.ALIGN_CENTRE | wx.TOP, 5)
        gdsizer2.Add(tab5_image, 0, wx.ALIGN_CENTRE | wx.TOP, 5)

        gdsizer2.Add(self.button4, 1, wx.EXPAND | wx.ALL, 30)
        gdsizer2.Add(self.button5, 1, wx.EXPAND | wx.ALL, 30)
        
        

        mainsizer.Add(horisizer, 0, wx.EXPAND)
        mainsizer.Add(horisizer2)
        mainsizer.Add(-1, 35)
        mainsizer.Add(gdsizer1, 1, wx.EXPAND)
        mainsizer.Add(gdsizer2, 1, wx.CENTRE)

        # Bind events
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        self.Bind(wx.EVT_BUTTON, self.OnButtonClick, self.button1)
        self.Bind(wx.EVT_BUTTON, self.OnButtonClick, self.button2)
        self.Bind(wx.EVT_BUTTON, self.OnButtonClick, self.button3)
        self.Bind(wx.EVT_BUTTON, self.OnButtonClick, self.button4)
        self.Bind(wx.EVT_BUTTON, self.OnButtonClick, self.button5)

        # Set tooltips
        self.button1.SetToolTip(wx.ToolTip("General Features Provided by Trust M"))
        self.button2.SetToolTip(wx.ToolTip("Cryptographic Functions(Sign/Verify/Encrypt/Decrypt"))
        self.button3.SetToolTip(wx.ToolTip("Using Trust M Provider and OpenSSL for secure client-server connection"))
        self.button4.SetToolTip(wx.ToolTip("Integrity and Confidential Protected Update for Key/Metadata/Data"))
        self.button5.SetToolTip(wx.ToolTip("Seure storge using HMAC Verify"))

        self.SetSizer(mainsizer)
        mainsizer.Fit(self)
        self.Show(True)
        
        self.Centre()     
            
    def Disable_Buttons(self):
            self.button1.Disable()
            self.button2.Disable()
            self.button3.Disable()
            self.button4.Disable()
            self.button5.Disable()
                    

    def OnCloseWindow(self, evt):
        self.Destroy()

    # Technically this can be split into 6 different functions but I prefer it this way
    def OnButtonClick(self, evt):
        event_obj = evt.GetEventObject()
        if (event_obj == self.FindWindowByLabel(label='General Features')):
            self.activetab = t1.Tab1Frame(self, "General")
        elif (event_obj == self.FindWindowByLabel(label='Cryptographic Functions')):
            self.activetab = t2.Tab2Frame(self, "Crypto")
        elif (event_obj == self.FindWindowByLabel(label='OpenSSL-Provider')):
            self.activetab = t3.Tab3Frame(self, "Provider")
        elif (event_obj == self.FindWindowByLabel(label='Protected Update')):
            self.activetab = t4.Tab4Frame(self, "Protected Update")
        elif (event_obj == self.FindWindowByLabel(label='Secure Storage')):
            self.activetab = t5.Tab5Frame(self, 'Secure Storage')       
        
        else:
            return
        self.Hide()


class Main(wx.App):
    def __init__(self, redirect=False, filename=None):
        wx.App.__init__(self, redirect, filename)
        dlg = MainFrame(None, title="Main")
        self.SetTopWindow(dlg)
        dlg.Centre()
        # wx.lib.inspection.InspectionTool().Show()
        dlg.Show()
#         print (os.path.abspath(__file__))


# Always executes as this is the main file anyway
# Note: This changes the working directory to /working_space, thus all created objects will be there
# Navigation always starts from the /working_space folder.
if __name__ == "__main__":
    exec_cmd.checkDir()
    app = Main()
    app.MainLoop()
