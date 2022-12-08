import wx

# Info for tab6_cloud
class CloudDemoInfoDlg(wx.MessageDialog):
    def __init__(self, parent, title):
        wx.MessageDialog.__init__(self, parent, message="", caption=title, style=wx.OK | wx.ICON_INFORMATION)
        self.SetMessage("TrustM Use Case with Amazon Web Services Internet-of-Things (AWS IoT):\n\
This tab is where the usage of the TrustM is shown, in a use-case involving the AWS IoT service.\n\n\
Setting up:\n\
Users are required to login or setup their AWS credentials through the AWS Command Line Interface or in this tab.\n\
After setting up, the user can click the '1-click provision' button to register this device to AWS.\n\
After provisioning, the user can now publish data to the AWS Cloud.")
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

    def OnCloseWindow(self, evt):
        self.Destroy()
