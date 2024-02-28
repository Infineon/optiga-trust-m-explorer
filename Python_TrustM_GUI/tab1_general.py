import wx
import shell_util as exec_cmd
import misc_dialogs as misc
import images as img
import config
import binascii
from binascii import unhexlify
import os
import subprocess
import xml.dom.minidom
import math

class Tab_GEN(wx.Panel):
    
    oidList = ['E0C0', 'E0C1', 'E0C2', 'E0C5', 'E0C6', 'F1C1', 'F1C2', 'E0E0', 'E0E1', 'E0E2', 'E0E3', 'E0C4', 'E0C3', 'F1C0', 'E0C9', 'E0E8', 'E0E9', 'E0EF', 'E120', 'E121', 'E122', 'E123', 'F1D0', 'F1D1', 'F1D2', 'F1D3', 'F1D4', 'F1D5', 'F1D6', 'F1D7', 'F1D8', 'F1D9', 'F1DA', 'F1DB', 'F1E0', 'F1E1', 'E140', 'E0F0', 'E0F1', 'E0F2', 'E0F3', 'E0FC', 'E0FD', 'E200']
    specialOIDList = ['E0F0', 'E0F1', 'E0F2', 'E0F3', 'E0FC', 'E0FD', 'E200']
    chipSpecificOIDList = ['E0E0', 'E0C0', 'E0C1', 'E0C2', 'E0C3', 'E0C4', 'E0C5', 'E0C6', 'E0C9', 'F1C0', 'F1C1', 'F1C2'] 
    noDataOIDList = ['E0C2', 'E0C5', 'F1C2', 'E0F0', 'E0F1', 'E0F2', 'E0F3', 'E0FC', 'E0FD', 'E200']
        
    def __init__(self, parent):
        
        wx.Panel.__init__(self, parent)
        
        textctrlfont = wx.Font()
        textctrlfont.SetPointSize(10)
        
        buttonfont = wx.Font(12, wx.ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        
        # declare the sizers
        mainsizer = wx.BoxSizer(wx.VERTICAL)
        mainhorisizer = wx.BoxSizer(wx.HORIZONTAL)
        
        midsizer = wx.BoxSizer(wx.VERTICAL)
        gdsizer3 = wx.GridSizer(rows=7, cols=1, vgap=25, hgap=10)
        
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
        button_export_config = wx.Button(self, 1, 'Generate OPTIGA Trust Configurator Files', size = wx.Size(350, 50))
        button_export_config.SetFont(buttonfont)
        
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
        
        backbuttonsizer.Add(backbutton, 0, wx.ALIGN_LEFT | wx.ALIGN_BOTTOM, 0)
        backbuttonsizer.AddSpacer(10)
        backbuttonsizer.Add(clearbutton, 0, wx.ALIGN_LEFT | wx.ALIGN_BOTTOM, 0)

        # Add sizers to midsizer
        midsizer.AddSpacer(20)
        midsizer.Add(gdsizer3, 0, wx.ALIGN_CENTRE | wx.ALL, 10)
        
        midsizer.AddSpacer(33)
        midsizer.Add(backbuttonsizer,1,wx.LEFT | wx.BOTTOM, 5)
        
        #add buttons into gdsizer3
        gdsizer3.AddMany([
           # (self.button_step1),
           (self.button_chip),
           (button_meta),
           (button_data),
           (button_priv),
           (button_metastatus),
           (button_status),
           (button_export_config),
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
        button_export_config.Bind(wx.EVT_BUTTON, self.OnExportConfig)
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
        
        button_export_config.SetToolTip(wx.ToolTip("OPTIGA Trust Configurator(OTC) is a tool which can be used to generate customer specific configurations for Infineon Secure Elements. The OTC files generated here can be imported into infineon OPTIGA Trust Configurator to create custom security chip configurations"))
        
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
    
    def OnExportConfig(self, evt):
        frame = wx.Frame(None, -1, '*.*')
        frame.SetSize(0,0,200,50)
        
        saveFileDialog = wx.DirDialog(frame, "Save Config File Folders", "", wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        saveFileDialog.SetPath(config.IMAGEPATH + "/working_space/")
        
        
        if saveFileDialog.ShowModal() == wx.ID_CANCEL :
                return
        
        self.configFilePath = saveFileDialog.GetPath() + "/OPTIGA_Trust_M_V3_SLS32AIA010ML_K_Infineon_Technologies"
        
        saveFileDialog.Destroy()
        
        infoDialog = wx.MessageDialog(None, "Please import the generated folder into OPTIGA Trust Configurator for final configuration. OPTIGA Trust Configurator can be downloaded from Infineon website.\nPlease wait for several minutes when Exporting the configurations", "Generate files in OPTIGA Trust Configurator Tool tabs", wx.OK | wx.CANCEL | wx.ICON_INFORMATION)
        
        # if user changes mind
        if infoDialog.ShowModal() == wx.ID_CANCEL:
                return
        
        if (os.path.exists(self.configFilePath) == False):
                os.mkdir(self.configFilePath)
        
        print(self.configFilePath)
        
        self.text_display.write("Exporting the configuration of all data objects\n")
        
        wx.CallLater(10, self.OnExportConfigExec)
        
    def OnExportConfigExec(self):
        # constants for default parameters (customer contact, intermediate CAs)
        CUSTOMER_NAME = "Example Name"
        CUSTOMER_EMAIL = "example@email.com"
        CUSTOMER_COMPANY = "Example"
        CUSTOMER_PROJECT = "Example"
        #
        
        
        #self.text_display.write("Exporting all data objects into OTC File/n")
        # create xml file
        configFile = xml.dom.minidom.parseString("<OPTIGA/>")    
        
        # assign root node
        root = configFile.documentElement
            
        # tool version
        toolVer = configFile.createElement("Tool_Version")
        ver = configFile.createTextNode("1.00.0177")
        toolVer.appendChild(ver)
        root.appendChild(toolVer)
        
        # product tags
        product = configFile.createElement("Product")
        product.setAttribute("Version", "OPTIGA™ Trust M V3 (SLS32AIA010ML/K)")
        root.appendChild(product)
        
        
        # infineon contact
        contactInfineon = configFile.createElement("Contact_infineon")
        contactInfineon.setAttribute("Domain", "Infineon")
        product.appendChild(contactInfineon) # append contact_infineon to product
        
        # customer contact
        contactCustomer = configFile.createElement("Contact_customer")
        contactCustomer.setAttribute("Domain", "customer")
        product.appendChild(contactCustomer) # append contact_customer to product
        
        # contact details
        # infineon contact
        contactInfineonChild = configFile.createElement("Contact")
        
        contactInfineonFirstName = configFile.createElement("First_Name")
        contactInfineonFirstName.appendChild(configFile.createTextNode("Example Name"))
        
        contactInfineonEmail = configFile.createElement("Email")
        contactInfineonEmail.appendChild(configFile.createTextNode("example@email.com"))
        
        contactInfineonChild.appendChild(contactInfineonFirstName)
        contactInfineonChild.appendChild(contactInfineonEmail)    
        
        contactInfineon.appendChild(contactInfineonChild)
        
        # customer contact
        contactCustomerChild = configFile.createElement("Contact")
        
        contactCustomerFirstName = configFile.createElement("Name")
        contactCustomerFirstName.appendChild(configFile.createTextNode(CUSTOMER_NAME))
        
        contactCustomerEmail = configFile.createElement("Email")
        contactCustomerEmail.appendChild(configFile.createTextNode(CUSTOMER_EMAIL))
        
        contactCustomerCompany = configFile.createElement("Company")
        contactCustomerCompany.appendChild(configFile.createTextNode(CUSTOMER_COMPANY))
        
        contactCustomerProject = configFile.createElement("Project_Name")
        contactCustomerProject.appendChild(configFile.createTextNode(CUSTOMER_PROJECT))
        
        contactCustomerChild.appendChild(contactCustomerFirstName)
        contactCustomerChild.appendChild(contactCustomerEmail)    
        contactCustomerChild.appendChild(contactCustomerCompany)
        contactCustomerChild.appendChild(contactCustomerProject)
        
        contactCustomer.appendChild(contactCustomerChild)
        
        # chip config
        chipConfig = configFile.createElement("Chip_config")
        chipConfig.setAttribute("value", "product_config")
        product.appendChild(chipConfig)
        
        slaveAddr = configFile.createElement("Slave_Address")
        slaveAddr.appendChild(configFile.createTextNode("0x30"))
        
        tempVar = configFile.createElement("Temp_Variant")
        tempVar.appendChild(configFile.createTextNode("STR (Standard, -25°c to +85°c)"))
        
        chipLabel = configFile.createElement("Chip_Label")
        chipLabel.appendChild(configFile.createTextNode("01"))
        
        chipIDName = configFile.createElement("Chip_Id_Name")
        chipIDName.setAttribute("user_modified", "false")
        chipIDName.appendChild(configFile.createTextNode("TMS30"))
        
        chipConfig.appendChild(slaveAddr)
        chipConfig.appendChild(tempVar)
        chipConfig.appendChild(chipLabel)
        chipConfig.appendChild(chipIDName)
        
        # objects tag for oids
        objects = configFile.createElement("objects")
        product.appendChild(objects)
            
        # write oid data into .dat and xml files 
        for oid in self.oidList:
                targetOID = "0x" + oid
                errorOutput = "Error"
                hasData = False
                startData = False
                
                ##########################################################################################################
                # if the current oid is not a speical oid (cannot read data and/or no meaningful data)
                if (oid not in self.noDataOIDList):
                        dataToWrite = ""
                        commandDataOutput = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_data", "-r", targetOID, "-X"])
                        decodedDataOutput = commandDataOutput.decode()
                        
                        # if the data inside cannot be read -> skip
                        if (errorOutput not in decodedDataOutput):
                                # has data
                                hasData = True
                        
                                ###########
                                self.text_display.write("Exporting data from OID " + oid)
                                ###########
                        
                                # reading each line in command output
                                for line in decodedDataOutput:
                                        # the colon ':' stats the data section of the command output
                                        if (line == ':'):
                                                startData = True
                                                continue
                                                
                                        # the '=' ends the data section of the command output
                                        if (line == '=' and startData == True):
                                                break
                                        
                                        # skip the spaces 
                                        if (line == ' '):
                                                continue
                                        
                                        # append to data output
                                        if (startData == True):
                                                dataToWrite += line
                                                                                    
                                # write output data to .dat file
                                with open(self.configFilePath + "/" + oid + ".dat", "w") as file:
                                        file.write(dataToWrite)
                                
                                # text cmd output
                                self.text_display.write(" ... done\n")
                                
                #########################################################################################################
                
                ###########
                self.text_display.write("Exporting metadata from OID " + oid)
                ###########
                
                # writing to xml
                commandMetadataOutput = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_metadata", "-r", targetOID, "-X"])
                decodedMetadataOutput = commandMetadataOutput.decode()
                
                # get the output lines by lists
                lines = decodedMetadataOutput.splitlines()
                metadataLineCount = 0 # counter to skip first 4 lines 
                metadataToWrite = ""
                
                # get the size of the metadata
                size = int(lines[4][6:10])
                lineLimit = math.ceil(size / 16.0)
                
                
                # reading line by line
                for line in lines[5:]:
                        # increase line count
                        metadataLineCount += 1
                        
                        # if we are still within limit of metadata
                        if (metadataLineCount <= lineLimit):
                                metadataToWrite += line.strip() + " "
                
                # remove headers from metadata        
                metadataToWrite.replace(" ", "")
                metadataToWrite = metadataToWrite[6:]
                
                # remove read tags for private key oids
                if (oid in self.specialOIDList):
                        readTagIndex = metadataToWrite.find("D1")
                
                        # if read tag exists
                        if (readTagIndex > -1):
                                # get size in bytes of the read tag
                                readTagSize = int(metadataToWrite[readTagIndex + 3:readTagIndex + 5])
                                
                                # find the substring of the read tag
                                readTag = metadataToWrite[readTagIndex:(readTagIndex + (4 + 3 * readTagSize) + 1)]
                                
                                # and remove the read tag altogether
                                metadataToWrite = metadataToWrite.replace(readTag, "")
                
                # actual parsing to xml file
                objectID = configFile.createElement("oid")
                objectID.setAttribute("id", oid)
                objects.appendChild(objectID)
                
                metadata = configFile.createElement("metadata")
                metadata.setAttribute("value", "Updated_Tags")
                metadata.appendChild(configFile.createTextNode(metadataToWrite))
                objectID.appendChild(metadata)
                
                data = configFile.createElement("data")
                if (hasData == True and oid not in self.chipSpecificOIDList):
                        data.setAttribute("data_from", "Customer")
                        data.setAttribute("value", "Updated")
                        #data.appendChild(configFile.createTextNode(oid + ".dat"))
                else:
                        data.setAttribute("data_from", "Infineon")
                        data.setAttribute("value", "Default")
                        #data.appendChild(configFile.createTextNode(""))
                        
                if (hasData == True):
                        data.appendChild(configFile.createTextNode(oid + ".dat"))
                
                else:
                        data.appendChild(configFile.createTextNode(""))
                        
                data.setAttribute("type", "Plain")
                data.setAttribute("chip_individual", "false")
                        
                objectID.appendChild(data)
                
                if (oid == 'E200'):
                        cryptMode = configFile.createElement("Crypto-Mode")
                        cryptMode.appendChild(configFile.createTextNode("AES_ECB"))
                        plaintext = configFile.createElement("Plain-Text")
                        ciphertext = configFile.createElement("Cipher-Text")
                        
                        objectID.appendChild(cryptMode)
                        objectID.appendChild(plaintext)
                        objectID.appendChild(ciphertext)
                        
                # text cmd output
                self.text_display.write(" ... done\n")
        
        # default keypair configuration 
        keypairs = configFile.createElement("keypairs")
        #keypairs.appendChild(configFile.createTextNode(""))
        
        # create keypair node
        keypair = configFile.createElement("keypair")
        keypairs.appendChild(keypair)
        
        # algo tag
        algo = configFile.createElement("algo")
        keypair.appendChild(algo)
        algo.setAttribute("required", "true")
        algo.appendChild(configFile.createTextNode("Elliptic Curve - NIST P 256"))
        
        # keypair name tag
        keypairName = configFile.createElement("keypair-name")
        keypair.appendChild(keypairName)
        keypairName.appendChild(configFile.createTextNode("E0F0-E0E0"))
        
        # private key tag
        privateKey = configFile.createElement("private-key")
        keypair.appendChild(privateKey)
        privateKey.appendChild(configFile.createTextNode("E0F0"))
        
        # public key tag
        publicKey = configFile.createElement("public-key")
        keypair.appendChild(publicKey)
        publicKey.appendChild(configFile.createTextNode("E0E0"))
        
        # cert type tag
        certType = configFile.createElement("cert-type")
        keypair.appendChild(certType)
        certType.appendChild(configFile.createTextNode("TLS Identity Certificate"))
        
        # cert chain tag
        certChain = configFile.createElement("cert-chain")
        keypair.appendChild(certChain)
        certChain.appendChild(configFile.createTextNode("XX"))
        
        # trust anchor
        trustAnchor = configFile.createElement("trust-Anchor")
        keypair.appendChild(trustAnchor)
        
        # root CA: signed by Infineon
        rootCA = configFile.createElement("root-ca")
        trustAnchor.appendChild(rootCA)
        rootCA.setAttribute("required", "true")
        rootCA.appendChild(configFile.createTextNode("Signed by Infineon"))

        # algo tag
        algo = configFile.createElement("algo")
        trustAnchor.appendChild(algo)
        algo.setAttribute("required", "true")
        algo.appendChild(configFile.createTextNode("Elliptic Curve - NIST P 384"))
        
        # trust-anchor tag
        # different style to avoid mismatching
        trustanchor = configFile.createElement("trust-anchor")
        trustAnchor.appendChild(trustanchor)
        
        # todo: add info to ask customer to double check and edit in contact + keypair tab
        trustanchor.appendChild(configFile.createTextNode(CUSTOMER_COMPANY + " IntermediateCA.pem"))
        
        # subject tab
        subject = configFile.createElement("subject")
        trustAnchor.appendChild(subject)
                
        # common name tag
        commonName = configFile.createElement("common-name")
        subject.appendChild(commonName)
        commonName.setAttribute("required", "true")
        commonName.appendChild(configFile.createTextNode(CUSTOMER_COMPANY + " IntermediateCA"))
        
        # email address tag
        emailAddr = configFile.createElement("email-address")
        subject.appendChild(emailAddr)
        
        # serial number tag
        serialNumber = configFile.createElement("serial-number")
        subject.appendChild(serialNumber)
        serialNumber.appendChild(configFile.createTextNode("17095fce"))
        
        # given name tag
        givenName = configFile.createElement("given-name")
        subject.appendChild(givenName)
        givenName.appendChild(configFile.createTextNode(""))
        
        # surname tag
        surname = configFile.createElement("surname")
        subject.appendChild(surname)
        surname.appendChild(configFile.createTextNode(""))
        
        # locality tag
        locality = configFile.createElement("locality")
        subject.appendChild(locality)
        locality.appendChild(configFile.createTextNode(""))
        
        # organization unit name
        orgUnitName = configFile.createElement("organization-unit-name")
        subject.appendChild(orgUnitName)
        orgUnitName.appendChild(configFile.createTextNode("OPTIGA (TM)"))
        
        # organization name
        orgName = configFile.createElement("organization-name")
        subject.appendChild(orgName)
        orgName.appendChild(configFile.createTextNode(CUSTOMER_COMPANY))
        
        # state province tags
        state = configFile.createElement("state-province")
        subject.appendChild(state)
        state.appendChild(configFile.createTextNode(""))
        
        # country name tags
        country = configFile.createElement("country-name")
        subject.appendChild(country)
        country.appendChild(configFile.createTextNode(""))
        
        # validity tags
        validity = configFile.createElement("validity")
        trustAnchor.appendChild(validity)
        
        validFrom = configFile.createElement("valid-from")
        validity.appendChild(validFrom)
        validFrom.appendChild(configFile.createTextNode("2020-08-07"))
        
        validTill = configFile.createElement("valid-till")
        validity.appendChild(validTill)
        validTill.appendChild(configFile.createTextNode("2050-08-07"))
        
        # basic constraints tab
        basicConstraints = configFile.createElement("basic-constraints")
        trustAnchor.appendChild(basicConstraints)
        
        # critical
        critical = configFile.createElement("critical")
        basicConstraints.appendChild(critical)
        critical.appendChild(configFile.createTextNode("false"))
        
        # ca cert
        caCert = configFile.createElement("ca-cert")
        basicConstraints.appendChild(caCert)
        caCert.appendChild(configFile.createTextNode("true"))

        # path length
        pathLength = configFile.createElement("path-length")
        basicConstraints.appendChild(pathLength)
        pathLength.appendChild(configFile.createTextNode("0"))
        
        # authority key id tag
        authKeyId = configFile.createElement("authority-key-id")
        trustAnchor.appendChild(authKeyId)
        
        # critical 
        authKeyCrit = configFile.createElement("critical")
        authKeyId.appendChild(authKeyCrit)
        authKeyCrit.appendChild(configFile.createTextNode("false"))
        
        # key id
        keyId = configFile.createElement("key-id")
        authKeyId.appendChild(keyId)
        keyId.appendChild(configFile.createTextNode("82b83dcc71b83e7ef69cd61dc84d5232706cc79d"))

        # name and sn
        nameSn = configFile.createElement("name-and-sn")
        authKeyId.appendChild(nameSn)
        nameSn.appendChild(configFile.createTextNode(""))
        
        # cert policy
        certPolicy = configFile.createElement("certificate-policy")
        trustAnchor.appendChild(certPolicy)
        
        # cert policy critical
        certPolicyCrit = configFile.createElement("critical")
        certPolicy.appendChild(certPolicyCrit)
        certPolicyCrit.appendChild(configFile.createTextNode("false"))
        
        # object id
        certPolicyObject = configFile.createElement("object-id")
        certPolicy.appendChild(certPolicyObject)
        certPolicyObject.appendChild(configFile.createTextNode("1.2.276.0.68.1.20.1"))
        
        # cps-uri tag
        cpsuri = configFile.createElement("cps-uri")
        certPolicy.appendChild(cpsuri)
        cpsuri.appendChild(configFile.createTextNode(""))
        
        # user notice tag
        usernotice = configFile.createElement("user-notice")
        certPolicy.appendChild(usernotice)
        usernotice.appendChild(configFile.createTextNode(""))
        
        # ca-crl-distribution tag
        caCrlDist = configFile.createElement("ca-crl-distribution")
        trustAnchor.appendChild(caCrlDist)
        
        # crit
        caCrlDistCrit = configFile.createElement("critical")
        caCrlDist.appendChild(caCrlDistCrit)
        caCrlDistCrit.appendChild(configFile.createTextNode("false"))
        
        # url tag
        url = configFile.createElement("url")
        caCrlDist.appendChild(url)
        url.appendChild(configFile.createTextNode(""))
        
        # issuer 
        issuer = configFile.createElement("issuer")
        caCrlDist.appendChild(issuer)
        issuer.appendChild(configFile.createTextNode(""))
        
        # cert template tag
        certTemplate = configFile.createElement("cert-template")
        trustAnchor.appendChild(certTemplate)

        # critical
        certTemplateCrit = configFile.createElement("critical")
        certTemplate.appendChild(certTemplateCrit)
        certTemplateCrit.appendChild(configFile.createTextNode("false"))
        
        # extension-val tag
        extension = configFile.createElement("extension-val")
        certTemplate.appendChild(extension)
        extension.appendChild(configFile.createTextNode(""))
        
        # key usage
        keyUsage = configFile.createElement("key-usage")
        trustAnchor.appendChild(keyUsage)
        
        # critical
        keyUsageCrit = configFile.createElement("critical")
        keyUsage.appendChild(keyUsageCrit)
        keyUsageCrit.appendChild(configFile.createTextNode("true"))
        
        # digital signature
        digitalSig = configFile.createElement("digital-signature")
        keyUsage.appendChild(digitalSig)
        digitalSig.appendChild(configFile.createTextNode("false"))
                
        # non repudiation tag
        nonRepudiation = configFile.createElement("non-repudiation")
        keyUsage.appendChild(nonRepudiation)
        nonRepudiation.appendChild(configFile.createTextNode("false"))        
        
        # key enchipherment tag
        keyEnchipherment = configFile.createElement("key-enchipherment")
        keyUsage.appendChild(keyEnchipherment)
        keyEnchipherment.appendChild(configFile.createTextNode("false"))
        
        # data enchipherment tag
        dataEnchipherment = configFile.createElement("data-enchipherment")
        keyUsage.appendChild(dataEnchipherment)
        dataEnchipherment.appendChild(configFile.createTextNode("false"))
        
        # key agreement tag
        keyAgreement = configFile.createElement("key-agreement")
        keyUsage.appendChild(keyAgreement)
        keyAgreement.appendChild(configFile.createTextNode("false"))
        
        # certificate signing tag
        certSigning = configFile.createElement("certificate-signing")
        keyUsage.appendChild(certSigning)
        certSigning.appendChild(configFile.createTextNode("true"))
        
        # crl-signing tag
        crlSigning = configFile.createElement("crl-signing")
        keyUsage.appendChild(crlSigning)
        crlSigning.appendChild(configFile.createTextNode("false"))
        
        # enipher only tag
        encipherOnly = configFile.createElement("encipher-only")
        keyUsage.appendChild(encipherOnly)
        encipherOnly.appendChild(configFile.createTextNode("false"))
        
        # decipher only tag
        decipherOnly = configFile.createElement("decipher-only")
        keyUsage.appendChild(decipherOnly)
        decipherOnly.appendChild(configFile.createTextNode("false"))
        
        # device certificate
        deviceCert = configFile.createElement("device-cert")
        keypair.appendChild(deviceCert)
        
        # subject tag
        subject = configFile.createElement("subject")
        deviceCert.appendChild(subject)
        
        # common name tag
        commonName = configFile.createElement("common-name")
        commonName.setAttribute("required", "true")
        subject.appendChild(commonName)
        commonName.appendChild(configFile.createTextNode(CUSTOMER_COMPANY + " IoTNode"))
        
        # email address
        emailAddr = configFile.createElement("email-address")
        subject.appendChild(emailAddr)
        emailAddr.appendChild(configFile.createTextNode(""))
                
        # serial number
        serialNumber = configFile.createElement("serial-number")
        subject.appendChild(serialNumber)
        serialNumber.appendChild(configFile.createTextNode(""))
        
        # given name
        givenName = configFile.createElement("given-name")
        subject.appendChild(givenName)
        givenName.appendChild(configFile.createTextNode(""))
        
        # surname
        surname = configFile.createElement("surname")
        subject.appendChild(surname)
        surname.appendChild(configFile.createTextNode(""))
        
        # locality
        locality = configFile.createElement("locality")
        subject.appendChild(locality)
        locality.appendChild(configFile.createTextNode(""))
        
        # organization unit name
        organizationUnitName = configFile.createElement("organization-unit-name")
        subject.appendChild(organizationUnitName)
        organizationUnitName.appendChild(configFile.createTextNode(""))
        
        # organization name
        organizationName = configFile.createElement("organization-name")
        subject.appendChild(organizationName)
        organizationName.appendChild(configFile.createTextNode(CUSTOMER_COMPANY))
        
        # state province
        stateProvince = configFile.createElement("state-province")
        subject.appendChild(stateProvince)
        stateProvince.appendChild(configFile.createTextNode(""))
        
        # country name
        country = configFile.createElement("country-name")
        subject.appendChild(country)
        country.appendChild(configFile.createTextNode(""))
        
        # basic constraints tab
        basicConstraints = configFile.createElement("basic-constraints")
        deviceCert.appendChild(basicConstraints)
        
        # critical
        critical = configFile.createElement("critical")
        basicConstraints.appendChild(critical)
        critical.appendChild(configFile.createTextNode("false"))
        
        # ca cert
        caCert = configFile.createElement("ca-cert")
        basicConstraints.appendChild(caCert)
        caCert.appendChild(configFile.createTextNode("true"))

        # path length
        pathLength = configFile.createElement("path-length")
        basicConstraints.appendChild(pathLength)
        pathLength.appendChild(configFile.createTextNode("0"))
        
        # authority key id tag
        authKeyId = configFile.createElement("authority-key-id")
        deviceCert.appendChild(authKeyId)
        
        # critical 
        authKeyCrit = configFile.createElement("critical")
        authKeyId.appendChild(authKeyCrit)
        authKeyCrit.appendChild(configFile.createTextNode("false"))
        
        # key id
        keyId = configFile.createElement("key-id")
        authKeyId.appendChild(keyId)
        keyId.appendChild(configFile.createTextNode(""))

        # name and sn
        nameSn = configFile.createElement("name-and-sn")
        authKeyId.appendChild(nameSn)
        nameSn.appendChild(configFile.createTextNode(""))
        
        # cert policy
        certPolicy = configFile.createElement("certificate-policy")
        deviceCert.appendChild(certPolicy)
        
        # cert policy critical
        certPolicyCrit = configFile.createElement("critical")
        certPolicy.appendChild(certPolicyCrit)
        certPolicyCrit.appendChild(configFile.createTextNode("false"))
        
        # object id
        certPolicyObject = configFile.createElement("object-id")
        certPolicy.appendChild(certPolicyObject)
        certPolicyObject.appendChild(configFile.createTextNode(""))
        
        # cps-uri tag
        cpsuri = configFile.createElement("cps-uri")
        certPolicy.appendChild(cpsuri)
        cpsuri.appendChild(configFile.createTextNode(""))
        
        # user notice tag
        usernotice = configFile.createElement("user-notice")
        certPolicy.appendChild(usernotice)
        usernotice.appendChild(configFile.createTextNode(""))
        
        # ca-crl-distribution tag
        caCrlDist = configFile.createElement("crl-distribution")
        deviceCert.appendChild(caCrlDist)
        
        # crit
        caCrlDistCrit = configFile.createElement("critical")
        caCrlDist.appendChild(caCrlDistCrit)
        caCrlDistCrit.appendChild(configFile.createTextNode("false"))
        
        # url tag
        url = configFile.createElement("url")
        caCrlDist.appendChild(url)
        url.appendChild(configFile.createTextNode(""))
        
        # issuer 
        issuer = configFile.createElement("issuer")
        caCrlDist.appendChild(issuer)
        issuer.appendChild(configFile.createTextNode(""))
        
        # cert template tag
        certTemplate = configFile.createElement("cert-template")
        deviceCert.appendChild(certTemplate)

        # critical
        certTemplateCrit = configFile.createElement("critical")
        certTemplate.appendChild(certTemplateCrit)
        certTemplateCrit.appendChild(configFile.createTextNode("false"))
        
        # extension-val tag
        extension = configFile.createElement("extension-val")
        certTemplate.appendChild(extension)
        extension.appendChild(configFile.createTextNode(""))
        
        # key usage
        keyUsage = configFile.createElement("key-usage")
        deviceCert.appendChild(keyUsage)
        
        # critical
        keyUsageCrit = configFile.createElement("critical")
        keyUsage.appendChild(keyUsageCrit)
        keyUsageCrit.appendChild(configFile.createTextNode("true"))
        
        # digital signature
        digitalSig = configFile.createElement("digital-signature")
        keyUsage.appendChild(digitalSig)
        digitalSig.appendChild(configFile.createTextNode("true"))
                
        # non repudiation tag
        nonRepudiation = configFile.createElement("non-repudiation")
        keyUsage.appendChild(nonRepudiation)
        nonRepudiation.appendChild(configFile.createTextNode("false"))        
        
        # key enchipherment tag
        keyEnchipherment = configFile.createElement("key-enchipherment")
        keyUsage.appendChild(keyEnchipherment)
        keyEnchipherment.appendChild(configFile.createTextNode("false"))
        
        # data enchipherment tag
        dataEnchipherment = configFile.createElement("data-enchipherment")
        keyUsage.appendChild(dataEnchipherment)
        dataEnchipherment.appendChild(configFile.createTextNode("false"))
        
        # key agreement tag
        keyAgreement = configFile.createElement("key-agreement")
        keyUsage.appendChild(keyAgreement)
        keyAgreement.appendChild(configFile.createTextNode("false"))
        
        # certificate signing tag
        certSigning = configFile.createElement("certificate-signing")
        keyUsage.appendChild(certSigning)
        certSigning.appendChild(configFile.createTextNode("false"))
        
        # crl-signing tag
        crlSigning = configFile.createElement("crl-signing")
        keyUsage.appendChild(crlSigning)
        crlSigning.appendChild(configFile.createTextNode("false"))
        
        # enipher only tag
        encipherOnly = configFile.createElement("encipher-only")
        keyUsage.appendChild(encipherOnly)
        encipherOnly.appendChild(configFile.createTextNode("false"))
        
        # deipher only tag
        decipherOnly = configFile.createElement("decipher-only")
        keyUsage.appendChild(decipherOnly)
        decipherOnly.appendChild(configFile.createTextNode("false"))
        
        # ext key usage tag
        extKeyUsage = configFile.createElement("ext-key-usage")
        deviceCert.appendChild(extKeyUsage)
        
        # critical 
        critical = configFile.createElement("critical")
        extKeyUsage.appendChild(critical)
        critical.appendChild(configFile.createTextNode("false"))
        
        # server auth
        serverAuth = configFile.createElement("server-auth")
        extKeyUsage.appendChild(serverAuth)
        serverAuth.appendChild(configFile.createTextNode("false"))
        
        # email protection 
        emailProtection = configFile.createElement("email-protection")
        extKeyUsage.appendChild(emailProtection)
        emailProtection.appendChild(configFile.createTextNode("false"))
        
        # client auth
        clientAuth = configFile.createElement("client-auth")
        extKeyUsage.appendChild(clientAuth)
        clientAuth.appendChild(configFile.createTextNode("false"))
        
        # time stamping
        timeStamp = configFile.createElement("time-stamping")
        extKeyUsage.appendChild(timeStamp)
        timeStamp.appendChild(configFile.createTextNode("false"))
        
        # code signing
        codeSign  = configFile.createElement("code-signing")
        extKeyUsage.appendChild(codeSign)
        codeSign.appendChild(configFile.createTextNode("false"))

        # ocp signing
        ocpSign = configFile.createElement("ocp-signing")
        extKeyUsage.appendChild(ocpSign)
        ocpSign.appendChild(configFile.createTextNode("false"))
        
        # validity
        validity = configFile.createElement("validity")
        deviceCert.appendChild(validity)
        
        # valid duration
        validDuration = configFile.createElement("valid-duration")
        validity.appendChild(validDuration)
        validDuration.setAttribute("required", "true")
        validDuration.appendChild(configFile.createTextNode("240"))
        

        #
        
        additionalInfo = configFile.createElement("additional_info")
        additionalInfo.appendChild(configFile.createTextNode(""))
        
        product.appendChild(keypairs)
        product.appendChild(additionalInfo)
        
        
        # misc
        common = configFile.createElement("common")
        product.appendChild(common)

        # save to xml file
        with open(self.configFilePath + "/OTC.xml", "w") as file:
                file.write(configFile.toprettyxml())
         
        self.text_display.AppendText("\n+++++++++++++++++++++++++++++++++++++++++++++++++++++")        
        self.text_display.AppendText("\nGenerated OTC file at " + self.configFilePath + "\n")
        self.text_display.AppendText("+++++++++++++++++++++++++++++++++++++++++++++++++++++")
    
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
        
        textctrlfont1 = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD,)
        
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
        text_pubkey = wx.StaticText(self, 0, "Public Key Certificate")
        
        self.pubkey = wx.ComboBox(self, 1, choices=pubkey_list, style=wx.CB_READONLY,  size = wx.Size(180, 30))
        self.pubkey.SetFont(textctrlfont)
        
        text_keyslot = wx.StaticText(self, 0, "Key Slot")
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
        
        backbuttonsizer.Add(backbutton, 0, wx.ALIGN_LEFT | wx.ALIGN_BOTTOM, 0)
        backbuttonsizer.AddSpacer(10)
        backbuttonsizer.Add(clearbutton, 0, wx.ALIGN_LEFT | wx.ALIGN_BOTTOM, 0)

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
        
        midsizer.AddSpacer(10)
        midsizer.Add(backbuttonsizer,1,wx.LEFT | wx.BOTTOM, 5)
        
        
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
        keyslotsizer.Add(text_keyslot, 1, wx.EXPAND)
        keyslotsizer.Add(self.keyslot)
        
        pubkeysizer.Add(text_pubkey, 1, wx.EXPAND)
        pubkeysizer.Add(self.pubkey)
        
        trustancsizer.Add(text_trustanc, 1, wx.EXPAND)
        trustancsizer.Add(self.trustanc)
        
        fileinputsizer.Add(text_filename_input, 1, wx.EXPAND)
        fileinputsizer.Add(self.filename_input)
        
        secretfilesizer.Add(text_secretfile, 1, wx.EXPAND)
        secretfilesizer.Add(self.secretfile)
        
        bindsizer.Add(text_bindsecret, 1, wx.EXPAND)
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
        
        command_output = exec_cmd.createProcess(f"python3 hex_to_binary.py {'0102030405060708090A0B0C0D0E0F101112131415161718191A1B1C1D1E1F202122232425262728292A2B2C2D2E2F303132333435363738393A3B3C3D3E3F40'} > platform_secret.dat")
        
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
        inputtext.SetMinSize((100, -1))
        self.input_display = wx.TextCtrl(self,value="1234")
        self.input_display.SetFont(textctrlfont)
        self.input_display.SetMaxSize((-1, 30))
        
        
        self.text_display = wx.TextCtrl(self, -1, style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.text_display.SetFont(wx.Font(11, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))


        clearimage = wx.Image(config.IMAGEPATH + "/images/clear.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        clearbutton = wx.BitmapButton(self, -1, clearimage)

        
        backimage = wx.Image(config.IMAGEPATH + "/images/back.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        backbutton = wx.BitmapButton(self, -1, backimage)
       
        #Add mainhorisizer to mainsizer
        mainsizer.AddSpacer(2)
        mainsizer.Add(input_sizer, 1, wx.EXPAND | wx.TOP, 5)
        mainsizer.Add(mainhorisizer, 1, wx.EXPAND)
        input_sizer.AddSpacer(20)
        input_sizer.Add(inputtext, 0, wx.EXPAND  | wx.TOP, 10)
        input_sizer.Add(self.input_display, 1 ,wx.EXPAND | wx.TOP, 5)
        
       
        # Add Sub Sizers to the mainhorisizer
        mainhorisizer.Add(midsizer, 1, wx.EXPAND )
        mainhorisizer.Add(self.text_display, 2, wx.EXPAND | wx.ALL, 5)
      
        backbuttonsizer.Add(backbutton, 0, wx.ALIGN_LEFT | wx.ALIGN_BOTTOM, 0)
        backbuttonsizer.AddSpacer(10)
        backbuttonsizer.Add(clearbutton, 0, wx.ALIGN_LEFT | wx.ALIGN_BOTTOM, 0)

        # Add sizers to midsizer
        midsizer.AddSpacer(10)
        
        
        midsizer.AddSpacer(10)
        midsizer.Add(gdsizer2, 0, wx.ALIGN_CENTRE | wx.ALL, 10)
        
        
        midsizer.AddSpacer(30)
        midsizer.Add(gdsizer3, 0, wx.ALIGN_CENTRE | wx.ALL, 10)
        
        midsizer.AddSpacer(100)
        midsizer.Add(backbuttonsizer,1,wx.LEFT | wx.BOTTOM, 5)
        
        
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
        datasizer.Add(text_data, 1, wx.EXPAND)
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
        
        exec_cmd.createProcess("echo " + datain + " >writedata.txt")                               
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
        gdsizer1 = wx.GridSizer(rows=3, cols=2, vgap=5, hgap=20)
        #gdsizer2 = wx.GridSizer(rows=3, cols=2, vgap=10, hgap=20)
        gdsizer2 = wx.GridSizer(cols=2, vgap=5, hgap=20)
        
        gdsizer3 = wx.GridSizer(rows=1, cols=1, vgap=5, hgap=20)
        gdsizer4 = wx.GridSizer(rows = 1, cols = 1, vgap = 5, hgap = 20)
        gdsizer5 = wx.GridSizer(rows=1, cols=2, vgap=5, hgap=20)
        gdsizer6 = wx.GridSizer(rows=1, cols=1, vgap=0, hgap=20)
        gdsizer7 = wx.GridSizer(rows=1, cols=2, vgap=5, hgap=20)
        gdsizer8 = wx.GridSizer(rows=1, cols=2, vgap=2, hgap=20)
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
        
        backbuttonsizer.Add(backbutton, 0, wx.ALIGN_LEFT | wx.ALIGN_BOTTOM, 0)
        backbuttonsizer.AddSpacer(10)
        backbuttonsizer.Add(clearbutton, 0, wx.ALIGN_LEFT | wx.ALIGN_BOTTOM, 0)

        # Add sizers to midsizer
        midsizer.AddSpacer(2)
        midsizer.Add(gdsizer1, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        midsizer.AddSpacer(2)
        midsizer.Add(gdsizer2, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        
        midsizer.AddSpacer(0)
        midsizer.Add(gdsizer3, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        
        midsizer.AddSpacer(0)
        midsizer.Add(gdsizer4, 0, wx.LEFT | wx.ALL, 2)
        
        midsizer.AddSpacer(0)
        midsizer.Add(gdsizer5, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        #midsizer.AddSpacer()
        midsizer.Add(gdsizer6, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        midsizer.AddSpacer(2)
        midsizer.Add(gdsizer7, 0, wx.ALIGN_CENTRE | wx.ALL, 2)
        midsizer.AddSpacer(2)
        midsizer.Add(gdsizer8, 0, wx.ALIGN_CENTRE | wx.ALL, 2)
        #midsizer.AddSpacer(5)
        #midsizer.Add(gdsizer8, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        midsizer.AddSpacer(5)
        midsizer.Add(backbuttonsizer,1,wx.LEFT | wx.BOTTOM, 5)
        
        
        
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
        sysdatasizer.Add(text_sysdata, 1, wx.EXPAND)
        sysdatasizer.Add(self.sysdata)
        
        counterobjsizer.Add(text_counterobj, 1, wx.EXPAND)
        counterobjsizer.Add(self.counterobj)
        
        keysizer.Add(text_key, 1, wx.EXPAND)
        keysizer.Add(self.key)
        
        certsizer.Add(text_cert, 1, wx.EXPAND)
        certsizer.Add(self.cert)
        gendataobjsizer.Add(text_gendataobj, 1, wx.EXPAND)
        gendataobjsizer.Add(self.gendataobj)
        
        bindsecretsizer.Add(text_bindsecret, 1, wx.EXPAND)
        bindsecretsizer.Add(self.bindsecret)
        
        lcs0sizer.Add(text_lcs0, 1, wx.EXPAND)
        lcs0sizer.Add(self.lcs0)
        changesizer.Add(text_change, 1, wx.EXPAND)
        changesizer.Add(self.change)
        readsizer.Add(text_read, 1, wx.EXPAND)
        readsizer.Add(self.read)
        exesizer.Add(text_exe, 1, wx.EXPAND)
        exesizer.Add(self.exe)
        file_sizer.Add(self.custom_metadata_input)

        
        # oid datatype sizer
        datatypesizer.Add(text_oid_datatype, 1, wx.EXPAND)
        datatypesizer.Add(self.oid_datatype)
        #
        


        #add objects into sizers in gdsizer2
        trustoidsizer.Add(text_trust_anchor_oid, 1, wx.EXPAND)
        trustoidsizer.Add(self.trust_anchor_oid)
#         targetoidsizer.Add(text_target_oid)
#         targetoidsizer.Add(self.target_oid)
        secretoidsizer.Add(text_secret_oid, 1, wx.EXPAND)
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
        command_output = exec_cmd.createProcess(f"python3 hex_to_binary.py {TRUST_ANCHOR_META} > trust_anchor_metadata.bin")
        self.text_display.AppendText("'python3 hex_to_binary.py {TRUST_ANCHOR_META} > trust_anchor_metadata.bin' executed \n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
        
        self.text_display.AppendText("Writing trust_anchor_metadata.bin as metadata of Trust Anchor OID... \n")
        command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_metadata", "-w", trust_anchor_oid, "-F", "trust_anchor_metadata.bin", ])
        self.text_display.AppendText(command_output)
        self.text_display.AppendText("'trustm_metadata -w 0x" + trust_anchor_oid + " -F trust_anchor_metadata.bin'" + " executed \n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
        
        
        #Step2: Provisioning metadata for Protected Update Secret OID
        self.text_display.AppendText("Provisioning for protected update secret metadata... \n")
        command_output = exec_cmd.createProcess(f"python3 hex_to_binary.py {PROTECTED_UPDATE_SECRET_META} > protected_update_secret_metadata.bin")
        self.text_display.AppendText("'python3 hex_to_binary.py {PROTECTED_UPDATE_SECRET_META} > protected_update_secret_metadata.bin' executed \n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
        
        self.text_display.AppendText("Writing protected update secret metadata into secret_oid... ")
        command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_metadata", "-w", secret_oid, "-F", "protected_update_secret_metadata.bin", ])
        self.text_display.AppendText(command_output)
        self.text_display.AppendText("'trustm_metadata -w " + secret_oid + " -F protected_update_secret_metadata.bin' executed \n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
        
        ##Set metadata for Target OID
        self.text_display.AppendText("Set metadata protected update for Target OID (Provision for Target OID)... \n")
        command_output = exec_cmd.createProcess(f"python3 hex_to_binary.py {TARGET_OID_META} > targetOID_metadata.bin")
        self.text_display.AppendText("'python3 hex_to_binary.py {TARGET_OID_META} > targetOID_metadata.bin' executed \n")
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
        exec_cmd.createProcess(f"python3 hex_to_binary.py {RESET_MUD_META} > mud_reset.bin")
        command_output = exec_cmd.execCLI(["python3", "emulator.py", "mud_reset.bin", ])
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
                                try:
                                        fout.write(unhexlify(''.join(line.split())))
                                
                                except binascii.Error:
                                        wx.CallLater(10, self.OnInvalidCustomMetadata)
                                        return
                                        
                command_output = exec_cmd.execCLI(["hd", customMetadataBin,])
                self.text_display.AppendText("Contents of the custom metadata file:\n")
                self.text_display.AppendText(command_output)
                
        except AttributeError:
                wx.CallLater(10, self.OnNoMetadataFileSelected)
                
    def OnNoMetadataFileSelected(self):
        infoDialog = wx.MessageDialog(None, "Select Metadata File to Write to Target OID", "No Metadata File Selected", wx.OK | wx.ICON_INFORMATION)
        infoDialog.ShowModal()
        
    def OnInvalidCustomMetadata(self):
        infoDialog = wx.MessageDialog(None, "Double check metadata file to ensure it contains only hex strings", "Invalid metadata file", wx.OK | wx.ICON_INFORMATION)
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
        
        
class Tab_PROV(wx.Panel):
    
    oidList = ['E0C0', 'E0C1', 'E0C2', 'E0C5', 'E0C6', 'F1C1', 'F1C2', 'E0E0', 'E0E1', 'E0E2', 'E0E3', 'E0C4', 'E0C3', 'F1C0', 'E0C9', 'E0E8', 'E0E9', 'E0EF', 'E120', 'E121', 'E122', 'E123', 'F1D0', 'F1D1', 'F1D2', 'F1D3', 'F1D4', 'F1D5', 'F1D6', 'F1D7', 'F1D8', 'F1D9', 'F1DA', 'F1DB', 'F1E0', 'F1E1', 'E140', 'E0F0', 'E0F1', 'E0F2', 'E0F3', 'E0FC', 'E0FD', 'E200']
    specialOIDList = ['E0F0', 'E0F1', 'E0F2', 'E0F3', 'E0FC', 'E0FD', 'E200']
    chipSpecificOIDList = ['E0E0', 'E0C0', 'E0C1', 'E0C2', 'E0C3', 'E0C4', 'E0C5', 'E0C6', 'E0C9', 'F1C0', 'F1C1', 'F1C2'] 
    noDataOIDList = ['E0C2', 'E0C5', 'F1C2', 'E0F0', 'E0F1', 'E0F2', 'E0F3', 'E0FC', 'E0FD', 'E200']
        
    def __init__(self, parent):
        
        wx.Panel.__init__(self, parent)
        
        textctrlfont = wx.Font()
        textctrlfont.SetPointSize(10)
        
        buttonfont = wx.Font(12, wx.ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        
        # declare the sizers
        mainsizer = wx.BoxSizer(wx.VERTICAL)
        mainhorisizer = wx.BoxSizer(wx.HORIZONTAL)
        
        midsizer = wx.BoxSizer(wx.VERTICAL)
        gdsizer3 = wx.GridSizer(rows=7, cols=1, vgap=25, hgap=10)
        
        backbuttonsizer = wx.BoxSizer(wx.HORIZONTAL)
        
        # declare sizers that will be in the grid1
        ecctypesizer = wx.BoxSizer(wx.VERTICAL)
        keyslotsizer = wx.BoxSizer(wx.VERTICAL)
        pubkeysizer = wx.BoxSizer(wx.VERTICAL)
        
        
        # instantiate the objects
        
        button_readcert = wx.Button(self, 1, 'Read IFX Pre-Provisioned Cert', size = wx.Size(350, 50))
        button_readcert.SetFont(buttonfont)
        button_pubkey = wx.Button(self, 1, 'Extract Public Key From Cert', size = wx.Size(350, 50))
        button_pubkey.SetFont(buttonfont)
        button_gencsr = wx.Button(self, 1, 'Generate DAC CSR Using Public Key', size = wx.Size(350, 50))
        button_gencsr.SetFont(buttonfont)
        button_gencert = wx.Button(self, 1, 'Generate DAC Cert Using Public Key', size = wx.Size(350, 50))
        button_gencert.SetFont(buttonfont)
        button_dac = wx.Button(self, 1, 'Write Test DAC', size = wx.Size(350, 50))
        button_dac.SetFont(buttonfont)
        button_pai = wx.Button(self, 1, 'Write Matter Test PAI', size = wx.Size(350, 50))
        button_pai.SetFont(buttonfont)
        button_cd = wx.Button(self, 1, 'Write Test CD', size = wx.Size(350, 50))
        button_cd.SetFont(buttonfont)
        
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
        
        backbuttonsizer.Add(backbutton, 0, wx.ALIGN_LEFT | wx.ALIGN_BOTTOM, 0)
        backbuttonsizer.AddSpacer(10)
        backbuttonsizer.Add(clearbutton, 0, wx.ALIGN_LEFT | wx.ALIGN_BOTTOM, 0)

        # Add sizers to midsizer
        midsizer.AddSpacer(20)
        midsizer.Add(gdsizer3, 0, wx.ALIGN_CENTRE | wx.ALL, 10)
        
        midsizer.AddSpacer(33)
        midsizer.Add(backbuttonsizer,1,wx.LEFT | wx.BOTTOM, 5)
        
        #add buttons into gdsizer3
        gdsizer3.AddMany([
           # (self.button_step1),
           (button_readcert),
           (button_pubkey),
           (button_gencsr),
           (button_gencert),
           (button_dac),
           (button_pai),
           (button_cd),
       ])
                       
        # Set Default inputs for Text Boxes      
        # attach objects to the sizer
        # declare and bind events     
        
        #bind events     
        
        button_readcert.Bind(wx.EVT_BUTTON, self.OnReadCert)
        button_pubkey.Bind(wx.EVT_BUTTON, self.OnExtPubkey)
        button_gencsr.Bind(wx.EVT_BUTTON, self.OnGenCsr)
        button_gencert.Bind(wx.EVT_BUTTON, self.OnGenCert)
        button_dac.Bind(wx.EVT_BUTTON, self.OnWriteDac)
        button_pai.Bind(wx.EVT_BUTTON, self.OnWritePai)
        button_cd.Bind(wx.EVT_BUTTON, self.OnWriteCd)
        clearbutton.Bind(wx.EVT_BUTTON, self.OnFlush)
        backbutton.Bind(wx.EVT_BUTTON, self.OnBack)
        
        

        button_readcert.SetToolTip(wx.ToolTip("Read ifx pre-provisioned cert from 0xe0e0"))
        
        button_pubkey.SetToolTip(wx.ToolTip("Extract public key from cert"))
        
        button_gencsr.SetToolTip(wx.ToolTip("Generate DAC csr using public key"))
        
        button_gencert.SetToolTip(wx.ToolTip("Generate DAC certificate using public key, Signed by Matter Test PAI "))
                                          
        button_dac.SetToolTip(wx.ToolTip("Write Test DAC into 0xe0e3"))
        
        button_pai.SetToolTip(wx.ToolTip("Write Matter test PAI into 0xe0e8"))
        
        button_cd.SetToolTip(wx.ToolTip("Write Test CD into 0xf1e0"))
        
        clearbutton.SetToolTip(wx.ToolTip("Clear all textboxes."))
        backbutton.SetToolTip(wx.ToolTip("Go back to main page."))

        self.SetSizer(mainsizer)
        mainsizer.Fit(self)  
        
        
    def OnReadCert(self, evt):
        
        self.text_display.AppendText("\nRead ifx pre-provisioned cert from 0xe0e0\n\n")
        wx.CallLater(10, self.OnReadCert1)
        
    def OnReadCert1(self):
        command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_cert", "-r", "0xe0e0", "-o", "ifx_cert_e0e0.pem", "-X", ])
        self.text_display.AppendText(command_output)
        self.text_display.AppendText("\n'/bin/trustm_cert -r 0xe0e0 -o ifx_cert_e0e0.pem -X' executed\n")
        command_output = exec_cmd.execCLI(["openssl", "x509", "-in", "ifx_cert_e0e0.pem", "-text", "-noout"] )
        self.text_display.AppendText(command_output)
        self.text_display.AppendText("\n'openssl x509 -in ifx_cert_e0e0.pem -text -noout' executed\n")        
        
        self.text_display.AppendText("++++++++++++++++++++++++++++++++\n")
        
    def OnExtPubkey(self, evt):
        
        self.text_display.AppendText("\nExtracting public key from cert\n")
        wx.CallLater(10, self.OnExtPubkey1)
        
    def OnExtPubkey1(self):
        
        command_output = exec_cmd.execCLI(["openssl", "x509", "-pubkey", "-noout", "-in", "ifx_cert_e0e0.pem",  ])
        #self.text_display.AppendText(command_output)
        self.text_display.AppendText("\n'openssl x509 -pubkey -noout -in ifx_cert_e0e0.pem' executed\n")
        with open("pubkey_e0e0.pem", "w") as outfile:
                outfile.write(command_output.decode("utf-8"))        
        command_output = exec_cmd.execCLI(["cat", "pubkey_e0e0.pem", ])
        self.text_display.AppendText(command_output)  
        self.text_display.AppendText("\n'cat pubkey_e0e0.pem' executed\n")           
        self.text_display.AppendText("++++++++++++++++++++++++++++++++\n")                      
        
    def OnGenCsr(self, evt):
        
        self.text_display.AppendText("\nGenerating DAC csr using public key\n\n")
        wx.CallLater(10, self.OnGenCsr1)
        
    def OnGenCsr1(self):
        
        command_output = exec_cmd.execCLI(["openssl", "req", "-new", "-newkey", "rsa:2048", "-nodes", "-keyout", "private.key", "-out", "request.csr", "-config", config.EXEPATH + "/scripts/matter_provisioning/openssl_matter.cnf",  ])
        
        self.text_display.AppendText(command_output)
        self.text_display.AppendText("\n'openssl req -new -newkey rsa:2048 -nodes -keyout private.key -out request.csr -config openssl_matter.cnf' executed\n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++\n")
         
            
    def OnGenCert(self, evt):
        
        self.text_display.AppendText("\nGenerating DAC certificate using public key, Signed by Matter test PAI\n")
        wx.CallLater(10, self.OnGenCert1)
        
    def OnGenCert1(self):
        
        command_output = exec_cmd.execCLI(["openssl", "x509","-req", "-in", "request.csr", "-extfile", config.EXEPATH + "/scripts/matter_provisioning/v3.ext", "-keyout", "-CA", config.EXEPATH + "/scripts/matter_provisioning/credentials/Matter-Development-PAI-noPID-Cert.pem", "-CAkey", config.EXEPATH + "/scripts/matter_provisioning/credentials/Matter-Development-PAI-noPID-Key.pem", "-CAcreateserial", "-out", "DAC_Cert.pem", "-days", "500", "-sha256", "-force_pubkey", "pubkey_e0e0.pem",  ])
        
        self.text_display.AppendText(command_output)
        self.text_display.AppendText("\n 'openssl x509 -req -in request.csr -extfile v3.ext -CA credentials/Matter-Development-PAI-noPID-Cert.pem -CAkey credentials/Matter-Development-PAI-noPID-Key.pem -CAcreateserial -out DAC_Cert.pem -days 500 -sha256 -force_pubkey pubkey_e0e0.pem' executed\n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++\n")
        
        
    def OnWriteDac(self, evt):
        
        self.text_display.AppendText("\nWrite test DAC into 0xe0e3\n")
        wx.CallLater(10, self.OnWriteDac1)
        
    
    def OnWriteDac1(self):
        
        command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_cert", "-w", "0xe0e3", "-i", "DAC_Cert.pem", "-X", ])
        
        self.text_display.AppendText(command_output)
        self.text_display.AppendText("\n 'trustm_cert -w 0xe0e3 -i DAC_Cert.pem -X' executed\n")
        self.text_display.AppendText("\nDisplaying DAC\n")        
        command_output = exec_cmd.execCLI(["openssl", "x509", "-in", "DAC_Cert.pem", "-text", "-noout",  ])
        self.text_display.AppendText(command_output)                
        self.text_display.AppendText("++++++++++++++++++++++++++++++++\n")
    
    def OnWritePai(self, evt):
        
        self.text_display.AppendText("\nWrite Matter test PAI into 0xe0e8\n")
        wx.CallLater(10, self.OnWritePai1)
    
    def OnWritePai1(self):
        
        command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_cert", "-w", "0xe0e8", "-i", config.EXEPATH + "/scripts/matter_provisioning/credentials/Matter-Development-PAI-noPID-Cert.pem", "-X", ])
        
        self.text_display.AppendText(command_output)
        self.text_display.AppendText("\n'trustm_cert -w 0xe0e8 -i credentials/Matter-Development-PAI-noPID-Cert.pem -X' executed\n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++\n")
    
    def OnWriteCd(self, evt):
        
        self.text_display.AppendText("\nWrite test CD into 0xf1e0\n")
        wx.CallLater(20, self.OnWriteCd1)
        
    def OnWriteCd1(self):
        
        command_output = exec_cmd.execCLI([config.EXEPATH + "/bin/trustm_data", "-e", "-w", "0xf1e0", "-i", config.EXEPATH + "/scripts/matter_provisioning/credentials/Chip-Test-CD-Cert.bin", "-X", ])
        
        self.text_display.AppendText(command_output)
        self.text_display.AppendText("\n'trustm_data -e -w 0xf1e0 -i credentials/Chip-Test-CD-Cert.bin -X' executed\n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++\n")

    
    # to clear the textbox
    def OnFlush(self, evt):
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
        self.tab5_prov = Tab_PROV(self.tab_base)        

        # Add tabs
        self.tab_base.AddPage(self.tab1_gen, 'General')
        self.tab_base.AddPage(self.tab2_key, 'Private Key and Cert OID')        
        self.tab_base.AddPage(self.tab3_app, 'Application Data OID')
        self.tab_base.AddPage(self.tab4_meta, 'Write Metadata')
        self.tab_base.AddPage(self.tab5_prov, 'Matter DAC Provisioning')        

        self.Show(True)
              
    
    def OnCloseWindow(self, evt):
        self.Parent.Show()
        self.Destroy()
