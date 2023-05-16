import wx
import shell_util as exec_cmd
import misc_dialogs as misc
import info_dialogs as info
import images as img
import binascii
import subprocess
import os
import config
import re
import math
from subprocess import PIPE

secret_list = ['Integrity Confidential']
enc_algo_list = ['AES-CCM-16-64-128']
sign_algo_list = ['ES_256']
content_reset_list = ['0']
metadata_list = ['metadata.txt']
keydata_list = ['ecc_secp256r1_test.pem' , 'ecc_secp384r1_test.pem' , 'ecc_secp521r1_test.pem' , 'ecc_brainpool_p256r1_test.pem' , 'ecc_brainpool_p384r1_test.pem' , 'ecc_brainpool_p512r1_test.pem' ,]
aesdata_list = ['aes_key_128.txt', 'aes_key_192.txt','aes_key_256.txt' ,]
rsadata_list = ['rsa_1024_test.pem' , 'rsa_2048_test.pem' ,]
meta_trust_anchor_oid_list = ['E0E8', 'E0E9', 'E0EF']
meta_target_oid_list = ['-', 'F1D0', 'F1D1', 'F1D2', 'F1D3', 'F1D4','F1D5', 'F1D6', 'F1D7', 'F1D8', 'F1D9', 'F1DA', 'F1DB', 'F1E0', 'F1E1', 'E0E1', 'E0E2', 'E0E3','E0F1', 'E0F2', 'E0F3', 'E0FC', 'E0FD']
meta_secret_oid_list = ['-','F1D4', 'F1D0', 'F1D6', 'F1D7', 'F1D8', 'F1D9', 'F1DA', 'F1DB']
step1_list = ['Step1: Set Lcso=0x03(Init) ResetType=0x01(Keep TargetData)','Step1: Set Lcso=0x03(Init) ResetType=0x11(Wipe TargetData)']

key_trust_anchor_oid_list = ['E0E8', 'E0E9', 'E0EF']
key_target_oid_list = ['E0F1', 'E0F2','E0F3']
key_secret_oid_list = ['F1D4', 'F1D0', 'F1D6', 'F1D7', 'F1D8', 'F1D9', 'F1DA', 'F1DB']
rsa_target_oid_list = ['E0FC', 'E0FD',]
aes_target_oid_list = ['E200',]

data_trust_anchor_oid_list = ['E0E8', 'E0E9', 'E0EF']
data_secret_oid_list = ['-','F1D4', 'F1D0', 'F1D6', 'F1D7', 'F1D8', 'F1D9', 'F1DA', 'F1DB']
data_target_oid_list = ['-','F1D0','F1D1','F1D2','F1D3','F1D4','F1D5', 'F1D6', 'F1D7', 'F1D8', 'F1D9', 'F1DA', 'F1DB','F1E0', 'F1E1', 'E0E1', 'E0E2', 'E0E3']

datatype_list = ['hex', 'ascii']
MAX_FRAGMENT_SIZE = 640
MAX_PAYLOAD_SIZE = 1280
MAX_NUM_OF_FRAGMENTS = 3
TYPE2_MAX_DATA_SIZE = 1500
TYPE3_MAX_DATA_SIZE = 140

