import wx
import shell_util as exec_cmd
import misc_dialogs as misc
import images as img
import config
from binascii import unhexlify
import os


class Tab_GEN(wx.Panel):
    
    def __init__(self, parent):
        
        wx.Panel.__init__(self, parent)
        
        textctrlfont = wx.Font()
        textctrlfont.SetPointSize(10)
        
        buttonfont = wx.Font(12, wx.ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        
        # declare the sizers
        mainsizer = wx.BoxSizer(wx.VERTICAL)
        mainhorisizer = wx.BoxSizer(wx.HORIZONTAL)
        
        midsizer = wx.BoxSizer(wx.VERTICAL)
        gdsizer3 = wx.GridSizer(rows=6, cols=1, vgap=30, hgap=10)
        
        backbuttonsizer = wx.BoxSizer(wx.HORIZONTAL)
        
        # declare sizers that will be in the grid1
        ecctypesizer = wx.BoxSizer(wx.VERTICAL)
        keyslotsizer = wx.BoxSizer(wx.VERTICAL)
        pubkeysizer = wx.BoxSizer(wx.VERTICAL)
        
        
        
        # instantiate the objects
        
        self.button_chip = wx.Button(self, 1, 'OPTIGA™ Trust M Chip Info', size = wx.Size(350, 50))
        self.button_chip.SetFont(buttonfont)
        button_meta = wx.Button(self, 1, 'Read Metadata For All Data Objects', size = wx.Size(350, 50))
        button_meta.SetFont(buttonfont)
        button_data = wx.Button(self, 1, 'Read All Objects Data', size = wx.Size(350, 50))
        button_data.SetFont(buttonfont)
        button_priv = wx.Button(self, 1, 'Read Metadata For Private Key Objects', size = wx.Size(350, 50))
        button_priv.SetFont(buttonfont)
        button_metastatus = wx.Button(self, 1, 'Read Metadata For Common Data Objects', size = wx.Size(350, 50))
        button_metastatus.SetFont(buttonfont)
        button_status = wx.Button(self, 1, 'Read Data For Common Data Objects', size = wx.Size(350, 50))
        button_status.SetFont(buttonfont)
        
        
        self.text_display = wx.TextCtrl(self, -1, style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.text_display.SetFont(wx.Font(11, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))


        clearimage = wx.Image(config.IMAGEPATH + "/images/clear.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        clearbutton = wx.BitmapButton(self, -1, clearimage)

        
        backimage = wx.Image(config.IMAGEPATH + "/images/back.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        backbutton = wx.BitmapButton(self, -1, backimage)
       
        #Add mainhorisizer to mainsizer
        mainsizer.AddSpacer(5)
        

        mainsizer.Add(mainhorisizer, 1, wx.EXPAND)
       
        # Add Sub Sizers to the mainhorisizer
        mainhorisizer.Add(midsizer, 1, wx.EXPAND)
        mainhorisizer.Add(self.text_display, 2, wx.EXPAND | wx.ALL, 5)
        
        backbuttonsizer.Add(backbutton, 0, wx.ALIGN_LEFT, 0)
        backbuttonsizer.AddSpacer(10)
        backbuttonsizer.Add(clearbutton, 0, wx.EXPAND, 0)

        # Add sizers to midsizer
        midsizer.AddSpacer(40)
        midsizer.Add(gdsizer3, 0, wx.ALIGN_CENTRE | wx.ALL, 10)
        
        midsizer.AddSpacer(80)
        midsizer.Add(backbuttonsizer,0,wx.LEFT | wx.BOTTOM, 5)
        
        #add buttons into gdsizer3
        gdsizer3.AddMany([
           # (self.button_step1),
           (self.button_chip),
           (button_meta),
           (button_data),
           (button_priv),
           (button_metastatus),
           (button_status),

       ])
                       
        # Set Default inputs for Text Boxes      
        # attach objects to the sizer
        # declare and bind events     
        
        #bind events     
        self.button_chip.Bind(wx.EVT_BUTTON, self.OnChipInfo)
        button_meta.Bind(wx.EVT_BUTTON, self.OnReadMeta)
        button_data.Bind(wx.EVT_BUTTON, self.OnReadData)
        button_priv.Bind(wx.EVT_BUTTON, self.OnReadPriv)
        button_metastatus.Bind(wx.EVT_BUTTON, self.OnMetaStatus)
        button_status.Bind(wx.EVT_BUTTON, self.OnReadStatus)
        clearbutton.Bind(wx.EVT_BUTTON, self.OnFlush)
        backbutton.Bind(wx.EVT_BUTTON, self.OnBack)
        
        

        self.button_chip.SetToolTip(wx.ToolTip("Display the OPTIGA™ Trust M chip information"))
        
        button_meta.SetToolTip(wx.ToolTip("Read all data objects metadata for oid: "+
        "0xE0E0-0xE0E3 , 0xE0E8-0xE0E9 , 0xE0EF , 0xE120-0xE123 , 0xE200 , 0xE140 , 0xF1D0-0xF1DB , 0xF1E0-0xF1E1"))
        
        button_data.SetToolTip(wx.ToolTip("Read all data object's data for oid: " +
        "0xE0E0-0xE0E3 , 0xE0E8-0xE0E9 , 0xE0EF , 0xE120-0xE123 ,0xE140 , 0xF1D0-0xF1DB , 0xF1E0-0xF1E1"))
        
        button_priv.SetToolTip(wx.ToolTip("Read Private data object's metadata for oid: 0xE0F0-0xE0F3 , 0xF1FC-0xE0FD "))
                                          
        button_metastatus.SetToolTip(wx.ToolTip("Read all data objects metadata status for oid: 0xE0C0-0xE0C6 , 0xF1C0-0xF1C2 "))
        
        button_status.SetToolTip(wx.ToolTip("Read all data object's status for oid: 0xE0C0-0xE0C6 , 0xF1C0-0xF1C2 "))
        
        clearbutton.SetToolTip(wx.ToolTip("Clear all textboxes."))
        backbutton.SetToolTip(wx.ToolTip("Go back to main page."))

        self.SetSizer(mainsizer)
        mainsizer.Fit(self)
        
    
    def OnChipInfo(self, evt):
        
        self.text_display.AppendText("\nReading OPTIGA™ Trust M chip info\n\n")
        wx.CallLater(10, self.OnChipInfo1)
        
    def OnChipInfo1(self):
        
        command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_chipinfo" ])
        
        self.text_display.AppendText(command_output)
        self.text_display.AppendText("\n'/bin/trustm_chipinfo' executed\n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++\n")
         
            
    def OnReadMeta(self, evt):
        
        self.text_display.AppendText("\nReading all Data Objects Metadata")
        wx.CallLater(10, self.OnReadMeta1)
        
    def OnReadMeta1(self):
        
        command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_readmetadata_data" ])
        
        self.text_display.AppendText(command_output)
        self.text_display.AppendText("\n '/bin/trustm_readmetadata_data' executed\n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++\n")
        
        
    def OnReadData(self, evt):
        
        self.text_display.AppendText("\nReading Data for all Data Objects\n")
        wx.CallLater(10, self.OnReadData1)
        
    
    def OnReadData1(self):
        
        command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_read_data" ])
        
        self.text_display.AppendText(command_output)
        self.text_display.AppendText("\n '/bin/trustm_read_data' executed\n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++\n")
    
    def OnReadPriv(self, evt):
        
        self.text_display.AppendText("\nReading Metadata of all Private Data Objects\n")
        wx.CallLater(10, self.OnReadPriv1)
    
    def OnReadPriv1(self):
        
        command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_readmetadata_private" ])
        
        self.text_display.AppendText(command_output)
        self.text_display.AppendText("\n'/bin/trustm_readmetadata_private' executed\n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++\n")
    
    def OnMetaStatus(self, evt):
        
        self.text_display.AppendText("\nReading Metadata Status of all Data Objects\n")
        wx.CallLater(20, self.OnMetaStatus1)
        
    def OnMetaStatus1(self):
        
        command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_readmetadata_status" ])
        
        self.text_display.AppendText(command_output)
        self.text_display.AppendText("\n'/bin/trustm_readmetadata_status' executed\n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++\n")
    
    def OnReadStatus(self, evt):
        
        self.text_display.AppendText("\nReading Status of all Data Objects\n")
        wx.CallLater(20, self.OnReadStatus1)
    
    def OnReadStatus1(self):
        
        command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_read_status" ])
        
        self.text_display.AppendText(command_output)
        self.text_display.AppendText("\n'/bin/trustm_read_status' executed\n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++\n")
    
    # to clear the textbox
    def OnFlush(self, evt):
        self.text_display.Clear()

    # Calling parent of the parent, as direct parent is the notebook,
    # then the second parent is the frame, from which we call the destruction
    def OnBack(self, evt):
        self.Parent.Parent.OnCloseWindow(None)
    


class Tab_KEY(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        
        textctrlfont = wx.Font()
        textctrlfont.SetPointSize(11)
        
        textctrlfont1 = wx.Font(11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD,)
        
        keyslot_list = ['E0F0', 'E0F1','E0F2','E0F3','E0FC', 'E0FD','E200']
        pubkey_list = ['E0E0-PreProvisioned', 'E0E1', 'E0E2','E0E3', 'E0E8-TrustAnchor','E0E9-TrustAnchor',]
        Destination_list = ['E0E1','E0E2','E0E3','E0E8','E0E9',]
        
        buttonfont = wx.Font(13, wx.ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        
        # declare the sizers
        mainsizer = wx.BoxSizer(wx.VERTICAL)
        input_sizer = wx.BoxSizer(wx.HORIZONTAL)
        mainhorisizer = wx.BoxSizer(wx.HORIZONTAL)
        
        midsizer = wx.BoxSizer(wx.VERTICAL)
       
        gdsizer1 = wx.GridSizer(rows=2, cols=1, vgap=5, hgap=10)
        gdsizer2 = wx.GridSizer(rows=3, cols=1, vgap=5, hgap=10)
        gdsizer3 = wx.GridSizer(rows=1, cols=2, vgap=5, hgap=10)
        gdsizer4 = wx.GridSizer(rows=1, cols=1, vgap=5, hgap=10)
        gdsizer5 = wx.GridSizer(rows=1, cols=2, vgap=5, hgap=10)
        backbuttonsizer = wx.BoxSizer(wx.HORIZONTAL)
        
        # declare sizers that will be in the grid1
        pubkeysizer = wx.BoxSizer(wx.VERTICAL)
        keyslotsizer = wx.BoxSizer(wx.VERTICAL)
        trustancsizer = wx.BoxSizer(wx.VERTICAL)
        fileinputsizer = wx.BoxSizer(wx.VERTICAL)
        bindsizer = wx.BoxSizer(wx.VERTICAL)
        secretfilesizer = wx.BoxSizer(wx.VERTICAL)
       
        
        # instantiate the objects
        text_pubkey = wx.StaticText(self, 0, "Public Key Certificate:")
        self.pubkey = wx.ComboBox(self, 1, choices=pubkey_list, style=wx.CB_READONLY,  size = wx.Size(180, 30))
        self.pubkey.SetFont(textctrlfont)
        
        text_keyslot = wx.StaticText(self, 0, "Key Slot:")
        self.keyslot = wx.ComboBox(self, 1, choices=keyslot_list, style=wx.CB_READONLY,  size = wx.Size(170, 30))
        self.keyslot.SetFont(textctrlfont)
        
        text_trustanc = wx.StaticText(self, 0, "Destination OID:")
        self.trustanc = wx.ComboBox(self, 1, choices=Destination_list, style=wx.CB_READONLY,  size = wx.Size(170, 30))
        self.trustanc.SetFont(textctrlfont)
        
        self.button_keymetadata = wx.Button(self, 1, 'Read Keyslot Metadata ', size = wx.Size(300, 40))
        self.button_keymetadata.SetFont(buttonfont)
        
        self.button_certmetadata = wx.Button(self, 1, 'Read Certificate Metadata', size = wx.Size(300, 40))
        self.button_certmetadata.SetFont(buttonfont)
        
        button_data = wx.Button(self, 1, 'Read Certificate', size = wx.Size(300, 40))
        button_data.SetFont(buttonfont)
        
        button_writecert = wx.Button(self, 1, 'Write Certificate', size = wx.Size(300, 40))
        button_writecert.SetFont(buttonfont)
        
        text_filename_input = wx.StaticText(self, 0, "Cert Filename:")
        self.filename_input = wx.TextCtrl(self, -1, value="testE0E0.crt", style=wx.CB_READONLY, size=(170, 30))
        self.filename_input.SetFont(textctrlfont)
        
        text_bindsecret = wx.StaticText(self, 0, "Platform Binding Secret:")
        text_bindsecret.SetFont(textctrlfont1)
        self.bindsecret = wx.TextCtrl(self, 1, value= "E140", style=wx.CB_READONLY ,  size = wx.Size(170, 30))
        self.bindsecret.SetFont(textctrlfont)
        
        
        button_secret = wx.Button(self, 1, 'Write Secret', size = wx.Size(300, 40))
        button_secret.SetFont(buttonfont)
        
        text_secretfile = wx.StaticText(self, 0, "Secret File:")
        self.secretfile = wx.TextCtrl(self, -1, value= "platform_secret.dat", style=wx.CB_READONLY , size=(170, 30))
        self.secretfile.SetFont(textctrlfont)
        
        self.text_display = wx.TextCtrl(self, -1, style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.text_display.SetFont(wx.Font(11, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))


        clearimage = wx.Image(config.IMAGEPATH + "/images/clear.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        clearbutton = wx.BitmapButton(self, -1, clearimage)

        
        backimage = wx.Image(config.IMAGEPATH + "/images/back.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        backbutton = wx.BitmapButton(self, -1, backimage)
       
        #Add mainhorisizer to mainsizer
        mainsizer.AddSpacer(5)

        mainsizer.Add(mainhorisizer, 1, wx.EXPAND)
       
        # Add Sub Sizers to the mainhorisizer
        mainhorisizer.Add(midsizer, 1, wx.EXPAND)
        mainhorisizer.Add(self.text_display, 2, wx.EXPAND | wx.ALL, 5)
        
        # Add Objects to leftsizer
        
        backbuttonsizer.Add(backbutton, 0, wx.ALIGN_LEFT, 0)
        backbuttonsizer.AddSpacer(10)
        backbuttonsizer.Add(clearbutton, 0, wx.EXPAND, 0)

        # Add sizers to midsizer
        midsizer.AddSpacer(15)
        midsizer.Add(gdsizer1, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        
        midsizer.AddSpacer(5)
        midsizer.Add(gdsizer2, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        
        
        midsizer.AddSpacer(5)
        midsizer.Add(gdsizer3, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        
        midsizer.AddSpacer(5)
        midsizer.Add(gdsizer4, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        
        midsizer.AddSpacer(10)
        midsizer.Add(gdsizer5, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        
        midsizer.AddSpacer(5)
        midsizer.Add(button_secret, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        
        midsizer.AddSpacer(50)
        midsizer.Add(backbuttonsizer,0,wx.LEFT | wx.BOTTOM, 5)
        
        
        #add buttons into gdsizer3
        
        gdsizer1.AddMany([
                (keyslotsizer, 0, wx.ALIGN_CENTRE | wx.ALL),
                (self.button_keymetadata),
        ])
        
        gdsizer2.AddMany([
                (pubkeysizer, 0, wx.ALIGN_CENTRE | wx.ALL),
                (self.button_certmetadata),
                (button_data),
                
        ])
        
        
        gdsizer3.AddMany([
              (trustancsizer, 0, wx.ALIGN_CENTRE | wx.ALL),
              (fileinputsizer),
              
       ])
        
        gdsizer4.AddMany([
            (button_writecert),   
            ])
        
        
        gdsizer5.AddMany([
              (bindsizer, 0, wx.ALIGN_CENTRE | wx.ALL),
              (secretfilesizer),
                
       ])
 
        #add objects into sizers in gdsizer2
        keyslotsizer.Add(text_keyslot)
        keyslotsizer.Add(self.keyslot)
        
        pubkeysizer.Add(text_pubkey)
        pubkeysizer.Add(self.pubkey)
        
        trustancsizer.Add(text_trustanc)
        trustancsizer.Add(self.trustanc)
        
        fileinputsizer.Add(text_filename_input)
        fileinputsizer.Add(self.filename_input)
        
        secretfilesizer.Add(text_secretfile)
        secretfilesizer.Add(self.secretfile)
        
        bindsizer.Add(text_bindsecret)
        bindsizer.Add(self.bindsecret)
 
        # Set Default inputs for Combo Boxes      
        self.pubkey.SetSelection(0)
        self.keyslot.SetSelection(0)   
        self.trustanc.SetSelection(2)
        
        #bind events
        self.button_keymetadata.Bind(wx.EVT_BUTTON, self.OnKeyMetadata)
        self.button_certmetadata.Bind(wx.EVT_BUTTON, self.OnCertmeta)
        button_data.Bind(wx.EVT_BUTTON, self.OnCertData)
        button_writecert.Bind(wx.EVT_BUTTON, self.OnWriteCert)
        button_secret.Bind(wx.EVT_BUTTON, self.OnWriteSecret)
        
        self.filename_input.Bind(wx.EVT_LEFT_DOWN,self.OnClickFileName)
        self.secretfile.Bind(wx.EVT_LEFT_DOWN,self.OnClickSecretFile)
        
        clearbutton.Bind(wx.EVT_BUTTON, self.OnClear)
        backbutton.Bind(wx.EVT_BUTTON, self.OnBack)
        
        
        # Set tooltips
        clearbutton.SetToolTip(wx.ToolTip("Clear all textboxes."))
        backbutton.SetToolTip(wx.ToolTip("Go back to main page."))

        self.SetSizer(mainsizer)
        mainsizer.Fit(self)
        
        if (self.pubkey.GetSelection() == 0):
            Puboid= "E0E0"
    
    def OnClickSecretFile(self, evt):
        frame = wx.Frame(None, -1, '*.*')
        frame.SetSize(0,0,200,50)
            
        openFileDialog = wx.FileDialog(frame, "Open", "", "","All|*.dat;*.crt;*.txt|Binary|*.dat|Secret|*.crt;*.txt", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        cert_dir= config.IMAGEPATH + "/working_space/"
        openFileDialog.SetDirectory(cert_dir)
        openFileDialog.SetFilename("platform_secret.dat")
        if openFileDialog.ShowModal() ==wx.ID_CANCEL:
            
                return
        print((openFileDialog.GetPath()))
        self.secretfile.SetValue(openFileDialog.GetPath())
        
    
    def OnClickFileName(self, evt):
        frame = wx.Frame(None, -1, '*.*')
        frame.SetSize(0,0,200,50)
            
        openFileDialog = wx.FileDialog(frame, "Open", "", "","All|*.bin;*.crt;*.der|Binary|*.bin|Certificate|*.crt;*.der", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        cert_dir= config.IMAGEPATH + "/working_space/"
        openFileDialog.SetDirectory(cert_dir)
        if openFileDialog.ShowModal() ==wx.ID_CANCEL:
            
                return
        print((openFileDialog.GetPath()))
        self.filename_input.SetValue(openFileDialog.GetPath())
        
        openFileDialog.Destroy()
    
  
    def OnKeyMetadata(self, evt): 
        
        keyslot = self.keyslot.GetValue()
        pubkey = self.pubkey.GetValue()
        
        
        self.text_display.AppendText("Reading out Metadata of OPTIGA™ TrustM's Key Slot " + keyslot + " ....\n")
        wx.CallLater(15, self.OnKeyMeta)
    
    # note: this function/command runs for quite a while as compared to ECC.
    def OnKeyMeta(self):
        keyslot = "0x" + self.keyslot.GetValue()
        
        command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_metadata", "-r", keyslot, ])
        self.text_display.AppendText(command_output)
        self.text_display.AppendText("'trustm_metadata -r " + keyslot + "' executed \n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
    
    def OnCertmeta (self, evt):
        pubkey = self.pubkey.GetValue()
        
        
        self.text_display.AppendText("Reading out Metadata for OPTIGA™ TrustM's Public Cert " + pubkey + "....\n")
        wx.CallLater(20, self.OnCertmeta1)
    
    def OnCertmeta1 (self):
        
        if (self.pubkey.GetSelection() == 0):
            Puboid = "E0E0"
           
        elif (self.pubkey.GetSelection() == 1):
            Puboid = "E0E1"
           
        elif (self.pubkey.GetSelection() == 2):
            Puboid = "E0E2"
            
        elif (self.pubkey.GetSelection() == 3):
            Puboid = "E0E3"
            
        elif (self.pubkey.GetSelection() == 4):
            Puboid = "E0E8"     
    
        elif (self.pubkey.GetSelection() == 5):
            Puboid = "E0E9" 
        
        pubkey = "0x" + Puboid
        
        command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_metadata", "-r", pubkey, ])
        self.text_display.AppendText(command_output)
        self.text_display.AppendText("'trustm_metadata -r " + pubkey + "' executed \n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n\n")
       
    
    def OnCertData(self, evt):
        
        pubkey = self.pubkey.GetValue()
        
        
        self.text_display.AppendText("Reading out data stored in OPTIGA™ TrustM's Public Cert: " + pubkey + "....\n")
        wx.CallLater(20, self.OnCertData1)


    def OnCertData1(self):
        
        if (self.pubkey.GetSelection() == 0):
            Puboid = "E0E0"
            
        
        elif (self.pubkey.GetSelection() == 1):
            Puboid = "E0E1"
            
        elif (self.pubkey.GetSelection() == 2):
            Puboid = "E0E2"
            
        elif (self.pubkey.GetSelection() == 3):
            Puboid = "E0E3"
            
        elif (self.pubkey.GetSelection() == 4):
            Puboid = "E0E8"     
    
        elif (self.pubkey.GetSelection() == 5):
            Puboid = "E0E9" 
        
        pubkey = "0x" + Puboid
        pubcert = Puboid
        
        command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_data", "-r", pubkey, ])
        self.text_display.AppendText(command_output)
        self.text_display.AppendText("'trustm_data -r " + pubkey + "' executed \n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n\n")
   
   
        command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_cert", "-r", pubkey, "-o" , "test" + pubcert + ".crt", ])
       
        output_message = exec_cmd.execCLI([
            "openssl", "x509",
            "-in", "test" + pubcert + ".crt",
            "-text", "-noout", 
        ])
   
        self.text_display.AppendText(output_message)
        self.text_display.AppendText( "\nopenssl x509 -in test" + pubcert + ".crt -text  -noout  executed\n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
   
    def OnWriteCert (self, evt):
        pubcert = self.trustanc.GetValue()
        
        
        self.text_display.AppendText("Writing Certificate into OID : " + pubcert + "....\n") 
        wx.CallLater(20, self.OnWriteCert1)
   
    def OnWriteCert1 (self):
        pubkey = "0x" + self.trustanc.GetValue()
        certfile = self.filename_input.GetValue()
                
        command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_cert", "-w", pubkey, "-i" , certfile, ])
        self.text_display.AppendText(command_output)
        self.text_display.AppendText("'trustm_data -w " + pubkey + "-i " + certfile + " executed \n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
   
   
    def OnWriteSecret (self, evt):
        bindingsecret = self.bindsecret.GetValue()                
        self.text_display.AppendText("Writing Platform Binding Secret into 0xE140:....\n") 
        wx.CallLater(20, self.OnWriteSecret1)
   
    def OnWriteSecret1 (self):
        
        command_output = exec_cmd.createProcess("echo '0102030405060708090A0B0C0D0E0F101112131415161718191A1B1C1D1E1F202122232425262728292A2B2C2D2E2F303132333435363738393A3B3C3D3E3F40' | xxd -r -p > platform_secret.dat", None)
        
        secretoid = "0x" + self.bindsecret.GetValue()
        certfile = self.secretfile.GetValue()
                
        command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_data", "-X" , "-w", secretoid, "-i" , certfile, ])
        self.text_display.AppendText(command_output)
        self.text_display.AppendText("'trustm_data -X -w " + secretoid + "-i " + certfile + " executed \n")
        command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_data", "-X" , "-r", secretoid, ])
        self.text_display.AppendText(command_output)
        self.text_display.AppendText("\n'trustm_data -X -r " + secretoid + " ...executed \n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")


    def OnClear(self, evt):
        self.text_display.Clear()

    # Calling parent of the parent, as direct parent is the notebook,
    # then the second parent is the frame, from which we call the destruction
    def OnBack(self, evt):
        self.Parent.Parent.OnCloseWindow(None)

       

class Tab_APP(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        
        textctrlfont = wx.Font()
        textctrlfont.SetPointSize(11)
        
        dataobject_list = ['F1D0','F1D1','F1D2','F1D3','F1D4','F1D5', 'F1D6', 'F1D7', 'F1D8', 'F1D9', 'F1DA', 'F1DB','F1E0', 'F1E1']
        
        buttonfont = wx.Font(13, wx.ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        
        # declare the sizers
        mainsizer = wx.BoxSizer(wx.VERTICAL)
        input_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        inputbyte_sizer = wx.BoxSizer(wx.HORIZONTAL)
        mainhorisizer = wx.BoxSizer(wx.HORIZONTAL)
        
        midsizer = wx.BoxSizer(wx.VERTICAL)
        
        gdsizer2 = wx.GridSizer(rows=1, cols=1, vgap=10, hgap=10)
        gdsizer3 = wx.GridSizer(rows=4, cols=1, vgap=30, hgap=10)
        
        
        backbuttonsizer = wx.BoxSizer(wx.HORIZONTAL)
        
        # declare sizers that will be in the grid1
        datasizer = wx.BoxSizer(wx.VERTICAL)
        
        # instantiate the objects
        text_data = wx.StaticText(self, 0, "Data Objects ID: ")
        self.data = wx.ComboBox(self, -1, choices=dataobject_list, style=wx.CB_READONLY,  size = wx.Size(170, 30))
        self.data.SetFont(textctrlfont)
        
        self.button_metadata = wx.Button(self, 1, 'Read Metadata of Data Objects ID', size = wx.Size(330, 50))
        self.button_metadata.SetFont(buttonfont)
        button_dataobj = wx.Button(self, 1, 'Read Data of Data Objects ID', size = wx.Size(330, 50))
        button_dataobj.SetFont(buttonfont)
        self.button_writedata = wx.Button(self, 1, 'Write Data into Data Objects ID', size = wx.Size(330, 50))
        self.button_writedata.SetFont(buttonfont)
        
        inputtext = wx.StaticText(self, -1, label="Data Input:")
        self.input_display = wx.TextCtrl(self,value="1234")
        self.input_display.SetFont(textctrlfont)
        
        
        self.text_display = wx.TextCtrl(self, -1, style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.text_display.SetFont(wx.Font(11, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))


        clearimage = wx.Image(config.IMAGEPATH + "/images/clear.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        clearbutton = wx.BitmapButton(self, -1, clearimage)

        
        backimage = wx.Image(config.IMAGEPATH + "/images/back.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        backbutton = wx.BitmapButton(self, -1, backimage)
       
        #Add mainhorisizer to mainsizer
        mainsizer.AddSpacer(2)
        mainsizer.Add(input_sizer, 0, wx.EXPAND | wx.TOP, 5)
        mainsizer.Add(mainhorisizer, 1, wx.EXPAND)
       
        input_sizer.Add(inputtext, 0, wx.ALIGN_CENTRE | wx.ALL , 3)
        input_sizer.Add(self.input_display, 1 ,wx.ALIGN_CENTRE | wx.ALL, 2)
        
       
        # Add Sub Sizers to the mainhorisizer
        mainhorisizer.Add(midsizer, 1, wx.EXPAND )
        mainhorisizer.Add(self.text_display, 2, wx.EXPAND | wx.ALL, 5)
      
        backbuttonsizer.Add(backbutton, 0, wx.ALIGN_LEFT, 0)
        backbuttonsizer.AddSpacer(10)
        backbuttonsizer.Add(clearbutton, 0, wx.EXPAND, 0)

        # Add sizers to midsizer
        midsizer.AddSpacer(10)
        
        
        midsizer.AddSpacer(10)
        midsizer.Add(gdsizer2, 0, wx.ALIGN_CENTRE | wx.ALL, 10)
        
        
        midsizer.AddSpacer(30)
        midsizer.Add(gdsizer3, 0, wx.ALIGN_CENTRE | wx.ALL, 10)
        
        midsizer.AddSpacer(130)
        midsizer.Add(backbuttonsizer,0,wx.LEFT | wx.BOTTOM, 5)
        
        
        #add buttons into gdsizer3
        gdsizer3.AddMany([
           
           (self.button_metadata),
           (button_dataobj),
           (self.button_writedata),
           
       ])
        
        gdsizer2.AddMany([
                (datasizer, 0, wx.EXPAND),

        ])
         
        
        #add objects into sizers in gdsizer2        
        datasizer.Add(text_data)
        datasizer.Add(self.data)

       
        
        # Set Default inputs for Text Boxes      
        self.data.SetSelection(0)
        
        #bind events
        self.button_metadata.Bind(wx.EVT_BUTTON, self.OnMeta1)
        button_dataobj.Bind(wx.EVT_BUTTON, self.OnData)
        self.button_writedata.Bind(wx.EVT_BUTTON, self.OnWrite)
        #self.button_inputbyte.Bind(wx.EVT_BUTTON, self.OnInput)
        
        #self.data.Bind(wx.EVT_COMBOBOX, self.OnType)
        clearbutton.Bind(wx.EVT_BUTTON, self.OnClear)
        backbutton.Bind(wx.EVT_BUTTON, self.OnBack)
        
        
        # Set tooltips        
        self.SetSizer(mainsizer)
        mainsizer.Fit(self)
    
    def OnMeta1(self, evt):
        self.text_display.AppendText("Reading out Metadata of OPTIGA™ TrustM's Data Object ID " + self.data.GetValue() + "....\n")
        wx.CallLater(20, self.OnMeta)
    
    def OnMeta(self):
        
        dataobj = "0x" + self.data.GetValue()
        command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_metadata", "-r", dataobj, ])
        self.text_display.AppendText(command_output)
        self.text_display.AppendText("'trustm_metadata -r " + dataobj + "' executed \n")
        self.text_display.AppendText("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ \n")

    def OnData(self, evt):
        self.text_display.AppendText("\nReading out data stored in OPTIGA™ TrustM's Data Object ID: " + self.data.GetValue() +"....\n")
        wx.CallLater(20, self.OnData1)

    def OnData1(self):
        
        dataobj = "0x" + self.data.GetValue()
        
        command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_data", "-r", dataobj, ])
        self.text_display.AppendText(command_output)
        self.text_display.AppendText("'trustm_data -r " + dataobj + "' executed \n")
        self.text_display.AppendText("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ \n")
        
    def OnWrite(self, evt):
        
        datain = self.input_display.GetValue()
        dataobj = "0x" + self.data.GetValue()
        
        exec_cmd.createProcess("echo " + datain + " >writedata.txt", None)                               
        command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_data", "-w", dataobj, "-e", "-i","writedata.txt" , ])
        self.text_display.AppendText(command_output)
        self.text_display.AppendText("\n'trustm_data -w " + dataobj + " -e  -i  writedata.txt ' executed \n")
        self.text_display.AppendText("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ \n")
        
                
    def OnClear(self, evt):
        self.text_display.Clear()

    # Calling parent of the parent, as direct parent is the notebook,
    # then the second parent is the frame, from which we call the destruction
    def OnBack(self, evt):
        self.Parent.Parent.OnCloseWindow(None)



class Tab_META(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        
        textctrlfont = wx.Font()
        textctrlfont.SetPointSize(11)
        
        buttonfont = wx.Font(11, wx.ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        
        # declare the sizers
        mainsizer = wx.BoxSizer(wx.VERTICAL)
        mainhorisizer = wx.BoxSizer(wx.HORIZONTAL)
        
        midsizer = wx.BoxSizer(wx.VERTICAL)
        gdsizer1 = wx.GridSizer(rows=3, cols=2, vgap=10, hgap=20)
        #gdsizer2 = wx.GridSizer(rows=3, cols=2, vgap=10, hgap=20)
        gdsizer2 = wx.GridSizer(cols=2, vgap=10, hgap=20)
        
        gdsizer3 = wx.GridSizer(rows=1, cols=1, vgap=5, hgap=20)
        gdsizer4 = wx.GridSizer(rows = 1, cols = 1, vgap = 5, hgap = 20)
        gdsizer5 = wx.GridSizer(rows=1, cols=2, vgap=5, hgap=20)
        gdsizer6 = wx.GridSizer(rows=1, cols=1, vgap=0, hgap=20)
        gdsizer7 = wx.GridSizer(rows=1, cols=2, vgap=5, hgap=20)
        gdsizer8 = wx.GridSizer(rows=1, cols=2, vgap=5, hgap=20)
        #gdsizer8 = wx.GridSizer(rows=1, cols=2, vgap = 5, hgap=20 )
        
        file_sizer = wx.BoxSizer(wx.VERTICAL)
        inputmetasizer = wx.BoxSizer(wx.VERTICAL)
        
        backbuttonsizer = wx.BoxSizer(wx.HORIZONTAL)
        
        # declare sizers that will be in the grid2
        
        lcs0sizer = wx.BoxSizer(wx.VERTICAL)
        changesizer = wx.BoxSizer(wx.VERTICAL)
        readsizer = wx.BoxSizer(wx.VERTICAL)
        exesizer = wx.BoxSizer(wx.VERTICAL)

        
        # declare sizers that will be in the grid1
        sysdatasizer = wx.BoxSizer(wx.VERTICAL)
        counterobjsizer = wx.BoxSizer(wx.VERTICAL)
        keysizer = wx.BoxSizer(wx.VERTICAL)
        certsizer = wx.BoxSizer(wx.VERTICAL)
        gendataobjsizer = wx.BoxSizer(wx.VERTICAL)
        bindsecretsizer = wx.BoxSizer(wx.VERTICAL)
        
        # declare sizers that will be in the grid3
        trustoidsizer = wx.BoxSizer(wx.VERTICAL)
        secretoidsizer = wx.BoxSizer(wx.VERTICAL)
        # MUD provision checkbox sizer
        MUDCheckBoxSizer = wx.BoxSizer(wx.VERTICAL)
        
        # general oid data type sizer
        datatypesizer = wx.BoxSizer(wx.VERTICAL)


        # instantiate the objects
        sysdatalist = ['E0C0','E0C1','E0C2','E0C3','E0C4','EOC5','E0C6','E0C9','-']
        key_list = ['E0F0', 'E0F1','E0F2','E0F3','E0FC','E0FD','E200','-']
        counter_list = ['E120','E121','E122','E123','-']
        cert_list = ['E0E1','E0E2','E0E3','E0E8','E0E9','E0EF','-']
        genoid_list = ['F1D0','F1D1','F1D2','F1D3','F1D4','F1D5', 'F1D6', 'F1D7', 'F1D8', 'F1D9', 'F1DA', 'F1DB','F1E0', 'F1E1','-']
        bind_list = ['E140','-']
        
        lcs0_list = ['Creation','Initialization','Operational','Termination']
        change_list = ['ALW','NEV','Lcs0<0x03','Lcs0<0x07','Lcs0<0x0F']
        read_list =  ['ALW','NEV','Lcs0<0x03','Lcs0<0x07','Lcs0<0x0F']
        exe_list = ['ALW','NEV','Lcs0<0x03','Lcs0<0x07','Lcs0<0x0F']
        
        trustoid_list = ['E0E8', 'E0E9', 'E0EF']
        secretoid_list = ['F1D4', 'F1D5','F1D6', 'F1DB']
        
        datatype_list = ['-', 'BSTR', 'UPCTR', 'TA', 'DEVCERT', 'PRESSEC', 'PTFBIND', 'UPDATESEC', 'AUTOREF']
        
        
        text_sysdata = wx.StaticText(self, 0, "System DataObject:")
        self.sysdata = wx.ComboBox(self, 1, choices=sysdatalist, style=wx.CB_READONLY,  size = wx.Size(178, -1))
        self.sysdata.SetFont(textctrlfont)
        
        text_counterobj = wx.StaticText(self, 0, "Counter Objects:")
        self.counterobj = wx.ComboBox(self, 1, choices=counter_list, style=wx.CB_READONLY,  size = wx.Size(178, -1))
        self.counterobj.SetFont(textctrlfont)
        
        text_key = wx.StaticText(self, 0, "ECC/RSA/AES key")
        self.key = wx.ComboBox(self, 1, choices=key_list, style=wx.CB_READONLY,  size = wx.Size(178, -1))
        self.key.SetFont(textctrlfont)
        
        text_cert = wx.StaticText(self, 0, "Cert")
        self.cert = wx.ComboBox(self, 1, choices=cert_list, style=wx.CB_READONLY,  size = wx.Size(178, -1))
        self.cert.SetFont(textctrlfont)
        
        text_gendataobj = wx.StaticText(self, 0, "General OID")
        self.gendataobj = wx.ComboBox(self, 1, choices=genoid_list, style=wx.CB_READONLY,  size = wx.Size(178, -1))
        self.gendataobj.SetFont(textctrlfont)
        
        text_bindsecret = wx.StaticText(self, 0, "Binding_Secret:")
        self.bindsecret = wx.ComboBox(self, 1, choices=bind_list,style=wx.CB_READONLY, size = wx.Size(178, -1))
        self.bindsecret.SetFont(textctrlfont)
        
        text_lcs0 = wx.StaticText(self, 0, "Lcs0:4 modes")
        self.lcs0 = wx.ComboBox(self, 1, choices=lcs0_list,style=wx.CB_READONLY, size = wx.Size(178, -1))
        self.lcs0.SetFont(textctrlfont)
        
        text_change = wx.StaticText(self, 0, "Change")
        self.change = wx.ComboBox(self, 1, choices=change_list,style=wx.CB_READONLY, size = wx.Size(178, -1))
        self.change.SetFont(textctrlfont)
        
        text_read = wx.StaticText(self, 0, "Read")
        self.read = wx.ComboBox(self, 1, choices=read_list,style=wx.CB_READONLY, size = wx.Size(178, -1))
        self.read.SetFont(textctrlfont)
        
        text_exe = wx.StaticText(self, 0, "Exe")
        self.exe = wx.ComboBox(self, 1, choices=exe_list,style=wx.CB_READONLY, size = wx.Size(178, -1))
        self.exe.SetFont(textctrlfont)
        
        # general OID data type
        text_oid_datatype = wx.StaticText(self, 0, "General OID data type")
        self.oid_datatype = wx.ComboBox(self, 1, choices=datatype_list, style=wx.CB_READONLY, size=wx.Size(178, -1))
        self.oid_datatype.SetFont(textctrlfont)
        #
        
        text_trust_anchor_oid = wx.StaticText(self, -1, "trust_anchor_oid:")
        self.trust_anchor_oid = wx.ComboBox(self, 1, choices=trustoid_list, style=wx.CB_READONLY, size = wx.Size(178, -1))
        self.trust_anchor_oid.SetFont(textctrlfont)
        

        
        text_secret_oid = wx.StaticText(self, -1, "secret_oid:")
        self.secret_oid = wx.ComboBox(self, 1, choices=secretoid_list, style=wx.CB_READONLY,  size = wx.Size(178, -1))
        self.secret_oid.SetFont(textctrlfont)
        
        # checkbox for MUD provision
        self.MUDCheckBox = wx.CheckBox(self, label = 'MUD Provision', style = wx.CHK_2STATE)
        self.MUDCheckBox.SetValue(True) # default to checked
        #
        

        self.custom_metadata_input = wx.TextCtrl(self, -1, value = "Custom Metadata", size = (190, 30))
        self.custom_metadata_input.SetFont(textctrlfont)
        
#       test
        button_write_metadata = wx.Button(self, 1, 'Write Metadata', size = (178, -1))
        button_write_metadata.SetFont(buttonfont)
#       

        # button to read current metadata
        button_read_metadata = wx.Button(self, 1, 'Read Metadata', size = (178, -1))
        button_read_metadata.SetFont(buttonfont)
        #

        button_reset_mud = wx.Button(self, 1, 'Reset MUD', size = wx.Size(190, -1))
        button_reset_mud.SetFont(buttonfont)
        button_write_custom_metadata = wx.Button(self, 1, 'Write Custom Metadata', size = wx.Size(190, -1))
        button_write_custom_metadata.SetFont(buttonfont)
        
        
        
        #button_save_custom_metadata = wx.Button(self, 1, 'Save Custom Metadata', size = wx.Size(178, -1))
        #button_save_custom_metadata.SetFont(buttonfont)

        
        self.text_display = wx.TextCtrl(self, -1, style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.text_display.SetFont(wx.Font(11, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))


        clearimage = wx.Image(config.IMAGEPATH + "/images/clear.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        clearbutton = wx.BitmapButton(self, -1, clearimage)
        
        
        backimage = wx.Image(config.IMAGEPATH + "/images/back.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        backbutton = wx.BitmapButton(self, -1, backimage)
       
        #Add mainhorisizer to mainsizer
        mainsizer.Add(mainhorisizer, 1, wx.EXPAND)
       
        # Add Sub Sizers to the mainhorisizer
        mainhorisizer.Add(midsizer, 1, wx.EXPAND)
        mainhorisizer.Add(self.text_display, 2, wx.EXPAND | wx.ALL, 5)
        
        # Add Objects to backbuttonsizer
        #leftsizer.Add(backbuttonsizer, 0, wx.LEFT | wx.BOTTOM, 10)
        
        backbuttonsizer.Add(backbutton, 0, wx.ALIGN_LEFT, 0)
        backbuttonsizer.AddSpacer(10)
        backbuttonsizer.Add(clearbutton, 0, wx.EXPAND, 0)

        # Add sizers to midsizer
        midsizer.AddSpacer(10)
        midsizer.Add(gdsizer1, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        midsizer.AddSpacer(10)
        midsizer.Add(gdsizer2, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        
        midsizer.AddSpacer(0)
        midsizer.Add(gdsizer3, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        
        midsizer.AddSpacer(0)
        midsizer.Add(gdsizer4, 0, wx.LEFT | wx.ALL, 5)
        
        midsizer.AddSpacer(0)
        midsizer.Add(gdsizer5, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        #midsizer.AddSpacer()
        midsizer.Add(gdsizer6, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        midsizer.AddSpacer(10)
        midsizer.Add(gdsizer7, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        midsizer.AddSpacer(10)
        midsizer.Add(gdsizer8, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        #midsizer.AddSpacer(5)
        #midsizer.Add(gdsizer8, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        midsizer.AddSpacer(10)
        midsizer.Add(backbuttonsizer,0,wx.LEFT | wx.BOTTOM, 5)
        
        
        
        #add buttons into gdsizer3
        gdsizer2.AddMany([
            (lcs0sizer, 0, wx.EXPAND),
            (changesizer, 0, wx.EXPAND),
            (readsizer, 0, wx.EXPAND),
            (exesizer, 0, wx.EXPAND),

        ])
        
        #add sizers to gdsizer1
        gdsizer1.AddMany([
                (sysdatasizer, 0, wx.EXPAND),
                (counterobjsizer, 0, wx.EXPAND),
                (keysizer, 0, wx.EXPAND),
                (certsizer, 0, wx.EXPAND),
                (gendataobjsizer, 0, wx.EXPAND),
                (bindsecretsizer, 0, wx.EXPAND),
        ])
        
        #add sizers to gdsizer3
        #gdsizer3.AddMany([(button_write_metadata),])
        
        gdsizer3.AddMany([(datatypesizer, 0, wx.EXPAND), ])
        
        gdsizer4.AddMany([(MUDCheckBoxSizer, 0, wx.EXPAND),])
        
        
        #add sizers to gdsizer4
        gdsizer5.AddMany([
                (trustoidsizer, 0, wx.EXPAND),
                (secretoidsizer, 0, wx.EXPAND),
        ])
        

        gdsizer6.AddMany([(button_reset_mud),])
        
                
        gdsizer7.AddMany([(button_read_metadata),
                (button_write_metadata),])
        

        gdsizer8.AddMany([(file_sizer),
                        (button_write_custom_metadata),])
        

                
        #add objects into sizers in gdsizer1
        sysdatasizer.Add(text_sysdata)
        sysdatasizer.Add(self.sysdata)
        
        counterobjsizer.Add(text_counterobj)
        counterobjsizer.Add(self.counterobj)
        
        keysizer.Add(text_key)
        keysizer.Add(self.key)
        
        certsizer.Add(text_cert)
        certsizer.Add(self.cert)
        gendataobjsizer.Add(text_gendataobj)
        gendataobjsizer.Add(self.gendataobj)
        
        bindsecretsizer.Add(text_bindsecret)
        bindsecretsizer.Add(self.bindsecret)
        
        lcs0sizer.Add(text_lcs0)
        lcs0sizer.Add(self.lcs0)
        changesizer.Add(text_change)
        changesizer.Add(self.change)
        readsizer.Add(text_read)
        readsizer.Add(self.read)
        exesizer.Add(text_exe)
        exesizer.Add(self.exe)
        file_sizer.Add(self.custom_metadata_input)

        
        # oid datatype sizer
        datatypesizer.Add(text_oid_datatype)
        datatypesizer.Add(self.oid_datatype)
        #
        


        #add objects into sizers in gdsizer2
        trustoidsizer.Add(text_trust_anchor_oid)
        trustoidsizer.Add(self.trust_anchor_oid)
#         targetoidsizer.Add(text_target_oid)
#         targetoidsizer.Add(self.target_oid)
        secretoidsizer.Add(text_secret_oid)
        secretoidsizer.Add(self.secret_oid)


        # MUD Checkbox sizer
        MUDCheckBoxSizer.Add(self.MUDCheckBox)


        # helper function to choose the last item in the list
        def lastIndex(inputList:list) -> int:
            return len(inputList) - 1
        #

        
        # Set Default inputs for Text Boxes      
        self.sysdata.SetSelection(lastIndex(sysdatalist))
        self.counterobj.SetSelection(lastIndex(counter_list))
        self.key.SetSelection(lastIndex(key_list))
        self.cert.SetSelection(lastIndex(cert_list))
        self.gendataobj.SetSelection(lastIndex(genoid_list))
        self.bindsecret.SetSelection(lastIndex(bind_list))
        
        self.oid_datatype.SetSelection(0)
        self.oid_datatype.Disable()
        
        self.lcs0.SetSelection(0)
        self.change.SetSelection(3)
        self.read.SetSelection(0)
        self.exe.SetSelection(0)
        self.trust_anchor_oid.SetSelection(0)
        self.secret_oid.SetSelection(0)
       

        # attach objects to the sizer
        # declare and bind events
        self.sysdata.Bind(wx.EVT_COMBOBOX, self.OnSys)
        self.counterobj.Bind(wx.EVT_COMBOBOX, self.OnCounter)
        self.key.Bind(wx.EVT_COMBOBOX, self.OnKey)
        self.cert.Bind(wx.EVT_COMBOBOX, self.OnCert)
        self.gendataobj.Bind(wx.EVT_COMBOBOX, self.OnGen)
        self.bindsecret.Bind(wx.EVT_COMBOBOX,self.OnBind)
        self.custom_metadata_input.Bind(wx.EVT_LEFT_DOWN, self.OnClickFileName)
# for normal write metadata
        self.lcs0.Bind(wx.EVT_COMBOBOX, self.OnLcs0)
        self.change.Bind(wx.EVT_COMBOBOX, self.OnChange)
        self.read.Bind(wx.EVT_COMBOBOX, self.OnRead)
        self.exe.Bind(wx.EVT_COMBOBOX, self.OnExe)
#
        clearbutton.Bind(wx.EVT_BUTTON, self.OnClear)
        backbutton.Bind(wx.EVT_BUTTON, self.OnBack)
        #self.input.Bind(wx.EVT_LEFT_DOWN,self.OnClickFileName)
# for normal write metadata
        button_write_metadata.Bind(wx.EVT_BUTTON, self.OnWriteMetadata)
#
        button_write_custom_metadata.Bind(wx.EVT_BUTTON, self.OnWriteCustomMetadata)
        #button_save_custom_metadata.Bind(wx.EVT_BUTTON, self.OnSaveMetadata)
        
        # for reading metadata
        button_read_metadata.Bind(wx.EVT_BUTTON, self.OnReadMetadata)
        #
        
        # for MUD provision checkbox
        self.MUDCheckBox.Bind(wx.EVT_CHECKBOX, self.OnMUDCheckBox)
        #
        
        # for reset access conditions
        button_reset_mud.Bind(wx.EVT_BUTTON, self.OnResetAccess)

        self.SetSizer(mainsizer)
        mainsizer.Fit(self)   
        

    def OnSys(self, evt):
        
        if (self.sysdata.GetValue() == '-'):
            self.counterobj.Enable()
            self.key.Enable()
            self.cert.Enable()
            self.gendataobj.Enable()
            self.bindsecret.Enable()
            
        else:
            self.counterobj.Disable()
            self.key.Disable()
            self.cert.Disable()
            self.gendataobj.Disable()
            self.bindsecret.Disable()
            self.oid_datatype.SetSelection(0)
            self.oid_datatype.Disable()

        self.dataobject = self.sysdata.GetValue()

    def OnCounter(self, evt):
        
        if (self.counterobj.GetValue() == '-'):
            self.sysdata.Enable()
            self.key.Enable()
            self.cert.Enable()
            self.gendataobj.Enable()
            self.bindsecret.Enable()
            
        else:
            self.sysdata.Disable()
            self.key.Disable()
            self.cert.Disable()
            self.gendataobj.Disable()
            self.bindsecret.Disable()
            self.oid_datatype.SetSelection(0)
            self.oid_datatype.Disable()
          
        self.dataobject = self.counterobj.GetValue() 
          
    def OnKey(self, evt):
        
        if (self.key.GetValue() == '-'):
            self.sysdata.Enable()
            self.counterobj.Enable()
            self.cert.Enable()
            self.gendataobj.Enable()
            self.bindsecret.Enable()
            
        else:
            self.sysdata.Disable()
            self.counterobj.Disable()
            self.cert.Disable()
            self.gendataobj.Disable()
            self.bindsecret.Disable()
            self.oid_datatype.SetSelection(0)
            self.oid_datatype.Disable()
      
        self.dataobject = self.key.GetValue()
      
    def OnCert(self, evt):
        
        if (self.cert.GetValue() == '-'):
            self.sysdata.Enable()
            self.counterobj.Enable()
            self.key.Enable()
            self.gendataobj.Enable()
            self.bindsecret.Enable()
            
        else:
            self.sysdata.Disable()
            self.counterobj.Disable()
            self.key.Disable()
            self.gendataobj.Disable()
            self.bindsecret.Disable() 
            self.oid_datatype.SetSelection(0)
            self.oid_datatype.Disable()
        
        self.dataobject = self.cert.GetValue()
        
    def OnGen(self, evt):
        
        if (self.gendataobj.GetValue() == '-'):
            self.sysdata.Enable()
            self.counterobj.Enable()
            self.key.Enable()
            self.cert.Enable()
            self.bindsecret.Enable()
            self.oid_datatype.SetSelection(0)
            self.oid_datatype.Disable()
            
        else:
            self.sysdata.Disable()
            self.counterobj.Disable()
            self.key.Disable()
            self.cert.Disable()
            self.bindsecret.Disable()   
            self.oid_datatype.Enable() 

        self.dataobject = self.gendataobj.GetValue()

    def OnBind(self, evt):
        
        if (self.bindsecret.GetValue() == '-'):
            self.sysdata.Enable()
            self.counterobj.Enable()
            self.key.Enable()
            self.cert.Enable()
            self.gendataobj.Enable()
            
        else:
            self.sysdata.Disable()
            self.counterobj.Disable()
            self.key.Disable()
            self.cert.Disable()
            self.gendataobj.Disable()
            self.oid_datatype.SetSelection(0)
            self.oid_datatype.Disable()
    
        self.dataobject = self.bindsecret.GetValue()
        
    def OnLcs0(self, evt):
        self.lcs0value = self.lcs0.GetValue()
        
        if (self.lcs0.GetValue() == 'Operational' or self.lcs0.GetValue() == 'Termination'):
                wx.CallLater(20, self.OnLcs0Warning)
        
    def OnLcs0Warning(self):
        if (self.MUDCheckBox.GetValue() == False):
        
                warningDialog = wx.MessageDialog(None, "Warning: Any manipulation with the lifecycle state might lock the data key/slot permanently. As a safety measure, \"MUD Provision\" has been enabled. This is NOT REVERSIBLE WITHOUT MUD PROVISION. Continue?", 'Warning', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_WARNING)
                result = warningDialog.ShowModal()
        
                if result == wx.ID_YES:
                        self.lcs0value = self.lcs0.GetValue()
                        self.MUDCheckBox.SetValue(True)
                        self.trust_anchor_oid.Enable()
                        self.secret_oid.Enable()
                        
                else:
                        self.lcs0.SetSelection(0)
                        self.lcs0value = self.lcs0.GetValue()
                
                warningDialog.Destroy()
        
    def OnChange(self, evt):
        self.changevalue = self.change.GetValue()

    def OnRead(self, evt):
        self.readvalue = self.read.GetValue()    
        
    def OnExe(self, evt):
        self.exevalue = self.exe.GetValue()
    
    def OnClickFileName(self, evt):
        frame = wx.Frame(None, -1, '*.*')
        frame.SetSize(0,0,200,50)
            
        #openFileDialog = wx.FileDialog(frame, "Open", "", "","All|*.bin;*.crt|Binary|*.bin|Certificate|*.crt", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        openFileDialog = wx.FileDialog(frame, "Open", "", "","Text|*.txt", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        cert_dir= config.IMAGEPATH + "/working_space/"
        openFileDialog.SetDirectory(cert_dir)
        openFileDialog.SetFilename("Custom_Metadata.txt")
        
        if openFileDialog.ShowModal() ==wx.ID_CANCEL:
            
                return
        print((openFileDialog.GetPath()))
        
        self.inputpath = os.path.dirname((openFileDialog.GetPath()))
        self.inputMetadata = (openFileDialog.GetPath())
        
        self.custom_metadata_input.Clear()
        self.custom_metadata_input.AppendText(os.path.basename(openFileDialog.GetPath()))
        
        openFileDialog.Destroy()
        
        wx.CallLater(15, self.OnSaveCustomMetadata)
    
# normal metadata write
    def OnWriteMetadata(self, evt):
        try:
                DataObject = self.dataobject
                
                if (self.MUDCheckBox.GetValue() == True):
                        wx.CallLater(15, self.OnWriteMetadataWithMUDExec)
                
                else :
                        self.text_display.AppendText("Writing Metadata to OPTIGA™ TrustM's Data Object " + DataObject + " ....\n")
                        wx.CallLater(15, self.OnWriteMetadataExec)

        except AttributeError:
                wx.CallLater(10, self.OnNoOIDSelected)

        
    def OnNoOIDSelected(self):
        infoDialog = wx.MessageDialog(None, "Select Target OID To Write/Read Metadata", "No Target OID Selected", wx.OK | wx.ICON_INFORMATION)
        infoDialog.ShowModal()
        
    def OnWriteMetadataWithMUDExec(self):
        trust_anchor_oid = "0x" + self.trust_anchor_oid.GetValue()
        secret_oid = "0x" + self.secret_oid.GetValue()
        target_oid = "0x" + self.dataobject
        
        TRUST_ANCHOR_META = "2003E80111"
        PROTECTED_UPDATE_SECRET_META = "200BD103E1FC07D30100E80123"
        TARGET_OID_META="2010C1020000F00101D80721" + self.trust_anchor_oid.GetValue() + "FD20" + self.secret_oid.GetValue()
        
        
        #Step1: Provisioning metadata for Trust Anchor
        self.text_display.AppendText("Provisioning for trust anchor metadata... \n")
        command_output = exec_cmd.createProcess("echo " + TRUST_ANCHOR_META + " | xxd -r -p > trust_anchor_metadata.bin", None)
        self.text_display.AppendText("'echo $TRUST_ANCHOR_META | xxd -r -p > trust_anchor_metadata.bin' executed \n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
        
        self.text_display.AppendText("Writing trust_anchor_metadata.bin as metadata of Trust Anchor OID... \n")
        command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_metadata", "-w", trust_anchor_oid, "-F", "trust_anchor_metadata.bin", ])
        self.text_display.AppendText(command_output)
        self.text_display.AppendText("'trustm_metadata -w 0x" + trust_anchor_oid + " -F trust_anchor_metadata.bin'" + " executed \n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
        
        
        #Step2: Provisioning metadata for Protected Update Secret OID
        self.text_display.AppendText("Provisioning for protected update secret metadata... \n")
        command_output = exec_cmd.createProcess("echo " + PROTECTED_UPDATE_SECRET_META + " | xxd -r -p > protected_update_secret_metadata.bin", None)
        self.text_display.AppendText("'$PROTECTED_UPDATE_SECRET_META xxd -r -p > protected_update_secret_metadata.bin' executed \n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
        
        self.text_display.AppendText("Writing protected update secret metadata into secret_oid... ")
        command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_metadata", "-w", secret_oid, "-F", "protected_update_secret_metadata.bin", ])
        self.text_display.AppendText(command_output)
        self.text_display.AppendText("'trustm_metadata -w " + secret_oid + " -F protected_update_secret_metadata.bin' executed \n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
        
        ##Set metadata for Target OID
        self.text_display.AppendText("Set metadata protected update for Target OID (Provision for Target OID)... \n")
        command_output = exec_cmd.createProcess("echo " + TARGET_OID_META + " | xxd -r -p > targetOID_metadata.bin", None)
        self.text_display.AppendText("'$TARGET_OID_META | xxd -r -p > targetOID_metadata.bin' executed \n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
        self.text_display.AppendText("Writing targetOID_metadata.bin as metadata of Target OID... \n")
        command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_metadata", "-w", target_oid, "-F", "targetOID_metadata.bin", ])
        self.text_display.AppendText(command_output)
        self.text_display.AppendText("'trustm_metadata -w " + target_oid + " -F targetOID_metadata.bin' executed \n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
        
        wx.CallLater(15, self.OnWriteMetadataExec)
        
        
    def OnWriteMetadataExec(self):
        DataObject = "0x" + self.dataobject
        MetadataToWrite = ""
        
        if (self.change.GetValue() == 'ALW'):
                changeToWrite = "-Ca"
        if (self.change.GetValue() == 'NEV'):
                changeToWrite = "-Cn"
        if (self.change.GetValue() == 'Lcs0<0x03'):
                changeToWrite = "-Ci"        
        if (self.change.GetValue() == 'Lcs0<0x07'):
                changeToWrite = "-Co"
        if (self.change.GetValue() == 'Lcs0<0x0F'):
                changeToWrite = "-Ct"
                
        if (self.read.GetValue() == 'ALW'):
                readToWrite = "-Ra"
        if (self.read.GetValue() == 'NEV'):
                readToWrite = "-Rn"
        if (self.read.GetValue() == 'Lcs0<0x03'):
                readToWrite = "-Ri"        
        if (self.read.GetValue() == 'Lcs0<0x07'):
                readToWrite = "-Ro"
        if (self.read.GetValue() == 'Lcs0<0x0F'):
                readToWrite = "-Rt"

        if (self.exe.GetValue() == 'ALW'):
                exeToWrite = "-Ea"
        if (self.exe.GetValue() == 'NEV'):
                exeToWrite = "-En"
        if (self.exe.GetValue() == 'Lcs0<0x03'):
                exeToWrite = "-Ei"        
        if (self.exe.GetValue() == 'Lcs0<0x07'):
                exeToWrite = "-Eo"
        if (self.exe.GetValue() == 'Lcs0<0x0F'):
                exeToWrite = "-Et"
                
        if (self.lcs0.GetValue() == 'Creation'):
                lcs0ToWrite = ""
        if (self.lcs0.GetValue() == 'Initialization'):
                lcs0ToWrite = "-I"
        if (self.lcs0.GetValue() == 'Operational'):
                lcs0ToWrite = "-O"
        if (self.lcs0.GetValue() == 'Termination'):
                lcs0ToWrite = "-T"        
        
        # if changing data type is selected
        if (self.oid_datatype.GetValue() != '-'):
                datatype = "2003E801"
                
                if (self.oid_datatype.GetValue() == 'BSTR'):
                        datatype += "00"
                
                elif (self.oid_datatype.GetValue() == 'UPCTR'):
                        datatype += "01"
                
                elif (self.oid_datatype.GetValue() == 'TA'):
                        datatype += "11"
                        
                elif (self.oid_datatype.GetValue() == 'DEVCERT'):
                        datatype += "12"
                
                elif (self.oid_datatype.GetValue() == 'PRESSEC'):
                        datatype += "21"
        
                elif (self.oid_datatype.GetValue() == 'PTFBIND'):
                        datatype += "22"
                
                elif (self.oid_datatype.GetValue() == 'UPDATSEC'):
                        datatype += "23"
                        
                elif (self.oid_datatype.GetValue() == 'AUTOREF'):
                        datatype += "31"
                        
                else:
                        datatype += "00" #default to BSTR
                
                datatype_file = config.IMAGEPATH + "/working_space/datatype_meta.bin"
                
                # writing data type metadata seperately since the linux cli commands dont support 
                with open (datatype_file, "wb") as file:
                        file.write(unhexlify(datatype))
                
                command_output = exec_cmd.execCLI(["hd", datatype_file,])
                self.text_display.AppendText("Contents of the data type file:\n")
                self.text_display.AppendText(command_output)
                
                command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_metadata", "-w", DataObject,"-F", datatype_file ])
                self.text_display.AppendText(command_output)
                self.text_display.AppendText("'trustm_metadata -w " + DataObject + " -F " + datatype_file + "' executed \n")
                self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
                
                
        command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_metadata", "-w", DataObject, changeToWrite, readToWrite, exeToWrite, lcs0ToWrite])
        self.text_display.AppendText(command_output)
        self.text_display.AppendText("'trustm_metadata -w " + DataObject + " " + changeToWrite + " " + readToWrite + " " + exeToWrite + " " + lcs0ToWrite + "' executed \n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
#
        
    def OnResetAccess(self, evt):
        try:
                DataObject = self.dataobject
                self.text_display.AppendText("Resetting Metadata Update Description tag for Target OID 0x" + DataObject + "\n")
                wx.CallLater(10, self.OnResetAccessExec)
        
        except AttributeError:
                wx.CallLater(10, self.OnNoOIDSelected)
        
    def OnResetAccessExec(self):
        RESET_MUD_META="2003D801FF"
        target_oid = "0x" + self.dataobject
        exec_cmd.createProcess("echo " + RESET_MUD_META + " | xxd -r -p > mud_reset.bin", None)
        command_output = exec_cmd.execCLI(["xxd", "mud_reset.bin", ])
        self.text_display.AppendText(command_output)
        self.text_display.AppendText("mud_reset.bin generated\n")
        self.text_display.AppendText("Writing metadata for Target OID... \n")
        exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_metadata", "-w", target_oid, "-F", "mud_reset.bin", ])
        self.text_display.AppendText("'trustm_metadata -w " + target_oid + " -F mud_reset.bin' executed \n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
        
    def OnSaveMetadata(self, evt):
        metadataInput = self.custom_metadata_input.GetValue()
        if (len(metadataInput) % 2 != 0):
                errorDialog = wx.MessageDialog(None, "Invalid Metadata Input", 'Error', wx.OK | wx.ICON_ERROR)
                if (errorDialog.ShowModal() == wx.ID_OK):
                        return
        
        
       # print(inputToFile)
        
        frame = wx.Frame(None, -1, '*.*')
        frame.SetSize(0,0,200,50)
        
        saveFileDialog = wx.FileDialog(frame, "Save Metadata", "", "", "Binary|*.bin|All|*.*", wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        saveFileDialog.SetDirectory(config.IMAGEPATH + "/working_space/")
        
        
        if saveFileDialog.ShowModal() == wx.ID_CANCEL :
                return
        
        self.saveFilePath = saveFileDialog.GetPath()
        
        with open(self.saveFilePath, "wb") as file:
               file.write(unhexlify(metadataInput))
         
        saveFileDialog.Destroy()

    def OnSaveCustomMetadata(self):
        try:
                customMetadataBin = self.inputpath + "/custom_metadata.bin"
                
                with open(self.inputMetadata) as f, open(customMetadataBin, 'wb') as fout:
                        for line in f:
                                fout.write(unhexlify(''.join(line.split())))
                
                command_output = exec_cmd.execCLI(["hd", customMetadataBin,])
                self.text_display.AppendText("Contents of the custom metadata file:\n")
                self.text_display.AppendText(command_output)
                
        except AttributeError:
                wx.CallLater(10, self.OnNoMetadataFileSelected)
                
    def OnNoMetadataFileSelected(self):
        infoDialog = wx.MessageDialog(None, "Select Metadata File to Write to Target OID", "No Metadata File Selected", wx.OK | wx.ICON_INFORMATION)
        infoDialog.ShowModal()

    def OnMUDCheckBox(self, evt):
        cb = evt.GetEventObject()
        
        if (cb.GetValue() == False):
                self.trust_anchor_oid.Disable()
                self.secret_oid.Disable()
                
        else:
                self.trust_anchor_oid.Enable()
                self.secret_oid.Enable()
                
        # add warning regarding LCS0
        if (cb.GetValue() == False and (self.lcs0.GetValue() == 'Operational' or self.lcs0.GetValue() == 'Termination')):
                warningDialog = wx.MessageDialog(None, "Warning: Any manipulation with the lifecycle state might lock the data key/slot permanently. As a safety measure, \"MUD Provision\" has been enabled. This is NOT REVERSIBLE WITHOUT MUD PROVISION. Continue?", 'Warning', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_WARNING)
                result = warningDialog.ShowModal()
                
                if (result == wx.ID_YES):
                        self.MUDCheckBox.SetValue(True)
                        self.trust_anchor_oid.Enable()
                        self.secret_oid.Enable()
                        
                else:
                        self.MUDCheckBox.SetValue(False)
                        self.lcs0.SetSelection(0)
                        self.trust_anchor_oid.Disable()
                        self.secret_oid.Disable()
                        
                warningDialog.Destroy()
    
     
    def OnMetadata(self, evt): 
        
        DataObject = self.dataobject
        
        self.text_display.AppendText("Writing Metadata to OPTIGA™ TrustM's Data Object " + DataObject + " ....\n")
        wx.CallLater(15, self.OnMetadata1)
        
    def OnWriteCustomMetadata(self, evt):
        try:
                DataObject = self.dataobject
        
                self.text_display.AppendText("Writing Metadata to OPTIGA™ TrustM's Data Object " + DataObject + " ....\n")
                wx.CallLater(10, self.OnMetadata1)
                
        except AttributeError:
                wx.CallLater(10, self.OnNoOIDSelected)
        
    def OnMetadata1(self):
        try:
                DataObject = "0x" + self.dataobject
                inputfile = self.inputpath + "/custom_metadata.bin"
        
                command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_metadata", "-w", DataObject,"-F", inputfile ])
                self.text_display.AppendText(command_output)
                self.text_display.AppendText("'trustm_metadata -w " + DataObject + " -F " + inputfile + "' executed \n")
                self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
                
        except AttributeError:
                wx.CallLater(10, self.OnNoMetadataFileSelected)

    def OnReadMetadata(self, evt):
        try:
                self.text_display.AppendText("Reading out Metadata of OPTIGA™ TrustM's Data Object ID " + self.dataobject + "....\n")
                wx.CallLater(20, self.OnReadMetadataExec)
        
        except AttributeError:
                wx.CallLater(20, self.OnNoOIDSelected)
                
    def OnReadMetadataExec(self):
        dataobj = "0x" + self.dataobject
        command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_metadata", "-r", dataobj, ])
        self.text_display.AppendText(command_output)
        self.text_display.AppendText("'trustm_metadata -r " + dataobj + "' executed \n")
        self.text_display.AppendText("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ \n")

    def OnClear(self, evt):
        self.text_display.Clear()

    # Calling parent of the parent, as direct parent is the notebook,
    # then the second parent is the frame, from which we call the destruction
    def OnBack(self, evt):
        self.Parent.Parent.OnCloseWindow(None)

class Tab1Frame(wx.Frame):
    
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title="General", size=(1280, 720), style=(wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX)))
        self.Centre(wx.BOTH)
        main_menu_font = wx.Font(12, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.SetFont(main_menu_font)
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

        # Instantiate all objects
        self.tab_base = wx.Notebook(self, id=wx.ID_ANY, style=wx.NB_TOP)
        self.tab1_gen = Tab_GEN(self.tab_base)
        self.tab2_key = Tab_KEY(self.tab_base)
        self.tab3_app = Tab_APP(self.tab_base)
        self.tab4_meta = Tab_META(self.tab_base)

        # Add tabs
        self.tab_base.AddPage(self.tab1_gen, 'General')
        self.tab_base.AddPage(self.tab2_key, 'Private Key and Cert OID')        
        self.tab_base.AddPage(self.tab3_app, 'Application Data OID')
        self.tab_base.AddPage(self.tab4_meta, 'Write Metadata')
        

        self.Show(True)
              
    
    def OnCloseWindow(self, evt):
        self.Parent.Show()
        self.Destroy()
