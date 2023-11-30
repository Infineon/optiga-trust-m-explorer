import wx
import shell_util as exec_cmd
import misc_dialogs as misc
import images as img
import config
from binascii import unhexlify
import os
import subprocess


class Tab_ECC(wx.Panel):
    
    def __init__(self, parent):
        
        wx.Panel.__init__(self, parent)
        
        textctrlfont = wx.Font()
        textctrlfont.SetPointSize(11)
        
        keyslot_list = ['E0F0', 'E0F1','E0F2','E0F3']
        ecctype_list = ['ECC256', 'ECC384','ECC521','BP256','BP384','BP512']
        keyusage1 = ['Auth/Sign','Sign','Sign/Key Agree']
        
        buttonfont = wx.Font(14, wx.ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        
        # declare the sizers
        mainsizer = wx.BoxSizer(wx.VERTICAL)
        input_sizer = wx.BoxSizer(wx.HORIZONTAL)
        mainhorisizer = wx.BoxSizer(wx.HORIZONTAL)
        
        midsizer = wx.BoxSizer(wx.VERTICAL)
        gdsizer1 = wx.GridSizer(rows=1, cols=2, vgap=10, hgap=10)
        gdsizer2 = wx.GridSizer(rows=1, cols=2, vgap=10, hgap=10)
        gdsizer3 = wx.GridSizer(rows=3, cols=1, vgap=30, hgap=10)

        backbuttonsizer = wx.BoxSizer(wx.HORIZONTAL)
        
        # declare sizers that will be in the grid1
        ecctypesizer = wx.BoxSizer(wx.VERTICAL)
        keyslotsizer = wx.BoxSizer(wx.VERTICAL)
        pubkeysizer = wx.BoxSizer(wx.VERTICAL)
        keyusage = wx.BoxSizer(wx.VERTICAL)
        
        
        
        # instantiate the objects
        text_ecctype = wx.StaticText(self, 0, "ECC Type:")
        self.ecctype = wx.ComboBox(self, 1, choices=ecctype_list, style=wx.CB_READONLY,  size = wx.Size(170, 30))
        self.ecctype.SetFont(textctrlfont)
        
        text_keyusage = wx.StaticText(self, 0, "Key_usage:")
        self.keyusage = wx.ComboBox(self, 1, choices=keyusage1, style=wx.CB_READONLY,  size = wx.Size(170, 30))
        self.keyusage.SetFont(textctrlfont)
        
        text_keyslot = wx.StaticText(self, 0, "Key Slot:")
        self.keyslot = wx.ComboBox(self, 1, choices=keyslot_list, style=wx.CB_READONLY,  size = wx.Size(170, 30))
        self.keyslot.SetFont(textctrlfont)
        
        text_pub_key = wx.StaticText(self, 0, "Pubkey OID:")
        self.pub_key = wx.TextCtrl(self, 1 , size = wx.Size(170, 30) ,style=wx.TE_READONLY)
        self.pub_key.SetFont(textctrlfont)
        
        inputtext = wx.StaticText(self, -1, label="Data Input:")
        self.input_display = wx.TextCtrl(self,value="Hello World")
        
        self.button_genkey = wx.Button(self, 1, 'Generate Key', size = wx.Size(300, 50))
        self.button_genkey.SetFont(buttonfont)
        button_eccsign = wx.Button(self, 1, 'ECC Sign', size = wx.Size(300, 50))
        button_eccsign.SetFont(buttonfont)
        button_eccverify = wx.Button(self, 1, 'ECC Verify', size = wx.Size(300, 50))
        button_eccverify.SetFont(buttonfont)
        

        
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
        
        mainsizer.Add(mainhorisizer, 1, wx.EXPAND)
       
        # Add Sub Sizers to the mainhorisizer
        mainhorisizer.Add(midsizer, 1, wx.EXPAND)
        mainhorisizer.Add(self.text_display, 2, wx.EXPAND | wx.ALL, 5)
             
        backbuttonsizer.Add(backbutton, 0, wx.ALIGN_LEFT | wx.ALIGN_BOTTOM, 0)
        backbuttonsizer.AddSpacer(10)
        backbuttonsizer.Add(clearbutton, 0, wx.ALIGN_LEFT | wx.ALIGN_BOTTOM, 0)

        # Add sizers to midsizer
        midsizer.AddSpacer(30)
        midsizer.Add(gdsizer1, 0, wx.EXPAND | wx.ALL, 10)
        midsizer.AddSpacer(30)
        midsizer.Add(gdsizer2, 0, wx.EXPAND | wx.ALL, 10)
        midsizer.AddSpacer(30)
        midsizer.Add(gdsizer3, 0, wx.ALIGN_CENTRE | wx.ALL, 10)
        
        midsizer.AddSpacer(65)
        midsizer.Add(backbuttonsizer,1,wx.LEFT | wx.BOTTOM, 5)
        
        #add buttons into gdsizer3
        gdsizer3.AddMany([
           # (self.button_step1),
           (self.button_genkey),
           (button_eccsign),
           (button_eccverify),

       ])
        
        gdsizer2.AddMany([
                (keyslotsizer, 0, wx.EXPAND),
                (pubkeysizer, 0, wx.EXPAND),

        ])
         
       
        #add sizers to gdsizer1
        gdsizer1.AddMany([
                (ecctypesizer, 0, wx.EXPAND),
                (keyusage, 0, wx.EXPAND),
        ])
        
        
        #add objects into sizers in gdsizer1
        ecctypesizer.Add(text_ecctype)
        ecctypesizer.Add(self.ecctype)
        
        
        #add objects into sizers in gdsizer2
        keyslotsizer.Add(text_keyslot)
        keyslotsizer.Add(self.keyslot)
        
        pubkeysizer.Add(text_pub_key)
        pubkeysizer.Add(self.pub_key)

        keyusage.Add(text_keyusage)
        keyusage.Add(self.keyusage)
        
        # Set Default inputs for Text Boxes      
        self.ecctype.SetSelection(0)
        self.keyslot.SetSelection(0)
        self.keyusage.SetSelection(0)

        # attach objects to the sizer
        # declare and bind events
        
        #bind events
        
        self.button_genkey.Bind(wx.EVT_BUTTON, self.OnGenKey)
        button_eccsign.Bind(wx.EVT_BUTTON, self.OnECCsign)
        button_eccverify.Bind(wx.EVT_BUTTON, self.OnECCverify)
        self.ecctype.Bind(wx.EVT_COMBOBOX, self.OnType)
        self.keyslot.Bind(wx.EVT_COMBOBOX, self.OnSlot)
        clearbutton.Bind(wx.EVT_BUTTON, self.OnFlush)
        backbutton.Bind(wx.EVT_BUTTON, self.OnBack)
        
        
        # Set tooltips
        self.button_genkey.SetToolTip(wx.ToolTip("Generate OPTIGA™ Trust M ECC key pair"))
        button_eccsign.SetToolTip(wx.ToolTip("Sign the message using OPTIGA™ Trust M ECC Key"))
        button_eccverify.SetToolTip(wx.ToolTip("Verify the signature using OPTIGA™ Trust M library"))
        self.ecctype.SetToolTip(wx.ToolTip("ECC Type Options List"))
        self.keyslot.SetToolTip(wx.ToolTip("Private Key Slot Options List"))
        clearbutton.SetToolTip(wx.ToolTip("Clear all textboxes."))
        backbutton.SetToolTip(wx.ToolTip("Go back to main page."))

        self.SetSizer(mainsizer)
        mainsizer.Fit(self)
    
        
        if (self.keyslot.GetSelection() == 0):
            self.ecctype.SetSelection(0)
            self.ecctype.Disable()
            self.button_genkey.Disable()
            
             
        else :
             self.ecctype.SetSelection(0)
             self.ecctype.Enable()
             self.button_genkey.Enable()
    
    #def Disable_Button(self):
        #button_genkey.Disable()
        
    def OnType(self, evt):
        
        if (self.ecctype.GetSelection() == 2 or self.ecctype.GetSelection() == 5):

            self.keyslot.Clear()
            self.pub_key.Clear()
            self.pub_key.AppendText("F1E0")
            keyslot_list = ['E0F0','E0F1','E0F2']
            self.keyslot.AppendItems(keyslot_list)		
            self.keyslot.SetSelection(1)

            if (self.keyslot.GetSelection() == 1):
            
                self.pub_key.Clear()
                self.pub_key.AppendText("F1E0")
                
            if (self.keyslot.GetSelection() == 2):
            
                self.pub_key.Clear()
                self.pub_key.AppendText("F1E1")
            
        else:
            self.keyslot.Clear()
            self.pub_key.Enable()
            self.pub_key.Clear()
            self.pub_key.AppendText("F1D1")            
            keyslot_list = ['E0F0', 'E0F1','E0F2','E0F3']
            self.keyslot.AppendItems(keyslot_list)
            self.keyslot.SetSelection(1)            
            
            if (self.keyslot.GetSelection() == 1):
            
                self.pub_key.Clear()
                self.pub_key.AppendText("F1D1")
        
            elif (self.keyslot.GetSelection() == 2):
            
                self.pub_key.Clear()
                self.pub_key.AppendText("F1D2")
        
            elif (self.keyslot.GetSelection() == 3):
            
                self.pub_key.Clear()
                self.pub_key.AppendText("F1D3")
    
    
    def OnSlot(self, evt):
        
        if (self.keyslot.GetSelection() == 0):
            
            self.pub_key.Clear()
            self.ecctype.SetSelection(0)
            self.ecctype.Disable()
            self.button_genkey.Disable()
        
        
        else :
            
            self.ecctype.Enable()
            self.button_genkey.Enable()
    
    
        if (self.ecctype.GetSelection() == 2 or self.ecctype.GetSelection() == 5):
            

            if (self.keyslot.GetSelection() == 1):
            
                self.pub_key.Clear()
                self.pub_key.AppendText("F1E0")
                
            if (self.keyslot.GetSelection() == 2):
            
                self.pub_key.Clear()
                self.pub_key.AppendText("F1E1")
                                
        else:

            if (self.keyslot.GetSelection() == 1):
            
                self.pub_key.Clear()
                self.pub_key.AppendText("F1D1")
        
            elif (self.keyslot.GetSelection() == 2):
            
                self.pub_key.Clear()
                self.pub_key.AppendText("F1D2")
        
            elif (self.keyslot.GetSelection() == 3):
            
                self.pub_key.Clear()
                self.pub_key.AppendText("F1D3")            
    
    def OnGenKey(self, evt):
        
        #key_usage = self.OnKeyUsage()
       # print(key_usage)
        
        if (self.keyusage.GetSelection() == 0):
            key_usage = "0x11"
            
              
        
        elif (self.keyusage.GetSelection() == 1):
            key_usage = "0x10"
        
            
        
        elif (self.keyusage.GetSelection() == 2):
            key_usage = "0x30"
        
        
        print(key_usage)
        
        # for ecctype 256yes ma'am -
        if (self.ecctype.GetSelection() == 0):
            
                
            if (self.keyslot.GetSelection() == 1):
                 output_message = exec_cmd.execCLI([
                 config.EXEPATH + "/bin/trustm_ecc_keygen",
                 "-g", "0xe0f1",
                 "-t", key_usage,
                 "-k", "0x03",
                 "-o", "test_e0f1_pub.pem",
                 "-s", 
                 
                 ])
                 
                 #self.pub_key.AppendText("F1D1")
                 
                 command_output = exec_cmd.execCLI([
                 "cat", "test_e0f1_pub.pem"
                 ])
                 
                 test_output = exec_cmd.execCLI([
                 config.EXEPATH + "/bin/trustm_data",
                 "-r", "0xf1d1",
                 ])
                 
                 meta_output = exec_cmd.execCLI([
                 config.EXEPATH + "/bin/trustm_metadata",
                 "-r", "0xe0f1"
                 ])
                     
                
            elif (self.keyslot.GetSelection() == 2):
                 output_message = exec_cmd.execCLI([
                 config.EXEPATH + "/bin/trustm_ecc_keygen",
                 "-g", "0xe0f2",
                 "-t", key_usage,
                 "-k", "0x03",
                 "-o", "test_e0f2_pub.pem",
                 "-s",      
              ])
                 
                 command_output = exec_cmd.execCLI([
                 "cat", "test_e0f2_pub.pem"
                 ])
                 
                 test_output = exec_cmd.execCLI([
                 config.EXEPATH + "/bin/trustm_data",
                 "-r", "0xf1d2",
                 ])
                 
                 meta_output = exec_cmd.execCLI([
                 config.EXEPATH + "/bin/trustm_metadata",
                 "-r", "0xe0f2"
                 ])
             
            elif (self.keyslot.GetSelection() == 3):
                output_message = exec_cmd.execCLI([
                 config.EXEPATH + "/bin/trustm_ecc_keygen",
                 "-g", "0xe0f3",
                 "-t", key_usage,
                 "-k", "0x03",
                 "-o", "test_e0f3_pub.pem",
                 "-s", 
              ])
                command_output = exec_cmd.execCLI([
                 "cat", "test_e0f3_pub.pem"
                 ])
                
                test_output = exec_cmd.execCLI([
                 config.EXEPATH + "/bin/trustm_data",
                 "-r", "0xf1d3",
                 ])
                
                meta_output = exec_cmd.execCLI([
                 config.EXEPATH + "/bin/trustm_metadata",
                 "-r", "0xe0f3"
                 ])
           
           #if eofo diable key gen
           
            self.text_display.AppendText(output_message)
            #to test
            self.text_display.AppendText(command_output)
            self.text_display.AppendText(test_output)
            self.text_display.AppendText(meta_output)
            
         # for ecctype384
        elif (self.ecctype.GetSelection() == 1):
            
            if (self.keyslot.GetSelection() == 1):
                 output_message = exec_cmd.execCLI([
                 config.EXEPATH + "/bin/trustm_ecc_keygen",
                 "-g", "0xe0f1",
                 "-t", key_usage,
                 "-k", "0x04",
                 "-o", "test_e0f1_pub_384.pem",
                 "-s", 
               ])
                 command_output = exec_cmd.execCLI([
                 "cat", "test_e0f1_pub_384.pem",
                 ])
                 
                 test_output = exec_cmd.execCLI([
                 config.EXEPATH + "/bin/trustm_data",
                 "-r", "0xf1d1",
                 ])
                 
                 meta_output = exec_cmd.execCLI([
                 config.EXEPATH + "/bin/trustm_metadata",
                 "-r", "0xe0f1"
                 ])
                 
            elif (self.keyslot.GetSelection() == 2):
                 output_message = exec_cmd.execCLI([
                 config.EXEPATH + "/bin/trustm_ecc_keygen",
                 "-g", "0xe0f2",
                 "-t", key_usage,
                 "-k", "0x04",
                 "-o", "test_e0f2_pub_384.pem",
                 "-s",     
              ])
                 command_output = exec_cmd.execCLI([
                 "cat", "test_e0f2_pub_384.pem",
                 ])
                 
                 test_output = exec_cmd.execCLI([
                 config.EXEPATH + "/bin/trustm_data",
                 "-r", "0xf1d2",
                 ])
                 
                 meta_output = exec_cmd.execCLI([
                 config.EXEPATH + "/bin/trustm_metadata",
                 "-r", "0xe0f2"
                 ])
             
            elif (self.keyslot.GetSelection() == 3):
                 output_message = exec_cmd.execCLI([
                 config.EXEPATH + "/bin/trustm_ecc_keygen",
                 "-g", "0xe0f3",
                 "-t", key_usage,
                 "-k", "0x04",
                 "-o", "test_e0f3_pub_384.pem",
                 "-s", 
              ])
                 command_output = exec_cmd.execCLI([
                 "cat", "test_e0f3_pub_384.pem",
                 ])
                     
                 test_output = exec_cmd.execCLI([
                 config.EXEPATH + "/bin/trustm_data",
                 "-r", "0xf1d3",
                 ])
                 
                 meta_output = exec_cmd.execCLI([
                 config.EXEPATH + "/bin/trustm_metadata",
                 "-r", "0xe0f3"
                 ])
         
            self.text_display.AppendText(output_message)
            #to test
            self.text_display.AppendText(command_output)
            self.text_display.AppendText(test_output)
            self.text_display.AppendText(meta_output)
            
        elif (self.ecctype.GetSelection() == 2):
            
            if (self.keyslot.GetSelection() == 1):
                 output_message = exec_cmd.execCLI([
                 config.EXEPATH + "/bin/trustm_ecc_keygen",
                 "-g", "0xe0f1",
                 "-t", key_usage,
                 "-k", "0x05",
                 "-o", "test_e0f1_pub_521.pem",
                 "-s", 
               ])
                 command_output = exec_cmd.execCLI([
                 "cat", "test_e0f1_pub_521.pem",
                 ])
                 
                 test_output = exec_cmd.execCLI([
                 config.EXEPATH + "/bin/trustm_data",
                 "-r", "0xf1e0",
                 ])
                 
                 meta_output = exec_cmd.execCLI([
                 config.EXEPATH + "/bin/trustm_metadata",
                 "-r", "0xe0f1"
                 ])
                 
            elif (self.keyslot.GetSelection() == 2):
                 output_message = exec_cmd.execCLI([
                 config.EXEPATH + "/bin/trustm_ecc_keygen",
                 "-g", "0xe0f2",
                 "-t", key_usage,
                 "-k", "0x05",
                 "-o", "test_e0f2_pub_521.pem",
                 "-s",     
              ])
                 command_output = exec_cmd.execCLI([
                 "cat", "test_e0f2_pub_521.pem",
                 ])
                 
                 test_output = exec_cmd.execCLI([
                 config.EXEPATH + "/bin/trustm_data",
                 "-r", "0xf1e1",
                 ])                 
                 
                 meta_output = exec_cmd.execCLI([
                 config.EXEPATH + "/bin/trustm_metadata",
                 "-r", "0xe0f2"
                 ])

#            elif (self.keyslot.GetSelection() == 3):
#            
#                 output_message = exec_cmd.execCLI([
#                 config.EXEPATH + "/bin/trustm_ecc_keygen",
#                 "-g", "0xe0f3",
#                 "-t", key_usage,
#                 "-k", "0x05",
#                 "-o", "test_e0f3_pub_521.pem",
#              ])
#                 command_output =  exec_cmd.execCLI([
#                      "cat", "test_e0f3_pub_521.pem",
#                  ])
               
#                 meta_output = exec_cmd.execCLI([
#                  config.EXEPATH + "/bin/trustm_metadata",
#                 "-r", "0xe0f3"
#                 ])

            self.text_display.AppendText(output_message)
            #to test
            self.text_display.AppendText(command_output)
            self.text_display.AppendText(test_output)            
            self.text_display.AppendText(meta_output)
            
        elif (self.ecctype.GetSelection() == 3):
            
            if (self.keyslot.GetSelection() == 1):
                 output_message = exec_cmd.execCLI([
                 config.EXEPATH + "/bin/trustm_ecc_keygen",
                 "-g", "0xe0f1",
                 "-t", key_usage,
                 "-k", "0x13",
                 "-o", "test_e0f1_pub_BP256.pem",
                 "-s", 
               ])
                 command_output = exec_cmd.execCLI([
                 "cat", "test_e0f1_pub_BP256.pem",
                 ])
                 
                 test_output = exec_cmd.execCLI([
                 config.EXEPATH + "/bin/trustm_data",
                 "-r", "0xf1d1",
                 ])
                 
                 meta_output = exec_cmd.execCLI([
                 config.EXEPATH + "/bin/trustm_metadata",
                 "-r", "0xe0f1"
                 ])
                 
            elif (self.keyslot.GetSelection() == 2):
                 output_message = exec_cmd.execCLI([
                 config.EXEPATH + "/bin/trustm_ecc_keygen",
                 "-g", "0xe0f2",
                 "-t", key_usage,
                 "-k", "0x13",
                 "-o", "test_e0f2_pub_BP256.pem",
                 "-s",      
              ])
                 command_output = exec_cmd.execCLI([
                 "cat", "test_e0f2_pub_BP256.pem",
                 ])
                 
                 test_output = exec_cmd.execCLI([
                 config.EXEPATH + "/bin/trustm_data",
                 "-r", "0xf1d2",
                 ])
                 
                 meta_output = exec_cmd.execCLI([
                 config.EXEPATH + "/bin/trustm_metadata",
                 "-r", "0xe0f2"
                 ])
             
            elif (self.keyslot.GetSelection() == 3):
                 output_message = exec_cmd.execCLI([
                 config.EXEPATH + "/bin/trustm_ecc_keygen",
                 "-g", "0xe0f3",
                 "-t", key_usage,
                 "-k", "0x13",
                 "-o", "test_e0f3_pub_BP256.pem",
                 "-s", 
              ])
                 command_output = exec_cmd.execCLI([
                 "cat", "test_e0f3_pub_BP256.pem",
                 ])
                     
                 test_output = exec_cmd.execCLI([
                 config.EXEPATH + "/bin/trustm_data",
                 "-r", "0xf1d3",
                 ])
                 
                 meta_output = exec_cmd.execCLI([
                 config.EXEPATH + "/bin/trustm_metadata",
                 "-r", "0xe0f3"
                 ])
         
            self.text_display.AppendText(output_message)
            #to test
            self.text_display.AppendText(command_output)
            self.text_display.AppendText(test_output)
            self.text_display.AppendText(meta_output)
        
        elif (self.ecctype.GetSelection() == 4):
            
            if (self.keyslot.GetSelection() == 1):
                 output_message = exec_cmd.execCLI([
                 config.EXEPATH + "/bin/trustm_ecc_keygen",
                 "-g", "0xe0f1",
                 "-t", key_usage,
                 "-k", "0x15",
                 "-o", "test_e0f1_pub_BP384.pem",
                 "-s", 
               ])
                 command_output = exec_cmd.execCLI([
                 "cat", "test_e0f1_pub_BP384.pem",
                 ])
                 
                 test_output = exec_cmd.execCLI([
                 config.EXEPATH + "/bin/trustm_data",
                 "-r", "0xf1d1",
                 ])
                 
                 meta_output = exec_cmd.execCLI([
                 config.EXEPATH + "/bin/trustm_metadata",
                 "-r", "0xe0f1"
                 ])
                  
            elif (self.keyslot.GetSelection() == 2):
                 output_message = exec_cmd.execCLI([
                 config.EXEPATH + "/bin/trustm_ecc_keygen",
                 "-g", "0xe0f2",
                 "-t", key_usage,
                 "-k", "0x15",
                 "-o", "test_e0f2_pub_BP384.pem",
                 "-s",     
              ])
                 command_output = exec_cmd.execCLI([
                 "cat", "test_e0f2_pub_BP384.pem",
                 ])
                 
                 test_output = exec_cmd.execCLI([
                 config.EXEPATH + "/bin/trustm_data",
                 "-r", "0xf1d2",
                 ])
                 
                 meta_output = exec_cmd.execCLI([
                 config.EXEPATH + "/bin/trustm_metadata",
                 "-r", "0xe0f2"
                 ])
             
            elif (self.keyslot.GetSelection() == 3):
                 output_message = exec_cmd.execCLI([
                 config.EXEPATH + "/bin/trustm_ecc_keygen",
                 "-g", "0xe0f3",
                 "-t", key_usage,
                 "-k", "0x15",
                 "-o", "test_e0f3_pub_BP384.pem",
                 "-s", 
              ])
                 command_output = exec_cmd.execCLI([
                 "cat", "test_e0f3_pub_BP384.pem",
                 ])
                     
                 test_output = exec_cmd.execCLI([
                 config.EXEPATH + "/bin/trustm_data",
                 "-r", "0xf1d3",
                 ])
                 
                 meta_output = exec_cmd.execCLI([
                 config.EXEPATH + "/bin/trustm_metadata",
                 "-r", "0xe0f3"
                 ])
         
            self.text_display.AppendText(output_message)
            #to test
            self.text_display.AppendText(command_output)
            self.text_display.AppendText(test_output)
            self.text_display.AppendText(meta_output)
        
        elif (self.ecctype.GetSelection() == 5):
            
            if (self.keyslot.GetSelection() == 1):
                 output_message = exec_cmd.execCLI([
                 config.EXEPATH + "/bin/trustm_ecc_keygen",
                 "-g", "0xe0f1",
                 "-t", key_usage,
                 "-k", "0x16",
                 "-o", "test_e0f1_pub_BP512.pem",
                 "-s",
               ])
                 command_output = exec_cmd.execCLI([
                 "cat", "test_e0f1_pub_BP512.pem",
                 ])
                 
                 test_output = exec_cmd.execCLI([
                 config.EXEPATH + "/bin/trustm_data",
                 "-r", "0xf1e0",
                 ])                 
                 
                 meta_output = exec_cmd.execCLI([
                 config.EXEPATH + "/bin/trustm_metadata",
                 "-r", "0xe0f1"
                 ])
                 
            elif (self.keyslot.GetSelection() == 2):
                 output_message = exec_cmd.execCLI([
                 config.EXEPATH + "/bin/trustm_ecc_keygen",
                 "-g", "0xe0f2",
                 "-t", key_usage,
                 "-k", "0x16",
                 "-o", "test_e0f2_pub_BP512.pem",
                 "-s",     
              ])
                 command_output = exec_cmd.execCLI([
                 "cat", "test_e0f2_pub_BP512.pem",
                 ])
                 
                 test_output = exec_cmd.execCLI([
                 config.EXEPATH + "/bin/trustm_data",
                 "-r", "0xf1e1",
                 ])                 
                 
                 meta_output = exec_cmd.execCLI([
                 config.EXEPATH + "/bin/trustm_metadata",
                 "-r", "0xe0f2"
                 ])
            
#            elif (self.keyslot.GetSelection() == 3):
                
#                output_message = exec_cmd.execCLI([
#                 config.EXEPATH + "/bin/trustm_ecc_keygen",
#                 "-g", "0xe0f3",
#                 "-t", key_usage,
#                 "-k", "0x16",
#                 "-o", "test_e0f3_pub_BP512.pem",     
#              ])
#                command_output = exec_cmd.execCLI([
#                 "cat", "test_e0f3_pub_BP512.pem",
#                 ])
                 
#                meta_output = exec_cmd.execCLI([
#                 config.EXEPATH + "/bin/trustm_metadata",
#                 "-r", "0xe0f3"
#                 ])
                 
            self.text_display.AppendText(output_message)
            #to test
            self.text_display.AppendText(command_output)
            self.text_display.AppendText(test_output)            
            self.text_display.AppendText(meta_output)     
            
    def OnECCsign(self, evt):
        
        exec_cmd.execCLI(["rm", "data_input.txt", ])
        input_message = self.input_display.GetValue()
        exec_cmd.createProcess("echo " + input_message + " > data_input.txt", None)
        self.text_display.AppendText("'echo " + input_message + " > data_input.txt' executed \n")
        
        if (self.ecctype.GetSelection() == 0):
            
            
            if (self.keyslot.GetSelection() == 0):
                
                command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_ecc_sign", "-k", "0xe0f0", "-o", "ecc_signature.bin", "-i", "data_input.txt", "-H", "-X", ])
                self.text_display.AppendText(command_output)
                self.text_display.AppendText("'trustm_ecc_sign -k 0xe0f0 -o ecc_signature.bin -i data_input.txt -H -X' executed \n")
                command_output = exec_cmd.execCLI(["xxd", "ecc_signature.bin", ])
                self.text_display.AppendText(command_output)
                self.text_display.AppendText("'xxd ecc_signature.bin' executed \n")
                self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
  
            elif (self.keyslot.GetSelection() == 1):
                command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_ecc_sign", "-k", "0xe0f1", "-o", "ecc_signature.bin", "-i", "data_input.txt", "-H", "-X", ])
                self.text_display.AppendText(command_output)
                self.text_display.AppendText("'trustm_ecc_sign -k 0xe0f1 -o ecc_signature.bin -i data_input.txt -H -X' executed \n")
                command_output = exec_cmd.execCLI(["xxd", "ecc_signature.bin", ])
                self.text_display.AppendText(command_output)
                self.text_display.AppendText("'xxd ecc_signature.bin' executed \n")
                self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
        
            elif (self.keyslot.GetSelection() == 2):
                command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_ecc_sign", "-k", "0xe0f2", "-o", "ecc_signature.bin", "-i", "data_input.txt", "-H", "-X", ])
                self.text_display.AppendText(command_output)
                self.text_display.AppendText("'trustm_ecc_sign -k 0xe0f2 -o ecc_signature.bin -i data_input.txt -H -X' executed \n")
                command_output = exec_cmd.execCLI(["xxd", "ecc_signature.bin", ])
                self.text_display.AppendText(command_output)
                self.text_display.AppendText("'xxd ecc_signature.bin' executed \n")
                self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
        
            elif (self.keyslot.GetSelection() == 3):
              command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_ecc_sign", "-k", "0xe0f3", "-o", "ecc_signature.bin", "-i", "data_input.txt", "-H", "-X", ])
              self.text_display.AppendText(command_output)
              self.text_display.AppendText("'trustm_ecc_sign -k 0xe0f3 -o ecc_signature.bin -i data_input.txt -H -X' executed \n")
              command_output = exec_cmd.execCLI(["xxd", "ecc_signature.bin", ])
              self.text_display.AppendText(command_output)
              self.text_display.AppendText("'xxd ecc_signature.bin' executed \n")
              self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
        
        # ecc signing for ECC384
        elif (self.ecctype.GetSelection() == 1):
            
            if (self.keyslot.GetSelection() == 1):
                command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_ecc_sign", "-k", "0xe0f1", "-o", "ecc_signature_384.bin", "-i", "data_input.txt", "-H", "-X", ])
                self.text_display.AppendText(command_output)
                self.text_display.AppendText("'trustm_ecc_sign -k 0xe0f1 -o ecc_signature_384.bin -i data_input.txt -H -X' executed \n")
                command_output = exec_cmd.execCLI(["xxd", "ecc_signature_384.bin", ])
                self.text_display.AppendText(command_output)
                self.text_display.AppendText("'xxd ecc_signature_384.bin' executed \n")
                self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
        
            elif (self.keyslot.GetSelection() == 2):
                command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_ecc_sign", "-k", "0xe0f2", "-o", "ecc_signature_384.bin", "-i", "data_input.txt", "-H", "-X", ])
                self.text_display.AppendText(command_output)
                self.text_display.AppendText("'trustm_ecc_sign -k 0xe0f2 -o ecc_signature_384.bin -i data_input.txt -H -X' executed \n")
                command_output = exec_cmd.execCLI(["xxd", "ecc_signature_384.bin", ])
                self.text_display.AppendText(command_output)
                self.text_display.AppendText("'xxd ecc_signature_384.bin' executed \n")
                self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
        
            elif (self.keyslot.GetSelection() == 3):
              command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_ecc_sign", "-k", "0xe0f3", "-o", "ecc_signature_384.bin", "-i", "data_input.txt", "-H", "-X", ])
              self.text_display.AppendText(command_output)
              self.text_display.AppendText("'trustm_ecc_sign -k 0xe0f3 -o ecc_signature_384.bin -i data_input.txt -H -X' executed \n")
              command_output = exec_cmd.execCLI(["xxd", "ecc_signature_384.bin", ])
              self.text_display.AppendText(command_output)
              self.text_display.AppendText("'xxd ecc_signature_384.bin' executed \n")
              self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
        
        elif (self.ecctype.GetSelection() == 2):
            
            if (self.keyslot.GetSelection() == 1):
                command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_ecc_sign", "-k", "0xe0f1", "-o", "ecc_signature_521.bin", "-i", "data_input.txt", "-H", "-X", ])
                self.text_display.AppendText(command_output)
                self.text_display.AppendText("'trustm_ecc_sign -k 0xe0f1 -o ecc_signature_521.bin -i data_input.txt -H -X' executed \n")
                command_output = exec_cmd.execCLI(["xxd", "ecc_signature_521.bin", ])
                self.text_display.AppendText(command_output)
                self.text_display.AppendText("'xxd ecc_signature_521.bin' executed \n")
                self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
        
            elif (self.keyslot.GetSelection() == 2):
                
                command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_ecc_sign", "-k", "0xe0f2", "-o", "ecc_signature_521.bin", "-i", "data_input.txt", "-H", "-X", ])
                self.text_display.AppendText(command_output)
                self.text_display.AppendText("'trustm_ecc_sign -k 0xe0f2 -o ecc_signature_521.bin -i data_input.txt -H -X' executed \n")
                command_output = exec_cmd.execCLI(["xxd", "ecc_signature_521.bin", ])
                self.text_display.AppendText(command_output)
                self.text_display.AppendText("'xxd ecc_signature_521.bin' executed \n")
                self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
        
            elif (self.keyslot.GetSelection() == 3):
                
                command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_ecc_sign", "-k", "0xe0f3", "-o", "ecc_signature_521.bin", "-i", "data_input.txt", "-H", "-X", ])
                self.text_display.AppendText(command_output)
                self.text_display.AppendText("'trustm_ecc_sign -k 0xe0f3 -o ecc_signature_521.bin -i data_input.txt -H -X' executed \n")
                command_output = exec_cmd.execCLI(["xxd", "ecc_signature_521.bin", ])
                self.text_display.AppendText(command_output)
                self.text_display.AppendText("'xxd ecc_signature_521.bin' executed \n")
                self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
            
                
                #self.text_display.AppendText("\n\nECC521 only available with E0F1 and EOF2\n" )
              
            
        elif (self.ecctype.GetSelection() == 3):
            
            if (self.keyslot.GetSelection() == 1):
                command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_ecc_sign", "-k", "0xe0f1", "-o", "ecc_signature_BP256.bin", "-i", "data_input.txt", "-H", "-X", ])
                self.text_display.AppendText(command_output)
                self.text_display.AppendText("'trustm_ecc_sign -k 0xe0f1 -o ecc_signature_BP256.bin -i data_input.txt -H -X' executed \n")
                command_output = exec_cmd.execCLI(["xxd", "ecc_signature_BP256.bin", ])
                self.text_display.AppendText(command_output)
                self.text_display.AppendText("'xxd ecc_signature_BP256.bin' executed \n")
                self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
        
            elif (self.keyslot.GetSelection() == 2):
                command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_ecc_sign", "-k", "0xe0f2", "-o", "ecc_signature_BP256.bin", "-i", "data_input.txt", "-H", "-X", ])
                self.text_display.AppendText(command_output)
                self.text_display.AppendText("'trustm_ecc_sign -k 0xe0f2 -o ecc_signature_BP256.bin -i data_input.txt -H -X' executed \n")
                command_output = exec_cmd.execCLI(["xxd", "ecc_signature_BP256.bin", ])
                self.text_display.AppendText(command_output)
                self.text_display.AppendText("'xxd ecc_signature_BP256.bin' executed \n")
                self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
        
            elif (self.keyslot.GetSelection() == 3):
              command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_ecc_sign", "-k", "0xe0f3", "-o", "ecc_signature_BP256.bin", "-i", "data_input.txt", "-H", "-X", ])
              self.text_display.AppendText(command_output)
              self.text_display.AppendText("'trustm_ecc_sign -k 0xe0f3 -o ecc_signature_BP256.bin -i data_input.txt -H -X' executed \n")
              command_output = exec_cmd.execCLI(["xxd", "ecc_signature_BP256.bin", ])
              self.text_display.AppendText(command_output)
              self.text_display.AppendText("'xxd ecc_signature_BP256.bin' executed \n")
              self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
        
        elif (self.ecctype.GetSelection() == 4):
            
            if (self.keyslot.GetSelection() == 1):
                command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_ecc_sign", "-k", "0xe0f1", "-o", "ecc_signature_BP384.bin", "-i", "data_input.txt", "-H", "-X", ])
                self.text_display.AppendText(command_output)
                self.text_display.AppendText("'trustm_ecc_sign -k 0xe0f1 -o ecc_signature_BP384.bin -i data_input.txt -H -X' executed \n")
                command_output = exec_cmd.execCLI(["xxd", "ecc_signature_BP384.bin", ])
                self.text_display.AppendText(command_output)
                self.text_display.AppendText("'xxd ecc_signature_BP384.bin' executed \n")
                self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
        
            elif (self.keyslot.GetSelection() == 2):
                command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_ecc_sign", "-k", "0xe0f2", "-o", "ecc_signature_BP384.bin", "-i", "data_input.txt", "-H", "-X", ])
                self.text_display.AppendText(command_output)
                self.text_display.AppendText("'trustm_ecc_sign -k 0xe0f2 -o ecc_signature_BP384.bin -i data_input.txt -H -X' executed \n")
                command_output = exec_cmd.execCLI(["xxd", "ecc_signature_BP384.bin", ])
                self.text_display.AppendText(command_output)
                self.text_display.AppendText("'xxd ecc_signature_BP384.bin' executed \n")
                self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
        
            elif (self.keyslot.GetSelection() == 3):
              command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_ecc_sign", "-k", "0xe0f3", "-o", "ecc_signature_BP384.bin", "-i", "data_input.txt", "-H", "-X", ])
              self.text_display.AppendText(command_output)
              self.text_display.AppendText("'trustm_ecc_sign -k 0xe0f3 -o ecc_signature_BP384.bin -i data_input.txt -H -X' executed \n")
              command_output = exec_cmd.execCLI(["xxd", "ecc_signature_BP384.bin", ])
              self.text_display.AppendText(command_output)
              self.text_display.AppendText("'xxd ecc_signature_BP384.bin' executed \n")
              self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
        
        elif (self.ecctype.GetSelection() == 5):
            
            if (self.keyslot.GetSelection() == 1):
                command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_ecc_sign", "-k", "0xe0f1", "-o", "ecc_signature_BP512.bin", "-i", "data_input.txt", "-H", "-X", ])
                self.text_display.AppendText(command_output)
                self.text_display.AppendText("'trustm_ecc_sign -k 0xe0f1 -o ecc_signature_BP512.bin -i data_input.txt -H -X' executed \n")
                command_output = exec_cmd.execCLI(["xxd", "ecc_signature_BP512.bin", ])
                self.text_display.AppendText(command_output)
                self.text_display.AppendText("'xxd ecc_signature_BP512.bin' executed \n")
                self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
        
            elif (self.keyslot.GetSelection() == 2):
                command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_ecc_sign", "-k", "0xe0f2", "-o", "ecc_signature_BP512.bin", "-i", "data_input.txt", "-H", "-X", ])
                self.text_display.AppendText(command_output)
                self.text_display.AppendText("'trustm_ecc_sign -k 0xe0f2 -o ecc_signature_BP512.bin -i data_input.txt -H -X' executed \n")
                command_output = exec_cmd.execCLI(["xxd", "ecc_signature_BP512.bin", ])
                self.text_display.AppendText(command_output)
                self.text_display.AppendText("'xxd ecc_signature_BP512.bin' executed \n")
                self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
            
            elif (self.keyslot.GetSelection() == 3):
                command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_ecc_sign", "-k", "0xe0f3", "-o", "ecc_signature_BP512.bin", "-i", "data_input.txt", "-H", "-X", ])
                self.text_display.AppendText(command_output)
                self.text_display.AppendText("'trustm_ecc_sign -k 0xe0f3 -o ecc_signature_BP512.bin -i data_input.txt -H -X' executed \n")
                command_output = exec_cmd.execCLI(["xxd", "ecc_signature_BP512.bin", ])
                self.text_display.AppendText(command_output)
                self.text_display.AppendText("'xxd ecc_signature_BP512.bin' executed \n")
                self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
                
        
    def OnECCverify(self, evt):
        
        
        exec_cmd.execCLI(["rm", "data_input.txt", ])
        input_message = self.input_display.GetValue()
        exec_cmd.createProcess("echo " + input_message + " > data_input.txt", None)
        self.text_display.AppendText("'echo " + input_message + " > data_input.txt' executed \n")
        
        if (self.ecctype.GetSelection() == 0):
            
            exec_cmd.execCLI(["rm", "data_input.txt", ])
            input_message = self.input_display.GetValue()
            exec_cmd.createProcess("echo " + input_message + " > data_input.txt", None)
            
            if (self.keyslot.GetSelection() == 0):
                
                exec_cmd.execCLI(["rm", "test_e0f0_pub.pem", ])
                #self.text_display.AppendText("Extracting public key from cert... \n")

                command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_cert","-r","0xe0e0", "-o", "cert_0xe0e0.pem", ])
                self.text_display.AppendText("'trustm_cert -r 0xe0e0 -o cert_0xe0e0.pem executed' \n")
                exec_cmd.createProcess("openssl x509 -pubkey -noout -in cert_0xe0e0.pem > test_e0f0_pub.pem", None)
                self.text_display.AppendText("'openssl x509 -pubkey -noout -in cert_0xe0e0.pem > test_e0f0_pub.pem' executed \n")
                
                command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_ecc_verify","-i","data_input.txt", "-s","ecc_signature.bin","-p","test_e0f0_pub.pem","-H", "-X", ])
                self.text_display.AppendText(command_output)
                self.text_display.AppendText("'trustm_ecc_verify -i data_input.txt -s ecc_signature.bin -p test_e0f0_pub.pem -H -X' executed \n")
                self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")        
            
            elif (self.keyslot.GetSelection() == 1):
				
                command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_data", "-r", "0xf1d1", "-o", "test_e0f1_pub.bin", ])
                self.text_display.AppendText(command_output)
                
                openssl_command = "openssl ec -pubin -inform DER -in test_e0f1_pub.bin -outform PEM -out test_e0f1_pub.pem"
                exec_cmd.createProcess(openssl_command, None)
                self.text_display.AppendText("'openssl ec -pubin -inform DER -in test_e0f1_pub.bin -outform PEM -out test_e0f1_pub.pem' executed \n")
                
                command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_ecc_verify","-i","data_input.txt", "-s","ecc_signature.bin","-p","test_e0f1_pub.pem","-H", "-X", ])
                self.text_display.AppendText(command_output)
                self.text_display.AppendText("'trustm_ecc_verify -i data_input.txt -s ecc_signature.bin -p test_e0f1_pub.pem -H -X' executed \n")	
                self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")

        
            elif (self.keyslot.GetSelection() == 2):

                command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_data", "-r", "0xf1d2", "-o", "test_e0f2_pub.bin", ])
                self.text_display.AppendText(command_output)
                
                openssl_command = "openssl ec -pubin -inform DER -in test_e0f2_pub.bin -outform PEM -out test_e0f2_pub.pem"
                exec_cmd.createProcess(openssl_command, None)
                self.text_display.AppendText("'openssl ec -pubin -inform DER -in test_e0f2_pub.bin -outform PEM -out test_e0f2_pub.pem' executed \n")				
				
                command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_ecc_verify","-i","data_input.txt", "-s","ecc_signature.bin","-p","test_e0f2_pub.pem","-H", "-X", ])
                self.text_display.AppendText(command_output)
                self.text_display.AppendText("'trustm_ecc_verify -i data_input.txt -s ecc_signature.bin -p test_e0f2_pub.pem -H -X' executed \n")
                self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
                
            elif (self.keyslot.GetSelection() == 3):
				
                command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_data", "-r", "0xf1d3", "-o", "test_e0f3_pub.bin", ])
                self.text_display.AppendText(command_output)
                
                openssl_command = "openssl ec -pubin -inform DER -in test_e0f3_pub.bin -outform PEM -out test_e0f3_pub.pem"
                exec_cmd.createProcess(openssl_command, None)
                self.text_display.AppendText("'openssl ec -pubin -inform DER -in test_e0f3_pub.bin -outform PEM -out test_e0f3_pub.pem' executed \n")
                
                command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_ecc_verify","-i","data_input.txt", "-s","ecc_signature.bin","-p","test_e0f3_pub.pem","-H", "-X", ])
                self.text_display.AppendText(command_output)
                self.text_display.AppendText("'trustm_ecc_verify -i data_input.txt -s ecc_signature.bin -p test_e0f3_pub.pem -H -X' executed \n")
                self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
                       
            
        elif (self.ecctype.GetSelection() == 1):
            
            if (self.keyslot.GetSelection() == 1):
				
                command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_data", "-r", "0xf1d1", "-o", "test_e0f1_pub_384.bin", ])
                self.text_display.AppendText(command_output)
                
                openssl_command = "openssl ec -pubin -inform DER -in test_e0f1_pub_384.bin -outform PEM -out test_e0f1_pub_384.pem"
                exec_cmd.createProcess(openssl_command, None)
                self.text_display.AppendText("'openssl ec -pubin -inform DER -in test_e0f1_pub_384.bin -outform PEM -out test_e0f1_pub_384.pem' executed \n")				
                
                command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_ecc_verify","-i","data_input.txt", "-s",
                                                   "ecc_signature_384.bin","-p","test_e0f1_pub_384.pem","-H", "-X", ])
                
                self.text_display.AppendText(command_output)
                self.text_display.AppendText("'trustm_ecc_verify -i data_input.txt -s ecc_signature_384.bin -p test_e0f1_pub_384.pem -H -X' executed \n")
                self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
        
            elif (self.keyslot.GetSelection() == 2):
				
                command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_data", "-r", "0xf1d2", "-o", "test_e0f2_pub_384.bin", ])
                self.text_display.AppendText(command_output)
                
                openssl_command = "openssl ec -pubin -inform DER -in test_e0f2_pub_384.bin -outform PEM -out test_e0f2_pub_384.pem"
                exec_cmd.createProcess(openssl_command, None)
                self.text_display.AppendText("'openssl ec -pubin -inform DER -in test_e0f2_pub_384.bin -outform PEM -out test_e0f2_pub_384.pem' executed \n")	
                
                command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_ecc_verify","-i","data_input.txt", "-s","ecc_signature_384.bin","-p","test_e0f2_pub_384.pem","-H", "-X", ])
                self.text_display.AppendText(command_output)
                self.text_display.AppendText("'trustm_ecc_verify -i data_input.txt -s ecc_signature_384.bin -p test_e0f2_pub_384.pem -H -X' executed \n")
                self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
                
            elif (self.keyslot.GetSelection() == 3):
				
                command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_data", "-r", "0xf1d3", "-o", "test_e0f3_pub_384.bin", ])
                self.text_display.AppendText(command_output)
                
                openssl_command = "openssl ec -pubin -inform DER -in test_e0f3_pub_384.bin -outform PEM -out test_e0f3_pub_384.pem"
                exec_cmd.createProcess(openssl_command, None)
                self.text_display.AppendText("'openssl ec -pubin -inform DER -in test_e0f3_pub_384.bin -outform PEM -out test_e0f3_pub_384.pem' executed \n")	
                				
                command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_ecc_verify","-i","data_input.txt", "-s","ecc_signature_384.bin","-p","test_e0f3_pub_384.pem","-H", "-X", ])
                self.text_display.AppendText(command_output)
                self.text_display.AppendText("'trustm_ecc_verify -i data_input.txt -s ecc_signature_384.bin -p test_e0f3_pub_384.pem -H -X' executed \n")
                self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")

            
        
        elif (self.ecctype.GetSelection() == 2):
            
            if (self.keyslot.GetSelection() == 1):
				
                command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_data", "-r", "0xf1e0", "-o", "test_e0f1_pub_521.bin", ])
                self.text_display.AppendText(command_output)
                
                openssl_command = "openssl ec -pubin -inform DER -in test_e0f1_pub_521.bin -outform PEM -out test_e0f1_pub_521.pem"
                exec_cmd.createProcess(openssl_command, None)
                self.text_display.AppendText("'openssl ec -pubin -inform DER -in test_e0f1_pub_521.bin -outform PEM -out test_e0f1_pub_521.pem' executed \n")	
                
                command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_ecc_verify","-i","data_input.txt", "-s",
                                                   "ecc_signature_521.bin","-p","test_e0f1_pub_521.pem","-H", "-X", ])
                
                self.text_display.AppendText(command_output)
                self.text_display.AppendText("'trustm_ecc_verify -i data_input.txt -s ecc_signature_521.bin -p test_e0f1_pub_521.pem -H -X' executed \n")
                self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
        
            elif (self.keyslot.GetSelection() == 2):
				
                command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_data", "-r", "0xf1e1", "-o", "test_e0f2_pub_521.bin", ])
                self.text_display.AppendText(command_output)
                
                openssl_command = "openssl ec -pubin -inform DER -in test_e0f2_pub_521.bin -outform PEM -out test_e0f2_pub_521.pem"
                exec_cmd.createProcess(openssl_command, None)
                self.text_display.AppendText("'openssl ec -pubin -inform DER -in test_e0f2_pub_521.bin -outform PEM -out test_e0f2_pub_521.pem' executed \n")	
                				
                command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_ecc_verify","-i","data_input.txt", "-s",
                                                   "ecc_signature_521.bin","-p","test_e0f2_pub_521.pem", "-H", "-X", ])
                self.text_display.AppendText(command_output)
                self.text_display.AppendText("'trustm_ecc_verify -i data_input.txt -s ecc_signature_521.bin -p test_e0f2_pub_521.pem -H -X' executed \n")
                self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
                
            #elif (self.keyslot.GetSelection() == 3):

                #command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_data", "-r", "0xf1d3", "-o", "test_e0f3_pub_521.bin", ])
                #self.text_display.AppendText(command_output)
                
                #openssl_command = "openssl ec -pubin -inform DER -in test_e0f3_pub_521.bin -outform PEM -out test_e0f3_pub_521.pem"
                #exec_cmd.createProcess(openssl_command, None)
                #self.text_display.AppendText("'openssl ec -pubin -inform DER -in test_e0f3_pub_521.bin -outform PEM -out test_e0f3_pub_521.pem' executed \n")	
                                
                #self.text_display.AppendText("\n\nECC521 only available with E0F1 and E0F2\n")
                #command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_ecc_verify","-i","data_input.txt", "-s","ecc_signature_521.bin","-p","test_e0f3_pub_521.pem","-H", "-X", ])
                #self.text_display.AppendText(command_output)
                #self.text_display.AppendText("'trustm_ecc_verify -i data_input.txt -s ecc_signature_521.bin -p test_e0f3_pub_521.pem -H -X' executed \n")
                #self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
        
        elif (self.ecctype.GetSelection() == 3):
            
            if (self.keyslot.GetSelection() == 1):
				
                command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_data", "-r", "0xf1d1", "-o", "test_e0f1_pub_BP256.bin", ])
                self.text_display.AppendText(command_output)
                
                openssl_command = "openssl ec -pubin -inform DER -in test_e0f1_pub_BP256.bin -outform PEM -out test_e0f1_pub_BP256.pem"
                exec_cmd.createProcess(openssl_command, None)
                self.text_display.AppendText("'openssl ec -pubin -inform DER -in test_e0f1_pub_BP256.bin -outform PEM -out test_e0f1_pub_BP256.pem' executed \n")					
                
                command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_ecc_verify","-i","data_input.txt", "-s", "ecc_signature_BP256.bin","-p","test_e0f1_pub_BP256.pem",
                                                   "-H",])
                
                self.text_display.AppendText(command_output)
                self.text_display.AppendText("'trustm_ecc_verify -i data_input.txt -s ecc_signature_BP256.bin -p test_e0f1_pub_BP256.pem -H -X' executed \n")
                self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
        
            elif (self.keyslot.GetSelection() == 2):
				
                command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_data", "-r", "0xf1d2", "-o", "test_e0f2_pub_BP256.bin", ])
                self.text_display.AppendText(command_output)
                
                openssl_command = "openssl ec -pubin -inform DER -in test_e0f2_pub_BP256.bin -outform PEM -out test_e0f2_pub_BP256.pem"
                exec_cmd.createProcess(openssl_command, None)
                self.text_display.AppendText("'openssl ec -pubin -inform DER -in test_e0f2_pub_BP256.bin -outform PEM -out test_e0f2_pub_BP256.pem' executed \n")	
                
                command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_ecc_verify","-i","data_input.txt", "-s","ecc_signature_BP256.bin","-p","test_e0f2_pub_BP256.pem",
                                                   "-H", "-X", ])
                self.text_display.AppendText(command_output)
                self.text_display.AppendText("'trustm_ecc_verify -i data_input.txt -s ecc_signature_BP256.bin -p test_e0f2_pub_BP256.pem -H -X' executed \n")
                self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
                
            elif (self.keyslot.GetSelection() == 3):
				
                command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_data", "-r", "0xf1d3", "-o", "test_e0f3_pub_BP256.bin", ])
                self.text_display.AppendText(command_output)
                
                openssl_command = "openssl ec -pubin -inform DER -in test_e0f3_pub_BP256.bin -outform PEM -out test_e0f3_pub_BP256.pem"
                exec_cmd.createProcess(openssl_command, None)
                self.text_display.AppendText("'openssl ec -pubin -inform DER -in test_e0f3_pub_BP256.bin -outform PEM -out test_e0f3_pub_BP256.pem' executed \n")					
				
                command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_ecc_verify","-i","data_input.txt", "-s","ecc_signature_BP256.bin","-p","test_e0f3_pub_BP256.pem",
                                                   "-H", "-X", ])
                self.text_display.AppendText(command_output)
                self.text_display.AppendText("'trustm_ecc_verify -i data_input.txt -s ecc_signature_BP256.bin -p test_e0f3_pub_BP256.pem -H -X' executed \n")
                self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
        
        elif (self.ecctype.GetSelection() == 4):
        
            if (self.keyslot.GetSelection() == 1):
				
                command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_data", "-r", "0xf1d1", "-o", "test_e0f1_pub_BP384.bin", ])
                self.text_display.AppendText(command_output)
                
                openssl_command = "openssl ec -pubin -inform DER -in test_e0f1_pub_BP384.bin -outform PEM -out test_e0f1_pub_BP384.pem"
                exec_cmd.createProcess(openssl_command, None)
                self.text_display.AppendText("'openssl ec -pubin -inform DER -in test_e0f1_pub_BP384.bin -outform PEM -out test_e0f1_pub_BP384.pem' executed \n")	
                
                command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_ecc_verify","-i","data_input.txt", "-s", "ecc_signature_BP384.bin","-p","test_e0f1_pub_BP384.pem",
                                                   "-H",])
                
                self.text_display.AppendText(command_output)
                self.text_display.AppendText("'trustm_ecc_verify -i data_input.txt -s ecc_signature_BP384.bin -p test_e0f1_pub_BP384.pem -H -X' executed \n")
                self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
        
            elif (self.keyslot.GetSelection() == 2):
				
                command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_data", "-r", "0xf1d2", "-o", "test_e0f2_pub_BP384.bin", ])
                self.text_display.AppendText(command_output)
                
                openssl_command = "openssl ec -pubin -inform DER -in test_e0f2_pub_BP384.bin -outform PEM -out test_e0f2_pub_BP384.pem"
                exec_cmd.createProcess(openssl_command, None)
                self.text_display.AppendText("'openssl ec -pubin -inform DER -in test_e0f2_pub_BP384.bin -outform PEM -out test_e0f2_pub_BP384.pem' executed \n")					
				
                command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_ecc_verify","-i","data_input.txt", "-s","ecc_signature_BP384.bin","-p","test_e0f2_pub_BP384.pem",
                                                   "-H", "-X", ])
                self.text_display.AppendText(command_output)
                self.text_display.AppendText("'trustm_ecc_verify -i data_input.txt -s ecc_signature_BP384.bin -p test_e0f2_pub_BP384.pem -H -X' executed \n")
                self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
                
            elif (self.keyslot.GetSelection() == 3):
				
                command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_data", "-r", "0xf1d3", "-o", "test_e0f3_pub_BP384.bin", ])
                self.text_display.AppendText(command_output)
                
                openssl_command = "openssl ec -pubin -inform DER -in test_e0f3_pub_BP384.bin -outform PEM -out test_e0f3_pub_BP384.pem"
                exec_cmd.createProcess(openssl_command, None)
                self.text_display.AppendText("'openssl ec -pubin -inform DER -in test_e0f3_pub_BP384.bin -outform PEM -out test_e0f3_pub_BP384.pem' executed \n")					
				
                command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_ecc_verify","-i","data_input.txt", "-s","ecc_signature_BP384.bin","-p","test_e0f3_pub_BP384.pem",
                                                   "-H", "-X", ])
                self.text_display.AppendText(command_output)
                self.text_display.AppendText("'trustm_ecc_verify -i data_input.txt -s ecc_signature_BP384.bin -p test_e0f3_pub_BP384.pem -H -X' executed \n")
                self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
        
        
        elif (self.ecctype.GetSelection() == 5):
            
            if (self.keyslot.GetSelection() == 1):
				
                command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_data", "-r", "0xf1e0", "-o", "test_e0f1_pub_BP512.bin", ])
                self.text_display.AppendText(command_output)
                
                openssl_command = "openssl ec -pubin -inform DER -in test_e0f1_pub_BP512.bin -outform PEM -out test_e0f1_pub_BP512.pem"
                exec_cmd.createProcess(openssl_command, None)
                self.text_display.AppendText("'openssl ec -pubin -inform DER -in test_e0f1_pub_BP512.bin -outform PEM -out test_e0f1_pub_BP512.pem' executed \n")					
                
                command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_ecc_verify","-i","data_input.txt", "-s", "ecc_signature_BP512.bin","-p","test_e0f1_pub_BP512.pem",
                                                   "-H",])
                self.text_display.AppendText(command_output)
                self.text_display.AppendText("'trustm_ecc_verify -i data_input.txt -s ecc_signature_BP512.bin -p test_e0f1_pub_BP512.pem -H -X' executed \n")
                self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
        
            elif (self.keyslot.GetSelection() == 2):
                
                command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_data", "-r", "0xf1e1", "-o", "test_e0f2_pub_BP512.bin", ])
                self.text_display.AppendText(command_output)
                
                openssl_command = "openssl ec -pubin -inform DER -in test_e0f2_pub_BP512.bin -outform PEM -out test_e0f2_pub_BP512.pem"
                exec_cmd.createProcess(openssl_command, None)
                self.text_display.AppendText("'openssl ec -pubin -inform DER -in test_e0f2_pub_BP512.bin -outform PEM -out test_e0f2_pub_BP512.pem' executed \n")		                
                
                command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_ecc_verify","-i","data_input.txt", "-s","ecc_signature_BP512.bin","-p","test_e0f2_pub_BP512.pem",
                                                   "-H", "-X", ])
                self.text_display.AppendText(command_output)
                self.text_display.AppendText("'trustm_ecc_verify -i data_input.txt -s ecc_signature_BP512.bin -p test_e0f2_pub_BP512.pem -H -X' executed \n")
                self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
            
            #elif (self.keyslot.GetSelection() == 3):
				
                #command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_data", "-r", "0xf1d3", "-o", "test_e0f3_pub_BP512.bin", ])
                #self.text_display.AppendText(command_output)
                
                #openssl_command = "openssl ec -pubin -inform DER -in test_e0f3_pub_BP512.bin -outform PEM -out test_e0f3_pub_BP512.pem"
                #exec_cmd.createProcess(openssl_command, None)
                #self.text_display.AppendText("'openssl ec -pubin -inform DER -in test_e0f3_pub_BP512.bin -outform PEM -out test_e0f3_pub_BP512.pem' executed \n")						
				
                #command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_ecc_verify","-i","data_input.txt", "-s","ecc_signature_BP512.bin","-p","test_e0f3_pub_BP512.pem",
                                                   #"-H", ])
                #self.text_display.AppendText(command_output)
                #self.text_display.AppendText("'trustm_ecc_verify -i data_input.txt -s ecc_signature_BP512.bin -p test_e0f3_pub_BP512.pem -H -X' executed \n")
                #self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
                
                #self.text_display.AppendText("\n\n BRAINPOOL512 only available with E0F1 AND E0F2\n")
    
    # to clear the textbox
    def OnFlush(self, evt):
        self.text_display.Clear()

    # Calling parent of the parent, as direct parent is the notebook,
    # then the second parent is the frame, from which we call the destruction
    def OnBack(self, evt):
        self.Parent.Parent.OnCloseWindow(None)
    


