import wx
import shell_util as exec_cmd
import misc_dialogs as misc
import images as img
import config
from binascii import unhexlify


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


        clearimage = wx.Image('../images/clear.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        clearbutton = wx.BitmapButton(self, -1, clearimage)

        
        backimage = wx.Image('../images/back.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
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
        
        keyslot_list = ['E0F0', 'E0F1','E0F2','E0F3','E0FC', 'E0FD','E200']
        pubkey_list = ['E0E0-PreProvisioned', 'E0E1', 'E0E2','E0E3', 'E0E8-TrustAnchor','E0E9-TrustAnchor',]
        Destination_list = ['E0E1','E0E2','E0E3','E0E8','E0E9',]
        
        buttonfont = wx.Font(13, wx.ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        
        # declare the sizers
        mainsizer = wx.BoxSizer(wx.VERTICAL)
        input_sizer = wx.BoxSizer(wx.HORIZONTAL)
        mainhorisizer = wx.BoxSizer(wx.HORIZONTAL)
        
        midsizer = wx.BoxSizer(wx.VERTICAL)
       
        gdsizer1 = wx.GridSizer(rows=2, cols=1, vgap=10, hgap=10)
        gdsizer2 = wx.GridSizer(rows=3, cols=1, vgap=10, hgap=10)
        gdsizer3 = wx.GridSizer(rows=1, cols=2, vgap=10, hgap=10)
        gdsizer4 = wx.GridSizer(rows=1, cols=1, vgap=5, hgap=10)
        backbuttonsizer = wx.BoxSizer(wx.HORIZONTAL)
        
        # declare sizers that will be in the grid1
        pubkeysizer = wx.BoxSizer(wx.VERTICAL)
        keyslotsizer = wx.BoxSizer(wx.VERTICAL)
        trustancsizer = wx.BoxSizer(wx.VERTICAL)
        fileinputsizer = wx.BoxSizer(wx.VERTICAL)
       
        
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
        self.filename_input = wx.TextCtrl(self, -1, value="testE0E0.crt", style=(wx.TE_CHARWRAP|wx.TE_MULTILINE), size=(170, 30))
        self.filename_input.SetFont(textctrlfont)
        
        self.text_display = wx.TextCtrl(self, -1, style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.text_display.SetFont(wx.Font(11, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))


        clearimage = wx.Image('../images/clear.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        clearbutton = wx.BitmapButton(self, -1, clearimage)

        
        backimage = wx.Image('../images/back.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
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

        midsizer.AddSpacer(5)
        midsizer.Add(gdsizer1, 0, wx.ALIGN_CENTRE | wx.ALL, 10)
        
        midsizer.AddSpacer(10)
        midsizer.Add(gdsizer2, 0, wx.ALIGN_CENTRE | wx.ALL, 10)
        
        
        midsizer.AddSpacer(10)
        midsizer.Add(gdsizer3, 0, wx.ALIGN_CENTRE | wx.ALL, 10)
        
        midsizer.AddSpacer(10)
        midsizer.Add(gdsizer4, 0, wx.ALIGN_CENTRE | wx.ALL, 10)
        
        midsizer.AddSpacer(110)
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
 
        #add objects into sizers in gdsizer2
        keyslotsizer.Add(text_keyslot)
        keyslotsizer.Add(self.keyslot)
        
        pubkeysizer.Add(text_pubkey)
        pubkeysizer.Add(self.pubkey)
        
        trustancsizer.Add(text_trustanc)
        trustancsizer.Add(self.trustanc)
        
        fileinputsizer.Add(text_filename_input)
        fileinputsizer.Add(self.filename_input)
 
        # Set Default inputs for Combo Boxes      
        self.pubkey.SetSelection(0)
        self.keyslot.SetSelection(0)   
        self.trustanc.SetSelection(2)
        
        #bind events
        self.button_keymetadata.Bind(wx.EVT_BUTTON, self.OnKeyMetadata)
        self.button_certmetadata.Bind(wx.EVT_BUTTON, self.OnCertmeta)
        button_data.Bind(wx.EVT_BUTTON, self.OnCertData)
        button_writecert.Bind(wx.EVT_BUTTON, self.OnWriteCert)
        
        self.filename_input.Bind(wx.EVT_LEFT_DOWN,self.OnClickFileName)
       
        clearbutton.Bind(wx.EVT_BUTTON, self.OnClear)
        backbutton.Bind(wx.EVT_BUTTON, self.OnBack)
        
        
        # Set tooltips
        clearbutton.SetToolTip(wx.ToolTip("Clear all textboxes."))
        backbutton.SetToolTip(wx.ToolTip("Go back to main page."))

        self.SetSizer(mainsizer)
        mainsizer.Fit(self)
        
        if (self.pubkey.GetSelection() == 0):
            Puboid= "E0E0"
    
    
    def OnClickFileName(self, evt):
        frame = wx.Frame(None, -1, '*.*')
        frame.SetSize(0,0,200,50)
            
        openFileDialog = wx.FileDialog(frame, "Open", "", "","All|*.bin;*.crt;*.der|Binary|*.bin|Certificate|*.crt;*.der", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
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


        clearimage = wx.Image('../images/clear.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        clearbutton = wx.BitmapButton(self, -1, clearimage)

        
        backimage = wx.Image('../images/back.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
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



class Tab6Frame(wx.Frame):
    
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

        # Add tabs
        self.tab_base.AddPage(self.tab1_gen, 'General')
        self.tab_base.AddPage(self.tab2_key, 'Private Key and Cert OID')
        
        self.tab_base.AddPage(self.tab3_app, 'Application Data OID')
        

        self.Show(True)
              
    
    def OnCloseWindow(self, evt):
        self.Parent.Show()
        self.Destroy()
