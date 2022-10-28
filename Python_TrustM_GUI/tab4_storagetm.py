import wx
import shell_util as exec_cmd
import misc_dialogs as misc
import info_dialogs as info
import os
import images as img
import config

TARGET_OID_list = ['F1D7', 'F1D8', 'F1D9', 'F1DA', 'F1DB', 'F1E0', 'F1E1']
SECRET_OID_list = ['F1D8', 'F1D7', 'F1D6', 'F1D9']

class Tab4Frame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title="Secure Storage", size=(1280, 720), style=(wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX)))
        self.Centre(wx.BOTH)
        self.SetBackgroundColour(wx.WHITE)
        main_menu_font = wx.Font(14, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.SetFont(main_menu_font)
        
        
        textctrlfont = wx.Font()
        textctrlfont.SetPointSize(11)
        
        inputfont = wx.Font()
        inputfont.SetPointSize(8)
        
        datafont = wx.Font()
        datafont.SetPointSize(11)
        
        buttonfont = wx.Font(14, wx.ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        
        # declare the sizers
        mainsizer = wx.BoxSizer(wx.VERTICAL)
        input_sizer = wx.BoxSizer(wx.HORIZONTAL)
        mainhorisizer = wx.BoxSizer(wx.HORIZONTAL)
        
        midsizer = wx.BoxSizer(wx.VERTICAL)
        gdsizer1 = wx.GridSizer(rows=1, cols=2, vgap=10, hgap=10)
        gdsizer3 = wx.GridSizer(rows=4, cols=1, vgap=30, hgap=10)
                
        backbuttonsizer = wx.BoxSizer(wx.HORIZONTAL)
        
        # declare sizers that will be in the grid
        targetoidsizer = wx.BoxSizer(wx.VERTICAL)
        secretoidsizer = wx.BoxSizer(wx.VERTICAL)
        secretsizer = wx.BoxSizer(wx.HORIZONTAL)
        
        
        
        # instantiate the objects
        text_targetoid = wx.StaticText(self, 0, "Target OID:")
        self.targetoid = wx.ComboBox(self, 1, choices=TARGET_OID_list, style=wx.CB_READONLY,  size = wx.Size(170, 30))
        self.targetoid.SetFont(textctrlfont)
        
        text_secretoid = wx.StaticText(self, 0, "Secret OID:")
        self.secretoid = wx.ComboBox(self, 1, choices=SECRET_OID_list, style=wx.CB_READONLY,  size = wx.Size(170, 30))
        self.secretoid.SetFont(textctrlfont)
        
        text_secret = wx.StaticText(self, -1, "    Secret:   ")
        self.secret = wx.TextCtrl(self,value="49C9F492A992F6D4C54F5B12C57EDB27CED224048F25482AA149C9F492A992F649C9F492A992F6D4C54F5B12C57EDB27CED224048F25482AA149C9F492A992F6"
                                  )
        self.secret.SetFont(inputfont)
        
        
        inputtext = wx.StaticText(self, -1, label="Data Input:")
        self.input_display = wx.TextCtrl(self,value="0102030405060708090A0B0C0D0E0F")
        self.input_display.SetFont(datafont)
        
        provision_button = wx.Button(self, -1, 'Provision HMAC Auth Storage', size=(300, 50))
        provision_button.SetFont(buttonfont)
        verify_read_button = wx.Button(self, -1, 'Verify and Read Target OID', size=(300, 50))
        verify_read_button.SetFont(buttonfont)
        verify_write_button = wx.Button(self, -1, 'Verify and Write to Target OID', size=(300, 50))
        verify_write_button.SetFont(buttonfont)
        read_meta = wx.Button(self, -1, 'Read Object Metadata', size=(300, 50))
        read_meta.SetFont(buttonfont)

        
        self.text_display = wx.TextCtrl(self, -1, style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.text_display.SetFont(wx.Font(11, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))


        clearimage = wx.Image(config.IMAGEPATH + "/images/clear.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        clearbutton = wx.BitmapButton(self, -1, clearimage)
        
        backimage = wx.Image(config.IMAGEPATH + "/images/back.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        backbutton = wx.BitmapButton(self, -1, backimage)
       
        #Add mainhorisizer to mainsizer
        mainsizer.AddSpacer(5)
        mainsizer.Add(input_sizer, 0, wx.EXPAND | wx.TOP, 5)
        
        input_sizer.Add(inputtext, 0, wx.ALIGN_CENTRE | wx.ALL , 2)
        input_sizer.Add(self.input_display, 1 ,wx.ALIGN_CENTRE | wx.ALL, 2)
        
        mainsizer.AddSpacer(2)
        mainsizer.Add(secretsizer, 0, wx.EXPAND)
        secretsizer.Add(text_secret, 0, wx.ALIGN_CENTRE | wx.ALL , 1)
        secretsizer.Add(self.secret, 1 ,wx.ALIGN_CENTRE | wx.ALL , 2)
        
        mainsizer.Add(mainhorisizer, 1, wx.EXPAND)
       
        # Add Sub Sizers to the mainhorisizer
        mainhorisizer.Add(midsizer, 1, wx.EXPAND)
        mainhorisizer.Add(self.text_display, 2, wx.EXPAND | wx.ALL, 5)
        

        backbuttonsizer.Add(backbutton, 0, wx.ALIGN_LEFT, 0)
        backbuttonsizer.AddSpacer(10)
        backbuttonsizer.Add(clearbutton, 0, wx.EXPAND, 0)

        # Add sizers to midsizer
        midsizer.AddSpacer(30)
        midsizer.Add(gdsizer1, 0, wx.ALIGN_LEFT | wx.ALL, 10)
        midsizer.AddSpacer(30)
        midsizer.Add(gdsizer3, 0, wx.ALIGN_CENTRE | wx.ALL, 10)
        
        midsizer.AddSpacer(50)
        midsizer.Add(backbuttonsizer,0,wx.LEFT | wx.BOTTOM, 5)
        
        #add buttons into gdsizer3
        gdsizer3.AddMany([
           # (self.button_step1),
           (provision_button),
           (verify_read_button),
           (verify_write_button),
           (read_meta),

       ])
        
        #add sizers to gdsizer1
        gdsizer1.AddMany([
                (targetoidsizer, 0, wx.EXPAND),
                (secretoidsizer, 0, wx.EXPAND),
                #(keyslotsizer, 0, wx.EXPAND),
                #(pubkeysizer, 0, wx.EXPAND),    
        ])
        
        
        #add objects into sizers in gdsizer1
        targetoidsizer.Add(text_targetoid)
        targetoidsizer.Add(self.targetoid)
        
        
        #add objects into sizers in gdsizer2
        secretoidsizer.Add(text_secretoid)
        secretoidsizer.Add(self.secretoid)
        
        

       
        
        # Set Default inputs for Text Boxes      
        self.targetoid.SetSelection(1)
        self.secretoid.SetSelection(2)

        
        #bind events
        self.Bind(wx.EVT_BUTTON, self.OnProvision1, provision_button)
        self.Bind(wx.EVT_BUTTON, self.OnVerifyRead1, verify_read_button)
        self.Bind(wx.EVT_BUTTON, self.OnVerifyWrite1, verify_write_button)
        self.Bind(wx.EVT_BUTTON, self.OnReadMeta, read_meta)
        self.Bind(wx.EVT_BUTTON, self.OnClear, clearbutton)
        self.Bind(wx.EVT_BUTTON, self.OnBack, backbutton)
                
        # Set tooltips
        provision_button.SetToolTip(wx.ToolTip("Provision initial data, metadata and shared secret for HMAC authenticated secure storage access."))
        verify_read_button.SetToolTip(wx.ToolTip("Verify HMAC SHA256 at SHARED_SECRET_OID and read data in DATA_OBJECT_OID."))
        verify_write_button.SetToolTip(wx.ToolTip("Verify HMAC SHA256 at SHARED_SECRET_OID and write new data into DATA_OBJECT_OID."))
        clearbutton.SetToolTip(wx.ToolTip("Clear all textboxes"))


        self.SetSizer(mainsizer)
        self.Show(True)
        mainsizer.Fit(self)
        
    def OnProvision1(self, evt):
        self.text_display.AppendText("Provisioning initial data, metadata and shared secret for HMAC authenticated secure storage access... \n")
        wx.CallLater(10, self.OnProvision)
    
    def OnProvision(self):
        TARGET_OID = "0x" + self.targetoid.GetValue()
        SECRET_OID = "0x" + self.secretoid.GetValue()
        DATA_OBJECT = self.input_display.GetValue()
        SHARED_SECRET= self.secret.GetValue()
        
        SHARED_SECRET_META="2011C00101D003E1FC07D10100D30100E80131"
                
        self.text_display.AppendText("Writing binary read access LcsO<0x07 metadata as metadata of Secret OID... \n")
        exec_cmd.createProcess("echo " + SHARED_SECRET_META + " | xxd -r -p > secret_autoref_metadata.bin", None)
        self.text_display.AppendText("'echo $SHARED_SECRET_META | xxd -r -p > secret_autoref_metadata.bin' executed \n")
        command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_metadata", "-w", SECRET_OID, "-F", "secret_autoref_metadata.bin", ])
        self.text_display.AppendText(command_output)
        self.text_display.AppendText("'trustm_metadata -w " + SECRET_OID + " -F secret_autoref_metadata.bin' executed \n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
        
        self.text_display.AppendText("Writing shared secret into Secret OID... \n")
        exec_cmd.createProcess("echo " + SHARED_SECRET + " | xxd -r -p > shared_secret.dat", None)
        self.text_display.AppendText("'echo $SHARED_SECRET | xxd -r -p > shared_secret.dat' executed \n")
        command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_data", "-e", "-w", SECRET_OID, "-i", "shared_secret.dat", ])
        self.text_display.AppendText(command_output)
        self.text_display.AppendText("'trustm_data -e -w " + SECRET_OID + " -i shared_secret.dat' executed \n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
        
        
        self.text_display.AppendText("Set the metadata of 0x$DATA_OBJECT_OID to Auto Change/Read with 0x$SHARED_SECRET_OID.... \n")
        exec_cmd.createProcess("echo " + "0323" + SECRET_OID + " | xxd -r -p > data_object_auto_metadata.bin", None)
        self.text_display.AppendText("'echo 0323$SHARED_SECRET_OID | xxd -r -p > data_object_auto_metadata.bin' executed \n")
        command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_metadata", "-w", TARGET_OID, "-Cf:data_object_auto_metadata.bin", "-Rf:data_object_auto_metadata.bin", ])
        self.text_display.AppendText(command_output)
        self.text_display.AppendText("'trustm_metadata -w " + TARGET_OID + " -Cf:data_object_auto_metadata.bin -Rf:data_object_auto_metadata.bin' executed \n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
    
    def OnVerifyWrite1(self, evt):
        self.text_display.AppendText("Writing data into Target OID if HMAC verification is successful... \n")
        wx.CallLater(10, self.OnVerifyWrite)
    
    def OnVerifyWrite(self):
        TARGET_OID = self.targetoid.GetValue()
        SECRET_OID = "0x" + self.secretoid.GetValue()
        DATA_OBJECT = self.input_display.GetValue()
        targetoid1 = "0x" + self.targetoid.GetValue()
        secretin = self.secret.GetValue()
        
        #convert data input to binary
        self.text_display.AppendText("\nConverting data input to binary data.dat...\n")
              
        exec_cmd.createProcess("echo " + DATA_OBJECT + " | xxd -r -p > data.dat", None)
        self.text_display.AppendText("'echo $DATA_OBJECT | xxd -r -p > data.dat' executed \n")
        
        exec_cmd.createProcess("echo " + secretin + " | xxd -r -p > secret.dat", None)
        self.text_display.AppendText("'echo $secretin | xxd -r -p > secret.dat' executed \n")
        
        command_output = exec_cmd.execCLI([
            config.EXEPATH + "/bin/trustm_hmac_verify_Auth",
            "-I", SECRET_OID,
            "-s", "secret.dat" ,
            "-w",targetoid1 ,
            "-i", "data.dat",
            ])
        self.text_display.AppendText(DATA_OBJECT)
        self.text_display.AppendText(command_output)
        self.text_display.AppendText("'trustm_hmac_verify_Auth -I " + SECRET_OID + " -s secret.dat -w 0x" + TARGET_OID + " -i data.dat \n")
        self.text_display.AppendText("\n" + DATA_OBJECT + "\n\n")
        
    def OnVerifyRead1(self, evt):
        self.text_display.AppendText("Reading out data from Target OID if HMAC verification is successful... \n")
        wx.CallLater(10, self.OnVerifyRead)
    
    def OnVerifyRead(self):
        TARGET_OID = self.targetoid.GetValue()
        SECRET_OID = "0x" + self.secretoid.GetValue()
        secretin = self.secret.GetValue()
        
        exec_cmd.createProcess("echo " + secretin + " | xxd -r -p > secret.dat", None)
        self.text_display.AppendText("'echo $secretin | xxd -r -p > secret.dat' executed \n")
        
        command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_hmac_verify_Auth", "-I", SECRET_OID, "-s","secret.dat","-r", "0x"+TARGET_OID,
                                           "-o", "data_" + TARGET_OID + ".bin", ])
        self.text_display.AppendText(command_output)
        
        self.text_display.AppendText("'trustm_hmac_verify_Auth -I " + SECRET_OID + " -s secret.dat -r 0x" + TARGET_OID + " -o data_" + TARGET_OID + ".bin' executed \n")
        
        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")

    def OnReadMeta(self, evt):
        self.text_display.AppendText("Reading Objects Metadata... \n\n")
        wx.CallLater(10, self.OnReadMeta1)
        
    def OnReadMeta1(self):
        
        target_oid = "0x" + self.targetoid.GetValue()
        secret_oid = "0x" + self.secretoid.GetValue()
        
                
        self.text_display.AppendText("Reading out metadata for secret_oid... \n")
        command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_metadata", "-r", secret_oid, ])
        self.text_display.AppendText(command_output)
        self.text_display.AppendText("'trustm_metadata -r " + secret_oid + "' executed \n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")

        self.text_display.AppendText("Reading out metadata for target_oid... \n")
        command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_metadata", "-r", target_oid, ])
        self.text_display.AppendText(command_output)
        self.text_display.AppendText("'trustm_metadata -r " + target_oid + "' executed \n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
        

    def OnClear(self, evt):
        self.text_display.Clear()

    def OnBack(self, evt):
        self.Parent.Show()
        self.Destroy()
    