class Tab_RSA(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        
        textctrlfont = wx.Font()
        textctrlfont.SetPointSize(11)
        
        keyslot_list = ['E0FC', 'E0FD']
        rsatype_list = ['RSA 1024', 'RSA 2048']
        
        buttonfont = wx.Font(14, wx.ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        
        # declare the sizers
        mainsizer = wx.BoxSizer(wx.VERTICAL)
        input_sizer = wx.BoxSizer(wx.HORIZONTAL)
        mainhorisizer = wx.BoxSizer(wx.HORIZONTAL)
        
        midsizer = wx.BoxSizer(wx.VERTICAL)
        
        gdsizer1 = wx.GridSizer(rows=1, cols=2, vgap=10, hgap=10)
        gdsizer2 = wx.GridSizer(rows=1, cols=2, vgap=10, hgap=10)
        gdsizer3 = wx.GridSizer(rows=5, cols=1, vgap=20, hgap=10)
        
        
        #leftsizer = wx.BoxSizer(wx.VERTICAL)
        #picturesizer = wx.BoxSizer(wx.VERTICAL)
        backbuttonsizer = wx.BoxSizer(wx.HORIZONTAL)
        
        # declare sizers that will be in the grid1
        rsatypesizer = wx.BoxSizer(wx.VERTICAL)
        keyslotsizer = wx.BoxSizer(wx.VERTICAL)
        keyusagesizer = wx.BoxSizer(wx.VERTICAL)
        pubkeysizer = wx.BoxSizer(wx.VERTICAL)
        
        keyusage = ['Auth','Enc','Sign','Auth/Enc/Sign','Key Agree']
       
        
        
        
        # instantiate the objects
        text_rsatype = wx.StaticText(self, 0, "RSA Algo:")
        self.rsatype = wx.ComboBox(self, 1, choices=rsatype_list, style=wx.CB_READONLY,  size = wx.Size(170, 30))
        self.rsatype.SetFont(textctrlfont)
        
        text_keyusage = wx.StaticText(self, 0, "Key_usage:")
        self.keyusage = wx.ComboBox(self, 1, choices=keyusage, style=wx.CB_READONLY,  size = wx.Size(170, 30))
        self.keyusage.SetFont(textctrlfont)
        
        text_keyslot = wx.StaticText(self, 0, "Key Slot:")
        self.keyslot = wx.ComboBox(self, 1, choices=keyslot_list, style=wx.CB_READONLY,  size = wx.Size(170, 30))
        self.keyslot.SetFont(textctrlfont)
        
        text_pub_key = wx.StaticText(self, 0, "Pubkey OID:")
        self.pub_key = wx.TextCtrl(self, 1 , size = wx.Size(170, 30) ,style=wx.TE_READONLY)
        self.pub_key.SetFont(textctrlfont)
        
        inputtext = wx.StaticText(self, -1, label="Data Input:")
        inputtext.SetMinSize((100, -1))        
        self.input_display = wx.TextCtrl(self,value="Hello World")
        
        self.button_genkey = wx.Button(self, 1, 'Generate RSA Keypair', size = wx.Size(300, 50))
        self.button_genkey.SetFont(buttonfont)
        button_rsaenc = wx.Button(self, 1, 'RSA Encrypt', size = wx.Size(300, 50))
        button_rsaenc.SetFont(buttonfont)
        button_rsadec = wx.Button(self, 1, 'RSA Decrypt', size = wx.Size(300, 50))
        button_rsadec.SetFont(buttonfont)
        button_rsasign = wx.Button(self, 1, 'RSA Sign', size = wx.Size(300, 50))
        button_rsasign.SetFont(buttonfont)
        button_rsaverify = wx.Button(self, 1, 'RSA Verify', size = wx.Size(300, 50))
        button_rsaverify.SetFont(buttonfont)

        
        self.text_display = wx.TextCtrl(self, -1, style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.text_display.SetFont(wx.Font(11, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))


        clearimage = wx.Image(config.IMAGEPATH + "/images/clear.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        clearbutton = wx.BitmapButton(self, -1, clearimage)
        
        backimage = wx.Image(config.IMAGEPATH + "/images/back.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        backbutton = wx.BitmapButton(self, -1, backimage)
       
        #Add mainhorisizer to mainsizer
        mainsizer.AddSpacer(5)
        mainsizer.Add(input_sizer, 0, wx.EXPAND | wx.TOP, 5)
        
        input_sizer.Add(inputtext, 0, wx.EXPAND | wx.TOP , 10)
        input_sizer.Add(self.input_display, 1 ,wx.EXPAND | wx.TOP , 5)
        
        mainsizer.Add(mainhorisizer, 1, wx.EXPAND)
       
        # Add Sub Sizers to the mainhorisizer
        mainhorisizer.Add(midsizer, 1, wx.EXPAND)
        mainhorisizer.Add(self.text_display, 2, wx.EXPAND | wx.ALL, 5)
              
        backbuttonsizer.Add(backbutton, 0, wx.ALIGN_LEFT | wx.ALIGN_BOTTOM, 0)
        backbuttonsizer.AddSpacer(10)
        backbuttonsizer.Add(clearbutton, 0, wx.ALIGN_LEFT | wx.ALIGN_BOTTOM, 0)
        
        # Add sizers to midsizer
        midsizer.AddSpacer(10)
        midsizer.AddSpacer(10)
        
        midsizer.Add(gdsizer1, 0, wx.EXPAND | wx.ALL, 10)
        midsizer.Add(gdsizer2, 0, wx.EXPAND | wx.ALL, 10)
        
        
        midsizer.AddSpacer(10)
        midsizer.Add(gdsizer3, 0, wx.ALIGN_CENTRE | wx.ALL, 10)
        
        midsizer.AddSpacer(10)
        midsizer.Add(backbuttonsizer,1,wx.LEFT | wx.BOTTOM, 5)
        
        
        #add buttons into gdsizer3
        gdsizer3.AddMany([
           
           (self.button_genkey),
           (button_rsaenc),
           (button_rsadec),
           (button_rsasign),
           (button_rsaverify),

       ])
        
        gdsizer1.AddMany([
                
                (rsatypesizer, 0, wx.EXPAND),
                (keyusagesizer, 0, wx.EXPAND),
        ])
                         
        gdsizer2.Add(keyslotsizer, 0, wx.EXPAND)
        gdsizer2.Add(pubkeysizer, 0, wx.EXPAND)
        
        
        #add objects into sizers in gdsizer2
        keyslotsizer.Add(text_keyslot, 1, wx.EXPAND)
        keyslotsizer.Add(self.keyslot)
        
        rsatypesizer.Add(text_rsatype, 1, wx.EXPAND)
        rsatypesizer.Add(self.rsatype)
        
        keyusagesizer.Add(text_keyusage, 1, wx.EXPAND)
        keyusagesizer.Add(self.keyusage)
        
        pubkeysizer.Add(text_pub_key, 1, wx.EXPAND)
        pubkeysizer.Add(self.pub_key)

    
        # Set Default inputs for Text Boxes      
        self.rsatype.SetSelection(1)
        self.keyslot.SetSelection(0)
        self.keyusage.SetSelection(3)
     
        #bind events
        self.button_genkey.Bind(wx.EVT_BUTTON, self.OnGenkey)
        self.keyslot.Bind(wx.EVT_COMBOBOX, self.OnKeyslot)
        button_rsaenc.Bind(wx.EVT_BUTTON, self.OnEnc)
        button_rsadec.Bind(wx.EVT_BUTTON, self.OnDec1)
        button_rsasign.Bind(wx.EVT_BUTTON, self.OnSign)
        button_rsaverify.Bind(wx.EVT_BUTTON, self.OnVerify)
        clearbutton.Bind(wx.EVT_BUTTON, self.OnClear)
        backbutton.Bind(wx.EVT_BUTTON, self.OnBack)
        
        
        # Set tooltips
       
        self.button_genkey.SetToolTip(wx.ToolTip("Generate OPTIGA™ Trust M RSA key pair"))
        button_rsaenc.SetToolTip(wx.ToolTip("Encrypt data with RSA public key"))
        button_rsadec.SetToolTip(wx.ToolTip("Decrypt data using the OID Key selected, an encrypted file datain.enc and output to datain.dec"))
        button_rsasign.SetToolTip(wx.ToolTip("Hash and Sign the Message using OPTIGA™ Trust M RSA key"))
        button_rsaverify.SetToolTip(wx.ToolTip("Verify the Signature Using OPTIGA™ Trust M Library"))
        self.rsatype.SetToolTip(wx.ToolTip("RSA Algorithm Options List"))
        self.keyslot.SetToolTip(wx.ToolTip("OID Key Slot Options List"))
        clearbutton.SetToolTip(wx.ToolTip("Clear all textboxes."))
        backbutton.SetToolTip(wx.ToolTip("Go back to main page."))

        self.SetSizer(mainsizer)
        mainsizer.Fit(self)
        
        if (self.keyslot.GetSelection() == 0):
            
            self.pub_key.Clear()
            self.pub_key.AppendText("F1E0")
      
    def OnKeyslot(self, evt):
        
        if (self.keyslot.GetSelection() == 0):
            self.pub_key.Clear()
            self.pub_key.AppendText("F1E0")
        
        elif (self.keyslot.GetSelection() == 1):
            self.pub_key.Clear()
            self.pub_key.AppendText("F1E1")
      
      
    def OnKeyUsage(self):
        
        if (self.keyusage.GetSelection() == 0):
            value = "0x01"
            
            return(value)
        
        elif (self.keyusage.GetSelection() == 1):
            value = "0x02"
         
            return(value)
        
        elif (self.keyusage.GetSelection() == 2):
            value = "0x10"
        
            return(value)
        
        elif (self.keyusage.GetSelection() == 3):
            value = "0x13"
        
            return(value)
        
        elif (self.keyusage.GetSelection() == 4):
            value = "0x20"
        
            return(value)
    
    def OnGenkey(self, evt):
        self.text_display.AppendText("Generating Trust M RSA key pair...")
        wx.CallLater(10, self.OnCreateKeyPair)
    
    # note: this function/command runs for quite a while as compared to ECC.
    def OnCreateKeyPair(self):
        key_usage = self.OnKeyUsage()
        print(key_usage)
        keyslot = "0x" + self.keyslot.GetValue()
        
#         pubkeyoid = "0x" + self.pub_key.GetValue()
        #pubkey = "rsa_" + self.keyslot.GetValue() + "_pub.pem"
        
        if (self.rsatype.GetSelection() == 0):
            pubkey = "rsa_" + self.keyslot.GetValue().lower() + "_pub_1024.pem"
            
        elif (self.rsatype.GetSelection() == 1):
            pubkey = "rsa_" + self.keyslot.GetValue().lower() + "_pub_2048.pem"	        
        
        if (self.rsatype.GetSelection() == 0):
            keysize = "0x41"
        else :
            keysize = "0x42"
        
        exec_cmd.execCLI(["rm", pubkey])
        output_message = exec_cmd.execCLI([
            config.EXEPATH + "/bin/trustm_rsa_keygen",
            "-g", keyslot,
            "-t", key_usage,
            "-k", keysize,
            "-o", pubkey,
            "-s",
        ])
        
        self.text_display.AppendText(output_message)
        self.text_display.AppendText("'trustm_rsa_keygen -g " + keyslot + " -t " + key_usage + " -k " + keysize + " -o " + pubkey + " -s executed\n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
        

    def OnEnc(self, evt):
        #pubkey = "rsa_" + self.keyslot.GetValue() + "_pub.pem"
        
        if (self.rsatype.GetSelection() == 0):
			
            pubkey = "rsa_" + self.keyslot.GetValue().lower() + "_pub_1024.pem"
            
            if(self.keyslot.GetSelection() == 0):
                command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_data", "-r", "0xf1e0", "-o", "rsa_e0fc_pub_1024.bin", ])
                self.text_display.AppendText(command_output)
					
                openssl_command = "openssl rsa -pubin -inform DER -in rsa_e0fc_pub_1024.bin -outform PEM -out rsa_e0fc_pub_1024.pem"
                exec_cmd.createProcess(openssl_command, None)
                self.text_display.AppendText("'openssl rsa -pubin -inform DER -in rsa_e0fc_pub_1024.bin -outform PEM -out rsa_e0fc_pub_1024.pem' executed \n")
                            
            if(self.keyslot.GetSelection()==1):
                command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_data", "-r", "0xf1e1", "-o", "rsa_e0fd_pub_1024.bin", ])
                self.text_display.AppendText(command_output)
					
                openssl_command = "openssl rsa -pubin -inform DER -in rsa_e0fd_pub_1024.bin -outform PEM -out rsa_e0fd_pub_1024.pem"
                exec_cmd.createProcess(openssl_command, None)
                self.text_display.AppendText("'openssl rsa -pubin -inform DER -in rsa_e0fd_pub_1024.bin -outform PEM -out rsa_e0fd_pub_1024.pem' executed \n")        
                
                        
            
        elif (self.rsatype.GetSelection() == 1):
			
            pubkey = "rsa_" + self.keyslot.GetValue().lower() + "_pub_2048.pem"	
            		    
            if(self.keyslot.GetSelection() == 0):
                command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_data", "-r", "0xf1e0", "-o", "rsa_e0fc_pub_2048.bin", ])
                self.text_display.AppendText(command_output)
					
                openssl_command = "openssl rsa -pubin -inform DER -in rsa_e0fc_pub_2048.bin -outform PEM -out rsa_e0fc_pub_2048.pem"
                exec_cmd.createProcess(openssl_command, None)
                self.text_display.AppendText("'openssl rsa -pubin -inform DER -in rsa_e0fc_pub_2048.bin -outform PEM -out rsa_e0fc_pub_2048.pem' executed \n")
                            
            if(self.keyslot.GetSelection()==1):
                command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_data", "-r", "0xf1e1", "-o", "rsa_e0fd_pub_2048.bin", ])
                self.text_display.AppendText(command_output)
					
                openssl_command = "openssl rsa -pubin -inform DER -in rsa_e0fd_pub_2048.bin -outform PEM -out rsa_e0fd_pub_2048.pem"
                exec_cmd.createProcess(openssl_command, None)
                self.text_display.AppendText("'openssl rsa -pubin -inform DER -in rsa_e0fd_pub_2048.bin -outform PEM -out rsa_e0fd_pub_2048.pem' executed \n")  
                
                
        self.text_display.AppendText("\nStoring data in datain.txt...\n")
        
        
        datain = self.input_display.GetValue()
        exec_cmd.createProcess("echo " + datain + " > datain.txt", None)
        self.text_display.AppendText("datain.txt generated\n")
        self.text_display.AppendText("\n++++++++++++++++++++++++++++++++++++++++++++\n")
        self.text_display.AppendText("Encrypting with RSA public key ...\n\n")
        exec_cmd.execCLI(["rm", "datain.enc"])
        output_message = exec_cmd.execCLI([
            config.EXEPATH + "/bin/trustm_rsa_enc",
            "-p", pubkey,
            "-o", "datain.enc",
            "-i", "datain.txt",
             
        ])
       
        self.text_display.AppendText(output_message)
#         self.Update()
        self.text_display.AppendText("'trustm_rsa_enc -p " + pubkey + " -o datain.enc -i datain.txt executed\n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
    
    def OnDec1(self, evt):
        self.text_display.AppendText("\nDecrypting with RSA private key...\n")
        wx.CallLater(10, self.OnDec)
    
    def OnDec(self):
        keyslot = "0x" + self.keyslot.GetValue()
        
        exec_cmd.execCLI(["rm", "datain.dec"])
        output_message = exec_cmd.execCLI([
            config.EXEPATH + "/bin/trustm_rsa_dec",
            "-k", keyslot,
            "-o", "datain.dec",
            "-i", "datain.enc",
             
        ])
        self.text_display.AppendText(output_message)
        self.text_display.AppendText("'trustm_rsa_dec -k " + keyslot + " -o datain.dec -i datain.enc executed\n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
        self.text_display.AppendText("Reading decrypted data...\n")
        output_message = exec_cmd.execCLI(["cat", "datain.dec"])
        self.text_display.AppendText(output_message)
        self.text_display.AppendText("'cat datain.dec' executed\n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
        
        
    def OnSign(self, evt):
        keyslot = "0x" + self.keyslot.GetValue()
        
        if (self.rsatype.GetSelection() == 0):
            outfile = "testsignature_1024.bin"
        elif (self.rsatype.GetSelection() == 1):
            outfile = "testsignature_2048.bin"
        
        self.text_display.AppendText("\nStoring data in datain.txt...\n")
        
        exec_cmd.execCLI(["rm", "datain.txt", ])
        
        datain = self.input_display.GetValue()
        exec_cmd.createProcess("echo " + datain + " > datain.txt", None)
        self.text_display.AppendText("\ndatain.txt generated\n")
        
        output_message = exec_cmd.execCLI([
            config.EXEPATH + "/bin/trustm_rsa_sign",
            "-k", keyslot,
            "-o", outfile,
            "-i", "datain.txt",
            "-H", 
            ])
       
        self.text_display.AppendText(output_message)
        self.text_display.AppendText("'trustm_rsa_dec -k " + keyslot + " -o " + outfile + " -i datain.txt executed\n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
       
        command_output = exec_cmd.execCLI(["xxd", outfile, ])
        self.text_display.AppendText(command_output)
       
        self.text_display.AppendText("'xxd " + outfile + " executed \n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
        
        
        
    def OnVerify(self, evt):
        
        #pubkey = "rsa_" + self.keyslot.GetValue() + "_pub.pem"
        
        if (self.rsatype.GetSelection() == 0):
            outfile = "testsignature_1024.bin"
            pubkey = "rsa_" + self.keyslot.GetValue().lower() + "_pub_1024.pem"
            
            if(self.keyslot.GetSelection()==0):
                command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_data", "-r", "0xf1e0", "-o", "rsa_e0fc_pub_1024.bin", ])
                self.text_display.AppendText(command_output)
					
                openssl_command = "openssl rsa -pubin -inform DER -in test_e0fc_pub_1024.bin -outform PEM -out rsa_e0fc_pub_1024.pem"
                exec_cmd.createProcess(openssl_command, None)
                self.text_display.AppendText("'openssl rsa -pubin -inform DER -in test_e0fc_pub_1024.bin -outform PEM -out rsa_e0fc_pub_1024.pem' executed \n")
                output_message = exec_cmd.execCLI([
					config.EXEPATH + "/bin/trustm_rsa_verify",
					"-i", "datain.txt",
					"-s", outfile,
					"-p", "rsa_e0fc_pub_1024.pem",
					"-H", 
					])
					
                self.text_display.AppendText(output_message)
                self.text_display.AppendText("'trustm_rsa_verify -i datain.txt -s " + outfile + " -p rsa_e0fc_pub_1024.pem -H executed\n")
                self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
                									
            elif(self.keyslot.GetSelection()==1):
                command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_data", "-r", "0xf1e1", "-o", "rsa_e0fd_pub_1024.bin", ])
                self.text_display.AppendText(command_output)
					
                openssl_command = "openssl rsa -pubin -inform DER -in rsa_e0fd_pub_1024.bin -outform PEM -out rsa_e0fd_pub_1024.pem"
                exec_cmd.createProcess(openssl_command, None)
                self.text_display.AppendText("'openssl rsa -pubin -inform DER -in rsa_e0fd_pub_1024.bin -outform PEM -out rsa_e0fd_pub_1024.pem' executed \n")
                output_message = exec_cmd.execCLI([
					config.EXEPATH + "/bin/trustm_rsa_verify",
					"-i", "datain.txt",
					"-s", outfile,
					"-p", "rsa_e0fd_pub_1024.pem",
					"-H", 
					])
					 
                self.text_display.AppendText(output_message)
                self.text_display.AppendText("'trustm_rsa_verify -i datain.txt -s " + outfile + " -p rsa_e0fd_pub_1024.pem -H executed\n")
                self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")	            
            	            
        elif (self.rsatype.GetSelection() == 1):
            outfile = "testsignature_2048.bin"
            pubkey = "rsa_" + self.keyslot.GetValue().lower() + "_pub_1024.pem"            
            if(self.keyslot.GetSelection()==0):
                command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_data", "-r", "0xf1e0", "-o", "rsa_e0fc_pub_2048.bin", ])
                self.text_display.AppendText(command_output)
					
                openssl_command = "openssl rsa -pubin -inform DER -in rsa_e0fc_pub_2048.bin -outform PEM -out rsa_e0fc_pub_2048.pem"
                exec_cmd.createProcess(openssl_command, None)
                self.text_display.AppendText("'openssl rsa -pubin -inform DER -in rsa_e0fc_pub_2048.bin -outform PEM -out rsa_e0fc_pub_2048.pem' executed \n")
                output_message = exec_cmd.execCLI([
					config.EXEPATH + "/bin/trustm_rsa_verify",
					"-i", "datain.txt",
					"-s", outfile,
					"-p", "rsa_e0fc_pub_2048.pem",
					"-H", 
					])
					
                self.text_display.AppendText(output_message)
                self.text_display.AppendText("'trustm_rsa_verify -i datain.txt -s " + outfile + " -p rsa_e0fc_pub_2048.pem -H executed\n")
                self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
                									
            elif(self.keyslot.GetSelection()==1):
                command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_data", "-r", "0xf1e1", "-o", "rsa_e0fd_pub_2048.bin", ])
                self.text_display.AppendText(command_output)
					
                openssl_command = "openssl rsa -pubin -inform DER -in rsa_e0fd_pub_2048.bin -outform PEM -out rsa_e0fd_pub_2048.pem"
                exec_cmd.createProcess(openssl_command, None)
                self.text_display.AppendText("'openssl rsa -pubin -inform DER -in rsa_e0fd_pub_2048.bin -outform PEM -out rsa_e0fd_pub_2048.pem' executed \n")
                output_message = exec_cmd.execCLI([
					config.EXEPATH + "/bin/trustm_rsa_verify",
					"-i", "datain.txt",
					"-s", outfile,
					"-p", "rsa_e0fd_pub_2048.pem",
					"-H", 
					])
					
                self.text_display.AppendText(output_message)
                self.text_display.AppendText("'trustm_rsa_verify -i datain.txt -s " + outfile + " -p rsa_e0fd_pub_2048.pem -H executed\n")
                self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")	                 
            
        
        #output_message = exec_cmd.execCLI([
            #config.EXEPATH + "/bin/trustm_rsa_verify",
            #"-i", "datain.txt",
            #"-s", outfile,
            #"-p", pubkey,
            #"-H", 
            #])
       
        #self.text_display.AppendText(output_message)
        #self.text_display.AppendText("'trustm_rsa_verify -i datain.txt -s " + outfile + " -p " + pubkey + " -H executed\n")
        #self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
        

    def OnClear(self, evt):
        self.text_display.Clear()

    # Calling parent of the parent, as direct parent is the notebook,
    # then the second parent is the frame, from which we call the destruction
    def OnBack(self, evt):
        self.Parent.Parent.OnCloseWindow(None)
        
        
        #to redo later
class Tab_AES(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        
        textctrlfont = wx.Font()
        textctrlfont.SetPointSize(11)
        
        aestype_list = ['AES 128', 'AES 192' , 'AES 256']
        keyusage = ['Auth','Enc','Sign','Auth/Enc/Sign','Key Agree']
        buttonfont = wx.Font(14, wx.ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        
        # declare the sizers
        mainsizer = wx.BoxSizer(wx.VERTICAL)
        input_sizer = wx.BoxSizer(wx.HORIZONTAL)
        mainhorisizer = wx.BoxSizer(wx.HORIZONTAL)
        datafile_sizer = wx.BoxSizer(wx.VERTICAL)
        ivfile_sizer = wx.BoxSizer(wx.VERTICAL)
        datafilecheckbox_sizer = wx.BoxSizer(wx.VERTICAL)
        
        midsizer = wx.BoxSizer(wx.VERTICAL)
        
        gdsizer0 = wx.GridSizer(rows = 1, cols = 1, vgap=5, hgap=5)
        gdsizer1 = wx.GridSizer(rows = 1, cols = 2, vgap=5, hgap=10)
        
        gdsizer2 = wx.GridSizer(rows=1, cols=2, vgap=10, hgap=10)
        gdsizer3 = wx.GridSizer(rows=3, cols=1, vgap=30, hgap=10)
        backbuttonsizer = wx.BoxSizer(wx.HORIZONTAL)
        
        # declare sizers that will be in the grid1
        aestypesizer = wx.BoxSizer(wx.VERTICAL)
        keyusagesizer = wx.BoxSizer(wx.VERTICAL)
        
        # instantiate the objects
        text_aestype = wx.StaticText(self, 0, "AES Key:")
        self.aestype = wx.ComboBox(self, -1, choices=aestype_list, style=wx.CB_READONLY,  size = wx.Size(170, 30))
        self.aestype.SetFont(textctrlfont)
        
        text_keyusage = wx.StaticText(self, 0, "Key_usage:")
        self.keyusage = wx.ComboBox(self, 1, choices=keyusage, style=wx.CB_READONLY,  size = wx.Size(178, -1))
        self.keyusage.SetFont(textctrlfont)
        
        inputtext = wx.StaticText(self, -1, label="Data Input:")
        inputtext.SetMinSize((100, -1))          
        self.input_display = wx.TextCtrl(self,value="Hello World1234")
        
        self.button_genkey = wx.Button(self, 1, 'Generate AES Key', size = wx.Size(300, 50))
        self.button_genkey.SetFont(buttonfont)
        button_aesenc = wx.Button(self, 1, 'AES Encrypt ', size = wx.Size(300, 50))
        button_aesenc.SetFont(buttonfont)
        button_aesdec = wx.Button(self, 1, 'AES Decrypt', size = wx.Size(300, 50))
        button_aesdec.SetFont(buttonfont)
        
        # custom data input
        datafiletext = wx.StaticText(self, -1, label="Data File Input")
        self.datafileinput = wx.TextCtrl(self, value="Custom Data File", size = (190, 30))
        self.datafileinput.Disable()
        
        self.datacheckbox = wx.CheckBox(self, label = "Use Data File Input", style = wx.CHK_2STATE)
        self.datacheckbox.SetValue(False)
        
        # initialization file input
        ivfiletext = wx.StaticText(self, -1, label ="Initialization File Input")
        self.ivfileinput = wx.TextCtrl(self, value="IV File", size = (190, 30))
 
        
        self.command_display = wx.TextCtrl(self, -1, style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.command_display.SetFont(wx.Font(11, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))


        clearimage = wx.Image(config.IMAGEPATH + "/images/clear.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        clearbutton = wx.BitmapButton(self, -1, clearimage)

        backimage = wx.Image(config.IMAGEPATH + "/images/back.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        backbutton = wx.BitmapButton(self, -1, backimage)

        #Add mainhorisizer to mainsizer
        mainsizer.AddSpacer(5)
        mainsizer.Add(input_sizer, 0, wx.EXPAND | wx.TOP, 5)
        
        input_sizer.Add(inputtext, 0, wx.ALIGN_CENTRE | wx.ALL , 2)
        input_sizer.Add(self.input_display, 1 ,wx.ALIGN_CENTRE | wx.ALL, 2)
        
        mainsizer.Add(mainhorisizer, 1, wx.EXPAND)
       
        # Add Sub Sizers to the mainhorisizer
        mainhorisizer.Add(midsizer, 1, wx.EXPAND)
        mainhorisizer.Add(self.command_display, 2, wx.EXPAND | wx.ALL, 5)
      
        backbuttonsizer.Add(backbutton, 0, wx.ALIGN_LEFT | wx.ALIGN_BOTTOM, 0)
        backbuttonsizer.AddSpacer(10)
        backbuttonsizer.Add(clearbutton, 0, wx.ALIGN_LEFT | wx.ALIGN_BOTTOM, 0)

        # Add sizers to midsizer
        midsizer.AddSpacer(10)
        midsizer.Add(gdsizer0, 0, wx.LEFT | wx.ALL, 10)
        
        midsizer.AddSpacer(10)
        midsizer.Add(gdsizer1, 0, wx.ALIGN_CENTRE | wx.ALL, 10)
        
        
        midsizer.AddSpacer(10)
        midsizer.Add(gdsizer2, 0, wx.ALIGN_CENTRE | wx.ALL, 10)
        
        
        midsizer.AddSpacer(30)
        midsizer.Add(gdsizer3, 0, wx.ALIGN_CENTRE | wx.ALL, 10)
        
        midsizer.AddSpacer(55)
        midsizer.Add(backbuttonsizer,1,wx.LEFT | wx.BOTTOM, 5)
        
        
        # add checkbox to gdsizer0
        gdsizer0.AddMany([(datafilecheckbox_sizer, 0, wx.EXPAND)])
        
        # add file selection to gdsizer1
        gdsizer1.AddMany([(datafile_sizer, 0, wx.EXPAND), 
                        (ivfile_sizer, 0, wx.EXPAND),])

        #add buttons into gdsizer3
        gdsizer3.AddMany([
           
           (self.button_genkey),
           (button_aesenc),
           (button_aesdec),

       ])
        
        gdsizer2.AddMany([
                (aestypesizer, 0, wx.EXPAND),
                (keyusagesizer, 0, wx.EXPAND),

        ])
         
        # add objects into data file sizer
        datafile_sizer.Add(datafiletext, 1, wx.EXPAND)
        datafile_sizer.Add(self.datafileinput)
        
        # add object into checkbox sizer
        datafilecheckbox_sizer.Add(self.datacheckbox)
        
        # add object into iv file sizer
        ivfile_sizer.Add(ivfiletext, 1, wx.EXPAND)
        ivfile_sizer.Add(self.ivfileinput)
        
        #add objects into sizers in gdsizer2
        
        aestypesizer.Add(text_aestype, 1, wx.EXPAND)
        aestypesizer.Add(self.aestype)
        keyusagesizer.Add(text_keyusage, 1, wx.EXPAND)
        keyusagesizer.Add(self.keyusage)
       
        
        # Set Default inputs for Text Boxes      
        self.aestype.SetSelection(0)
        self.keyusage.SetSelection(3)
        
        #bind events
        self.button_genkey.Bind(wx.EVT_BUTTON, self.OnCreateKeyPair1)
        button_aesenc.Bind(wx.EVT_BUTTON, self.OnEnc)
        button_aesdec.Bind(wx.EVT_BUTTON, self.OnDec1)
        #self.aestype.Bind(wx.EVT_COMBOBOX, self.OnType)
        clearbutton.Bind(wx.EVT_BUTTON, self.OnClear)
        backbutton.Bind(wx.EVT_BUTTON, self.OnBack)
        self.datacheckbox.Bind(wx.EVT_CHECKBOX, self.OnDataCheckBox)
        self.ivfileinput.Bind(wx.EVT_LEFT_DOWN, self.OnClickInputIV)
        self.datafileinput.Bind(wx.EVT_LEFT_DOWN, self.OnClickInputData)
        
        
        # Set tooltips
        
        self.button_genkey.SetToolTip(wx.ToolTip("Generate OPTIGA™ Trust M AES Symmetric key" ))
        button_aesenc.SetToolTip(wx.ToolTip("Encrypt data using AES symmetric key CBC mode"))
        button_aesdec.SetToolTip(wx.ToolTip("Decrypt using AES CBC mode and output to mydata.txt.dec"))
        clearbutton.SetToolTip(wx.ToolTip("Clear all textboxes"))
        backbutton.SetToolTip(wx.ToolTip("Go back to main page.")) 

        self.SetSizer(mainsizer)
        mainsizer.Fit(self)
        
    def OnDataCheckBox(self, evt):
        cb = evt.GetEventObject()
        
        if (cb.GetValue() == False):
            self.input_display.Enable()
            self.datafileinput.Disable()
            
        else:
            self.input_display.Disable()
            self.datafileinput.Enable()
             
    def OnClickInputIV(self, evt):
        frame = wx.Frame(None, -1, '*.*')
        frame.SetSize(0,0,200,50)
        
        openFileDialog = wx.FileDialog(frame, "Open", "", "","Binary|*.bin", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        filedir = config.IMAGEPATH + "/working_space/"
        openFileDialog.SetDirectory(filedir)
        
        if openFileDialog.ShowModal() ==wx.ID_CANCEL:
            return
                
        print((openFileDialog.GetPath()))
        
        self.inputiv = (openFileDialog.GetPath())
        
        self.ivfileinput.Clear()
        self.ivfileinput.AppendText(os.path.basename(openFileDialog.GetPath()))
        
        openFileDialog.Destroy()

    def OnClickInputData(self, evt):
        frame = wx.Frame(None, -1, '*.*')
        frame.SetSize(0,0,200,50)
        
        openFileDialog = wx.FileDialog(frame, "Open", "", "","All|*.*", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        filedir = config.IMAGEPATH + "/working_space/"
        openFileDialog.SetDirectory(filedir)
        
        if openFileDialog.ShowModal() ==wx.ID_CANCEL:
            return
                
        print((openFileDialog.GetPath()))
        
        self.inputdata = (openFileDialog.GetPath())
        
        self.datafileinput.Clear()
        self.datafileinput.AppendText(os.path.basename(openFileDialog.GetPath()))
        
        openFileDialog.Destroy()
    
    def OnKeyUsage(self):
        
        if (self.keyusage.GetSelection() == 0):
            value = "0x01"
            
            return(value)
        
        elif (self.keyusage.GetSelection() == 1):
            value = "0x02"
         
            return(value)
        
        elif (self.keyusage.GetSelection() == 2):
            value = "0x10"
        
            return(value)
        
        elif (self.keyusage.GetSelection() == 3):
            value = "0x13"
        
            return(value)
        
        elif (self.keyusage.GetSelection() == 4):
            value = "0x20"
        
            return(value)
    
    def OnCreateKeyPair1(self, evt):
        self.command_display.AppendText("Generating Trust M " + self.aestype.GetValue() + " key... \n")
        self.command_display.AppendText("Set Change to ALW to enable AES Key Gen(Only executable when LcsO<op)")
        wx.CallLater(10, self.OnCreateKeyPair)
    
    # note: this function/command runs for quite a while as compared to ECC.
    def OnCreateKeyPair(self):
        
        key_usage = self.OnKeyUsage()
        print(key_usage)
        
        output_message = exec_cmd.execCLI([
            config.EXEPATH + "/bin/trustm_metadata",
            "-w", "0xe200",
            "-Ca",
            ]) 
        self.command_display.AppendText(output_message)
        self.command_display.AppendText("\n./bin/trustm_metadata -w 0xe200 -Ca \n")
        self.command_display.AppendText("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ \n") 
        if (self.aestype.GetSelection() == 0):
            keytype = "0x81"
        
        elif (self.aestype.GetSelection() == 1):
            keytype = "0x82"
        
        elif (self.aestype.GetSelection() == 2):
            keytype = "0x83"
        
        
        output_message = exec_cmd.execCLI([
            config.EXEPATH + "/bin/trustm_symmetric_keygen",
            "-t", key_usage,
            "-k", keytype,
        ])
        
        self.command_display.AppendText(output_message)
        self.command_display.AppendText("\n./bin/trustm_symmetric_keygen -t " + key_usage + " -k " + keytype + " executed \n")
        self.command_display.AppendText("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ \n")


    def OnEnc(self, evt):
        
        if (self.datacheckbox.GetValue() == False):
             datain = self.input_display.GetValue()
             exec_cmd.createProcess("echo " + datain + " > mydata.txt", None)           
        
        else:
             try:
                datain = self.inputdata
             
             except AttributeError:
                wx.CallLater(10, self.OnNoDataFileSelected)
                return
                
        try:
             iv = self.inputiv
             
        except AttributeError:
             wx.CallLater(10, self.OnNoIVFileSelected)
             return
             
        if (self.aestype.GetSelection() == 0):
             aesenc = "aes128.enc"
             
        elif (self.aestype.GetSelection() == 1):
             aesenc = "aes192.enc"
        
        elif (self.aestype.GetSelection() == 2):
             aesenc = "aes256.enc"
        
        exec_cmd.execCLI(["rm", aesenc])
        
        self.command_display.AppendText("\nEncrypting " + self.aestype.GetValue() + " key...\n")
    
        if (self.datacheckbox.GetValue() == False):
             output_message = exec_cmd.execCLI([
             config.EXEPATH + "/bin/trustm_symmetric_enc",
             "-m", "0x09",
             "-o", aesenc,
             "-i", "mydata.txt",
             "-v", iv,     
            ])
         
             self.command_display.AppendText(output_message)   
                
             self.command_display.AppendText("\n/trustm_symmetric_enc -m 0x09 -v " + iv + " -i mydata.txt -o " + aesenc + " is executed\n")
             self.command_display.AppendText("\n++++++++++++++++++++++++++++++++++++++++++++\n")
        
        else:
             output_message = exec_cmd.execCLI([
             config.EXEPATH + "/bin/trustm_symmetric_enc",
             "-m", "0x09",
             "-o", aesenc,
             "-i", datain,
             "-v", iv,     
            ])
         
             self.command_display.AppendText(output_message)   
                
             self.command_display.AppendText("\n/trustm_symmetric_enc -m 0x09 -v " + iv + " -i " + datain + " -o  " + aesenc +  " is executed\n")
             self.command_display.AppendText("\n++++++++++++++++++++++++++++++++++++++++++++\n")
    
    def OnNoDataFileSelected(self):
        infoDialog = wx.MessageDialog(None, "Select Data File to Encrypt", "No Data File Selected", wx.OK | wx.ICON_INFORMATION)
        infoDialog.ShowModal()
        
    def OnNoIVFileSelected(self):
        infoDialog = wx.MessageDialog(None, "Select Initialization File", "No Initialization File Selected", wx.OK | wx.ICON_INFORMATION)
        infoDialog.ShowModal()    
    
    def OnDec1(self, evt):
        wx.CallLater(10, self.OnDec)
    
    def OnDec(self):
        try:
            iv = self.inputiv
            
        except AttributeError:
            wx.CallLater(10, self.OnNoIVFileSelected)
            return    
        
        
        if (self.aestype.GetSelection() == 0):
            aesenc = "aes128.enc"
                
        elif (self.aestype.GetSelection() == 1):
            aesenc = "aes192.enc"
            
        elif (self.aestype.GetSelection() == 2):
            aesenc = "aes256.enc"
        
        
        self.command_display.AppendText("\nDecrypting with " + self.aestype.GetValue() + " Symmetric key...\n")
        
        output_message = exec_cmd.execCLI([
            config.EXEPATH + "/bin/trustm_symmetric_dec",
            "-m", "0x09",
            "-v", iv,
            "-i", aesenc,
            "-o", "mydata.txt.dec"
        ])
        self.command_display.AppendText(output_message)
#         self.Update()
        self.command_display.AppendText("\n/trustm_symmetric_dec -m 0x09 -v" + iv + " -i " + aesenc + " -o mydata.txt.dec  is executed\n")
        self.command_display.AppendText("\n+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")
        self.command_display.AppendText("\nReading decrypted data...\n\n")
        output_message = exec_cmd.execCLI(["cat", "mydata.txt.dec"])
        self.command_display.AppendText(output_message)
        self.command_display.AppendText("\n'cat mydata.txt.dec' executed\n")
        self.command_display.AppendText("\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")


    def OnClear(self, evt):
        self.command_display.Clear()

    # Calling parent of the parent, as direct parent is the notebook,
    # then the second parent is the frame, from which we call the destruction
    def OnBack(self, evt):
        self.Parent.Parent.OnCloseWindow(None)


class Tab2Frame(wx.Frame):
    
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title="Cryptographic Functions", size=(1280, 720), style=(wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX)))
        self.Centre(wx.BOTH)
        main_menu_font = wx.Font(12, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.SetFont(main_menu_font)
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

        # Instantiate all objects
        self.tab_base = wx.Notebook(self, id=wx.ID_ANY, style=wx.NB_TOP)
        self.tab1_ecc = Tab_ECC(self.tab_base)
        self.tab2_rsa = Tab_RSA(self.tab_base)
        self.tab4_aes = Tab_AES(self.tab_base)

        # Add tabs
        self.tab_base.AddPage(self.tab1_ecc, 'ECC')
        self.tab_base.AddPage(self.tab2_rsa, 'RSA')
        self.tab_base.AddPage(self.tab4_aes, 'AES')

        self.Show(True)
        
    
    def OnCloseWindow(self, evt):
        self.Parent.Show()
        self.Destroy()