class Tab_MetaConfidentialUpdate(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        
        title = wx.StaticText(self, -1, style=wx.ALIGN_CENTER, label="Metadata Integrity Confidential Protected Update")
        font = wx.Font(20, wx.ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        title.SetFont(font)
        
        textctrlfont = wx.Font()
        textctrlfont.SetPointSize(11)
        
        buttonfont = wx.Font(12, wx.ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        
        # declare the sizers
        mainsizer = wx.BoxSizer(wx.VERTICAL)
        mainhorisizer = wx.BoxSizer(wx.HORIZONTAL)
        
        midsizer = wx.BoxSizer(wx.VERTICAL)
        gdsizer1 = wx.GridSizer(rows=3, cols=3, vgap=10, hgap=10)
        gdsizer2 = wx.GridSizer(rows=2, cols=3, vgap=10, hgap=10)
        gdsizer3 = wx.GridSizer(rows=2, cols=2, vgap=20, hgap=10)
        step1_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        titlesizer = wx.BoxSizer(wx.HORIZONTAL)
        
        leftsizer = wx.BoxSizer(wx.VERTICAL)
        picturesizer = wx.BoxSizer(wx.VERTICAL)
        backbuttonsizer = wx.BoxSizer(wx.HORIZONTAL)
        
        # declare sizers that will be in the grid2
        labelsizer = wx.BoxSizer(wx.VERTICAL)
        secretsizer = wx.BoxSizer(wx.VERTICAL)
        encsizer = wx.BoxSizer(wx.VERTICAL)
        payloadversizer = wx.BoxSizer(wx.VERTICAL)
        payloadtypesizer = wx.BoxSizer(wx.VERTICAL)
        signsizer = wx.BoxSizer(wx.VERTICAL)
        metasizer = wx.BoxSizer(wx.VERTICAL)
        contentsizer = wx.BoxSizer(wx.VERTICAL)
        privsizer = wx.BoxSizer(wx.VERTICAL)
        
        # declare sizers that will be in the grid1
        trustoidsizer = wx.BoxSizer(wx.VERTICAL)
        targetoidsizer = wx.BoxSizer(wx.VERTICAL)
        secretoidsizer = wx.BoxSizer(wx.VERTICAL)
        trustcertsizer = wx.BoxSizer(wx.VERTICAL)
        
        secret1sizer = wx.BoxSizer(wx.VERTICAL)
        secret2sizer = wx.BoxSizer(wx.VERTICAL)

        # instantiate the objects
        self.secret2path = config.EXEPATH + "/ex_protected_update_data_set/samples/confidentiality/secret.txt"
        text_secret2 = wx.StaticText(self, 0, "secret:")
        self.secret2 = wx.TextCtrl(self, 1, value= "secret.txt", style=wx.CB_READONLY,  size = wx.Size(178, -1))
        self.secret2.SetFont(textctrlfont)
        
        self.secret1path = config.EXEPATH + "/ex_protected_update_data_set/samples/confidentiality/secret.txt"
        text_secret1 = wx.StaticText(self, 0, "secret:")
        self.secret1 = wx.TextCtrl(self, 1, value= "secret.txt", style=wx.CB_READONLY,  size = wx.Size(178, -1))
        self.secret1.SetFont(textctrlfont)
        text_secret = wx.StaticText(self, 0, "Protected_Update:")
        self.secret = wx.ComboBox(self, 1, choices=secret_list, style=wx.CB_READONLY,  size = wx.Size(178, -1))
        self.secret.SetFont(textctrlfont)
        text_payload_version = wx.StaticText(self, 0, "payload_version:")
        self.payload_version = wx.TextCtrl(self, 1, value="1",  size = wx.Size(178, -1))
        self.payload_version.SetFont(textctrlfont)
        text_payload_type = wx.StaticText(self, 0, "payload_type:")
        self.payload_type = wx.TextCtrl(self, 1, value="metadata",  size = wx.Size(178, -1))
        self.payload_type.SetFont(textctrlfont)
        text_sign_algo = wx.StaticText(self, 0, "sign_algo:")
        self.sign_algo = wx.ComboBox(self, 1, choices=sign_algo_list, style=wx.CB_READONLY,  size = wx.Size(178, -1))
        self.sign_algo.SetFont(textctrlfont)
        
        self.metapath = config.EXEPATH + "/ex_protected_update_data_set/samples/payload/metadata/metadata.txt"
        text_metadata = wx.StaticText(self, 0, "metadata:")
        self.metadata = wx.TextCtrl(self, 1, value= "metadata.txt", style=wx.CB_READONLY,  size = wx.Size(178, -1))
        self.metadata.SetFont(textctrlfont)
        
        self.priv_keypath = config.EXEPATH + "/scripts/certificates/sample_ec_256_priv.pem"
        text_priv_key = wx.StaticText(self, 0, "trust_anchor_key:")
        self.priv_key = wx.TextCtrl(self, -1, value= "sample_ec_256_priv.pem", style=wx.CB_READONLY, size=(178, 30))
        self.priv_key.SetFont(textctrlfont)
        text_trust_anchor_oid = wx.StaticText(self, -1, "trust_anchor_oid:")
        self.trust_anchor_oid = wx.ComboBox(self, 1, choices=meta_trust_anchor_oid_list, style=wx.CB_READONLY, size = wx.Size(178, -1))
        self.trust_anchor_oid.SetFont(textctrlfont)
        text_target_oid = wx.StaticText(self, -1, "target_oid:")
        self.target_oid = wx.ComboBox(self, 1, choices = meta_target_oid_list, style=wx.CB_READONLY,  size = wx.Size(178, -1))
        self.target_oid.SetFont(textctrlfont)
        text_secret_oid = wx.StaticText(self, -1, "secret_oid:")
        self.secret_oid = wx.ComboBox(self, 1, choices=meta_secret_oid_list, style=wx.CB_READONLY,  size = wx.Size(178, -1))
        self.secret_oid.SetFont(textctrlfont)
        
        self.trust_anchor_certpath = config.EXEPATH + "/scripts/certificates/sample_ec_256_cert.pem"
        text_trust_anchor_cert = wx.StaticText(self, -1, "trust_anchor_cert:")
        self.trust_anchor_cert = wx.TextCtrl(self, 1, value= "sample_ec_256_cert.pem",style=wx.CB_READONLY, size = wx.Size(178, 30))
        self.trust_anchor_cert.SetFont(textctrlfont)
        button_step2 = wx.Button(self, 1, 'Step2: Generate Manifest', size = wx.Size(270, -1))
        button_step2.SetFont(buttonfont)
        button_step3 = wx.Button(self, 1, 'Step3: Update Trust M Objects', size = wx.Size(270, -1))
        button_step3.SetFont(buttonfont)
        button_read_objects_metadata = wx.Button(self, 1, 'Read Objects Metadata', size = wx.Size(270, -1))
        button_read_objects_metadata.SetFont(buttonfont)
        button_reset_mud = wx.Button(self, 1, 'Reset Access Condition', size = wx.Size(270, -1))
        button_reset_mud.SetFont(buttonfont)

        self.step1_combo_box = wx.ComboBox(self, 1, choices=step1_list, style=wx.CB_READONLY, size = wx.Size(554, -1))
        self.step1_combo_box.SetFont(buttonfont)
        self.button_step1 = wx.Button(self, -1, 'Step1: Provisioning for All OIDs', size = wx.Size(270, -1))
        self.button_step1.SetFont(buttonfont)
        
        self.text_display = wx.TextCtrl(self, -1, style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.text_display.SetFont(wx.Font(11, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))

        serverimage = wx.Image(config.IMAGEPATH + "/images/server.png", wx.BITMAP_TYPE_PNG).Scale(110,110,wx.IMAGE_QUALITY_HIGH).ConvertToBitmap()
        serverimage = wx.StaticBitmap(self, -1, serverimage)

        clearimage = wx.Image(config.IMAGEPATH + "/images/clear.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        clearbutton = wx.BitmapButton(self, -1, clearimage)
        
        lockedarrow = wx.Image(config.IMAGEPATH + "/images/LockedArrow.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        lockedarrowimage = wx.StaticBitmap(self, -1,lockedarrow)

        chipimage = wx.Image(config.IMAGEPATH + "/images/chipp3.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        chipimage = wx.StaticBitmap(self, -1,chipimage)
        
        backimage = wx.Image(config.IMAGEPATH + "/images/back.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        backbutton = wx.BitmapButton(self, -1, backimage)
       
        #Add mainhorisizer and title to mainsizer
        mainsizer.Add(title, 0, wx.CENTRE | wx.ALL, 5)
        mainsizer.Add(mainhorisizer, 1, wx.EXPAND)
       
        # Add Sub Sizers to the mainhorisizer
        mainhorisizer.Add(leftsizer, 0, wx.EXPAND)
        mainhorisizer.Add(midsizer, 1, wx.EXPAND)
        mainhorisizer.Add(self.text_display, 1, wx.EXPAND | wx.ALL, 5)
        
        # Add Objects to leftsizer
        leftsizer.Add(picturesizer, 0, wx.TOP, 65)
        leftsizer.AddSpacer(115)
        leftsizer.Add(backbuttonsizer, 0, wx.LEFT | wx.BOTTOM, 10)
        picturesizer.Add(serverimage, 0 , wx.ALIGN_CENTER, 0 )
        picturesizer.AddSpacer(30)
        picturesizer.Add(lockedarrowimage, 0, wx.ALIGN_CENTER, 0)
        picturesizer.AddSpacer(20)
        picturesizer.Add(chipimage, 0, wx.ALIGN_CENTER, 0)
        backbuttonsizer.Add(backbutton, 0, wx.ALIGN_LEFT, 0)
        backbuttonsizer.AddSpacer(10)
        backbuttonsizer.Add(clearbutton, 0, wx.EXPAND, 0)

        # Add sizers to midsizer
        midsizer.AddSpacer(10)
        midsizer.Add(gdsizer1, 0, wx.EXPAND | wx.ALL, 5)
        midsizer.AddSpacer(5)
        midsizer.Add(button_step2, 0, wx.ALL, 5)
        midsizer.AddSpacer(5)
        midsizer.AddSpacer(20)
        midsizer.Add(gdsizer2, 0, wx.EXPAND | wx.ALL, 5)
        midsizer.AddSpacer(5)
        midsizer.Add(step1_sizer)
        midsizer.AddSpacer(5)
        midsizer.Add(gdsizer3, 0, wx.EXPAND | wx.ALL, 5)
        
        #add step1 button into step1_sizer
        step1_sizer.Add(self.step1_combo_box, 1, wx.EXPAND | wx.ALL, 5)
        
        
        #add buttons into gdsizer3
        gdsizer3.AddMany([
            (self.button_step1),
            (button_read_objects_metadata),
            (button_step3),
            (button_reset_mud),

        ])
        
        #add sizers to gdsizer1
        gdsizer1.AddMany([
                (secretsizer, 0, wx.EXPAND),
                (payloadversizer, 0, wx.EXPAND),
                (payloadtypesizer, 0, wx.EXPAND),
                (signsizer, 0, wx.EXPAND),
                (metasizer, 0, wx.EXPAND),
                (privsizer, 0, wx.EXPAND)
        ])
        
        gdsizer1.AddSpacer(20)
        gdsizer1.AddSpacer(20)
        gdsizer1.Add(secret1sizer, 0, wx.EXPAND)
        
        #add sizers to gdsizer2
        gdsizer2.AddMany([
                (trustoidsizer, 0, wx.EXPAND),
                (targetoidsizer, 0, wx.EXPAND),
                (secretoidsizer, 0, wx.EXPAND),
                (trustcertsizer, 0, wx.EXPAND),
        ])
        
        gdsizer2.AddSpacer(20)
        gdsizer2.Add(secret2sizer, 0, wx.EXPAND)
                
        #add objects into sizers in gdsizer1
        secretsizer.Add(text_secret)
        secretsizer.Add(self.secret)
        payloadversizer.Add(text_payload_version)
        payloadversizer.Add(self.payload_version)
        payloadtypesizer.Add(text_payload_type)
        payloadtypesizer.Add(self.payload_type)
        signsizer.Add(text_sign_algo)
        signsizer.Add(self.sign_algo)
        metasizer.Add(text_metadata)
        metasizer.Add(self.metadata)
        privsizer.Add(text_priv_key)
        privsizer.Add(self.priv_key)
        secret1sizer.Add(text_secret1)
        secret1sizer.Add(self.secret1)

        #add objects into sizers in gdsizer2
        trustoidsizer.Add(text_trust_anchor_oid)
        trustoidsizer.Add(self.trust_anchor_oid)
        targetoidsizer.Add(text_target_oid)
        targetoidsizer.Add(self.target_oid)
        secretoidsizer.Add(text_secret_oid)
        secretoidsizer.Add(self.secret_oid)
        trustcertsizer.Add(text_trust_anchor_cert)
        trustcertsizer.Add(self.trust_anchor_cert)
        secret2sizer.Add(text_secret2)
        secret2sizer.Add(self.secret2)

        
        # Set Default inputs for Text Boxes      
        self.secret.SetSelection(0)
        self.sign_algo.SetSelection(0)
        #self.metadata.SetSelection(0)
        self.trust_anchor_oid.SetSelection(0)
        self.target_oid.SetSelection(1)
        self.secret_oid.SetSelection(1)
        self.step1_combo_box.SetSelection(0)

        # attach objects to the sizer
        # declare and bind events
        clearbutton.Bind(wx.EVT_BUTTON, self.OnFlush)
        backbutton.Bind(wx.EVT_BUTTON, self.OnBack)
        button_read_objects_metadata.Bind(wx.EVT_BUTTON, self.OnReadMetadata1)
        self.button_step1.Bind(wx.EVT_BUTTON, self.OnRunStep1)
        button_step2.Bind(wx.EVT_BUTTON, self.OnGenManifest)
        button_step3.Bind(wx.EVT_BUTTON, self.OnProtectedUpdate1)
        button_reset_mud.Bind(wx.EVT_BUTTON, self.OnResetMUD1)
        self.secret1.Bind(wx.EVT_LEFT_DOWN,self.OnClickSecret)
        self.secret2.Bind(wx.EVT_LEFT_DOWN,self.OnClickSecret2)
        self.priv_key.Bind(wx.EVT_LEFT_DOWN,self.OnClickFileName)
        self.trust_anchor_cert.Bind(wx.EVT_LEFT_DOWN,self.OnClickCertName)
        self.metadata.Bind(wx.EVT_LEFT_DOWN,self.OnClickMetadata)
        
        # bind target_oid and secret_oid to events to prevent same selection
        self.target_oid.Bind(wx.EVT_COMBOBOX, self.OnSelectTargetOid)
        self.secret_oid.Bind(wx.EVT_COMBOBOX, self.OnSelectSecretOid)
        
        # Set tooltips
        self.button_step1.SetToolTip(wx.ToolTip("Provision metadata for Trust Anchor OID, Protected Update Secret OID and Target OID.\n" \
                                                "Keep Data: Provision Target OID (Set Lcso=0x03(Init) Reset Type=0x01)\n" \
                                                "Wipe Data: Provision Target OID (Set Lcso=0x03(Init) Reset Type=0x11)"))
        button_step2.SetToolTip(wx.ToolTip("Generate the correct manifest and fragment for protected update."))
        button_step3.SetToolTip(wx.ToolTip("Perform protected update for metadata of Target OID."))
        clearbutton.SetToolTip(wx.ToolTip("Clear all textboxes."))
        backbutton.SetToolTip(wx.ToolTip("Go back to main page."))

        self.SetSizer(mainsizer)
        mainsizer.Fit(self)   
        
    def OnSelectTargetOid(self, evt):
        if (self.target_oid.GetValue() == self.secret_oid.GetValue() and self.target_oid.GetValue() != '-'):
                infoDialog = wx.MessageDialog(None, "Target OID and Secret OID cannot be the same", "Duplicated Target and Secret OID", wx.OK | wx.ICON_INFORMATION)
                infoDialog.ShowModal()
                
                self.target_oid.SetSelection(0)
                 
    def OnSelectSecretOid(self, evt):
        if (self.secret_oid.GetValue() == self.target_oid.GetValue() and self.secret_oid.GetValue() != '-'):
                infoDialog = wx.MessageDialog(None, "Target OID and Secret OID cannot be the same", "Duplicated Target and Secret OID", wx.OK | wx.ICON_INFORMATION)
                infoDialog.ShowModal()
                
                self.secret_oid.SetSelection(0)


    def OnNoOidSelected(self):
        infoDialog = wx.MessageDialog(None, "Please select target and/or secret OID", "No OID selected", wx.OK | wx.ICON_INFORMATION)
        infoDialog.ShowModal()

    def OnClickMetadata(self, evt):
        frame = wx.Frame(None, -1, '*.*')
        frame.SetSize(0,0,200,50)
            
        openFileDialog = wx.FileDialog(frame, "Open", "", "","All|*.txt;*.pem|metadata|*.txt;*.pem", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST |wx.FD_CHANGE_DIR)
        
        some_dir= config.EXEPATH + "/ex_protected_update_data_set/samples/payload/metadata/"
        
        openFileDialog.SetDirectory(some_dir)
        openFileDialog.SetFilename("metadata.txt")
        
        if openFileDialog.ShowModal() ==wx.ID_CANCEL:
            
                return
        print((openFileDialog.GetPath()))
        #self.metadata.SetValue(openFileDialog.GetPath())
        self.metapath = openFileDialog.GetPath()
        
        self.metadata.Clear()
        self.metadata.AppendText(os.path.basename(openFileDialog.GetPath()))
#         print(self.metadata.GetValue())
#         filename= os.path.basename(openFileDialog.GetPath())
#         print(filename)
        
        openFileDialog.Destroy()
 

    def OnClickFileName(self, evt):
        frame = wx.Frame(None, -1, '*.*')
        frame.SetSize(0,0,200,50)
            
        openFileDialog = wx.FileDialog(frame, "Open", "", "","All|*.crt;*.pem|Certificate|*.crt;*.pem", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST |wx.FD_CHANGE_DIR)
        
        some_dir= config.EXEPATH + "/scripts/certificates/"
        
        openFileDialog.SetDirectory(some_dir)
        openFileDialog.SetFilename("sample_ec_256_priv.pem")

        
        if openFileDialog.ShowModal() ==wx.ID_CANCEL:
            
                return
        print((openFileDialog.GetPath()))
        #self.priv_key.SetValue(openFileDialog.GetPath())
        self.priv_keypath = openFileDialog.GetPath()
        
        self.priv_key.Clear()
        self.priv_key.AppendText(os.path.basename(openFileDialog.GetPath()))
        
        openFileDialog.Destroy()    

    def OnClickCertName(self, evt):
        frame = wx.Frame(None, -1, '*.*')
        frame.SetSize(0,0,200,50)
            
        openFileDialog = wx.FileDialog(frame, "Open", "", "","All|*.crt;*.pem|Certificate|*.crt;*.pem", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST |wx.FD_CHANGE_DIR)
        
        some_Dir= config.EXEPATH + "/scripts/certificates/"
        
        openFileDialog.SetDirectory(some_Dir)
        openFileDialog.SetFilename("sample_ec_256_cert.pem")
        
        if openFileDialog.ShowModal() ==wx.ID_CANCEL:
            
                return
        print((openFileDialog.GetPath()))
        #self.trust_anchor_cert.SetValue(openFileDialog.GetPath())
        self.trust_anchor_certpath = openFileDialog.GetPath()
        
        self.trust_anchor_cert.Clear()
        self.trust_anchor_cert.AppendText(os.path.basename(openFileDialog.GetPath()))
        
        openFileDialog.Destroy()


    def OnClickSecret(self, evt):
        frame = wx.Frame(None, -1, '*.*')
        frame.SetSize(0,0,200,50)
            
        openFileDialog = wx.FileDialog(frame, "Open", "", "","All|*.crt;*.txt|Certificate|*.crt;*.txt", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST )
        
        some_Dir= config.EXEPATH + "/ex_protected_update_data_set/samples/confidentiality/"
        
        openFileDialog.SetDirectory(some_Dir)
        openFileDialog.SetFilename("secret.txt")
        
        if openFileDialog.ShowModal() ==wx.ID_CANCEL:
            
                return
        print((openFileDialog.GetPath()))
        #self.secret1.SetValue(openFileDialog.GetPath())
        self.secret1path = openFileDialog.GetPath()
        
        self.secret1.Clear()
        self.secret1.AppendText(os.path.basename(openFileDialog.GetPath()))
        
        openFileDialog.Destroy()
    
    def OnClickSecret2(self, evt):
        frame = wx.Frame(None, -1, '*.*')
        frame.SetSize(0,0,200,50)
            
        openFileDialog = wx.FileDialog(frame, "Open", "", "","All|*.crt;*.txt|Certificate|*.crt;*.txt", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST )
        
        some_Dir= config.EXEPATH + "/ex_protected_update_data_set/samples/confidentiality/"
        
        openFileDialog.SetDirectory(some_Dir)
        openFileDialog.SetFilename("secret.txt")
        
        
        if openFileDialog.ShowModal() ==wx.ID_CANCEL:
            
                return
        print((openFileDialog.GetPath()))
        #self.secret2.SetValue(openFileDialog.GetPath())
        self.secret2path = openFileDialog.GetPath()
        
        self.secret2.Clear()
        self.secret2.AppendText(os.path.basename(openFileDialog.GetPath()))
        
        openFileDialog.Destroy()

    def OnRunStep1(self, evt):
        if (self.target_oid.GetValue() == '-' or self.secret_oid.GetValue() == '-'):
            wx.CallLater(10, self.OnNoOidSelected)
            return
        
        if (self.step1_combo_box.GetSelection() == 0):
            self.OnSetupTempDecom1()
        elif (self.step1_combo_box.GetSelection() == 1):
            self.OnSetupWipeData1()

    def OnSetup(self):
        trust_anchor_oid = "0x" + self.trust_anchor_oid.GetValue()
        target_oid = "0x" + self.target_oid.GetValue()
        secret_oid = "0x" + self.secret_oid.GetValue()
        certfile = self.trust_anchor_certpath
        
        TRUST_ANCHOR_META = "2003E80111"
        #PROTECTED_UPDATE_SECRET = "49C9F492A992F6D4C54F5B12C57EDB27CED224048F25482AA149C9F492A992F649C9F492A992F6D4C54F5B12C57EDB27CED224048F25482AA149C9F492A992F6"
        
        f = open(self.secret2path, 'r')
        file= f.read()
        print(file)
        PROTECTED_UPDATE_SECRET = file
        f.close()
        
        PROTECTED_UPDATE_SECRET_META = "200BD103E1FC07D30100E80123"
     
        #Step1: Provisioning initial Trust Anchor, metadata for Trust Anchor
        self.text_display.AppendText("Provisioning for initial Trust Anchor OID... \n")
        command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_cert", "-w", trust_anchor_oid, "-i", certfile, ])
        self.text_display.AppendText(command_output)
        self.text_display.AppendText("'trustm_cert -w 0x" + trust_anchor_oid + " -i " + certfile + "'" + " executed \n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
        
        self.text_display.AppendText("Provisioning for trust anchor metadata... \n")
        command_output = exec_cmd.createProcess("echo " + TRUST_ANCHOR_META + " | xxd -r -p > trust_anchor_metadata.bin", None)
        self.text_display.AppendText("'echo $TRUST_ANCHOR_META | xxd -r -p > trust_anchor_metadata.bin' executed \n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
        
        self.text_display.AppendText("Writing trust_anchor_metadata.bin as metadata of Trust Anchor OID... \n")
        command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_metadata", "-w", trust_anchor_oid, "-F", "trust_anchor_metadata.bin", ])
        self.text_display.AppendText(command_output)
        self.text_display.AppendText("'trustm_metadata -w 0x" + trust_anchor_oid + " -F trust_anchor_metadata.bin'" + " executed \n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
        
        
        #Step2: Provisioning Protected Update Secret OID, metadata for Protected Update Secret OID
        self.text_display.AppendText("Provisioning for protected update secret... \n")
        command_output = exec_cmd.createProcess("echo " + PROTECTED_UPDATE_SECRET + " | xxd -r -p > protected_update_secret.dat", None)
        self.text_display.AppendText("'$PROTECTED_UPDATE_SECRET xxd -r -p > protected_update_secret.dat' executed \n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")    
        
        self.text_display.AppendText("Writing protected update secret into secret_oid...")
        command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_data", "-e", "-w", secret_oid, "-i", "protected_update_secret.dat", ])
        self.text_display.AppendText(command_output)
        self.text_display.AppendText("'trustm_data -e -w 0x" + secret_oid + " -i protected_update_secret.dat'" + " executed \n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
       
        self.text_display.AppendText("Provisioning for protected update secret metadata... \n")
        command_output = exec_cmd.createProcess("echo " + PROTECTED_UPDATE_SECRET_META + " | xxd -r -p > protected_update_secret_metadata.bin", None)
        self.text_display.AppendText("'$PROTECTED_UPDATE_SECRET_META xxd -r -p > protected_update_secret_metadata.bin' executed \n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
        
        self.text_display.AppendText("Writing protected update secret metadata into secret_oid... ")
        command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_metadata", "-w", secret_oid, "-F", "protected_update_secret_metadata.bin", ])
        self.text_display.AppendText(command_output)
        self.text_display.AppendText("'trustm_metadata -w " + secret_oid + " -F protected_update_secret_metadata.bin' executed \n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
        
        
    def OnSetupTempDecom1(self):
        self.text_display.AppendText("Provisioning Data Objects ... \n")
        wx.CallLater(10, self.OnSetupTempDecom)
        
        
    def OnSetupTempDecom(self):
        trust_anchor_oid = "0x" + self.trust_anchor_oid.GetValue()
        target_oid = "0x" + self.target_oid.GetValue()
        secret_oid = "0x" + self.secret_oid.GetValue()
        secret_list_value=self.secret.GetValue()
        
       # if (self.secret.GetSelection() == 1):
        if (secret_list_value=="Integrity"):
            TARGET_OID_META="200CC1020000F00101D80321" + self.trust_anchor_oid.GetValue()
        #if (secret_list_value=="(None)"):
        else:
            TARGET_OID_META="2010C1020000F00101D80721" + self.trust_anchor_oid.GetValue() + "FD20" + self.secret_oid.GetValue()
        
        self.OnSetup()
        
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

        #Set LcsO to Initialization mode
        self.text_display.AppendText("Change Target OID Lcs0 to Initialization mode... \n")
        command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_metadata", "-w", target_oid, "-I"])
        self.text_display.AppendText(command_output)
        self.text_display.AppendText("'trustm_metadata -w " + target_oid + " -I' executed \n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
        
    def OnSetupWipeData1(self):
        self.text_display.AppendText("Provisioning Data Objects (for Wipe Data)... \n")
        wx.CallLater(10, self.OnSetupWipeData)
    
    def OnSetupWipeData(self):
        trust_anchor_oid = "0x" + self.trust_anchor_oid.GetValue()
        target_oid = "0x" + self.target_oid.GetValue()
        secret_oid = "0x" + self.secret_oid.GetValue()
        secret_list_value=self.secret.GetValue()
        if (secret_list_value=="Integrity"):    
            TARGET_OID_META_PER="200CC1020000F00111D80321" + self.trust_anchor_oid.GetValue()        
        else:
            TARGET_OID_META_PER="2010C1020000F00111D80721" + self.trust_anchor_oid.GetValue() + "FD20" + self.secret_oid.GetValue()  
        
        self.OnSetup()
        
        #Set metadata for Target OID
        self.text_display.AppendText("Set protected update for Target OID (Provision for Target OID)... \n")
        command_output = exec_cmd.createProcess("echo " + TARGET_OID_META_PER + " | xxd -r -p > targetOID_metadata_permanent.bin", None)
        self.text_display.AppendText("'$TARGET_OID_META | xxd -r -p > targetOID_metadata.bin' executed \n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
        self.text_display.AppendText("Writing targetOID_metadata_permanent.bin as metadata of Target OID... \n")
        command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_metadata", "-w", target_oid, "-F", "targetOID_metadata_permanent.bin", ])
        self.text_display.AppendText(command_output)
        self.text_display.AppendText("'trustm_metadata -w " + target_oid + " -F targetOID_metadata.bin' executed \n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")

        #Set LcsO to Initialization mode
        self.text_display.AppendText("Change Target OID Lcs0 to Initialization mode... \n")
        command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_metadata", "-w", target_oid, "-I"])
        self.text_display.AppendText(command_output)
        self.text_display.AppendText("'trustm_metadata -w " + target_oid + " -I' executed \n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")     
        
    def OnReadMetadata1(self, evt):
        if (self.target_oid.GetValue() == '-' or self.secret_oid.GetValue() == '-'):
            wx.CallLater(10, self.OnNoOidSelected)
            return
        
        self.text_display.AppendText("Reading Objects Metadata... \n")
        wx.CallLater(10, self.OnReadMetadata)
    
    def OnReadMetadata(self):
        trust_anchor_oid = "0x" + self.trust_anchor_oid.GetValue()
        target_oid = "0x" + self.target_oid.GetValue()
        secret_oid = "0x" + self.secret_oid.GetValue()
        
        self.text_display.AppendText("Reading out metadata for trust_anchor_oid... \n")
        command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_metadata", "-r", trust_anchor_oid, ])
        self.text_display.AppendText(command_output)
        self.text_display.AppendText("'trustm_metadata -r " + trust_anchor_oid + "' executed \n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
                
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
        
    def OnGenManifest(self, evt):
        if (self.target_oid.GetValue() == '-' or self.secret_oid.GetValue() == '-'):
                wx.CallLater(10, self.OnNoOidSelected)
                return
                
        # constants for cli output parsing
        MANIFEST_SIZE_INDEX = 24
        FRAGMENT_SIZE_INDEX = 28
        BYTES_PER_LINE = 16
        #    
            
        payload_version = "payload_version=" + self.payload_version.GetValue()
        trust_anchor_oid = "trust_anchor_oid=" + self.trust_anchor_oid.GetValue()
        target_oid = "target_oid=" + self.target_oid.GetValue()
        sign_algo = "sign_algo=" + self.sign_algo.GetValue()
        #priv_key = "priv_key=" + self.priv_key.GetValue()
        priv_key = "priv_key=" + self.priv_keypath
        payload_type = "payload_type=" + self.payload_type.GetValue()
        
        #metadata = "metadata=" + self.metadata.GetValue()
        #print(self.metapath)
        metadata = "metadata=" + self.metapath
        content_reset = "content_reset=0"
        label = "label=test"
        enc_algo = "enc_algo=AES-CCM-16-64-128"
        secret_oid = "secret_oid=" + self.secret_oid.GetValue()
        
        secret_list_value=self.secret.GetValue()
        if (secret_list_value=="Integrity"):    
            command_output = exec_cmd.createProcess(config.EXEPATH + "/ex_protected_update_data_set/Linux/bin/trustm_protected_update_set " + payload_version + " "
                                                    + trust_anchor_oid + " " + target_oid + " " + sign_algo + " " + priv_key + " " + payload_type
                                                    + " " + metadata + " " + content_reset + " " + label + " " + enc_algo + " " + secret_oid 
                                                    + "| grep -A10 'uint8_t manifest_data\|uint8_t fragment_01' | sed '1,2d' | sed '11,12d' | sed '$d' | sed 's/0x//g' | tr -d ',[:space:]'",
                                                    None)
        else:
            secret = "secret=" + self.secret1path
            #command_output = exec_cmd.createProcess(config.EXEPATH + "/ex_protected_update_data_set/Linux/bin/trustm_protected_update_set " + payload_version + " "
            #                                        + trust_anchor_oid + " " + target_oid + " " + sign_algo + " " + priv_key + " " + payload_type
            #                                        + " " + metadata + " " + content_reset + " " + label + " " + enc_algo + " " + secret_oid + " " + secret +
            #                                        "| grep -A16 'uint8_t manifest_data\|uint8_t fragment_01' | sed '1,2d' | sed '17,18d' | sed '$d' | sed 's/0x//g' | tr -d ',[:space:]'",
            #                                        None)
                                                    
                                                    
            test = exec_cmd.createProcess(config.EXEPATH + "/ex_protected_update_data_set/Linux/bin/trustm_protected_update_set " + payload_version + " "
                                                    + trust_anchor_oid + " " + target_oid + " " + sign_algo + " " + priv_key + " " + payload_type
                                                    + " " + metadata + " " + content_reset + " " + label + " " + enc_algo + " " + secret_oid + " " + secret, None)
                                                    
            testDecoded = test.stdout.read().decode()
            
            
        ########################################## CLI output parsing ######################################
        print(testDecoded)
        lines = testDecoded.splitlines()
        
        # get the line index of manifest data
        manifestStartLine = 0
        
        for line in lines:
                if ("Manifest Data" in line):
                        break

                manifestStartLine += 1        
        
        # extract info on manifest size
        manifestSize = int(lines[manifestStartLine][MANIFEST_SIZE_INDEX:MANIFEST_SIZE_INDEX+3])
        
        # number of lines to read from manifest data
        manifestDataLineLimit = math.ceil(manifestSize / BYTES_PER_LINE)
        
        # extract manifest as it is from cli
        manifestData = ""
        for manifestLines in lines[manifestStartLine+3:manifestStartLine+3+manifestDataLineLimit]:
                manifestData += manifestLines
        
        # clean extracted manifest
        manifestData = manifestData.replace('0x', '')
        manifestData = manifestData.replace(',', '')
        manifestData = manifestData.replace(' ', '')
        manifestData = re.sub('\n', '', manifestData)
        manifestData = re.sub('\t', '', manifestData)
                
        # extracting fragments
        lineIndex = 0
        fragmentData = ""
        for line in lines:
                if ("Fragment number" in line):
                        # get fragment size
                        fragmentSize = int(line[FRAGMENT_SIZE_INDEX:FRAGMENT_SIZE_INDEX+3])
                        fragmentDataLinesLimit = math.ceil(fragmentSize / BYTES_PER_LINE)
                        
                        for fragmentLines in lines[lineIndex+3:lineIndex+3+fragmentDataLinesLimit]:
                                fragmentData += fragmentLines
                
                lineIndex +=1
        
        # clean extracted fragments
        fragmentData = fragmentData.replace('0x', '')
        fragmentData = fragmentData.replace(',', '')
        fragmentData = fragmentData.replace(' ', '')
        fragmentData = re.sub('\n', '', fragmentData)
        fragmentData = re.sub('\t', '', fragmentData)
        
        ####################################################################################################

        self.text_display.AppendText("manifest: " + manifestData)
        self.text_display.AppendText("\n\nfragment: " + fragmentData)
        exec_cmd.createProcess("echo " + manifestData + " | xxd -r -p > manifest.dat", None)
        exec_cmd.createProcess("echo " + fragmentData + " | xxd -r -p > fragment.dat", None)
        self.text_display.AppendText("\n\nmanifest.dat and fragment.dat generated\n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
    
    def OnProtectedUpdate1(self, evt):
        if (self.target_oid.GetValue() == '-' or self.secret_oid.GetValue() == '-'):
                wx.CallLater(10, self.OnNoOidSelected)
                return
                
        self.text_display.AppendText("Metadata protected update for Target OID... \n")
        wx.CallLater(10, self.OnProtectedUpdate)
    
    def OnProtectedUpdate(self):
        target_oid = "0x" + self.target_oid.GetValue()
        command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_protected_update", "-k", target_oid, "-m", "manifest.dat", "-f", "fragment.dat", ])
        self.text_display.AppendText(command_output)
        self.text_display.AppendText("'trustm_protected_update -k " + target_oid + " -m manifest.dat -f fragment.dat' executed \n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
        
    def OnResetMUD1(self, evt):
        if (self.target_oid.GetValue() == '-'):
                wx.CallLater(10, self.OnNoOidSelected)
                return
                
        self.text_display.AppendText("Resetting Metadata Update Description tag for Target OID... \n")
        wx.CallLater(10, self.OnResetMUD)
    
    def OnResetMUD(self):
        RESET_MUD_META="2003D801FF"
        target_oid = "0x" + self.target_oid.GetValue()
        exec_cmd.createProcess("echo " + RESET_MUD_META + " | xxd -r -p > mud_reset.bin", None)
        command_output = exec_cmd.execCLI(["xxd", "mud_reset.bin", ])
        self.text_display.AppendText(command_output)
        self.text_display.AppendText("mud_reset.bin generated\n")
        self.text_display.AppendText("Writing metadata for Target OID... \n")
        exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_metadata", "-w", target_oid, "-F", "mud_reset.bin", ])
        self.text_display.AppendText("'trustm_metadata -w " + target_oid + " -F mud_reset.bin' executed \n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
    
    
    def OnFlush(self, evt):
        self.text_display.Clear()

    # Calling parent of the parent, as direct parent is the notebook,
    # then the second parent is the frame, from which we call the destruction
    def OnBack(self, evt):
        self.Parent.Parent.OnCloseWindow(None)
        

class Tab_KeyConfidentialUpdate(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        
        title = wx.StaticText(self, -1, style=wx.ALIGN_CENTER, label="ECC Key Integrity Confidential Protected Update")
        font = wx.Font(20, wx.ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        title.SetFont(font)
        
        textctrlfont = wx.Font()
        textctrlfont.SetPointSize(10)
        
        textctrlfont1 = wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD,)
        buttonfont = wx.Font(12, wx.ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        
        # declare the sizers
        mainsizer = wx.BoxSizer(wx.VERTICAL)
        mainhorisizer = wx.BoxSizer(wx.HORIZONTAL)
        
        midsizer = wx.BoxSizer(wx.VERTICAL)
        gdsizer1 = wx.GridSizer(rows=3, cols=3, vgap=10, hgap=5)
        gdsizer2 = wx.GridSizer(rows=2, cols=3, vgap=10, hgap=10)
        gdsizer3 = wx.GridSizer(rows=2, cols=2, vgap=20, hgap=10)
        step1_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        titlesizer = wx.BoxSizer(wx.HORIZONTAL)
        
        leftsizer = wx.BoxSizer(wx.VERTICAL)
        picturesizer = wx.BoxSizer(wx.VERTICAL)
        backbuttonsizer = wx.BoxSizer(wx.HORIZONTAL)
        
        # declare sizers that will be in the grid1
        labelsizer = wx.BoxSizer(wx.VERTICAL)
        secretsizer = wx.BoxSizer(wx.VERTICAL)
        encsizer = wx.BoxSizer(wx.VERTICAL)
        payloadversizer = wx.BoxSizer(wx.VERTICAL)
        payloadtypesizer = wx.BoxSizer(wx.VERTICAL)
        signsizer = wx.BoxSizer(wx.VERTICAL)
        keydatasizer = wx.BoxSizer(wx.VERTICAL)
        contentsizer = wx.BoxSizer(wx.VERTICAL)
        privsizer = wx.BoxSizer(wx.VERTICAL)
        
        # declare sizers that will be in the grid2
        trustoidsizer = wx.BoxSizer(wx.VERTICAL)
        targetoidsizer = wx.BoxSizer(wx.VERTICAL)
        secretoidsizer = wx.BoxSizer(wx.VERTICAL)
        trustcertsizer = wx.BoxSizer(wx.VERTICAL)
        secret1sizer = wx.BoxSizer(wx.VERTICAL)
        keylengthsizer = wx.BoxSizer(wx.VERTICAL)
        keyusagesizer = wx.BoxSizer(wx.VERTICAL)
        secret2sizer = wx.BoxSizer(wx.VERTICAL)
        
        keyusage = ['Auth/Sign','Sign','Sign/Key Agree']
        confidential_list = ['Integrity Confidential']
        keylength = ['ecc_secp256r1', 'ecc_secp384r1', 'ecc_secp521r1', 'ecc_brainpool_p256r1', 'ecc_brainpool_p384r1', 'ecc_brainpool_p512r1']
        
        # instantiate the objects
        self.secret2path = config.EXEPATH + "/ex_protected_update_data_set/samples/confidentiality/secret.txt"
        text_secret2 = wx.StaticText(self, 0, "secret:")
        self.secret2 = wx.TextCtrl(self, 1, value= "secret.txt", style=wx.CB_READONLY,  size = wx.Size(178, -1))
        self.secret2.SetFont(textctrlfont)
        text_keylength = wx.StaticText(self, 0, "Key_length:")
        self.keylength = wx.ComboBox(self, 1, choices=keylength, style=wx.CB_READONLY, size=wx.Size(178, -1))
        self.keylength.SetFont(textctrlfont)
        text_keyusage = wx.StaticText(self, 0, "Key_usage:")
        self.keyusage = wx.ComboBox(self, 1, choices=keyusage, style=wx.CB_READONLY,  size = wx.Size(178, -1))
        self.keyusage.SetFont(textctrlfont)
        text_secret = wx.StaticText(self, 0, "Protected_Update:")
        self.secret = wx.ComboBox(self, 1, choices=confidential_list, style=wx.CB_READONLY,  size = wx.Size(178, -1))
        self.secret.SetFont(textctrlfont)
        text_payload_version = wx.StaticText(self, 0, "payload_version:")
        self.payload_version = wx.TextCtrl(self, 1, value="1",  size = wx.Size(178, -1))
        self.payload_version.SetFont(textctrlfont)
        text_payload_type = wx.StaticText(self, 0, "payload_type:")
        self.payload_type = wx.TextCtrl(self, 1, value="key",  size = wx.Size(178, -1))
        self.payload_type.SetFont(textctrlfont)
        text_sign_algo = wx.StaticText(self, 0, "sign_algo:")
        self.sign_algo = wx.ComboBox(self, 1, choices=sign_algo_list, style=wx.CB_READONLY,  size = wx.Size(178, -1))
        self.sign_algo.SetFont(textctrlfont)
        
        self.keypath = config.EXEPATH + "/ex_protected_update_data_set/samples/payload/key/ecc_secp256r1_test.pem"
        text_keydata = wx.StaticText(self, 0, "key_data:")
        self.keydata = wx.TextCtrl(self, 1, value= "ecc_secp256r1_test.pem", style=wx.CB_READONLY,  size = wx.Size(178, -1))
        self.keydata.SetFont(textctrlfont)
        
        self.priv_keypath = config.EXEPATH + "/scripts/certificates/sample_ec_256_priv.pem"
        text_priv_key = wx.StaticText(self, 0, "trust_anchor_privkey:")
        text_priv_key.SetFont(textctrlfont1)
        self.priv_key = wx.TextCtrl(self, -1, value= "sample_ec_256_priv.pem", style=wx.CB_READONLY, size=(178, 30))
        self.priv_key.SetFont(textctrlfont)
        text_trust_anchor_oid = wx.StaticText(self, -1, "trust_anchor_oid:")
        self.trust_anchor_oid = wx.ComboBox(self, 1, choices=key_trust_anchor_oid_list, style=wx.CB_READONLY, size = wx.Size(178, -1))
        self.trust_anchor_oid.SetFont(textctrlfont)
        text_target_oid = wx.StaticText(self, -1, "target_oid_ECC:")
        self.target_oid = wx.ComboBox(self, 1, choices =key_target_oid_list, style=wx.CB_READONLY,  size = wx.Size(178, -1))
        self.target_oid.SetFont(textctrlfont)
        text_secret_oid = wx.StaticText(self, -1, "secret_oid:")
        self.secret_oid = wx.ComboBox(self, 1, choices=key_secret_oid_list, style=(wx.TE_CHARWRAP|wx.TE_MULTILINE), size=(178, 30))
        self.secret_oid.SetFont(textctrlfont)
        
        self.secret1path = config.EXEPATH + "/ex_protected_update_data_set/samples/confidentiality/secret.txt"
        text_secret1 = wx.StaticText(self, 0, "secret:")
        self.secret1 = wx.TextCtrl(self, 1, value= "secret.txt", style=wx.CB_READONLY,  size = wx.Size(178, -1))
        self.secret1.SetFont(textctrlfont)

        self.trust_anchor_certpath = config.EXEPATH + "/scripts/certificates/sample_ec_256_cert.pem"
        text_trust_anchor_cert = wx.StaticText(self, -1, "trust_anchor_cert:")
        self.trust_anchor_cert = wx.TextCtrl(self, 1, value= "sample_ec_256_cert.pem",style=wx.CB_READONLY, size = wx.Size(178, 30))
        self.trust_anchor_cert.SetFont(textctrlfont)
        button_step2 = wx.Button(self, 1, 'Step2: Generate Manifest', size = wx.Size(270, -1))
        button_step2.SetFont(buttonfont)
        button_step3 = wx.Button(self, 1, 'Step3: Update Trust M Objects', size = wx.Size(270, -1))
        button_step3.SetFont(buttonfont)
        button_read_objects_metadata = wx.Button(self, 1, 'Read Objects Metadata', size = wx.Size(270, -1))
        button_read_objects_metadata.SetFont(buttonfont)
        button_reset_access = wx.Button(self, 1, 'Reset Access Condition', size = wx.Size(270, -1))
        button_reset_access.SetFont(buttonfont)

        self.button_step1 = wx.Button(self, -1, 'Step1:Provision for all OIDs', size = wx.Size(270, -1))
        self.button_step1.SetFont(buttonfont)
        
        self.text_display = wx.TextCtrl(self, -1, style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.text_display.SetFont(wx.Font(11, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))

        serverimage = wx.Image(config.IMAGEPATH + "/images/server.png", wx.BITMAP_TYPE_PNG).Scale(110,110,wx.IMAGE_QUALITY_HIGH).ConvertToBitmap()
        serverimage = wx.StaticBitmap(self, -1, serverimage)

        clearimage = wx.Image(config.IMAGEPATH + "/images/clear.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        clearbutton = wx.BitmapButton(self, -1, clearimage)
        
        lockedarrow = wx.Image(config.IMAGEPATH + "/images/LockedArrow.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        lockedarrowimage = wx.StaticBitmap(self, -1,lockedarrow)

        chipimage = wx.Image(config.IMAGEPATH + "/images/chipp3.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        chipimage = wx.StaticBitmap(self, -1,chipimage)
        
        backimage = wx.Image(config.IMAGEPATH + "/images/back.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        backbutton = wx.BitmapButton(self, -1, backimage)
       
        #Add mainhorisizer and title to mainsizer
        mainsizer.Add(title, 0, wx.CENTRE | wx.ALL, 5)
        mainsizer.Add(mainhorisizer, 1, wx.EXPAND)
       
        # Add Sub Sizers to the mainhorisizer
        mainhorisizer.Add(leftsizer, 0, wx.EXPAND)
        mainhorisizer.Add(midsizer, 1, wx.EXPAND)
        mainhorisizer.Add(self.text_display, 1, wx.EXPAND | wx.ALL, 5)
        
        # Add Objects to leftsizer
        leftsizer.Add(picturesizer, 0, wx.TOP, 65)
        leftsizer.AddSpacer(110)
        leftsizer.Add(backbuttonsizer, 0, wx.LEFT | wx.BOTTOM, 10)
        picturesizer.Add(serverimage, 0 , wx.ALIGN_CENTER, 0 )
        picturesizer.AddSpacer(30)
        picturesizer.Add(lockedarrowimage, 0, wx.ALIGN_CENTER, 0)
        picturesizer.AddSpacer(20)
        picturesizer.Add(chipimage, 0, wx.ALIGN_CENTER, 0)
        backbuttonsizer.Add(backbutton, 0, wx.ALIGN_LEFT, 0)
        backbuttonsizer.AddSpacer(10)
        backbuttonsizer.Add(clearbutton, 0, wx.EXPAND, 0)

        # Add sizers to midsizer
        midsizer.AddSpacer(20)
        midsizer.Add(gdsizer1, 0, wx.EXPAND | wx.ALL, 5)
        midsizer.AddSpacer(10)
        midsizer.Add(button_step2, 0, wx.ALL, 5)
        midsizer.AddSpacer(30)
        midsizer.Add(gdsizer2, 0, wx.EXPAND | wx.ALL, 5)
        midsizer.AddSpacer(10)
        midsizer.Add(gdsizer3, 0, wx.EXPAND | wx.ALL, 5)
        
        #add buttons into gdsizer3
        gdsizer3.AddMany([
            (self.button_step1),   
            (button_read_objects_metadata),
            (button_step3),
            (button_reset_access),

        ])
        
        #add sizers to gdsizer1
        gdsizer1.AddMany([
                (secretsizer, 0, wx.EXPAND),
                (payloadversizer, 0, wx.EXPAND),
                (payloadtypesizer, 0, wx.EXPAND),
                (signsizer, 0, wx.EXPAND),
                (keydatasizer, 0, wx.EXPAND),
                (privsizer, 0, wx.EXPAND)
                
        ])
        
        gdsizer1.Add(keylengthsizer, 0, wx.EXPAND)
        gdsizer1.Add(keyusagesizer, 0, wx.EXPAND)
        gdsizer1.Add(secret2sizer, 0, wx.EXPAND)
        
        #add sizers to gdsizer2
        gdsizer2.AddMany([
                (trustoidsizer, 0, wx.EXPAND),
                (targetoidsizer, 0, wx.EXPAND),
                (secretoidsizer, 0, wx.EXPAND),
                (trustcertsizer, 0, wx.EXPAND),
        ])
        
        gdsizer2.AddSpacer(20)
        gdsizer2.Add(secret1sizer, 0, wx.EXPAND)
                
        #add objects into sizers in gdsizer1
        secretsizer.Add(text_secret)
        secretsizer.Add(self.secret)
        payloadversizer.Add(text_payload_version)
        payloadversizer.Add(self.payload_version)
        payloadtypesizer.Add(text_payload_type)
        payloadtypesizer.Add(self.payload_type)
        signsizer.Add(text_sign_algo)
        signsizer.Add(self.sign_algo)
        keydatasizer.Add(text_keydata)
        keydatasizer.Add(self.keydata)
        keylengthsizer.Add(text_keylength)
        keylengthsizer.Add(self.keylength)
        privsizer.Add(text_priv_key)
        privsizer.Add(self.priv_key)
        keyusagesizer.Add(text_keyusage)
        keyusagesizer.Add(self.keyusage)
        secret2sizer.Add(text_secret2)
        secret2sizer.Add(self.secret2)

        #add objects into sizers in gdsizer2
        trustoidsizer.Add(text_trust_anchor_oid)
        trustoidsizer.Add(self.trust_anchor_oid)
        targetoidsizer.Add(text_target_oid)
        targetoidsizer.Add(self.target_oid)
        secretoidsizer.Add(text_secret_oid)
        secretoidsizer.Add(self.secret_oid)
        trustcertsizer.Add(text_trust_anchor_cert)
        trustcertsizer.Add(self.trust_anchor_cert)
        secret1sizer.Add(text_secret1)
        secret1sizer.Add(self.secret1)
        
        # Set Default inputs for Text Boxes      
        self.secret.SetSelection(0)
        self.sign_algo.SetSelection(0)
        self.trust_anchor_oid.SetSelection(0)
        self.target_oid.SetSelection(0)
        self.secret_oid.SetSelection(0)
        self.keyusage.SetSelection(0)
        self.keylength.SetSelection(0)


        # attach objects to the sizer
        # declare and bind events
        clearbutton.Bind(wx.EVT_BUTTON, self.OnFlush)
        backbutton.Bind(wx.EVT_BUTTON, self.OnBack)
        button_read_objects_metadata.Bind(wx.EVT_BUTTON, self.OnReadMetadata1)
        button_step2.Bind(wx.EVT_BUTTON, self.OnGenManifest)
        button_step3.Bind(wx.EVT_BUTTON, self.OnProtectedUpdate1)
        button_reset_access.Bind(wx.EVT_BUTTON, self.OnResetAccess1)
        self.button_step1.Bind(wx.EVT_BUTTON, self.OnRunStep1)
        
        self.priv_key.Bind(wx.EVT_LEFT_DOWN,self.OnClickFileName)
        self.trust_anchor_cert.Bind(wx.EVT_LEFT_DOWN,self.OnClickCertName)
        self.secret1.Bind(wx.EVT_LEFT_DOWN,self.OnClickSecret)
        self.secret2.Bind(wx.EVT_LEFT_DOWN,self.OnClickSecret2)
        self.keydata.Bind(wx.EVT_LEFT_DOWN,self.OnClickKeydata)

        self.SetSizer(mainsizer)
        mainsizer.Fit(self)
        
        
        
    def OnClickKeydata(self, evt):
        frame = wx.Frame(None, -1, '*.*')
        frame.SetSize(0,0,200,50)
            
        openFileDialog = wx.FileDialog(frame, "Open", "", "","All|*.crt;*.pem|Certificate|*.crt;*.pem", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST |wx.FD_CHANGE_DIR)
        
        some_dir= config.EXEPATH + "/ex_protected_update_data_set/samples/payload/key/"
        
        openFileDialog.SetDirectory(some_dir)
        openFileDialog.SetFilename("ecc_secp256r1_test.pem")
        
        if openFileDialog.ShowModal() ==wx.ID_CANCEL:
            
                return
        print((openFileDialog.GetPath()))
        #self.keydata.SetValue(openFileDialog.GetPath())
        
        self.keypath = openFileDialog.GetPath()
        
        self.keydata.Clear()
        self.keydata.AppendText(os.path.basename(openFileDialog.GetPath()))
        
        openFileDialog.Destroy()    
        
    def OnKeyUsage(self):
        
        if (self.keyusage.GetSelection() == 0):
            value = "key_usage=11"
            
            return(value)   
        
        elif (self.keyusage.GetSelection() == 1):
            value = "key_usage=10"
        
            return(value)
        
        elif (self.keyusage.GetSelection() == 2):
            value = "key_usage=30"
        
            return(value)
            
    def OnKeyLength(self):
        value = "key_algo=3"
        
        if (self.keylength.GetSelection() == 0):
            value = "key_algo=3"
            return (value)
            
        elif (self.keylength.GetSelection() == 1):
            value = "key_algo=4"
            return (value)
        
        elif (self.keylength.GetSelection() == 2):
            value = "key_algo=5"
            return (value)
        
        elif (self.keylength.GetSelection() == 3):
            value = "key_algo=19"
            return (value)
        
        elif (self.keylength.GetSelection() == 4):
            value = "key_algo=21"
            return (value)
            
        else:
            value = "key_algo=22"
            return (value)
            
        
    def OnClickFileName(self, evt):
        frame = wx.Frame(None, -1, '*.*')
        frame.SetSize(0,0,200,50)
            
        openFileDialog = wx.FileDialog(frame, "Open", "", "","All|*.crt;*.pem|Certificate|*.crt;*.pem", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST |wx.FD_CHANGE_DIR)
        
        some_dir= config.EXEPATH + "/scripts/certificates/"
        
        openFileDialog.SetDirectory(some_dir)
        openFileDialog.SetFilename("sample_ec_256_priv.pem")
        
        if openFileDialog.ShowModal() ==wx.ID_CANCEL:
            
                return
        print((openFileDialog.GetPath()))
        #self.priv_key.SetValue(openFileDialog.GetPath())
        self.priv_keypath = openFileDialog.GetPath()
        
        self.priv_key.Clear()
        self.priv_key.AppendText(os.path.basename(openFileDialog.GetPath()))
        
        openFileDialog.Destroy()    

    def OnClickCertName(self, evt):
        frame = wx.Frame(None, -1, '*.*')
        frame.SetSize(0,0,200,50)
            
        openFileDialog = wx.FileDialog(frame, "Open", "", "","All|*.crt;*.pem|Certificate|*.crt;*.pem", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST |wx.FD_CHANGE_DIR)
        
        some_Dir= config.EXEPATH + "/scripts/certificates/"
        
        openFileDialog.SetDirectory(some_Dir)
        openFileDialog.SetFilename("sample_ec_256_cert.pem")
        
        if openFileDialog.ShowModal() ==wx.ID_CANCEL:
            
                return
        print((openFileDialog.GetPath()))
        #self.trust_anchor_cert.SetValue(openFileDialog.GetPath())
        self.trust_anchor_certpath = openFileDialog.GetPath()
        
        self.trust_anchor_cert.Clear()
        self.trust_anchor_cert.AppendText(os.path.basename(openFileDialog.GetPath()))
        
        openFileDialog.Destroy()

    
    
    def OnClickSecret(self, evt):
        frame = wx.Frame(None, -1, '*.*')
        frame.SetSize(0,0,200,50)
            
        openFileDialog = wx.FileDialog(frame, "Open", "", "","All|*.crt;*.txt|Certificate|*.crt;*.txt", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST )
        
        some_Dir= config.EXEPATH + "/ex_protected_update_data_set/samples/confidentiality/"
        
        openFileDialog.SetDirectory(some_Dir)
        openFileDialog.SetFilename("secret.txt")
        
        if openFileDialog.ShowModal() ==wx.ID_CANCEL:
            
                return
        print((openFileDialog.GetPath()))
        #self.secret1.SetValue(openFileDialog.GetPath())
        self.secret1path = openFileDialog.GetPath()
        
        self.secret1.Clear()
        self.secret1.AppendText(os.path.basename(openFileDialog.GetPath()))
        
        openFileDialog.Destroy()
    
    def OnClickSecret2(self, evt):
        frame = wx.Frame(None, -1, '*.*')
        frame.SetSize(0,0,200,50)
            
        openFileDialog = wx.FileDialog(frame, "Open", "", "","All|*.crt;*.txt|Certificate|*.crt;*.txt", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST )
        
        some_Dir= config.EXEPATH + "/ex_protected_update_data_set/samples/confidentiality/"
        
        openFileDialog.SetDirectory(some_Dir)
        openFileDialog.SetFilename("secret.txt")
        
        if openFileDialog.ShowModal() ==wx.ID_CANCEL:
            
                return
        print((openFileDialog.GetPath()))
        #self.secret2.SetValue(openFileDialog.GetPath())
        self.secret2path = openFileDialog.GetPath()
        
        self.secret2.Clear()
        self.secret2.AppendText(os.path.basename(openFileDialog.GetPath()))
        
        openFileDialog.Destroy()

    def OnRunStep1(self, evt):
        self.OnSetupEccKeyUpdate1()
        

    def OnSetup(self):
        trust_anchor_oid = "0x" + self.trust_anchor_oid.GetValue()
        target_oid = "0x" + self.target_oid.GetValue()
        secret_oid = "0x" + self.secret_oid.GetValue()
        certfile = self.trust_anchor_certpath
        
        TRUST_ANCHOR_META = "2003E80111"
        
        f = open(self.secret1path, 'r')
        file= f.read()
        print(file)
        PROTECTED_UPDATE_SECRET = file
        f.close()
        
        PROTECTED_UPDATE_SECRET_META = "200BD103E1FC07D30100E80123"
     
        #Step1: Provisioning initial Trust Anchor, metadata for Trust Anchor
        self.text_display.AppendText("Provisioning for initial Trust Anchor OID... \n")
        command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_cert", "-w", trust_anchor_oid, "-i", certfile, ])
        self.text_display.AppendText(command_output)
        self.text_display.AppendText("'trustm_cert -w " + trust_anchor_oid + " -i " + certfile + "'" + " executed \n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
        
        self.text_display.AppendText("Provisioning for trust anchor metadata... \n")
        command_output = exec_cmd.createProcess("echo " + TRUST_ANCHOR_META + " | xxd -r -p > trust_anchor_metadata.bin", None)
        self.text_display.AppendText("'echo $TRUST_ANCHOR_META | xxd -r -p > trust_anchor_metadata.bin' executed \n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
        
        self.text_display.AppendText("Writing trust_anchor_metadata.bin as metadata of Trust Anchor OID... \n")
        command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_metadata", "-w", trust_anchor_oid, "-F", "trust_anchor_metadata.bin", ])
        self.text_display.AppendText(command_output)
        self.text_display.AppendText("'trustm_metadata -w " + trust_anchor_oid + " -F trust_anchor_metadata.bin'" + " executed \n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
        
        
        #Step2: Provisioning Protected Update Secret OID, metadata for Protected Update Secret OID
        self.text_display.AppendText("Provisioning for protected update secret... \n")
        command_output = exec_cmd.createProcess("echo " + PROTECTED_UPDATE_SECRET + " | xxd -r -p > protected_update_secret.dat", None)
        self.text_display.AppendText("'$PROTECTED_UPDATE_SECRET xxd -r -p > protected_update_secret.dat' executed \n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")    
        
        self.text_display.AppendText("Writing protected update secret into secret_oid...")
        command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_data", "-e", "-w", secret_oid, "-i", "protected_update_secret.dat", ])
        self.text_display.AppendText(command_output)
        self.text_display.AppendText("'trustm_data -e -w " + secret_oid + " -i protected_update_secret.dat'" + " executed \n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
       
        self.text_display.AppendText("Provisioning for protected update secret metadata... \n")
        command_output = exec_cmd.createProcess("echo " + PROTECTED_UPDATE_SECRET_META + " | xxd -r -p > protected_update_secret_metadata.bin", None)
        self.text_display.AppendText("'$PROTECTED_UPDATE_SECRET_META xxd -r -p > protected_update_secret_metadata.bin' executed \n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
        
        self.text_display.AppendText("Writing protected update secret metadata into secret_oid... ")
        command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_metadata", "-w", secret_oid, "-F", "protected_update_secret_metadata.bin", ])
        self.text_display.AppendText(command_output)
        self.text_display.AppendText("'trustm_metadata -w " + secret_oid + " -F protected_update_secret_metadata.bin' executed \n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")     
        
        
        
    def OnSetupEccKeyUpdate1(self):
        self.text_display.AppendText("Provisioning Data Objects ... \n")
        wx.CallLater(10, self.OnSetupEccKeyUpdate)
        
    def OnSetupEccKeyUpdate(self):
        trust_anchor_oid = "0x" + self.trust_anchor_oid.GetValue()
        target_oid = "0x" + self.target_oid.GetValue()
        secret_oid = "0x" + self.secret_oid.GetValue()
        secret_list_value=self.secret.GetValue()
        if (secret_list_value=="Integrity"):
           TARGET_OID_META="2009C1020000D00321" + self.trust_anchor_oid.GetValue()
        else:
           TARGET_OID_META="200dC1020000D00721" + self.trust_anchor_oid.GetValue() + "FD20" + self.secret_oid.GetValue()
        
        self.OnSetup()
        
        #step 1
        self.text_display.AppendText("Set metadata protected update for Target OID (Provision for Target OID)... \n")
        command_output = exec_cmd.createProcess("echo " + TARGET_OID_META + " | xxd -r -p > targetOID_metadata.bin", None)
        self.text_display.AppendText("'$TARGET_OID_META | xxd -r -p > targetOID_metadata.bin' executed \n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
        self.text_display.AppendText("Writing targetOID_metadata.bin as metadata of Target OID... \n")
        command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_metadata", "-w", target_oid, "-F", "targetOID_metadata.bin", ])
        self.text_display.AppendText(command_output)
        self.text_display.AppendText("'trustm_metadata -w " + target_oid + " -F targetOID_metadata.bin' executed \n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
        command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_metadata", "-r", target_oid,])
        self.text_display.AppendText(command_output)
        self.text_display.AppendText("'trustm_metadata --r " + target_oid + " executed \n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")

        
    def OnReadMetadata1(self, evt):
        self.text_display.AppendText("Reading Objects Metadata... \n")
        wx.CallLater(10, self.OnReadMetadata)
    
    def OnReadMetadata(self):
        trust_anchor_oid = "0x" + self.trust_anchor_oid.GetValue()
        target_oid = "0x" + self.target_oid.GetValue()
        secret_oid = "0x" + self.secret_oid.GetValue()
        
        self.text_display.AppendText("Reading out metadata for trust_anchor_oid... \n")
        command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_metadata", "-r", trust_anchor_oid, ])
        self.text_display.AppendText(command_output)
        self.text_display.AppendText("'trustm_metadata -r " + trust_anchor_oid + "' executed \n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
                
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
        
    def OnGenManifest(self, evt):
        payload_version = "payload_version=" + self.payload_version.GetValue()
        trust_anchor_oid = "trust_anchor_oid=" + self.trust_anchor_oid.GetValue()
        target_oid = "target_oid=" + self.target_oid.GetValue()
        sign_algo = "sign_algo=" + self.sign_algo.GetValue()
        #priv_key = "priv_key=" + self.priv_key.GetValue()
        priv_key = "priv_key=" + self.priv_keypath
        payload_type = "payload_type=" + self.payload_type.GetValue()
        
        key_algo = self.OnKeyLength()
        print(key_algo)
        
        key_usage = self.OnKeyUsage()
        print(key_usage)
        
        #key_data = "key_data=" + self.keydata.GetValue() 
        key_data = "key_data=" + self.keypath
        
        print(key_data) 
        
        content_reset = "content_reset=0"
        label = "label=test"
        seed_length = "seed_length=64"
        enc_algo = "enc_algo=AES-CCM-16-64-128"
        secret_oid = "secret_oid=" + self.secret_oid.GetValue()
        
        secret_list_value=self.secret.GetValue()
        if (secret_list_value=="Integrity"):    
            command_output = exec_cmd.createProcess(config.EXEPATH + "/ex_protected_update_data_set/Linux/bin/trustm_protected_update_set " + payload_version + " "
                                                    + trust_anchor_oid + " " + target_oid + " " + sign_algo + " " + priv_key + " " + payload_type
                                                    + " " + key_algo + " " + key_usage + " " + key_data + " " + label + " " + seed_length + " " + enc_algo + " " + secret_oid 
                                                    + "| grep -A10 'uint8_t manifest_data\|uint8_t fragment_01' | sed '1,2d' | sed '11,12d' | sed '$d' | sed 's/0x//g' | tr -d ',[:space:]'",
                                                    None)
        #if (secret_list_value=="Integrity"):
            
        else:
            secret = "secret=" + self.secret2path
            print(secret)
            command_output = exec_cmd.createProcess(config.EXEPATH + "/ex_protected_update_data_set/Linux/bin/trustm_protected_update_set " + payload_version + " "
                                                    + trust_anchor_oid + " " + target_oid + " " + sign_algo + " " + priv_key + " " + payload_type
                                                    + " " + key_algo + " " + key_usage + " " + key_data + " " + label + " " + seed_length + " " + enc_algo + " " + secret_oid + " " + secret 
                                                    + " | grep -A16 'uint8_t manifest_data\|uint8_t fragment_01' | sed '1,2d' | sed '17,18d' | sed '$d' | sed 's/0x//g' | tr -d ',[:space:]'",
                                                    None)
    
        manifest_and_frag_string = command_output.stdout.read().decode("utf-8")
        manifest_and_frag_string = manifest_and_frag_string.split('--')
        manifest = manifest_and_frag_string[0]
        fragment = manifest_and_frag_string[1]

        self.text_display.AppendText("manifest: " + manifest)
        self.text_display.AppendText("\n\nfragment: " + fragment)
        
        exec_cmd.createProcess("echo " + manifest + " | xxd -r -p > manifest.dat", None)
        exec_cmd.createProcess("echo " + fragment + " | xxd -r -p > fragment.dat", None)
        self.text_display.AppendText("\n\nmanifest.dat and fragment.dat generated\n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
    
    def OnProtectedUpdate1(self, evt):
        self.text_display.AppendText("ECC Key protected update for Target OID... \n")
        wx.CallLater(10, self.OnProtectedUpdate)
    
    def OnProtectedUpdate(self):
        target_oid = "0x" + self.target_oid.GetValue()
        command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_protected_update_ecckey", "-k", target_oid, "-f", "fragment.dat", "-m", "manifest.dat",  ])
        self.text_display.AppendText(command_output)
        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
     
    
    def OnResetAccess1(self, evt):
        self.text_display.AppendText("Resetting Access Condition tag for Target OID... \n")
        wx.CallLater(10, self.OnResetAccess)
    
    def OnResetAccess(self):
        RESET_ACCESS_META="2005D003E1FC07"
        target_oid = "0x" + self.target_oid.GetValue()
        exec_cmd.createProcess("echo " + RESET_ACCESS_META + " | xxd -r -p > access_reset.bin", None)
        command_output = exec_cmd.execCLI(["xxd", "access_reset.bin", ])
        self.text_display.AppendText(command_output)
        self.text_display.AppendText("access_reset.bin generated\n")
        self.text_display.AppendText("Writing metadata for Target OID... \n")
        exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_metadata", "-w", target_oid, "-F", "access_reset.bin", ])
        self.text_display.AppendText("'trustm_metadata -w " + target_oid + " -F access_reset.bin' executed \n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
    
    
    def OnFlush(self, evt):
        self.text_display.Clear()

    # Calling parent of the parent, as direct parent is the notebook,
    # then the second parent is the frame, from which we call the destruction
    def OnBack(self, evt):
        self.Parent.Parent.OnCloseWindow(None)

class Tab_AesConfidentialUpdate(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        
        title = wx.StaticText(self, -1, style=wx.ALIGN_CENTER, label="AES Key Integrity Confidential Protected Update")
        font = wx.Font(20, wx.ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        title.SetFont(font)
        
        textctrlfont = wx.Font()
        textctrlfont.SetPointSize(10)
        
        textctrlfont1 = wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD,)
        
        buttonfont = wx.Font(12, wx.ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        
        # declare the sizers
        mainsizer = wx.BoxSizer(wx.VERTICAL)
        mainhorisizer = wx.BoxSizer(wx.HORIZONTAL)
        
        midsizer = wx.BoxSizer(wx.VERTICAL)
        gdsizer1 = wx.GridSizer(rows=3, cols=3, vgap=10, hgap=5)
        gdsizer2 = wx.GridSizer(rows=2, cols=3, vgap=10, hgap=10)
        gdsizer3 = wx.GridSizer(rows=2, cols=2, vgap=20, hgap=10)
        step1_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        titlesizer = wx.BoxSizer(wx.HORIZONTAL)
        
        leftsizer = wx.BoxSizer(wx.VERTICAL)
        picturesizer = wx.BoxSizer(wx.VERTICAL)
        backbuttonsizer = wx.BoxSizer(wx.HORIZONTAL)
        
        # declare sizers that will be in the grid1
        labelsizer = wx.BoxSizer(wx.VERTICAL)
        secretsizer = wx.BoxSizer(wx.VERTICAL)
        encsizer = wx.BoxSizer(wx.VERTICAL)
        payloadversizer = wx.BoxSizer(wx.VERTICAL)
        payloadtypesizer = wx.BoxSizer(wx.VERTICAL)
        signsizer = wx.BoxSizer(wx.VERTICAL)
        keydatasizer = wx.BoxSizer(wx.VERTICAL)
        keylengthsizer = wx.BoxSizer(wx.VERTICAL)
        contentsizer = wx.BoxSizer(wx.VERTICAL)
        privsizer = wx.BoxSizer(wx.VERTICAL)
        
        # declare sizers that will be in the grid2
        trustoidsizer = wx.BoxSizer(wx.VERTICAL)
        targetoidsizer = wx.BoxSizer(wx.VERTICAL)
        secretoidsizer = wx.BoxSizer(wx.VERTICAL)
        trustcertsizer = wx.BoxSizer(wx.VERTICAL)
        secret1sizer = wx.BoxSizer(wx.VERTICAL)
        keyusagesizer = wx.BoxSizer(wx.VERTICAL)
        secret2sizer = wx.BoxSizer(wx.VERTICAL)
        
        keyusage = ['Auth','Enc','Sign','Auth/Enc/Sign','Key Agree']
        confidential_list = ['Integrity Confidential']
        keylength = ['AES 128', 'AES 192', 'AES 256']
        
        # instantiate the objects
        self.secret2path = config.EXEPATH + "/ex_protected_update_data_set/samples/confidentiality/secret.txt"
        text_secret2 = wx.StaticText(self, 0, "secret:")
        self.secret2 = wx.TextCtrl(self, 1, value= "secret.txt", style=wx.CB_READONLY,  size = wx.Size(178, -1))
        self.secret2.SetFont(textctrlfont)
        text_keyusage = wx.StaticText(self, 0, "Key_usage:")
        self.keyusage = wx.ComboBox(self, 1, choices=keyusage, style=wx.CB_READONLY,  size = wx.Size(178, -1))
        self.keyusage.SetFont(textctrlfont)
        text_keylength = wx.StaticText(self, 0, "Key_length")
        self.keylength = wx.ComboBox(self, 1, choices=keylength, style=wx.CB_READONLY, size=wx.Size(178, -1))
        self.keylength.SetFont(textctrlfont)
        text_secret = wx.StaticText(self, 0, "Protected_Update:")
        self.secret = wx.ComboBox(self, 1, choices=confidential_list, style=wx.CB_READONLY,  size = wx.Size(178, -1))
        self.secret.SetFont(textctrlfont)
        text_payload_version = wx.StaticText(self, 0, "payload_version:")
        self.payload_version = wx.TextCtrl(self, 1, value="1",  size = wx.Size(178, -1))
        self.payload_version.SetFont(textctrlfont)
        text_payload_type = wx.StaticText(self, 0, "payload_type:")
        self.payload_type = wx.TextCtrl(self, 1, value="key",  size = wx.Size(178, -1))
        self.payload_type.SetFont(textctrlfont)
        text_sign_algo = wx.StaticText(self, 0, "sign_algo:")
        self.sign_algo = wx.ComboBox(self, 1, choices=sign_algo_list, style=wx.CB_READONLY,  size = wx.Size(178, -1))
        self.sign_algo.SetFont(textctrlfont)
        
        self.keypath = config.EXEPATH + "/ex_protected_update_data_set/samples/payload/key/aes_key_128.txt"
        text_keydata = wx.StaticText(self, 0, "key_data:")
        self.keydata = wx.TextCtrl(self, 1, value= "aes_key_128.txt", style=wx.CB_READONLY,  size = wx.Size(178, -1))
        self.keydata.SetFont(textctrlfont)
        
        self.priv_keypath = config.EXEPATH + "/scripts/certificates/sample_ec_256_priv.pem"
        text_priv_key = wx.StaticText(self, 0, "trust_anchor_privkey:")
        text_priv_key.SetFont(textctrlfont1)
        self.priv_key = wx.TextCtrl(self, -1, value= "sample_ec_256_priv.pem", style=wx.CB_READONLY , size=(178, 30))
        self.priv_key.SetFont(textctrlfont)
        text_trust_anchor_oid = wx.StaticText(self, -1, "trust_anchor_oid:")
        self.trust_anchor_oid = wx.ComboBox(self, 1, choices=key_trust_anchor_oid_list, style=wx.CB_READONLY, size = wx.Size(178, -1))
        self.trust_anchor_oid.SetFont(textctrlfont)
        text_target_oid = wx.StaticText(self, -1, "target_oid_AES:")
        self.target_oid = wx.ComboBox(self, 1, choices =aes_target_oid_list, style=wx.CB_READONLY,  size = wx.Size(178, -1))
        self.target_oid.SetFont(textctrlfont)
        text_secret_oid = wx.StaticText(self, -1, "secret_oid:")
        self.secret_oid = wx.ComboBox(self, 1, choices=key_secret_oid_list, style=wx.CB_READONLY,  size = wx.Size(178, -1))
        self.secret_oid.SetFont(textctrlfont)
        
        self.secret1path = config.EXEPATH + "/ex_protected_update_data_set/samples/confidentiality/secret.txt"
        text_secret1 = wx.StaticText(self, 0, "secret:")
        self.secret1 = wx.TextCtrl(self, 1, value= "secret.txt", style=wx.CB_READONLY,  size = wx.Size(178, -1))
        self.secret1.SetFont(textctrlfont)
        
        self.trust_anchor_certpath= config.EXEPATH + "/scripts/certificates/sample_ec_256_cert.pem"
        text_trust_anchor_cert = wx.StaticText(self, -1, "trust_anchor_cert:")
        self.trust_anchor_cert = wx.TextCtrl(self, 1, "sample_ec_256_cert.pem",style=wx.CB_READONLY, size = wx.Size(178, 30))
        self.trust_anchor_cert.SetFont(textctrlfont)
        button_step2 = wx.Button(self, 1, 'Step2: Generate Manifest', size = wx.Size(270, -1))
        button_step2.SetFont(buttonfont)
        button_step3 = wx.Button(self, 1, 'Step3: Update Trust M Objects', size = wx.Size(270, -1))
        button_step3.SetFont(buttonfont)
        button_read_objects_metadata = wx.Button(self, 1, 'Read Objects Metadata', size = wx.Size(270, -1))
        button_read_objects_metadata.SetFont(buttonfont)
        button_reset_access = wx.Button(self, 1, 'Reset Access Condition', size = wx.Size(270, -1))
        button_reset_access.SetFont(buttonfont)


        self.button_step1 = wx.Button(self, -1, 'Step1:Provision for all OIDs', size = wx.Size(270, -1))
        self.button_step1.SetFont(buttonfont)
        
        self.text_display = wx.TextCtrl(self, -1, style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.text_display.SetFont(wx.Font(11, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))

        serverimage = wx.Image(config.IMAGEPATH + "/images/server.png", wx.BITMAP_TYPE_PNG).Scale(110,110,wx.IMAGE_QUALITY_HIGH).ConvertToBitmap()
        serverimage = wx.StaticBitmap(self, -1, serverimage)

        clearimage = wx.Image(config.IMAGEPATH + "/images/clear.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        clearbutton = wx.BitmapButton(self, -1, clearimage)
        
        lockedarrow = wx.Image(config.IMAGEPATH + "/images/LockedArrow.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        lockedarrowimage = wx.StaticBitmap(self, -1,lockedarrow)

        chipimage = wx.Image(config.IMAGEPATH + "/images/chipp3.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        chipimage = wx.StaticBitmap(self, -1,chipimage)
        
        backimage = wx.Image(config.IMAGEPATH + "/images/back.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        backbutton = wx.BitmapButton(self, -1, backimage)
       
        #Add mainhorisizer and title to mainsizer
        mainsizer.Add(title, 0, wx.CENTRE | wx.ALL, 5)
        mainsizer.Add(mainhorisizer, 1, wx.EXPAND)
       
        # Add Sub Sizers to the mainhorisizer
        mainhorisizer.Add(leftsizer, 0, wx.EXPAND)
        mainhorisizer.Add(midsizer, 1, wx.EXPAND)
        mainhorisizer.Add(self.text_display, 1, wx.EXPAND | wx.ALL, 5)
        
        # Add Objects to leftsizer
        leftsizer.Add(picturesizer, 0, wx.TOP, 65)
        leftsizer.AddSpacer(110)
        leftsizer.Add(backbuttonsizer, 0, wx.LEFT | wx.BOTTOM, 10)
        picturesizer.Add(serverimage, 0 , wx.ALIGN_CENTER, 0 )
        picturesizer.AddSpacer(30)
        picturesizer.Add(lockedarrowimage, 0, wx.ALIGN_CENTER, 0)
        picturesizer.AddSpacer(20)
        picturesizer.Add(chipimage, 0, wx.ALIGN_CENTER, 0)
        backbuttonsizer.Add(backbutton, 0, wx.ALIGN_LEFT, 0)
        backbuttonsizer.AddSpacer(10)
        backbuttonsizer.Add(clearbutton, 0, wx.EXPAND, 0)

        # Add sizers to midsizer
        midsizer.AddSpacer(20)
        midsizer.Add(gdsizer1, 0, wx.EXPAND | wx.ALL, 5)
        midsizer.AddSpacer(10)
        midsizer.Add(button_step2, 0, wx.ALL, 5)
        midsizer.AddSpacer(30)
        midsizer.Add(gdsizer2, 0, wx.EXPAND | wx.ALL, 5)
        midsizer.AddSpacer(10)
        midsizer.Add(gdsizer3, 0, wx.EXPAND | wx.ALL, 5)
        
        
        #add buttons into gdsizer3
        gdsizer3.AddMany([
            (self.button_step1),   
            (button_read_objects_metadata),
            (button_step3),
            (button_reset_access),

        ])
        
        #add sizers to gdsizer1
        gdsizer1.AddMany([
                (secretsizer, 0, wx.EXPAND),
                (payloadversizer, 0, wx.EXPAND),
                (payloadtypesizer, 0, wx.EXPAND),
                (signsizer, 0, wx.EXPAND),
                (keydatasizer, 0, wx.EXPAND),
                (privsizer, 0, wx.EXPAND)
        ])
        
        gdsizer1.Add(keylengthsizer)
        gdsizer1.Add(keyusagesizer, 0, wx.EXPAND)
        gdsizer1.Add(secret2sizer, 0, wx.EXPAND)
        
        #add sizers to gdsizer2
        gdsizer2.AddMany([
                (trustoidsizer, 0, wx.EXPAND),
                (targetoidsizer, 0, wx.EXPAND),
                (secretoidsizer, 0, wx.EXPAND),
                (trustcertsizer, 0, wx.EXPAND),
        ])
        
        gdsizer2.AddSpacer(20)
        gdsizer2.Add(secret1sizer, 0, wx.EXPAND)
                
        #add objects into sizers in gdsizer1
        secretsizer.Add(text_secret)
        secretsizer.Add(self.secret)
        payloadversizer.Add(text_payload_version)
        payloadversizer.Add(self.payload_version)
        payloadtypesizer.Add(text_payload_type)
        payloadtypesizer.Add(self.payload_type)
        signsizer.Add(text_sign_algo)
        signsizer.Add(self.sign_algo)
        keydatasizer.Add(text_keydata)
        keydatasizer.Add(self.keydata)
        privsizer.Add(text_priv_key)
        privsizer.Add(self.priv_key)
        secret2sizer.Add(text_secret2)
        secret2sizer.Add(self.secret2)
        keyusagesizer.Add(text_keyusage)
        keyusagesizer.Add(self.keyusage)
        keylengthsizer.Add(text_keylength)
        keylengthsizer.Add(self.keylength)
        
        #add objects into sizers in gdsizer2
        trustoidsizer.Add(text_trust_anchor_oid)
        trustoidsizer.Add(self.trust_anchor_oid)
        targetoidsizer.Add(text_target_oid)
        targetoidsizer.Add(self.target_oid)
        secretoidsizer.Add(text_secret_oid)
        secretoidsizer.Add(self.secret_oid)
        trustcertsizer.Add(text_trust_anchor_cert)
        trustcertsizer.Add(self.trust_anchor_cert)
        secret1sizer.Add(text_secret1)
        secret1sizer.Add(self.secret1)
        
        # Set Default inputs for Text Boxes      
        self.secret.SetSelection(0)
        self.sign_algo.SetSelection(0)
        #self.keydata.SetSelection(0)
        self.trust_anchor_oid.SetSelection(0)
        self.target_oid.SetSelection(0)
        self.secret_oid.SetSelection(0)
        self.keyusage.SetSelection(3)
        self.keylength.SetSelection(0)

        # attach objects to the sizer
        # declare and bind events
        clearbutton.Bind(wx.EVT_BUTTON, self.OnFlush)
        backbutton.Bind(wx.EVT_BUTTON, self.OnBack)
        button_read_objects_metadata.Bind(wx.EVT_BUTTON, self.OnReadMetadata1)
        button_step2.Bind(wx.EVT_BUTTON, self.OnGenManifest)
        button_step3.Bind(wx.EVT_BUTTON, self.OnProtectedUpdate1)
        button_reset_access.Bind(wx.EVT_BUTTON, self.OnResetAccess1)
        self.button_step1.Bind(wx.EVT_BUTTON, self.OnRunStep1)
        
        self.secret2.Bind(wx.EVT_LEFT_DOWN, self.OnClickSecret2)
        self.secret1.Bind(wx.EVT_LEFT_DOWN, self.OnClickSecret)
        self.priv_key.Bind(wx.EVT_LEFT_DOWN,self.OnClickFileName)
        self.trust_anchor_cert.Bind(wx.EVT_LEFT_DOWN,self.OnClickCertName)
        self.keydata.Bind(wx.EVT_LEFT_DOWN,self.OnClickKeydata)
        

        self.SetSizer(mainsizer)
        mainsizer.Fit(self)
        
    def OnClickKeydata(self, evt):
        frame = wx.Frame(None, -1, '*.*')
        frame.SetSize(0,0,200,50)
            
        openFileDialog = wx.FileDialog(frame, "Open", "", "","All|*.txt;*.pem|key|*.txt;*.pem", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST |wx.FD_CHANGE_DIR)
        
        some_dir= config.EXEPATH + "/ex_protected_update_data_set/samples/payload/key/"
        
        openFileDialog.SetDirectory(some_dir)
        openFileDialog.SetFilename("aes_key_128.txt")
        
        if openFileDialog.ShowModal() ==wx.ID_CANCEL:
            
                return
        print((openFileDialog.GetPath()))
        #self.keydata.SetValue(openFileDialog.GetPath())
        self.keypath = openFileDialog.GetPath()
        
        self.keydata.Clear()
        self.keydata.AppendText(os.path.basename(openFileDialog.GetPath()))
        
        openFileDialog.Destroy()    
        
    def OnKeyUsage(self):
        
        if (self.keyusage.GetSelection() == 0):
            value = "key_usage=01"
            
            return(value)
        
        elif (self.keyusage.GetSelection() == 1):
            value = "key_usage=02"
         
            return(value)
        
        elif (self.keyusage.GetSelection() == 2):
            value = "key_usage=10"
        
            return(value)
        
        elif (self.keyusage.GetSelection() == 3):
            value = "key_usage=13"
        
            return(value)
        
        elif (self.keyusage.GetSelection() == 4):
            value = "key_usage=20"
        
            return(value)
                
    def OnKeyLength(self):
        value = "key_algo=129"
        if (self.keylength.GetSelection() == 0):
            value = "key_algo=129"
            return (value)
        
        elif (self.keylength.GetSelection() == 1):
            value = "key_algo=130"
            return (value)
                
        elif (self.keylength.GetSelection() == 2):
            value = "key_algo=131"
            return (value)
        
        return (value)
        
    def OnClickFileName(self, evt):
        frame = wx.Frame(None, -1, '*.*')
        frame.SetSize(0,0,200,50)
            
        openFileDialog = wx.FileDialog(frame, "Open", "", "","All|*.crt;*.pem|Certificate|*.crt;*.pem", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST |wx.FD_CHANGE_DIR)
        
        some_dir= config.EXEPATH + "/scripts/certificates/"
        
        openFileDialog.SetDirectory(some_dir)
        openFileDialog.SetFilename("sample_ec_256_priv.pem")
        
        if openFileDialog.ShowModal() ==wx.ID_CANCEL:
            
                return
        print((openFileDialog.GetPath()))
        #self.priv_key.SetValue(openFileDialog.GetPath())
        self.priv_keypath = openFileDialog.GetPath()
        
        self.priv_key.Clear()
        self.priv_key.AppendText(os.path.basename(openFileDialog.GetPath()))
        
        openFileDialog.Destroy()    

    def OnClickCertName(self, evt):
        frame = wx.Frame(None, -1, '*.*')
        frame.SetSize(0,0,200,50)
            
        openFileDialog = wx.FileDialog(frame, "Open", "", "","All|*.crt;*.pem|Certificate|*.crt;*.pem", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST |wx.FD_CHANGE_DIR)
        
        some_Dir= config.EXEPATH + "/scripts/certificates/"
        
        openFileDialog.SetDirectory(some_Dir)
        openFileDialog.SetFilename("sample_ec_256_cert.pem")
        
        if openFileDialog.ShowModal() ==wx.ID_CANCEL:
            
                return
        print((openFileDialog.GetPath()))
        #self.trust_anchor_cert.SetValue(openFileDialog.GetPath())
        self.trust_anchor_certpath = openFileDialog.GetPath()
        
        self.trust_anchor_cert.Clear()
        self.trust_anchor_cert.AppendText(os.path.basename(openFileDialog.GetPath()))
        
        openFileDialog.Destroy()


    def OnClickSecret(self, evt):
        frame = wx.Frame(None, -1, '*.*')
        frame.SetSize(0,0,200,50)
            
        openFileDialog = wx.FileDialog(frame, "Open", "", "","All|*.crt;*.txt|Certificate|*.crt;*.txt", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST |wx.FD_CHANGE_DIR)
        
        some_Dir= config.EXEPATH + "/ex_protected_update_data_set/samples/confidentiality/"
        
        openFileDialog.SetDirectory(some_Dir)
        openFileDialog.SetFilename("secret.txt")
        
        
        if openFileDialog.ShowModal() ==wx.ID_CANCEL:
            
                return
        print((openFileDialog.GetPath()))
        #self.secret1.SetValue(openFileDialog.GetPath())
        self.secret1path = openFileDialog.GetPath()
        
        self.secret1.Clear()
        self.secret1.AppendText(os.path.basename(openFileDialog.GetPath()))
        
        openFileDialog.Destroy()

   
    def OnClickSecret2(self, evt):
        frame = wx.Frame(None, -1, '*.*')
        frame.SetSize(0,0,200,50)
            
        openFileDialog = wx.FileDialog(frame, "Open", "", "","All|*.crt;*.txt|Certificate|*.crt;*.txt", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST |wx.FD_CHANGE_DIR)
        
        some_Dir= config.EXEPATH + "/ex_protected_update_data_set/samples/confidentiality/"
        
        openFileDialog.SetDirectory(some_Dir)
        openFileDialog.SetFilename("secret.txt")
        
        if openFileDialog.ShowModal() ==wx.ID_CANCEL:
            
                return
        print((openFileDialog.GetPath()))
        #self.secret2.SetValue(openFileDialog.GetPath())
        self.secret2path = openFileDialog.GetPath()
        
        self.secret2.Clear()
        self.secret2.AppendText(os.path.basename(openFileDialog.GetPath()))
        
        openFileDialog.Destroy()


    def OnRunStep1(self, evt):
        self.OnSetupAesKeyUpdate1()
        

    def OnSetup(self):
        trust_anchor_oid = "0x" + self.trust_anchor_oid.GetValue()
        target_oid = "0x" + self.target_oid.GetValue()
        secret_oid = "0x" + self.secret_oid.GetValue()
        certfile = self.trust_anchor_certpath
        
        TRUST_ANCHOR_META = "2003E80111"
        
        f = open(self.secret1path, 'r')
        file= f.read()
        print(file)
        PROTECTED_UPDATE_SECRET = file
        f.close()
        
        PROTECTED_UPDATE_SECRET_META = "200BD103E1FC07D30100E80123"
     
        #Step1: Provisioning initial Trust Anchor, metadata for Trust Anchor
        self.text_display.AppendText("Provisioning for initial Trust Anchor OID... \n")
        command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_cert", "-w", trust_anchor_oid, "-i", certfile, ])
        self.text_display.AppendText(command_output)
        self.text_display.AppendText("'trustm_cert -w " + trust_anchor_oid + " -i " + certfile + "'" + " executed \n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
        
        self.text_display.AppendText("Provisioning for trust anchor metadata... \n")
        command_output = exec_cmd.createProcess("echo " + TRUST_ANCHOR_META + " | xxd -r -p > trust_anchor_metadata.bin", None)
        self.text_display.AppendText("'echo $TRUST_ANCHOR_META | xxd -r -p > trust_anchor_metadata.bin' executed \n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
        
        self.text_display.AppendText("Writing trust_anchor_metadata.bin as metadata of Trust Anchor OID... \n")
        command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_metadata", "-w", trust_anchor_oid, "-F", "trust_anchor_metadata.bin", ])
        self.text_display.AppendText(command_output)
        self.text_display.AppendText("'trustm_metadata -w " + trust_anchor_oid + " -F trust_anchor_metadata.bin'" + " executed \n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
        
        
        #Step2: Provisioning Protected Update Secret OID, metadata for Protected Update Secret OID
        self.text_display.AppendText("Provisioning for protected update secret... \n")
        command_output = exec_cmd.createProcess("echo " + PROTECTED_UPDATE_SECRET + " | xxd -r -p > protected_update_secret.dat", None)
        self.text_display.AppendText("'$PROTECTED_UPDATE_SECRET xxd -r -p > protected_update_secret.dat' executed \n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")    
        
        self.text_display.AppendText("Writing protected update secret into secret_oid...")
        command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_data", "-e", "-w", secret_oid, "-i", "protected_update_secret.dat", ])
        self.text_display.AppendText(command_output)
        self.text_display.AppendText("'trustm_data -e -w " + secret_oid + " -i protected_update_secret.dat'" + " executed \n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
       
        self.text_display.AppendText("Provisioning for protected update secret metadata... \n")
        command_output = exec_cmd.createProcess("echo " + PROTECTED_UPDATE_SECRET_META + " | xxd -r -p > protected_update_secret_metadata.bin", None)
        self.text_display.AppendText("'$PROTECTED_UPDATE_SECRET_META xxd -r -p > protected_update_secret_metadata.bin' executed \n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
        
        self.text_display.AppendText("Writing protected update secret metadata into secret_oid... ")
        command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_metadata", "-w", secret_oid, "-F", "protected_update_secret_metadata.bin", ])
        self.text_display.AppendText(command_output)
        self.text_display.AppendText("'trustm_metadata -w " + secret_oid + " -F protected_update_secret_metadata.bin' executed \n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")       
 
        
    def OnSetupAesKeyUpdate1(self):
        self.text_display.AppendText("Provisioning Data Objects ... \n")
        wx.CallLater(10, self.OnSetupAesKeyUpdate)
        
    def OnSetupAesKeyUpdate(self):
        trust_anchor_oid = "0x" + self.trust_anchor_oid.GetValue()
        target_oid = "0x" + self.target_oid.GetValue()
        secret_oid = "0x" + self.secret_oid.GetValue()
        secret_list_value=self.secret.GetValue()
        #if (self.secret.GetSelection() == 1):
        if (secret_list_value=="Integrity"):
            TARGET_OID_META="2009C1020000D00321" + self.trust_anchor_oid.GetValue()
        else:
            TARGET_OID_META="200dC1020000D00721" + self.trust_anchor_oid.GetValue() + "FD20" + self.secret_oid.GetValue()
        
        self.OnSetup()
        
        #step 1
        self.text_display.AppendText("Set metadata protected update for Target OID (Provision for Target OID)... \n")
        command_output = exec_cmd.createProcess("echo " + TARGET_OID_META + " | xxd -r -p > targetOID_metadata.bin", None)
        self.text_display.AppendText("'$TARGET_OID_META | xxd -r -p > targetOID_metadata.bin' executed \n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
        self.text_display.AppendText("Writing targetOID_metadata.bin as metadata of Target OID... \n")
        command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_metadata", "-w", target_oid, "-F", "targetOID_metadata.bin", ])
        self.text_display.AppendText(command_output)
        self.text_display.AppendText("'trustm_metadata -w " + target_oid + " -F targetOID_metadata.bin' executed \n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
        command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_metadata", "-r", target_oid,])
        self.text_display.AppendText(command_output)
        self.text_display.AppendText("'trustm_metadata --r " + target_oid + " executed \n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
        
    def OnReadMetadata1(self, evt):
        self.text_display.AppendText("Reading Objects Metadata... \n")
        wx.CallLater(10, self.OnReadMetadata)
    
    def OnReadMetadata(self):
        trust_anchor_oid = "0x" + self.trust_anchor_oid.GetValue()
        target_oid = "0x" + self.target_oid.GetValue()
        secret_oid = "0x" + self.secret_oid.GetValue()
        
        self.text_display.AppendText("Reading out metadata for trust_anchor_oid... \n")
        command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_metadata", "-r", trust_anchor_oid, ])
        self.text_display.AppendText(command_output)
        self.text_display.AppendText("'trustm_metadata -r " + trust_anchor_oid + "' executed \n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
                
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
        
    def OnGenManifest(self, evt):
        payload_version = "payload_version=" + self.payload_version.GetValue()
        trust_anchor_oid = "trust_anchor_oid=" + self.trust_anchor_oid.GetValue()
        target_oid = "target_oid=" + self.target_oid.GetValue()
        sign_algo = "sign_algo=" + self.sign_algo.GetValue()
        priv_key = "priv_key=" + self.priv_keypath
        payload_type = "payload_type=" + self.payload_type.GetValue()
        
        
        key_algo = self.OnKeyLength()
        print(key_algo)
        
        key_usage = self.OnKeyUsage()
        print(key_usage)
       
        key_data = "key_data=" + self.keypath
        content_reset = "content_reset=0"
        label = "label=test"
        seed_length = "seed_length=64"
        enc_algo = "enc_algo=AES-CCM-16-64-128"
        secret_oid = "secret_oid=" + self.secret_oid.GetValue()
        
        secret_list_value=self.secret.GetValue()
        if (secret_list_value=="Integrity"):    
            command_output = exec_cmd.createProcess(config.EXEPATH + "/ex_protected_update_data_set/Linux/bin/trustm_protected_update_set " + payload_version + " "
                                                    + trust_anchor_oid + " " + target_oid + " " + sign_algo + " " + priv_key + " " + payload_type
                                                    + " " + key_algo + " " + key_usage + " " + key_data + " " + label + " " + seed_length + " " + enc_algo + " " + secret_oid 
                                                    + "| grep -A10 'uint8_t manifest_data\|uint8_t fragment_01' | sed '1,2d' | sed '11,12d' | sed '$d' | sed 's/0x//g' | tr -d ',[:space:]'",
                                                    None)
        else:
            secret = "secret=" + self.secret2path
            print(secret)
            command_output = exec_cmd.createProcess(config.EXEPATH + "/ex_protected_update_data_set/Linux/bin/trustm_protected_update_set " + payload_version + " "
                                                    + trust_anchor_oid + " " + target_oid + " " + sign_algo + " " + priv_key + " " + payload_type
                                                    + " " + key_algo + " " + key_usage + " " + key_data + " " + label + " " + seed_length + " " + enc_algo + " " + secret_oid + " " + secret 
                                                    + " | grep -A16 'uint8_t manifest_data\|uint8_t fragment_01' | sed '1,2d' | sed '17,18d' | sed '$d' | sed 's/0x//g' | tr -d ',[:space:]'",
                                                    None)
    
        manifest_and_frag_string = command_output.stdout.read().decode("utf-8")
        manifest_and_frag_string = manifest_and_frag_string.split('--')
        manifest = manifest_and_frag_string[0]
        fragment = manifest_and_frag_string[1]

        self.text_display.AppendText("manifest: " + manifest)
        self.text_display.AppendText("\n\nfragment: " + fragment)
        
        exec_cmd.createProcess("echo " + manifest + " | xxd -r -p > manifest.dat", None)
        exec_cmd.createProcess("echo " + fragment + " | xxd -r -p > fragment.dat", None)
        self.text_display.AppendText("\n\nmanifest.dat and fragment.dat generated\n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
    
    def OnProtectedUpdate1(self, evt):
        self.text_display.AppendText("AES Key protected update for Target OID... \n")
        wx.CallLater(10, self.OnProtectedUpdate)
    
    def OnProtectedUpdate(self):
        target_oid = "0x" + self.target_oid.GetValue()
        command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_protected_update_aeskey", "-k", target_oid, "-f", "fragment.dat", "-m", "manifest.dat",  ])
        self.text_display.AppendText(command_output)
        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
       
    def OnResetAccess1(self, evt):
        self.text_display.AppendText("Resetting Access Condition tag for Target OID... \n")
        wx.CallLater(10, self.OnResetAccess)
    
    def OnResetAccess(self):
        RESET_ACCESS_META="2005D003E1FC07"
        target_oid = "0x" + self.target_oid.GetValue()
        exec_cmd.createProcess("echo " + RESET_ACCESS_META + " | xxd -r -p > access_reset.bin", None)
        command_output = exec_cmd.execCLI(["xxd", "access_reset.bin", ])
        self.text_display.AppendText(command_output)
        self.text_display.AppendText("access_reset.bin generated\n")
        self.text_display.AppendText("Writing metadata for Target OID... \n")
        exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_metadata", "-w", target_oid, "-F", "access_reset.bin", ])
        self.text_display.AppendText("'trustm_metadata -w " + target_oid + " -F access_reset.bin' executed \n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")   
       
    
    def OnFlush(self, evt):
        self.text_display.Clear()

    # Calling parent of the parent, as direct parent is the notebook,
    # then the second parent is the frame, from which we call the destruction
    def OnBack(self, evt):
        self.Parent.Parent.OnCloseWindow(None)


class Tab_RsaConfidentialUpdate(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        
        title = wx.StaticText(self, -1, style=wx.ALIGN_CENTER, label="RSA Key Integrity Confidential Protected Update")
        font = wx.Font(20, wx.ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        title.SetFont(font)
        
        textctrlfont = wx.Font()
        textctrlfont.SetPointSize(10)
        
        textctrlfont1 = wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD,)
        
        buttonfont = wx.Font(12, wx.ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        
        # declare the sizers
        mainsizer = wx.BoxSizer(wx.VERTICAL)
        mainhorisizer = wx.BoxSizer(wx.HORIZONTAL)
        
        midsizer = wx.BoxSizer(wx.VERTICAL)
        gdsizer1 = wx.GridSizer(rows=3, cols=3, vgap=10, hgap= 5)
        gdsizer2 = wx.GridSizer(rows=2, cols=3, vgap=10, hgap=10)
        gdsizer3 = wx.GridSizer(rows=2, cols=2, vgap=20, hgap=10)
        step1_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        titlesizer = wx.BoxSizer(wx.HORIZONTAL)
        
        leftsizer = wx.BoxSizer(wx.VERTICAL)
        picturesizer = wx.BoxSizer(wx.VERTICAL)
        backbuttonsizer = wx.BoxSizer(wx.HORIZONTAL)
        
        # declare sizers that will be in the grid1
        labelsizer = wx.BoxSizer(wx.VERTICAL)
        secretsizer = wx.BoxSizer(wx.VERTICAL)
        encsizer = wx.BoxSizer(wx.VERTICAL)
        payloadversizer = wx.BoxSizer(wx.VERTICAL)
        payloadtypesizer = wx.BoxSizer(wx.VERTICAL)
        signsizer = wx.BoxSizer(wx.VERTICAL)
        keydatasizer = wx.BoxSizer(wx.VERTICAL)
        keylengthsizer = wx.BoxSizer(wx.VERTICAL)
        contentsizer = wx.BoxSizer(wx.VERTICAL)
        privsizer = wx.BoxSizer(wx.VERTICAL)
        
        # declare sizers that will be in the grid2
        trustoidsizer = wx.BoxSizer(wx.VERTICAL)
        targetoidsizer = wx.BoxSizer(wx.VERTICAL)
        secretoidsizer = wx.BoxSizer(wx.VERTICAL)
        trustcertsizer = wx.BoxSizer(wx.VERTICAL)
        secret1sizer = wx.BoxSizer(wx.VERTICAL)
        keyusagesizer = wx.BoxSizer(wx.VERTICAL)
        secret2sizer = wx.BoxSizer(wx.VERTICAL)
        
        keyusage = ['Auth','Enc','Sign','Auth/Enc/Sign','Key Agree']
        confidential_list = ['Integrity Confidential']
        keylength = ['RSA 1024', 'RSA 2048']
        
        # instantiate the objects
        text_keyusage = wx.StaticText(self, 0, "Key_usage:")
        self.keyusage = wx.ComboBox(self, 1, choices=keyusage, style=wx.CB_READONLY,  size = wx.Size(178, -1))
        self.keyusage.SetFont(textctrlfont)
        text_keylength = wx.StaticText(self, 0, "Key_length:")
        self.keylength = wx.ComboBox(self, 1, choices=keylength, style=wx.CB_READONLY, size = wx.Size(178, -1))
        self.keylength.SetFont(textctrlfont)
        text_secret = wx.StaticText(self, 0, "Protected_Update:")
        self.secret = wx.ComboBox(self, 1, choices=confidential_list, style=wx.CB_READONLY,  size = wx.Size(178, -1))
        self.secret.SetFont(textctrlfont)
        text_payload_version = wx.StaticText(self, 0, "payload_version:")
        self.payload_version = wx.TextCtrl(self, 1, value="1",  size = wx.Size(178, -1))
        self.payload_version.SetFont(textctrlfont)
        text_payload_type = wx.StaticText(self, 0, "payload_type:")
        self.payload_type = wx.TextCtrl(self, 1, value="key",  size = wx.Size(178, -1))
        self.payload_type.SetFont(textctrlfont)
        text_sign_algo = wx.StaticText(self, 0, "sign_algo:")
        self.sign_algo = wx.ComboBox(self, 1, choices=sign_algo_list, style=wx.CB_READONLY,  size = wx.Size(178, -1))
        self.sign_algo.SetFont(textctrlfont)
        
        self.keypath = config.EXEPATH + "/ex_protected_update_data_set/samples/payload/key/rsa_1024_test.pem"
        text_keydata = wx.StaticText(self, 0, "key_data:")
        self.keydata = wx.TextCtrl(self, 1, value= "rsa_1024_test.pem", style=wx.CB_READONLY,  size = wx.Size(178, -1))
        self.keydata.SetFont(textctrlfont)
        
        self.priv_keypath = config.EXEPATH + "/scripts/certificates/sample_ec_256_priv.pem"
        text_priv_key = wx.StaticText(self, 0, "trust_anchor_privkey:")
        text_priv_key.SetFont(textctrlfont1)
        self.priv_key = wx.TextCtrl(self, -1, value= "sample_ec_256_priv.pem", style=wx.CB_READONLY, size=(178, 30))
        self.priv_key.SetFont(textctrlfont)
        text_trust_anchor_oid = wx.StaticText(self, -1, "trust_anchor_oid:")
        self.trust_anchor_oid = wx.ComboBox(self, 1, choices=key_trust_anchor_oid_list, style=wx.CB_READONLY, size = wx.Size(178, -1))
        self.trust_anchor_oid.SetFont(textctrlfont)
        text_target_oid = wx.StaticText(self, -1, "target_oid_RSA:")
        self.target_oid = wx.ComboBox(self, 1, choices =rsa_target_oid_list, style=wx.CB_READONLY,  size = wx.Size(178, -1))
        self.target_oid.SetFont(textctrlfont)
        text_secret_oid = wx.StaticText(self, -1, "secret_oid:")
        self.secret_oid = wx.ComboBox(self, 1, choices=key_secret_oid_list, style=wx.CB_READONLY, size=(178, 30))
        self.secret_oid.SetFont(textctrlfont)
        
        self.secret1path = config.EXEPATH + "/ex_protected_update_data_set/samples/confidentiality/secret.txt"
        text_secret1 = wx.StaticText(self, 0, "secret:")
        self.secret1 = wx.TextCtrl(self, 1, value= "secret.txt", style=wx.CB_READONLY,  size = wx.Size(178, -1))
        self.secret1.SetFont(textctrlfont)
        
        self.secret2path = config.EXEPATH + "/ex_protected_update_data_set/samples/confidentiality/secret.txt"
        text_secret2 = wx.StaticText(self, 0, "secret:")
        self.secret2 = wx.TextCtrl(self, 1, value= "secret.txt", style=wx.CB_READONLY,  size = wx.Size(178, -1))
        self.secret2.SetFont(textctrlfont)
        
        self.trust_anchor_certpath = config.EXEPATH + "/scripts/certificates/sample_ec_256_cert.pem"
        text_trust_anchor_cert = wx.StaticText(self, -1, "trust_anchor_cert:")
        self.trust_anchor_cert = wx.TextCtrl(self, 1, value= "sample_ec_256_cert.pem",style=wx.CB_READONLY, size = wx.Size(178, 30))
        self.trust_anchor_cert.SetFont(textctrlfont)
        button_step2 = wx.Button(self, 1, 'Step2: Generate Manifest', size = wx.Size(270, -1))
        button_step2.SetFont(buttonfont)
        button_step3 = wx.Button(self, 1, 'Step3: Update Trust M Objects', size = wx.Size(270, -1))
        button_step3.SetFont(buttonfont)
        button_read_objects_metadata = wx.Button(self, 1, 'Read Objects Metadata', size = wx.Size(270, -1))
        button_read_objects_metadata.SetFont(buttonfont)
        button_reset_access = wx.Button(self, 1, 'Reset Access Condition', size = wx.Size(270, -1))
        button_reset_access.SetFont(buttonfont)

        self.button_step1 = wx.Button(self, -1, 'Step1:Provision for all OIDs', size = wx.Size(270, -1))
        self.button_step1.SetFont(buttonfont)
        
        self.text_display = wx.TextCtrl(self, -1, style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.text_display.SetFont(wx.Font(11, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))

        serverimage = wx.Image(config.IMAGEPATH + "/images/server.png", wx.BITMAP_TYPE_PNG).Scale(110,110,wx.IMAGE_QUALITY_HIGH).ConvertToBitmap()
        serverimage = wx.StaticBitmap(self, -1, serverimage)

        clearimage = wx.Image(config.IMAGEPATH + "/images/clear.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        clearbutton = wx.BitmapButton(self, -1, clearimage)
        
        lockedarrow = wx.Image(config.IMAGEPATH + "/images/LockedArrow.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        lockedarrowimage = wx.StaticBitmap(self, -1,lockedarrow)

        chipimage = wx.Image(config.IMAGEPATH + "/images/chipp3.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        chipimage = wx.StaticBitmap(self, -1,chipimage)
        
        backimage = wx.Image(config.IMAGEPATH + "/images/back.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        backbutton = wx.BitmapButton(self, -1, backimage)
       
        #Add mainhorisizer and title to mainsizer
        mainsizer.Add(title, 0, wx.CENTRE | wx.ALL, 5)
        mainsizer.Add(mainhorisizer, 1, wx.EXPAND)
       
        # Add Sub Sizers to the mainhorisizer
        mainhorisizer.Add(leftsizer, 0, wx.EXPAND)
        mainhorisizer.Add(midsizer, 1, wx.EXPAND)
        mainhorisizer.Add(self.text_display, 1, wx.EXPAND | wx.ALL, 5)
        
        # Add Objects to leftsizer
        leftsizer.Add(picturesizer, 0, wx.TOP, 65)
        leftsizer.AddSpacer(110)
        leftsizer.Add(backbuttonsizer, 0, wx.LEFT | wx.BOTTOM, 10)
        picturesizer.Add(serverimage, 0 , wx.ALIGN_CENTER, 0 )
        picturesizer.AddSpacer(30)
        picturesizer.Add(lockedarrowimage, 0, wx.ALIGN_CENTER, 0)
        picturesizer.AddSpacer(20)
        picturesizer.Add(chipimage, 0, wx.ALIGN_CENTER, 0)
        backbuttonsizer.Add(backbutton, 0, wx.ALIGN_LEFT, 0)
        backbuttonsizer.AddSpacer(10)
        backbuttonsizer.Add(clearbutton, 0, wx.EXPAND, 0)

        # Add sizers to midsizer
        midsizer.AddSpacer(20)
        midsizer.Add(gdsizer1, 0, wx.EXPAND | wx.ALL, 5)
        midsizer.AddSpacer(10)
        midsizer.Add(button_step2, 0, wx.ALL, 5)
        midsizer.AddSpacer(30)
        midsizer.Add(gdsizer2, 0, wx.EXPAND | wx.ALL, 5)
        midsizer.AddSpacer(10)
        midsizer.Add(gdsizer3, 0, wx.EXPAND | wx.ALL, 5)
        
        
        #add buttons into gdsizer3
        gdsizer3.AddMany([
            (self.button_step1),   
            (button_read_objects_metadata),
            (button_step3),
            (button_reset_access),

        ])
        
        #add sizers to gdsizer1
        gdsizer1.AddMany([
                (secretsizer, 0, wx.EXPAND),
                (payloadversizer, 0, wx.EXPAND),
                (payloadtypesizer, 0, wx.EXPAND),
                (signsizer, 0, wx.EXPAND),
                (keydatasizer, 0, wx.EXPAND),
                (privsizer, 0, wx.EXPAND)
        ])
        
        gdsizer1.Add(keylengthsizer, 0, wx.EXPAND)
        gdsizer1.Add(keyusagesizer, 0, wx.EXPAND)
        gdsizer1.Add(secret2sizer, 0, wx.EXPAND)
        
        #add sizers to gdsizer2
        gdsizer2.AddMany([
                (trustoidsizer, 0, wx.EXPAND),
                (targetoidsizer, 0, wx.EXPAND),
                (secretoidsizer, 0, wx.EXPAND),
                (trustcertsizer, 0, wx.EXPAND),
        ])
        
        gdsizer2.AddSpacer(20)
        gdsizer2.Add(secret1sizer, 0, wx.EXPAND)
                
        #add objects into sizers in gdsizer1
        secretsizer.Add(text_secret)
        secretsizer.Add(self.secret)
        payloadversizer.Add(text_payload_version)
        payloadversizer.Add(self.payload_version)
        payloadtypesizer.Add(text_payload_type)
        payloadtypesizer.Add(self.payload_type)
        signsizer.Add(text_sign_algo)
        signsizer.Add(self.sign_algo)
        keydatasizer.Add(text_keydata)
        keydatasizer.Add(self.keydata)
        privsizer.Add(text_priv_key)
        privsizer.Add(self.priv_key)
        keyusagesizer.Add(text_keyusage)
        keyusagesizer.Add(self.keyusage)
        keylengthsizer.Add(text_keylength)
        keylengthsizer.Add(self.keylength)
        secret2sizer.Add(text_secret2)
        secret2sizer.Add(self.secret2)

        #add objects into sizers in gdsizer2
        trustoidsizer.Add(text_trust_anchor_oid)
        trustoidsizer.Add(self.trust_anchor_oid)
        targetoidsizer.Add(text_target_oid)
        targetoidsizer.Add(self.target_oid)
        secretoidsizer.Add(text_secret_oid)
        secretoidsizer.Add(self.secret_oid)
        trustcertsizer.Add(text_trust_anchor_cert)
        trustcertsizer.Add(self.trust_anchor_cert)
        secret1sizer.Add(text_secret1)
        secret1sizer.Add(self.secret1)
        
        # Set Default inputs for Text Boxes      
        self.secret.SetSelection(0)
        self.sign_algo.SetSelection(0)
        #self.keydata.SetSelection(0)
        self.trust_anchor_oid.SetSelection(0)
        self.target_oid.SetSelection(0)
        self.secret_oid.SetSelection(0)
        self.keyusage.SetSelection(3)
        self.keylength.SetSelection(0)

        # attach objects to the sizer
        # declare and bind events
        clearbutton.Bind(wx.EVT_BUTTON, self.OnFlush)
        backbutton.Bind(wx.EVT_BUTTON, self.OnBack)
        button_read_objects_metadata.Bind(wx.EVT_BUTTON, self.OnReadMetadata1)
        button_step2.Bind(wx.EVT_BUTTON, self.OnGenManifest)
        button_step3.Bind(wx.EVT_BUTTON, self.OnProtectedUpdate1)
        button_reset_access.Bind(wx.EVT_BUTTON, self.OnResetAccess1)
        self.button_step1.Bind(wx.EVT_BUTTON, self.OnRunStep1)
        
        self.priv_key.Bind(wx.EVT_LEFT_DOWN,self.OnClickFileName)
        self.trust_anchor_cert.Bind(wx.EVT_LEFT_DOWN,self.OnClickCertName)
        self.secret1.Bind(wx.EVT_LEFT_DOWN,self.OnClickSecret)
        self.secret2.Bind(wx.EVT_LEFT_DOWN,self.OnClickSecret2)
        self.keydata.Bind(wx.EVT_LEFT_DOWN,self.OnClickKeydata)
        
        # Set tooltips
        self.button_step1.SetToolTip(wx.ToolTip("Provision metadata for Trust Anchor OID, Protected Update Secret OID and Target OID.\n" \
                                                "Temp Decommission: Provision Target OID for Temporary Decommissioning and set Lcs0 to Termination mode.\n" \
                                                "Wipe Data: Provision Target OID to flush away certificate inside and set Lcs0 to Termination mode."))
        button_read_objects_metadata.SetToolTip(wx.ToolTip("Read metadata of Trust Anchor OID, Secret OID and Target OID."))
        button_step2.SetToolTip(wx.ToolTip("Generate the correct manifest and fragment for protected update."))
        button_step3.SetToolTip(wx.ToolTip("Perform protected update for metadata of Target OID."))
        clearbutton.SetToolTip(wx.ToolTip("Clear all textboxes."))
        backbutton.SetToolTip(wx.ToolTip("Go back to main page."))

        self.SetSizer(mainsizer)
        mainsizer.Fit(self)
    
    def OnClickKeydata(self, evt):
        frame = wx.Frame(None, -1, '*.*')
        frame.SetSize(0,0,200,50)
            
        openFileDialog = wx.FileDialog(frame, "Open", "", "","All|*.txt;*.pem|key|*.txt;*.pem", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST |wx.FD_CHANGE_DIR)
        
        some_dir= config.EXEPATH + "/ex_protected_update_data_set/samples/payload/key/"
        
        openFileDialog.SetDirectory(some_dir)
        openFileDialog.SetFilename("rsa_1024_test.pem")
        
        if openFileDialog.ShowModal() ==wx.ID_CANCEL:
            
                return
        print((openFileDialog.GetPath()))
#         self.keydata.SetValue(openFileDialog.GetPath())
        self.keypath = openFileDialog.GetPath()
        
        self.keydata.Clear()
        self.keydata.AppendText(os.path.basename(openFileDialog.GetPath()))
        
        
        openFileDialog.Destroy()
    
    def OnKeyUsage(self):
        
        if (self.keyusage.GetSelection() == 0):
            value = "key_usage=01"
            
            return(value)
        
        elif (self.keyusage.GetSelection() == 1):
            value = "key_usage=02"
         
            return(value)
        
        elif (self.keyusage.GetSelection() == 2):
            value = "key_usage=10"
        
            return(value)
        
        elif (self.keyusage.GetSelection() == 3):
            value = "key_usage=13"
        
            return(value)
        
        elif (self.keyusage.GetSelection() == 4):
            value = "key_usage=20"
        
            return(value)
            
    def OnKeyLength(self):
        value = "key_algo=65"
        
        if (self.keylength.GetSelection() == 0):
            value = "key_algo=65"
            return (value)
            
        else:
            value = "key_algo=66"
            return (value)
            
        return (value)
        
    def OnClickFileName(self, evt):
        frame = wx.Frame(None, -1, '*.*')
        frame.SetSize(0,0,200,50)
            
        openFileDialog = wx.FileDialog(frame, "Open", "", "","All|*.crt;*.pem|Certificate|*.crt;*.pem", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST |wx.FD_CHANGE_DIR)
        
        some_dir= config.EXEPATH + "/scripts/certificates/"
        
        openFileDialog.SetDirectory(some_dir)
        openFileDialog.SetFilename("sample_ec_256_priv.pem")
        
        if openFileDialog.ShowModal() ==wx.ID_CANCEL:
            
                return
        print((openFileDialog.GetPath()))
        #self.priv_key.SetValue(openFileDialog.GetPath())
        self.priv_keypath = openFileDialog.GetPath()
        
        self.priv_key.Clear()
        self.priv_key.AppendText(os.path.basename(openFileDialog.GetPath()))
        
        openFileDialog.Destroy()    

    def OnClickCertName(self, evt):
        frame = wx.Frame(None, -1, '*.*')
        frame.SetSize(0,0,200,50)
            
        openFileDialog = wx.FileDialog(frame, "Open", "", "","All|*.crt;*.pem|Certificate|*.crt;*.pem", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST |wx.FD_CHANGE_DIR)
        
        some_Dir= config.EXEPATH + "/scripts/certificates/"
        
        openFileDialog.SetDirectory(some_Dir)
        openFileDialog.SetFilename("sample_ec_256_cert.pem")
        
        
        if openFileDialog.ShowModal() ==wx.ID_CANCEL:
            
                return
        print((openFileDialog.GetPath()))
        #self.trust_anchor_cert.SetValue(openFileDialog.GetPath())
        self.trust_anchor_certpath = openFileDialog.GetPath()
        
        self.trust_anchor_cert.Clear()
        self.trust_anchor_cert.AppendText(os.path.basename(openFileDialog.GetPath()))
        
        openFileDialog.Destroy()

    def OnClickSecret(self, evt):
        frame = wx.Frame(None, -1, '*.*')
        frame.SetSize(0,0,200,50)
            
        openFileDialog = wx.FileDialog(frame, "Open", "", "","All|*.crt;*.txt|Certificate|*.crt;*.txt", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST )
        
        some_Dir= config.EXEPATH + "/ex_protected_update_data_set/samples/confidentiality/"
        
        openFileDialog.SetDirectory(some_Dir)
        openFileDialog.SetFilename("secret.txt")
        
        
        if openFileDialog.ShowModal() ==wx.ID_CANCEL:
            
                return
        print((openFileDialog.GetPath()))
        #self.secret1.SetValue(openFileDialog.GetPath())
        self.secret1path = openFileDialog.GetPath()
        
        self.secret1.Clear()
        self.secret1.AppendText(os.path.basename(openFileDialog.GetPath()))
        
        openFileDialog.Destroy()
 
    def OnClickSecret2(self, evt):
        frame = wx.Frame(None, -1, '*.*')
        frame.SetSize(0,0,200,50)
            
        openFileDialog = wx.FileDialog(frame, "Open", "", "","All|*.crt;*.txt|Certificate|*.crt;*.txt", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST )
        
        some_Dir= config.EXEPATH + "/ex_protected_update_data_set/samples/confidentiality/"
        
        openFileDialog.SetDirectory(some_Dir)
        openFileDialog.SetFilename("secret.txt")
        
        if openFileDialog.ShowModal() ==wx.ID_CANCEL:
            
                return
        print((openFileDialog.GetPath()))
        #self.secret2.SetValue(openFileDialog.GetPath())
        self.secret2path = openFileDialog.GetPath()
        
        self.secret2.Clear()
        self.secret2.AppendText(os.path.basename(openFileDialog.GetPath()))
        
        openFileDialog.Destroy()


    def OnRunStep1(self, evt):
        self.OnSetupRSAKeyUpdate1()
        

    def OnSetup(self):
        trust_anchor_oid = "0x" + self.trust_anchor_oid.GetValue()
        target_oid = "0x" + self.target_oid.GetValue()
        secret_oid = "0x" + self.secret_oid.GetValue()
        certfile = self.trust_anchor_certpath
        
        TRUST_ANCHOR_META = "2003E80111"
        
        f = open(self.secret1path, 'r')
        file= f.read()
        print(file)
        PROTECTED_UPDATE_SECRET = file
        f.close()
        
        PROTECTED_UPDATE_SECRET_META = "200BD103E1FC07D30100E80123"
     
        #Step1: Provisioning initial Trust Anchor, metadata for Trust Anchor
        self.text_display.AppendText("Provisioning for initial Trust Anchor OID... \n")
        command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_cert", "-w", trust_anchor_oid, "-i", certfile, ])
        self.text_display.AppendText(command_output)
        self.text_display.AppendText("'trustm_cert -w 0x" + trust_anchor_oid + " -i " + certfile + "'" + " executed \n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
        
        self.text_display.AppendText("Provisioning for trust anchor metadata... \n")
        command_output = exec_cmd.createProcess("echo " + TRUST_ANCHOR_META + " | xxd -r -p > trust_anchor_metadata.bin", None)
        self.text_display.AppendText("'echo $TRUST_ANCHOR_META | xxd -r -p > trust_anchor_metadata.bin' executed \n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
        
        self.text_display.AppendText("Writing trust_anchor_metadata.bin as metadata of Trust Anchor OID... \n")
        command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_metadata", "-w", trust_anchor_oid, "-F", "trust_anchor_metadata.bin", ])
        self.text_display.AppendText(command_output)
        self.text_display.AppendText("'trustm_metadata -w 0x" + trust_anchor_oid + " -F trust_anchor_metadata.bin'" + " executed \n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
        
        
        #Step2: Provisioning Protected Update Secret OID, metadata for Protected Update Secret OID
        self.text_display.AppendText("Provisioning for protected update secret... \n")
        command_output = exec_cmd.createProcess("echo " + PROTECTED_UPDATE_SECRET + " | xxd -r -p > protected_update_secret.dat", None)
        self.text_display.AppendText("'$PROTECTED_UPDATE_SECRET xxd -r -p > protected_update_secret.dat' executed \n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")    
        
        self.text_display.AppendText("Writing protected update secret into secret_oid...")
        command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_data", "-e", "-w", secret_oid, "-i", "protected_update_secret.dat", ])
        self.text_display.AppendText(command_output)
        self.text_display.AppendText("'trustm_data -e -w 0x" + secret_oid + " -i protected_update_secret.dat'" + " executed \n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
       
        self.text_display.AppendText("Provisioning for protected update secret metadata... \n")
        command_output = exec_cmd.createProcess("echo " + PROTECTED_UPDATE_SECRET_META + " | xxd -r -p > protected_update_secret_metadata.bin", None)
        self.text_display.AppendText("'$PROTECTED_UPDATE_SECRET_META xxd -r -p > protected_update_secret_metadata.bin' executed \n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
        
        self.text_display.AppendText("Writing protected update secret metadata into secret_oid... ")
        command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_metadata", "-w", secret_oid, "-F", "protected_update_secret_metadata.bin", ])
        self.text_display.AppendText(command_output)
        self.text_display.AppendText("'trustm_metadata -w " + secret_oid + " -F protected_update_secret_metadata.bin' executed \n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")       
        
        
    def OnSetupRSAKeyUpdate1(self):
        self.text_display.AppendText("Provisioning Data Objects ... \n")
        wx.CallLater(10, self.OnSetupRSAKeyUpdate)
        
    def OnSetupRSAKeyUpdate(self):
        trust_anchor_oid = "0x" + self.trust_anchor_oid.GetValue()
        target_oid = "0x" + self.target_oid.GetValue()
        secret_oid = "0x" + self.secret_oid.GetValue()
        secret_list_value=self.secret.GetValue()
        if (secret_list_value=="Integrity"):
           TARGET_OID_META="2009C1020000D00321" + self.trust_anchor_oid.GetValue()
        else:
           TARGET_OID_META="200dC1020000D00721" + self.trust_anchor_oid.GetValue() + "FD20" + self.secret_oid.GetValue()
        
        self.OnSetup()
        
        #step 1
        self.text_display.AppendText("Set metadata protected update for Target OID (Provision for Target OID)... \n")
        command_output = exec_cmd.createProcess("echo " + TARGET_OID_META + " | xxd -r -p > targetOID_metadata.bin", None)
        self.text_display.AppendText("'$TARGET_OID_META | xxd -r -p > targetOID_metadata.bin' executed \n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
        self.text_display.AppendText("Writing targetOID_metadata.bin as metadata of Target OID... \n")
        command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_metadata", "-w", target_oid, "-F", "targetOID_metadata.bin", ])
        self.text_display.AppendText(command_output)
        self.text_display.AppendText("'trustm_metadata -w " + target_oid + " -F targetOID_metadata.bin' executed \n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
        command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_metadata", "-r", target_oid,])
        self.text_display.AppendText(command_output)
        self.text_display.AppendText("'trustm_metadata --r " + target_oid + " executed \n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
 
        
    def OnReadMetadata1(self, evt):
        self.text_display.AppendText("Reading Objects Metadata... \n")
        wx.CallLater(10, self.OnReadMetadata)
    
    def OnReadMetadata(self):
        trust_anchor_oid = "0x" + self.trust_anchor_oid.GetValue()
        target_oid = "0x" + self.target_oid.GetValue()
        secret_oid = "0x" + self.secret_oid.GetValue()
        
        self.text_display.AppendText("Reading out metadata for trust_anchor_oid... \n")
        command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_metadata", "-r", trust_anchor_oid, ])
        self.text_display.AppendText(command_output)
        self.text_display.AppendText("'trustm_metadata -r " + trust_anchor_oid + "' executed \n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
                
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
        
    def OnGenManifest(self, evt):
        payload_version = "payload_version=" + self.payload_version.GetValue()
        trust_anchor_oid = "trust_anchor_oid=" + self.trust_anchor_oid.GetValue()
        target_oid = "target_oid=" + self.target_oid.GetValue()
        sign_algo = "sign_algo=" + self.sign_algo.GetValue()
        priv_key = "priv_key=" + self.priv_keypath
        payload_type = "payload_type=" + self.payload_type.GetValue()
        
        key_algo = self.OnKeyLength()
        print(key_algo)
        
        key_usage = self.OnKeyUsage()
        print(key_usage)
        
        key_data = "key_data=" + self.keypath 
        print(key_data)
        label = "label=test"
        seed_length = "seed_length=64"
        enc_algo = "enc_algo=AES-CCM-16-64-128"
        secret_oid = "secret_oid=" + self.secret_oid.GetValue()
        
        secret_list_value=self.secret.GetValue()
        if (secret_list_value=="Integrity"):    
            command_output = exec_cmd.createProcess(config.EXEPATH + "/ex_protected_update_data_set/Linux/bin/trustm_protected_update_set " + payload_version + " "
                                                    + trust_anchor_oid + " " + target_oid + " " + sign_algo + " " + priv_key + " " + payload_type
                                                    + " " + key_algo + " " + key_usage + " " + key_data + " " + label + " " + seed_length + " " + enc_algo + " " + secret_oid 
                                                    + "| grep -A40 'uint8_t manifest_data\|uint8_t fragment_01' | sed '1,2d' | sed '11,14d' | sed '$d' | sed 's/0x//g' | tr -d ',[:space:]'",
                                                    None)
            
        else:
            secret = "secret=" + self.secret2path
            print(secret)
            command_output = exec_cmd.createProcess(config.EXEPATH + "/ex_protected_update_data_set/Linux/bin/trustm_protected_update_set " + payload_version + " "
                                                    + trust_anchor_oid + " " + target_oid + " " + sign_algo + " " + priv_key + " " + payload_type
                                                    + " " + key_algo + " " + key_usage + " " + key_data + " " + label + " " + seed_length + " " + enc_algo + " " + secret_oid + " " + secret 
                                                    + " | grep -A40 'uint8_t manifest_data\|uint8_t fragment_01' |  sed '1,2d'| sed '17,20d' | sed '$d' | sed 's/0x//g' | tr -d ',[:space:]'",
                                                    None)
    
        manifest_and_frag_string = command_output.stdout.read().decode("utf-8")
        manifest_and_frag_string = manifest_and_frag_string.split('};')
        manifest = manifest_and_frag_string[0]
        fragment = manifest_and_frag_string[1]

        self.text_display.AppendText("manifest: " + manifest)
        self.text_display.AppendText("\n\nfragment: " + fragment)
        
        exec_cmd.createProcess("echo " + manifest + " | xxd -r -p > manifest.dat", None)
        exec_cmd.createProcess("echo " + fragment + " | xxd -r -p > fragment.dat", None)
        self.text_display.AppendText("\n\nmanifest.dat and fragment.dat generated\n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
    
    def OnProtectedUpdate1(self, evt):
        self.text_display.AppendText("RSA Key protected update for Target OID... \n")
        wx.CallLater(10, self.OnProtectedUpdate)
    
    def OnProtectedUpdate(self):
        target_oid = "0x" + self.target_oid.GetValue()
        command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_protected_update_rsakey", "-k", target_oid, "-f", "fragment.dat", "-m", "manifest.dat", "-X", ])
        self.text_display.AppendText(command_output)
        self.text_display.AppendText("'trustm_protected_update_rsakey -k " + target_oid + " -m manifest.dat -f fragment.dat' executed \n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
    
    def OnResetAccess1(self, evt):
        self.text_display.AppendText("Resetting Access Condition tag for Target OID... \n")
        wx.CallLater(10, self.OnResetAccess)
    
    def OnResetAccess(self):
        RESET_ACCESS_META="2005D003E1FC07"
        target_oid = "0x" + self.target_oid.GetValue()
        exec_cmd.createProcess("echo " + RESET_ACCESS_META + " | xxd -r -p > access_reset.bin", None)
        command_output = exec_cmd.execCLI(["xxd", "access_reset.bin", ])
        self.text_display.AppendText(command_output)
        self.text_display.AppendText("access_reset.bin generated\n")
        self.text_display.AppendText("Writing metadata for Target OID... \n")
        exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_metadata", "-w", target_oid, "-F", "access_reset.bin", ])
        self.text_display.AppendText("'trustm_metadata -w " + target_oid + " -F access_reset.bin' executed \n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
    
    
    def OnFlush(self, evt):
        self.text_display.Clear()

    # Calling parent of the parent, as direct parent is the notebook,
    # then the second parent is the frame, from which we call the destruction
    def OnBack(self, evt):
        self.Parent.Parent.OnCloseWindow(None)


class Tab_DataUpdate(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        
        title = wx.StaticText(self, -1, style=wx.ALIGN_CENTER, label="Data Integrity Confidential Protected Update")
        font = wx.Font(20, wx.ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        title.SetFont(font)
        
        textctrlfont = wx.Font()
        textctrlfont.SetPointSize(11)
        
        buttonfont = wx.Font(12, wx.ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        
        # declare the sizers
        mainsizer = wx.BoxSizer(wx.VERTICAL)
        mainhorisizer = wx.BoxSizer(wx.HORIZONTAL)
        
        midsizer = wx.BoxSizer(wx.VERTICAL)
        gdsizer1 = wx.GridSizer(rows=3, cols=3, vgap=10, hgap=10)
        gdsizer2 = wx.GridSizer(rows=2, cols=3, vgap=10, hgap=10)
        gdsizer3 = wx.GridSizer(rows=2, cols=2, vgap=20, hgap=10)
        #step1_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        titlesizer = wx.BoxSizer(wx.HORIZONTAL)
        
        leftsizer = wx.BoxSizer(wx.VERTICAL)
        picturesizer = wx.BoxSizer(wx.VERTICAL)
        backbuttonsizer = wx.BoxSizer(wx.HORIZONTAL)
        
        # declare sizers that will be in the grid2
        labelsizer = wx.BoxSizer(wx.VERTICAL)
        secretsizer = wx.BoxSizer(wx.VERTICAL)
        encsizer = wx.BoxSizer(wx.VERTICAL)
        payloadversizer = wx.BoxSizer(wx.VERTICAL)
        payloadtypesizer = wx.BoxSizer(wx.VERTICAL)
        signsizer = wx.BoxSizer(wx.VERTICAL)
        metasizer = wx.BoxSizer(wx.VERTICAL)
        contentsizer = wx.BoxSizer(wx.VERTICAL)
        privsizer = wx.BoxSizer(wx.VERTICAL)
        datatypesizer = wx.BoxSizer(wx.VERTICAL)
        
        # declare sizers that will be in the grid1
        trustoidsizer = wx.BoxSizer(wx.VERTICAL)
        targetoidsizer = wx.BoxSizer(wx.VERTICAL)
        secretoidsizer = wx.BoxSizer(wx.VERTICAL)
        trustcertsizer = wx.BoxSizer(wx.VERTICAL)
        readdatasizer = wx.BoxSizer(wx.VERTICAL)
        
        secret1sizer = wx.BoxSizer(wx.VERTICAL)
        secret2sizer = wx.BoxSizer(wx.VERTICAL)

        # instantiate the objects
        self.secret2path = config.EXEPATH + "/ex_protected_update_data_set/samples/confidentiality/secret.txt"
        text_secret2 = wx.StaticText(self, 0, "secret:")
        self.secret2 = wx.TextCtrl(self, 1, value= "secret.txt", style=wx.CB_READONLY,  size = wx.Size(178, -1))
        self.secret2.SetFont(textctrlfont)
        
        self.secret1path = config.EXEPATH + "/ex_protected_update_data_set/samples/confidentiality/secret.txt"
        text_secret1 = wx.StaticText(self, 0, "secret:")
        self.secret1 = wx.TextCtrl(self, 1, value= "secret.txt", style=wx.CB_READONLY,  size = wx.Size(178, -1))
        self.secret1.SetFont(textctrlfont)
        text_secret = wx.StaticText(self, 0, "Protected_Update:")
        self.secret = wx.ComboBox(self, 1, choices=secret_list, style=wx.CB_READONLY,  size = wx.Size(178, -1))
        self.secret.SetFont(textctrlfont)
        text_payload_version = wx.StaticText(self, 0, "payload_version:")
        self.payload_version = wx.TextCtrl(self, 1, value="1",  size = wx.Size(178, -1))
        self.payload_version.SetFont(textctrlfont)
        text_payload_type = wx.StaticText(self, 0, "payload_type:")
        self.payload_type = wx.TextCtrl(self, 1, value="data",  size = wx.Size(178, -1))
        self.payload_type.SetFont(textctrlfont)
        text_sign_algo = wx.StaticText(self, 0, "sign_algo:")
        self.sign_algo = wx.ComboBox(self, 1, choices=sign_algo_list, style=wx.CB_READONLY,  size = wx.Size(178, -1))
        self.sign_algo.SetFont(textctrlfont)
        
        self.datapath = config.EXEPATH + "/ex_protected_update_data_set/samples/payload/data/hex_data.txt"
        text_data = wx.StaticText(self, 0, "data:")
        self.data = wx.TextCtrl(self, 1, value= "type3_data.txt", style=wx.CB_READONLY,  size = wx.Size(178, -1))
        self.data.SetFont(textctrlfont)
        
        # data types to accomondate both ascii and hex 
        datatype_text = wx.StaticText(self, 0, "data type:")
        self.datatype = wx.ComboBox(self, 1, choices=datatype_list, style=wx.CB_READONLY, size = wx.Size(178, -1))
        self.datatype.SetFont(textctrlfont)
        
        self.priv_keypath = config.EXEPATH + "/scripts/certificates/sample_ec_256_priv.pem"
        text_priv_key = wx.StaticText(self, 0, "trust_anchor_key:")
        self.priv_key = wx.TextCtrl(self, -1, value= "sample_ec_256_priv.pem", style=wx.CB_READONLY, size=(178, 30))
        self.priv_key.SetFont(textctrlfont)
        text_trust_anchor_oid = wx.StaticText(self, -1, "trust_anchor_oid:")
        self.trust_anchor_oid = wx.ComboBox(self, 1, choices=data_trust_anchor_oid_list, style=wx.CB_READONLY, size = wx.Size(178, -1))
        self.trust_anchor_oid.SetFont(textctrlfont)
        text_target_oid = wx.StaticText(self, -1, "target_oid:")
        self.target_oid = wx.ComboBox(self, 1, choices = data_target_oid_list, style=wx.CB_READONLY,  size = wx.Size(178, -1))
        self.target_oid.SetFont(textctrlfont)
        text_secret_oid = wx.StaticText(self, -1, "secret_oid:")
        self.secret_oid = wx.ComboBox(self, 1, choices=data_secret_oid_list, style=wx.CB_READONLY,  size = wx.Size(178, -1))
        self.secret_oid.SetFont(textctrlfont)
        
        self.trust_anchor_certpath = config.EXEPATH + "/scripts/certificates/sample_ec_256_cert.pem"
        text_trust_anchor_cert = wx.StaticText(self, -1, "trust_anchor_cert:")
        self.trust_anchor_cert = wx.TextCtrl(self, 1, value= "sample_ec_256_cert.pem",style=wx.CB_READONLY, size = wx.Size(178, 30))
        self.trust_anchor_cert.SetFont(textctrlfont)
        button_step2 = wx.Button(self, 1, 'Step2: Generate Manifest', size = wx.Size(270, -1))
        button_step2.SetFont(buttonfont)
        button_step3 = wx.Button(self, 1, 'Step3: Update Trust M Objects', size = wx.Size(270, -1))
        button_step3.SetFont(buttonfont)
        button_read_objects_metadata = wx.Button(self, 1, 'Read Objects Metadata', size = wx.Size(270, -1))
        button_read_objects_metadata.SetFont(buttonfont)
        button_reset_mud = wx.Button(self, 1, 'Reset Access Condition', size = wx.Size(270, -1))
        button_reset_mud.SetFont(buttonfont)

        #self.step1_combo_box = wx.ComboBox(self, 1, choices=step1_list, style=wx.CB_READONLY, size = wx.Size(554, -1))
        #self.step1_combo_box.SetFont(buttonfont)
        self.button_step1 = wx.Button(self, -1, 'Step1: Provisioning for All OIDs', size = wx.Size(270, -1))
        self.button_step1.SetFont(buttonfont)
        
        # read data button
        button_read_data = wx.Button(self, 1, 'Read Target OID Data', size = wx.Size(178, -1))
        button_read_data.SetFont(buttonfont)
        
        
        self.text_display = wx.TextCtrl(self, -1, style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.text_display.SetFont(wx.Font(11, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))

        serverimage = wx.Image(config.IMAGEPATH + "/images/server.png", wx.BITMAP_TYPE_PNG).Scale(110,110,wx.IMAGE_QUALITY_HIGH).ConvertToBitmap()
        serverimage = wx.StaticBitmap(self, -1, serverimage)

        clearimage = wx.Image(config.IMAGEPATH + "/images/clear.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        clearbutton = wx.BitmapButton(self, -1, clearimage)
        
        lockedarrow = wx.Image(config.IMAGEPATH + "/images/LockedArrow.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        lockedarrowimage = wx.StaticBitmap(self, -1,lockedarrow)

        chipimage = wx.Image(config.IMAGEPATH + "/images/chipp3.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        chipimage = wx.StaticBitmap(self, -1,chipimage)
        
        backimage = wx.Image(config.IMAGEPATH + "/images/back.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        backbutton = wx.BitmapButton(self, -1, backimage)
       
        #Add mainhorisizer and title to mainsizer
        mainsizer.Add(title, 0, wx.CENTRE | wx.ALL, 5)
        mainsizer.Add(mainhorisizer, 1, wx.EXPAND)
       
        # Add Sub Sizers to the mainhorisizer
        mainhorisizer.Add(leftsizer, 0, wx.EXPAND)
        mainhorisizer.Add(midsizer, 1, wx.EXPAND)
        mainhorisizer.Add(self.text_display, 1, wx.EXPAND | wx.ALL, 5)
        
        # Add Objects to leftsizer
        leftsizer.Add(picturesizer, 0, wx.TOP, 65)
        leftsizer.AddSpacer(115)
        leftsizer.Add(backbuttonsizer, 0, wx.LEFT | wx.BOTTOM, 10)
        picturesizer.Add(serverimage, 0 , wx.ALIGN_CENTER, 0 )
        picturesizer.AddSpacer(30)
        picturesizer.Add(lockedarrowimage, 0, wx.ALIGN_CENTER, 0)
        picturesizer.AddSpacer(20)
        picturesizer.Add(chipimage, 0, wx.ALIGN_CENTER, 0)
        backbuttonsizer.Add(backbutton, 0, wx.ALIGN_LEFT, 0)
        backbuttonsizer.AddSpacer(10)
        backbuttonsizer.Add(clearbutton, 0, wx.EXPAND, 0)

        # Add sizers to midsizer
        midsizer.AddSpacer(10)
        midsizer.Add(gdsizer1, 0, wx.EXPAND | wx.ALL, 5)
        midsizer.AddSpacer(5)
        midsizer.Add(button_step2, 0, wx.ALL, 5)
        midsizer.AddSpacer(5)
        midsizer.AddSpacer(20)
        midsizer.Add(gdsizer2, 0, wx.EXPAND | wx.ALL, 5)
        midsizer.AddSpacer(5)
        #midsizer.Add(step1_sizer)
        midsizer.AddSpacer(5)
        midsizer.AddSpacer(5)
        midsizer.Add(gdsizer3, 0, wx.EXPAND | wx.ALL, 5)
        
        #add step1 button into step1_sizer
        #step1_sizer.Add(self.step1_combo_box, 1, wx.EXPAND | wx.ALL, 5)
        
        
        #add buttons into gdsizer3
        gdsizer3.AddMany([
            (self.button_step1),
            (button_read_objects_metadata),
            (button_step3),
            (button_reset_mud),

        ])
        
        #add sizers to gdsizer1
        gdsizer1.AddMany([
                (secretsizer, 0, wx.EXPAND),
                (payloadversizer, 0, wx.EXPAND),
                (payloadtypesizer, 0, wx.EXPAND),
                (signsizer, 0, wx.EXPAND),
                (metasizer, 0, wx.EXPAND),
                (privsizer, 0, wx.EXPAND)
        ])
        
        gdsizer1.AddSpacer(20)
        #gdsizer1.AddSpacer(20)
        gdsizer1.Add(datatypesizer, 0, wx.EXPAND)
        gdsizer1.Add(secret1sizer, 0, wx.EXPAND)
        
        #add sizers to gdsizer2
        gdsizer2.AddMany([
                (trustoidsizer, 0, wx.EXPAND),
                (targetoidsizer, 0, wx.EXPAND),
                (secretoidsizer, 0, wx.EXPAND),
                (trustcertsizer, 0, wx.EXPAND),
                (readdatasizer, 0, wx.EXPAND),
                (secret2sizer, 0, wx.EXPAND),
        ])
        
        #gdsizer2.AddSpacer(20)
        #gdsizer2.Add(secret2sizer, 0, wx.EXPAND)
                
        #add objects into sizers in gdsizer1
        secretsizer.Add(text_secret)
        secretsizer.Add(self.secret)
        payloadversizer.Add(text_payload_version)
        payloadversizer.Add(self.payload_version)
        payloadtypesizer.Add(text_payload_type)
        payloadtypesizer.Add(self.payload_type)
        signsizer.Add(text_sign_algo)
        signsizer.Add(self.sign_algo)
        metasizer.Add(text_data)
        metasizer.Add(self.data)
        privsizer.Add(text_priv_key)
        privsizer.Add(self.priv_key)
        secret1sizer.Add(text_secret1)
        secret1sizer.Add(self.secret1)
        datatypesizer.Add(datatype_text)
        datatypesizer.Add(self.datatype)
        
        #add objects into sizers in gdsizer2
        trustoidsizer.Add(text_trust_anchor_oid)
        trustoidsizer.Add(self.trust_anchor_oid)
        targetoidsizer.Add(text_target_oid)
        targetoidsizer.Add(self.target_oid)
        secretoidsizer.Add(text_secret_oid)
        secretoidsizer.Add(self.secret_oid)
        trustcertsizer.Add(text_trust_anchor_cert)
        trustcertsizer.Add(self.trust_anchor_cert)
        secret2sizer.Add(text_secret2)
        secret2sizer.Add(self.secret2)
        readdatasizer.AddSpacer(23)
        readdatasizer.Add(button_read_data)
        
        # Set Default inputs for Text Boxes      
        self.secret.SetSelection(0)
        self.sign_algo.SetSelection(0)
        self.trust_anchor_oid.SetSelection(0)
        self.target_oid.SetSelection(11)
        self.secret_oid.SetSelection(1)
        self.datatype.SetSelection(0)

        # attach objects to the sizer
        # declare and bind events
        clearbutton.Bind(wx.EVT_BUTTON, self.OnFlush)
        backbutton.Bind(wx.EVT_BUTTON, self.OnBack)
        button_read_objects_metadata.Bind(wx.EVT_BUTTON, self.OnReadMetadata1)
        self.button_step1.Bind(wx.EVT_BUTTON, self.OnRunStep1)
        button_step2.Bind(wx.EVT_BUTTON, self.OnGenManifest)
        button_step3.Bind(wx.EVT_BUTTON, self.OnProtectedUpdate1)
        button_reset_mud.Bind(wx.EVT_BUTTON, self.OnResetAccess1)
        button_read_data.Bind(wx.EVT_BUTTON, self.OnReadData1)
        self.secret1.Bind(wx.EVT_LEFT_DOWN,self.OnClickSecret)
        self.secret2.Bind(wx.EVT_LEFT_DOWN,self.OnClickSecret2)
        self.priv_key.Bind(wx.EVT_LEFT_DOWN,self.OnClickFileName)
        self.trust_anchor_cert.Bind(wx.EVT_LEFT_DOWN,self.OnClickCertName)
        self.data.Bind(wx.EVT_LEFT_DOWN,self.OnClickData)
        
        # bind target_oid and secret_oid to events to prevent same selection
        self.target_oid.Bind(wx.EVT_COMBOBOX, self.OnSelectTargetOid)
        self.secret_oid.Bind(wx.EVT_COMBOBOX, self.OnSelectSecretOid)
        
        
        # Set tooltips
        self.button_step1.SetToolTip(wx.ToolTip("Provision metadata for Trust Anchor OID, Protected Update Secret OID and Target OID.\n"))
        button_step2.SetToolTip(wx.ToolTip("Generate the correct manifest and fragment for protected update."))
        button_step3.SetToolTip(wx.ToolTip("Perform protected update for data of Target OID."))
        clearbutton.SetToolTip(wx.ToolTip("Clear all textboxes."))
        backbutton.SetToolTip(wx.ToolTip("Go back to main page."))

        self.SetSizer(mainsizer)
        mainsizer.Fit(self)   
        
    def OnSelectTargetOid(self, evt):
        if (self.target_oid.GetValue() == self.secret_oid.GetValue() and self.target_oid.GetValue() != '-'):
                infoDialog = wx.MessageDialog(None, "Target OID and Secret OID cannot be the same", "Duplicated Target and Secret OID", wx.OK | wx.ICON_INFORMATION)
                infoDialog.ShowModal()
                
                self.target_oid.SetSelection(0)
                 
    def OnSelectSecretOid(self, evt):
        if (self.secret_oid.GetValue() == self.target_oid.GetValue() and self.secret_oid.GetValue() != '-'):
                infoDialog = wx.MessageDialog(None, "Target OID and Secret OID cannot be the same", "Duplicated Target and Secret OID", wx.OK | wx.ICON_INFORMATION)
                infoDialog.ShowModal()
                
                self.secret_oid.SetSelection(0)


    def OnNoOidSelected(self):
        infoDialog = wx.MessageDialog(None, "Please select target and/or secret OID", "No OID selected", wx.OK | wx.ICON_INFORMATION)
        infoDialog.ShowModal()

    def OnClickData(self, evt):
        frame = wx.Frame(None, -1, '*.*')
        frame.SetSize(0,0,200,50)
            
        openFileDialog = wx.FileDialog(frame, "Open", "", "","All|*.txt;*.pem|data|*.txt;*.pem", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST |wx.FD_CHANGE_DIR)
        
        some_dir = config.IMAGEPATH + "/working_space/samples"
        
        openFileDialog.SetDirectory(some_dir)
        openFileDialog.SetFilename("type3_data.txt")
        
        if openFileDialog.ShowModal() ==wx.ID_CANCEL:
            
                return
        print((openFileDialog.GetPath()))
        #self.metadata.SetValue(openFileDialog.GetPath())
        self.datapath = openFileDialog.GetPath()
        
        self.data.Clear()
        self.data.AppendText(os.path.basename(openFileDialog.GetPath()))
#         print(self.metadata.GetValue())
#         filename= os.path.basename(openFileDialog.GetPath())
#         print(filename)
        
        openFileDialog.Destroy()
 

    def OnClickFileName(self, evt):
        frame = wx.Frame(None, -1, '*.*')
        frame.SetSize(0,0,200,50)
            
        openFileDialog = wx.FileDialog(frame, "Open", "", "","All|*.crt;*.pem|Certificate|*.crt;*.pem", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST |wx.FD_CHANGE_DIR)
        
        some_dir= config.EXEPATH + "/scripts/certificates/"
        
        openFileDialog.SetDirectory(some_dir)
        openFileDialog.SetFilename("sample_ec_256_priv.pem")

        
        if openFileDialog.ShowModal() ==wx.ID_CANCEL:
            
                return
        print((openFileDialog.GetPath()))
        #self.priv_key.SetValue(openFileDialog.GetPath())
        self.priv_keypath = openFileDialog.GetPath()
        
        self.priv_key.Clear()
        self.priv_key.AppendText(os.path.basename(openFileDialog.GetPath()))
        
        openFileDialog.Destroy()    

    def OnClickCertName(self, evt):
        frame = wx.Frame(None, -1, '*.*')
        frame.SetSize(0,0,200,50)
            
        openFileDialog = wx.FileDialog(frame, "Open", "", "","All|*.crt;*.pem|Certificate|*.crt;*.pem", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST |wx.FD_CHANGE_DIR)
        
        some_Dir= config.EXEPATH + "/scripts/certificates/"
        
        openFileDialog.SetDirectory(some_Dir)
        openFileDialog.SetFilename("sample_ec_256_cert.pem")
        
        if openFileDialog.ShowModal() ==wx.ID_CANCEL:
            
                return
        print((openFileDialog.GetPath()))
        #self.trust_anchor_cert.SetValue(openFileDialog.GetPath())
        self.trust_anchor_certpath = openFileDialog.GetPath()
        
        self.trust_anchor_cert.Clear()
        self.trust_anchor_cert.AppendText(os.path.basename(openFileDialog.GetPath()))
        
        openFileDialog.Destroy()


    def OnClickSecret(self, evt):
        frame = wx.Frame(None, -1, '*.*')
        frame.SetSize(0,0,200,50)
            
        openFileDialog = wx.FileDialog(frame, "Open", "", "","All|*.crt;*.txt|Certificate|*.crt;*.txt", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST )
        
        some_Dir= config.EXEPATH + "/ex_protected_update_data_set/samples/confidentiality/"
        
        openFileDialog.SetDirectory(some_Dir)
        openFileDialog.SetFilename("secret.txt")
        
        if openFileDialog.ShowModal() ==wx.ID_CANCEL:
            
                return
        print((openFileDialog.GetPath()))
        #self.secret1.SetValue(openFileDialog.GetPath())
        self.secret1path = openFileDialog.GetPath()
        
        self.secret1.Clear()
        self.secret1.AppendText(os.path.basename(openFileDialog.GetPath()))
        
        openFileDialog.Destroy()
    
    def OnClickSecret2(self, evt):
        frame = wx.Frame(None, -1, '*.*')
        frame.SetSize(0,0,200,50)
            
        openFileDialog = wx.FileDialog(frame, "Open", "", "","All|*.crt;*.txt|Certificate|*.crt;*.txt", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST )
        
        some_Dir= config.EXEPATH + "/ex_protected_update_data_set/samples/confidentiality/"
        
        openFileDialog.SetDirectory(some_Dir)
        openFileDialog.SetFilename("secret.txt")
        
        
        if openFileDialog.ShowModal() ==wx.ID_CANCEL:
            
                return
        print((openFileDialog.GetPath()))
        #self.secret2.SetValue(openFileDialog.GetPath())
        self.secret2path = openFileDialog.GetPath()
        
        self.secret2.Clear()
        self.secret2.AppendText(os.path.basename(openFileDialog.GetPath()))
        
        openFileDialog.Destroy()

    def OnRunStep1(self, evt):
        if (self.target_oid.GetValue() == '-' or self.secret_oid.GetValue() == '-'):
                wx.CallLater(10, self.OnNoOidSelected)
        
        else :
                self.OnSetupTempDecom1()


    def OnSetup(self):
        trust_anchor_oid = "0x" + self.trust_anchor_oid.GetValue()
        target_oid = "0x" + self.target_oid.GetValue()
        secret_oid = "0x" + self.secret_oid.GetValue()
        certfile = self.trust_anchor_certpath
        
        TRUST_ANCHOR_META = "2003E80111"
        #PROTECTED_UPDATE_SECRET = "49C9F492A992F6D4C54F5B12C57EDB27CED224048F25482AA149C9F492A992F649C9F492A992F6D4C54F5B12C57EDB27CED224048F25482AA149C9F492A992F6"
        
        f = open(self.secret2path, 'r')
        file= f.read()
        print(file)
        PROTECTED_UPDATE_SECRET = file
        f.close()
        
        PROTECTED_UPDATE_SECRET_META = "200BD103E1FC07D30100E80123"
     
        #Step1: Provisioning initial Trust Anchor, metadata for Trust Anchor
        self.text_display.AppendText("Provisioning for initial Trust Anchor OID... \n")
        command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_cert", "-w", trust_anchor_oid, "-i", certfile, ])
        self.text_display.AppendText(command_output)
        self.text_display.AppendText("'trustm_cert -w 0x" + trust_anchor_oid + " -i " + certfile + "'" + " executed \n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
        
        self.text_display.AppendText("Provisioning for trust anchor metadata... \n")
        command_output = exec_cmd.createProcess("echo " + TRUST_ANCHOR_META + " | xxd -r -p > trust_anchor_metadata.bin", None)
        self.text_display.AppendText("'echo $TRUST_ANCHOR_META | xxd -r -p > trust_anchor_metadata.bin' executed \n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
        
        self.text_display.AppendText("Writing trust_anchor_metadata.bin as metadata of Trust Anchor OID... \n")
        command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_metadata", "-w", trust_anchor_oid, "-F", "trust_anchor_metadata.bin", ])
        self.text_display.AppendText(command_output)
        self.text_display.AppendText("'trustm_metadata -w 0x" + trust_anchor_oid + " -F trust_anchor_metadata.bin'" + " executed \n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
        
        
        #Step2: Provisioning Protected Update Secret OID, metadata for Protected Update Secret OID
        self.text_display.AppendText("Provisioning for protected update secret... \n")
        command_output = exec_cmd.createProcess("echo " + PROTECTED_UPDATE_SECRET + " | xxd -r -p > protected_update_secret.dat", None)
        self.text_display.AppendText("'$PROTECTED_UPDATE_SECRET xxd -r -p > protected_update_secret.dat' executed \n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")    
        
        self.text_display.AppendText("Writing protected update secret into secret_oid...")
        command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_data", "-e", "-w", secret_oid, "-i", "protected_update_secret.dat", ])
        self.text_display.AppendText(command_output)
        self.text_display.AppendText("'trustm_data -e -w 0x" + secret_oid + " -i protected_update_secret.dat'" + " executed \n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
       
        self.text_display.AppendText("Provisioning for protected update secret metadata... \n")
        command_output = exec_cmd.createProcess("echo " + PROTECTED_UPDATE_SECRET_META + " | xxd -r -p > protected_update_secret_metadata.bin", None)
        self.text_display.AppendText("'$PROTECTED_UPDATE_SECRET_META xxd -r -p > protected_update_secret_metadata.bin' executed \n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
        
        self.text_display.AppendText("Writing protected update secret metadata into secret_oid... ")
        command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_metadata", "-w", secret_oid, "-F", "protected_update_secret_metadata.bin", ])
        self.text_display.AppendText(command_output)
        self.text_display.AppendText("'trustm_metadata -w " + secret_oid + " -F protected_update_secret_metadata.bin' executed \n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
        
        
    def OnSetupTempDecom1(self):
        self.text_display.AppendText("Provisioning Data Objects ... \n")
        wx.CallLater(10, self.OnSetupTempDecom)
        
        
    def OnSetupTempDecom(self):
        trust_anchor_oid = "0x" + self.trust_anchor_oid.GetValue()
        target_oid = "0x" + self.target_oid.GetValue()
        secret_oid = "0x" + self.secret_oid.GetValue()
        secret_list_value=self.secret.GetValue()
        
       # if (self.secret.GetSelection() == 1):
        if (secret_list_value=="Integrity"):
            TARGET_OID_META="200CC1020000F00101D80321" + self.trust_anchor_oid.GetValue()
        #if (secret_list_value=="(None)"):
        else:
            TARGET_OID_META="200DC1020000D00721" + self.trust_anchor_oid.GetValue() + "FD20" + self.secret_oid.GetValue()
        
        self.OnSetup()
        
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

        #Set LcsO to Initialization mode
        self.text_display.AppendText("Change Target OID Lcs0 to Initialization mode... \n")
        command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_metadata", "-w", target_oid, "-I"])
        self.text_display.AppendText(command_output)
        self.text_display.AppendText("'trustm_metadata -w " + target_oid + " -I' executed \n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
          
        
    def OnReadMetadata1(self, evt):
        if (self.target_oid.GetValue() == '-' or self.secret_oid.GetValue() == '-'):
                wx.CallLater(10, self.OnNoOidSelected)    
        else :
                self.text_display.AppendText("Reading Objects Metadata... \n")
                wx.CallLater(10, self.OnReadMetadata)
    
    def OnReadMetadata(self):
        trust_anchor_oid = "0x" + self.trust_anchor_oid.GetValue()
        target_oid = "0x" + self.target_oid.GetValue()
        secret_oid = "0x" + self.secret_oid.GetValue()
        
        self.text_display.AppendText("Reading out metadata for trust_anchor_oid... \n")
        command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_metadata", "-r", trust_anchor_oid, ])
        self.text_display.AppendText(command_output)
        self.text_display.AppendText("'trustm_metadata -r " + trust_anchor_oid + "' executed \n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
                
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
    

    def OnGenManifest(self, evt):
        if (self.target_oid.GetValue() == '-' or self.secret_oid.GetValue() == '-'):
                wx.CallLater(10, self.OnNoOidSelected) 
                return  
        
        # constants for cli output parsing
        MANIFEST_SIZE_INDEX = 24
        FRAGMENT_SIZE_INDEX = 28
        BYTES_PER_LINE = 16
        #    
            
        payload_version = "payload_version=" + self.payload_version.GetValue()
        trust_anchor_oid = "trust_anchor_oid=" + self.trust_anchor_oid.GetValue()
        target_oid = "target_oid=" + self.target_oid.GetValue()
        sign_algo = "sign_algo=" + self.sign_algo.GetValue()
        #priv_key = "priv_key=" + self.priv_key.GetValue()
        priv_key = "priv_key=" + self.priv_keypath
        payload_type = "payload_type=" + self.payload_type.GetValue()
        
        #metadata = "metadata=" + self.metadata.GetValue()
        #print(self.metapath)
        data = "data=" + self.datapath
        content_reset = "content_reset=0"
        label = "label=test"
        enc_algo = "enc_algo=AES-CCM-16-64-128"
        secret_oid = "secret_oid=" + self.secret_oid.GetValue()
        
        write_type = "write_type=2"
        in_data_format= "in_data_format=" + self.datatype.GetValue()
        
        secret_list_value=self.secret.GetValue()
        if (secret_list_value=="Integrity"):    
            command_output = exec_cmd.createProcess(config.EXEPATH + "/ex_protected_update_data_set/Linux/bin/trustm_protected_update_set " + payload_version + " "
                                                    + trust_anchor_oid + " " + target_oid + " " + sign_algo + " " + priv_key + " " + payload_type
                                                    + " " + metadata + " " + content_reset + " " + label + " " + enc_algo + " " + secret_oid 
                                                    + "| grep -A10 'uint8_t manifest_data\|uint8_t fragment_01' | sed '1,2d' | sed '11,12d' | sed '$d' | sed 's/0x//g' | tr -d ',[:space:]'",
                                                    None)
        else:
            secret = "secret=" + self.secret1path
                                                    
                                                    
            test = exec_cmd.createProcess(config.EXEPATH + "/ex_protected_update_data_set/Linux/bin/trustm_protected_update_set " + payload_version + " "
                                                    + trust_anchor_oid + " " + target_oid + " " + sign_algo + " " + priv_key + " " + payload_type
                                                    + " " + data + " " + label + " " + enc_algo + " " + secret_oid + " " + secret + " " + write_type + " " + in_data_format, None)
                                                    
            testDecoded = test.stdout.read().decode()
            
            
        ########################################## CLI output parsing ######################################
        print(testDecoded)
        lines = testDecoded.splitlines()
        
        # get the line index of manifest data
        manifestStartLine = 0
        
        for line in lines:
                if ("Manifest Data" in line):
                        break

                manifestStartLine += 1        
        
        # extract info on manifest size
        try:
                manifestSize = int(lines[manifestStartLine][MANIFEST_SIZE_INDEX:MANIFEST_SIZE_INDEX+3])
        except IndexError:
                # raise info dialog here
                infoDialog = wx.MessageDialog(None, "Double check input data file", "Error Reading Data File", wx.OK | wx.ICON_INFORMATION)
                infoDialog.ShowModal()
                return
        
        # number of lines to read from manifest data
        manifestDataLineLimit = math.ceil(manifestSize / BYTES_PER_LINE)
        
        # extract manifest as it is from cli
        manifestData = ""
        for manifestLines in lines[manifestStartLine+3:manifestStartLine+3+manifestDataLineLimit]:
                manifestData += manifestLines
        
        # clean extracted manifest
        manifestData = manifestData.replace('0x', '')
        manifestData = manifestData.replace(',', '')
        manifestData = manifestData.replace(' ', '')
        manifestData = re.sub('\n', '', manifestData)
        manifestData = re.sub('\t', '', manifestData)
                
        # extracting fragments
        lineIndex = 0
        fragmentData = ["", "", ""]
        continueFragmentData = ""
        finalFragmentData = ""
        currentFragmentSize = 0
        self.fragmentNumber = 0
        self.useContinueFragment = False
        
        for line in lines:
                if ("Fragment number" in line):
                        # get fragment size
                        fragmentSize = int(line[FRAGMENT_SIZE_INDEX:FRAGMENT_SIZE_INDEX+3])
                        fragmentDataLinesLimit = math.ceil(fragmentSize / BYTES_PER_LINE)
                        
                        # track current fragment size 
                        currentFragmentSize += fragmentSize
                        
                        
                        # for now cannot write more than 1280 bytes
                        #if (currentFragmentSize > 1500):
                        #        infoDialog = wx.MessageDialog(None, "Please limit data size to less than 1500 bytes", "Maximum payload size reached", wx.OK | wx.ICON_INFORMATION)
                        #       infoDialog.ShowModal()
                        #        return
                                
                        if (self.fragmentNumber > MAX_NUM_OF_FRAGMENTS):
                                infoDialog = wx.MessageDialog(None, "Please limit fragment numbers than 4 fragments", "Maximum number of fragments reached", wx.OK | wx.ICON_INFORMATION)
                                infoDialog.ShowModal()
                                return
                                
                        for fragmentLines in lines[lineIndex+3:lineIndex+3+fragmentDataLinesLimit]:
                                fragmentData[self.fragmentNumber] += fragmentLines
                                
                        # track current fragment number
                        self.fragmentNumber += 1
                        
                                
                lineIndex +=1
                  
                        
        # clean extracted fragments
        for x in range (self.fragmentNumber):
                fragmentData[x] = fragmentData[x].replace('0x', '')
                fragmentData[x] = fragmentData[x].replace(',', '')
                fragmentData[x] = fragmentData[x].replace(' ', '')
                fragmentData[x] = re.sub('\n', '', fragmentData[x])
                fragmentData[x] = re.sub('\t', '', fragmentData[x])
        
        ####################################################################################################
        self.text_display.AppendText("manifest: " + manifestData)
        exec_cmd.createProcess("echo " + manifestData + " | xxd -r -p > manifest.dat", None)
        
        for x in range  (self.fragmentNumber):
                self.text_display.AppendText("\nFragment number " + str(x) + ": " + fragmentData[x])
                exec_cmd.createProcess("echo " + fragmentData[x] + " | xxd -r -p > fragment_" + str(x) + ".dat", None)
        self.text_display.AppendText("\n\nmanifest.dat, fragment_x.dat generated\n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
    
    def OnProtectedUpdate1(self, evt):
        if (self.target_oid.GetValue() == '-' or self.secret_oid.GetValue() == '-'):
                wx.CallLater(10, self.OnNoOidSelected) 
                return   
        
        self.text_display.AppendText("Data protected update for Target OID... \n")
        wx.CallLater(10, self.OnProtectedUpdate)
    
    def OnProtectedUpdate(self):
        target_oid = "0x" + self.target_oid.GetValue()
        try:
                if (self.fragmentNumber == 1):
                        command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_protected_update_data", "-k", target_oid, "-m", "manifest.dat", "-f", "fragment_0.dat"])
                        self.text_display.AppendText(command_output)
                        self.text_display.AppendText("'trustm_protected_update -k " + target_oid + " -m manifest.dat -f fragment_0.dat' executed \n")
                        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
                
                if (self.fragmentNumber == 2):
                        command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_protected_update_data", "-k", target_oid, "-m", "manifest.dat", "-c", "fragment_0.dat", "-f", "fragment_1.dat"])
                        self.text_display.AppendText(command_output)
                        self.text_display.AppendText("'trustm_protected_update -k " + target_oid + " -m manifest.dat -c fragment_0.dat -f fragment_1.dat' executed \n")
                        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
                
                if (self.fragmentNumber == 3):
                        command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_protected_update_data", "-k", target_oid, "-m", "manifest.dat", "-c", "fragment_0.dat", "-d", "fragment_1.dat", "-f", "fragment_2.dat"])
                        self.text_display.AppendText(command_output)
                        self.text_display.AppendText("'trustm_protected_update -k " + target_oid + " -m manifest.dat -c fragment_0.dat -d fragment_1.dat -f fragment_2.dat' executed \n")
                        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
        
        except AttributeError:
                infoDialog = wx.MessageDialog(None, "Please run Step 2: Generate Manifest", "Manifest Not generated", wx.OK | wx.ICON_INFORMATION)
                infoDialog.ShowModal()
        
    def OnResetAccess1(self, evt):
        if (self.target_oid.GetValue() == '-'):
                wx.CallLater(10, self.OnNoOidSelected)  
                return  
        
        self.text_display.AppendText("Resetting Access Condition tag for Target OID... \n")
        wx.CallLater(10, self.OnResetAccess)
    
    def OnResetAccess(self):
        RESET_ACCESS_META="2005D003E1FC07"
        target_oid = "0x" + self.target_oid.GetValue()
        exec_cmd.createProcess("echo " + RESET_ACCESS_META + " | xxd -r -p > access_reset.bin", None)
        command_output = exec_cmd.execCLI(["xxd", "access_reset.bin", ])
        self.text_display.AppendText(command_output)
        self.text_display.AppendText("access_reset.bin generated\n")
        self.text_display.AppendText("Writing metadata for Target OID... \n")
        exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_metadata", "-w", target_oid, "-F", "access_reset.bin", ])
        self.text_display.AppendText("'trustm_metadata -w " + target_oid + " -F access_reset.bin' executed \n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
        
    def OnReadData1(self, evt):
        if (self.target_oid.GetValue() == '-'):
                wx.CallLater(10, self.OnNoOidSelected) 
                return
        
        self.text_display.AppendText("\nReading out data stored in OPTIGA™ TrustM's Data Object ID: " + self.target_oid.GetValue() +"....\n")
        wx.CallLater(10, self.OnReadData)
        
    def OnReadData(self):
        dataobj = "0x" + self.target_oid.GetValue()
        
        command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_data", "-r", dataobj, ])
        self.text_display.AppendText(command_output)
        self.text_display.AppendText("'trustm_data -r " + dataobj + "' executed \n")
        self.text_display.AppendText("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ \n")
    
    
    def OnFlush(self, evt):
        self.text_display.Clear()

    # Calling parent of the parent, as direct parent is the notebook,
    # then the second parent is the frame, from which we call the destruction
    def OnBack(self, evt):
        self.Parent.Parent.OnCloseWindow(None)


class Tab4Frame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title="Trust M GUI", size=(1280, 720), style=(wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX)))
        self.Centre(wx.BOTH)
        main_menu_font = wx.Font(14, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.SetFont(main_menu_font)
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        
        # Instantiate all objects
        self.tab_base = wx.Notebook(self, id=wx.ID_ANY, style=wx.NB_TOP)
        self.tab1_metaupdate = Tab_MetaConfidentialUpdate(self.tab_base)
        self.tab2_keyupdate = Tab_KeyConfidentialUpdate(self.tab_base)
        self.tab3_aesupdate = Tab_AesConfidentialUpdate(self.tab_base)
        self.tab4_rsaupdate = Tab_RsaConfidentialUpdate(self.tab_base)
        self.tab5_dataupdate = Tab_DataUpdate(self.tab_base)
        
        # Add tabs
        self.tab_base.AddPage(self.tab1_metaupdate, 'Metadata Update')
        self.tab_base.AddPage(self.tab2_keyupdate, 'ECC Key Update')
        self.tab_base.AddPage(self.tab3_aesupdate, 'AES Key Update')
        self.tab_base.AddPage(self.tab4_rsaupdate, 'RSA Key Update')
        self.tab_base.AddPage(self.tab5_dataupdate, 'Data Update')
        
        self.Show(True) 


    def OnCloseWindow(self, evt):
        self.Parent.Show()
        self.Destroy()   # declare sizers that will be in the grid2
 
