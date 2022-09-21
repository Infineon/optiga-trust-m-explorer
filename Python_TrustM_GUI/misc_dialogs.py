import wx
import shell_util as exec_cmd
import tab1_setuptm as t1


# Generic File Editor for AWS Cloud connectivity (for tab5 use)
class EditorFrame(wx.Dialog):
    def __init__(self, parent, title, filename):
        wx.Dialog.__init__(self, parent, wx.ID_ANY, title=title)
        mainsizer = wx.BoxSizer(wx.VERTICAL)
        self.editor = wx.TextCtrl(self, 1, size=wx.Size(800, 600), style=wx.TE_MULTILINE)
        mainsizer.Add(self.editor)
        self.filename = filename
        # Open the file, read the contents and set them into
        # the text edit window
        filehandle = open(self.filename, 'r')
        self.editor.SetValue(filehandle.read())
        filehandle.close()

        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        mainsizer.Fit(self)
        self.Centre(wx.BOTH)
        self.Show()

    def OnCloseWindow(self, evt):
        # Save away the edited text
        # Open the file, do a check for an overwrite!
        user_input = wx.MessageDialog(
            self,
            "Yes: Overwrite jsn file. \nNo: No changes shall be made. \n",
            "Warning!",
            wx.YES_NO)
        if (user_input.ShowModal() == wx.ID_YES):
            # Grab the content to be saved
            text_to_overwrite = self.editor.GetValue()

            filehandle = open(self.filename, 'w')
            filehandle.write(text_to_overwrite)
            filehandle.close()
        # Get rid of the dialog to keep things tidy
        user_input.Destroy()
        self.Destroy()


# Warning Dialog for AWS Region mis-match
# Note by default the AWS C application is set to us-east-1.
class AwsRegionWarning(wx.MessageDialog):
    def __init__(self, parent, title):
        wx.MessageDialog.__init__(self, parent, message="", caption=title, style=wx.OK | wx.ICON_WARNING)

        self.SetMessage("WARNING, as you have set the AWS region to a NON us-west-2 region, when attempting to publish to the AWS Cloud, the application will crash.\n\n\
To fix this problem:\n\
    Edit the file, 'aws_iot_config.h' in /aws_trustm/sample_apps/eHealthTrustM/eHealthDevice, and edit the value AWS_IOT_MQTT_HOST with the correct endpoint.\n\
    Or, just use the AWS region us-west-2.")
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

    def OnCloseWindow(self, evt):
        self.EndModal(-1)
        self.Destroy()
