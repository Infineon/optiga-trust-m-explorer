import wx
import shell_util as exec_cmd
import multiprocessing
import time
import os
import subprocess
from subprocess import call
import images as img
import time
# from wx.lib.pubsub import setuparg1
# from wx.lib.pubsub import pub as Publisher
# from pubsub import setuparg1
from pubsub import pub as Publisher
import config
import threading
from threading import Thread
import signal
import ctypes

# """
# Already done: The creation of the server and CA keypairs, CA self-signed certificate.
# 
# TO-DO: Get the start_client/start_server and write_client/write_server functions to work. The aim of the two tabs are to:
# Display a client and server process that connect to each other using the trustm commands.
# Additionally show connectivity by sending messages from client/server and showing that the message appears in the server/client.
# 
# Running subprocess does not block the UI, however, sending messages through the PIPE in subprocess does block the UI.
# The main issue here is the many methods of sending messages to the client/server processes are blocking (the UI).
# """
# index 0, 1 respectively
server_proc = None
server_thread=None
client_proc = None
client_thread=None
server_log = None
client_log = None

RSA_Server_thread_active_flag=0
RSA_Client_thread_active_flag=0

ECC_Server_thread_active_flag=0
ECC_Client_thread_active_flag=0


def ClientProcess(client_log):
    global client_proc
    if (client_proc is not None):
        try:
            client_proc.terminate()
        except OSError:
            client_proc = None
    client_proc = exec_cmd.createProcess("lxterminal --command='openssl s_client -connect localhost:4433 -tls1_2 -CAfile CA_rsa_cert.pem'", client_log)


def LogReader(text_server, text_client, server_log, client_log):
    print(("server log is: " + str(server_log)))
    print(("client log is: " + str(client_log)))
    print(("text_server is: " + str(text_server)))
    print(("text_client is: " + str(text_client)))
    time.sleep(2)
    server_log.seek(0)
    client_log.seek(0)
    while (True):
        line_client = client_log.readline()
        if (line_client != ''):
            text_client.AppendText(line_client + "\n")
        line_server = server_log.readline()
        if (line_server != ''):
            text_server.AppendText(line_server + "\n")


# check and kill the processes if they are still running
def checkProcesses():
    global server_proc, client_proc, server_log, client_log
    if (server_proc is not None):
        try:
            server_proc.terminate()
        except OSError:
            server_proc = None
    if (client_proc is not None):
        try:
            client_proc.terminate()
        except OSError:
            client_proc = None
    if (server_log is not None):
        server_log.close()
    if (client_log is not None):
        client_log.close()

def kill_child_processes(parent_pid, sig=signal.SIGTERM):
        ps_command = subprocess.Popen("ps -o pid --ppid %d --noheaders" % parent_pid, shell=True, stdout=subprocess.PIPE)
        ps_output = ps_command.stdout.read()
        retcode = ps_command.wait()
        #assert retcode == 0, "ps command returned %d" % retcode
        if (retcode==0):
            for pid_str in ps_output.split("\n".encode())[:-1]:
                    os.kill(int(pid_str), sig)
        else:
            print("ps command returned %d" % retcode)


class Tab_ECC_CS(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        # declare the sizers
        mainsizer = wx.BoxSizer(wx.HORIZONTAL)
        steps_sizer = wx.BoxSizer(wx.VERTICAL)
        server_sizer = wx.BoxSizer(wx.VERTICAL)
        client_sizer = wx.BoxSizer(wx.VERTICAL)

        # instantiate the objects
        button_gen_server_privkey = wx.Button(self, -1, 'Create Server ECC Private Key', size = (-1, 48))
        button_gen_server_key_csr = wx.Button(self, -1, 'Create Server ECC Keys CSR', size = (-1, 48))
        button_gen_server_cert = wx.Button(self, -1, 'Create Server Cert', size = (-1, 48))
        
        button_gen_client_key_csr = wx.Button(self, -1, 'Create Client ECC Key and CSR', size = (-1, 48))
        button_extract_pubkey = wx.Button(self, -1, 'Extract Public Key from CSR', size = (-1, 48))
        button_gen_client_cert = wx.Button(self, -1, 'Create Client Cert', size = (-1, 48))
        
        button_start_server = wx.Button(self, -1, 'Start/Stop Server')
        button_start_client = wx.Button(self, -1, 'Start/Stop Client')
        button_write_to_server = wx.Button(self, -1, 'Write to Server')
        button_write_to_client = wx.Button(self, -1, 'Write to Client')
        button_flush_client = wx.Button(self, -1, 'Clear Client text', size = (-1, 48))
        button_flush_server = wx.Button(self, -1, 'Clear Server text', size = (-1, 48))
        self.text_client = wx.TextCtrl(self, -1, style=(wx.TE_MULTILINE | wx.TE_READONLY))
        self.text_server = wx.TextCtrl(self, -1, style=(wx.TE_MULTILINE | wx.TE_READONLY))
        self.text_client.SetFont(wx.Font(12, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        self.text_server.SetFont(wx.Font(12, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        
        self.input_client = wx.TextCtrl(self, -1,value="Hello from Client")
        self.input_server = wx.TextCtrl(self, -1,value="Hello from Server")
        backimage = wx.Image(config.IMAGEPATH + "/images/back.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        backbutton = wx.BitmapButton(self, -1, backimage)
        #~ backbutton = wx.BitmapButton(self, -1, img.back.getBitmap())

        # attach the objects to the sizers
        mainsizer.Add(steps_sizer, 0, wx.EXPAND | wx.LEFT | wx.TOP | wx.BOTTOM, 5)
        mainsizer.Add(server_sizer, 1, wx.EXPAND | wx.ALL, 5)
        mainsizer.Add(client_sizer, 1, wx.EXPAND | wx.ALL, 5)
        steps_sizer.Add(button_gen_server_privkey, 0, wx.EXPAND | wx.ALL, 5)
        steps_sizer.Add(button_gen_server_key_csr, 0, wx.EXPAND | wx.ALL, 5)
        steps_sizer.Add(button_gen_server_cert, 0, wx.EXPAND | wx.ALL, 5)
        steps_sizer.AddSpacer(48)
        steps_sizer.Add(button_gen_client_key_csr, 0, wx.EXPAND | wx.ALL, 5)
        steps_sizer.Add(button_extract_pubkey, 0, wx.EXPAND | wx.ALL, 5)
        steps_sizer.Add(button_gen_client_cert, 0, wx.EXPAND | wx.ALL, 5)
        steps_sizer.AddSpacer(48)
        steps_sizer.Add(button_flush_server, 0, wx.EXPAND | wx.ALL, 5)
        steps_sizer.Add(button_flush_client, 0, wx.EXPAND | wx.ALL, 5)
#         steps_sizer.AddSpacer(236)
        steps_sizer.AddSpacer(24)
        steps_sizer.Add(backbutton, 0, wx.ALL, 5)
        server_sizer.Add(self.text_server, 1, wx.EXPAND | wx.ALL, 5)
        server_sizer.Add(button_start_server, 0, wx.EXPAND | wx.ALL, 5)
        server_sizer.Add(self.input_server, 0, wx.EXPAND | wx.ALL, 5)
        server_sizer.Add(button_write_to_client, 0, wx.EXPAND | wx.ALL, 5)
        client_sizer.Add(self.text_client, 1, wx.EXPAND | wx.ALL, 5)
        client_sizer.Add(button_start_client, 0, wx.EXPAND | wx.ALL, 5)
        client_sizer.Add(self.input_client, 0, wx.EXPAND | wx.ALL, 5)
        client_sizer.Add(button_write_to_server, 0, wx.EXPAND | wx.ALL, 5)

        # Set tooltips
        button_gen_server_privkey.SetToolTip(wx.ToolTip("Generate ECC private key using prime256v1 Elliptic Curve."))
        button_gen_server_key_csr.SetToolTip(wx.ToolTip("Generate CSR using EC Key."))
        button_gen_server_cert.SetToolTip(wx.ToolTip("Create Server Certificate using Certificate Authority."))
        
        button_gen_client_key_csr.SetToolTip(wx.ToolTip("Create ECC 256 key length with Auth/Enc/Sign usage and Certificate Signing Request using Trust M."))
        button_extract_pubkey.SetToolTip(wx.ToolTip("Extract ECC Public Key from CSR."))
        button_gen_client_cert.SetToolTip(wx.ToolTip("Create Client Certificate using Certificate Authority."))

        # declare and bind events
        self.Bind(wx.EVT_BUTTON, self.OnFlushClient, button_flush_client)
        self.Bind(wx.EVT_BUTTON, self.OnFlushServer, button_flush_server)
        
        self.Bind(wx.EVT_BUTTON, self.OnGenServerPrivateKey, button_gen_server_privkey)
        self.Bind(wx.EVT_BUTTON, self.OnGenServerKeyCSR, button_gen_server_key_csr)
        self.Bind(wx.EVT_BUTTON, self.OnGenServerCert, button_gen_server_cert)
        
        self.Bind(wx.EVT_BUTTON, self.OnGenClientKeyCSR1, button_gen_client_key_csr)
        self.Bind(wx.EVT_BUTTON, self.OnExtractPublicKey, button_extract_pubkey)
        self.Bind(wx.EVT_BUTTON, self.OnGenClientCert, button_gen_client_cert)
        
        self.Bind(wx.EVT_BUTTON, self.OnStartServer, button_start_server)
        self.Bind(wx.EVT_BUTTON, self.OnStartClient, button_start_client)
        self.Bind(wx.EVT_BUTTON, self.OnWriteToServer, button_write_to_server)
        self.Bind(wx.EVT_BUTTON, self.OnWriteToClient, button_write_to_client)
        self.Bind(wx.EVT_BUTTON, self.OnBack, backbutton)
        
        # Setup Publisher for text field update
        Publisher.subscribe(self.Upd_Server_Status, "ECC_Server_Text")
        Publisher.subscribe(self.Upd_Client_Status, "ECC_Client_Text")

        self.SetSizer(mainsizer)
        # declare threads related parameters
        self.Server_thread_active_flag=0
        self.Client_thread_active_flag=0
        self.server_proc=None
        self.client_proc=None
        
    #read each line from stdout and publishes it 
    def server_thread(self):
        try:    
            while self.Server_thread_active_flag==1 :
                line = self.server_proc.stdout.readline()
                if line != '':
                    wx.CallAfter(Publisher.sendMessage, "ECC_Server_Text", msg=line)
        finally:
            self.Server_thread_active_flag=0
            print("Exit ECC server Thread\n")
            wx.CallAfter(Publisher.sendMessage, "ECC_Server_Text", msg="Server Stopped..\n")

    def client_thread(self):
        while self.Client_thread_active_flag==1 :
            line = self.client_proc.stdout.readline()
            
            if line != '':
                wx.CallAfter(Publisher.sendMessage, "ECC_Client_Text", msg=line)
            
        self.Client_thread_active_flag=0
        print("Exit ECC client Thread\n")
        wx.CallAfter(Publisher.sendMessage, "ECC_Client_Text", msg="Client Stopped..\n")    
                
    def Upd_Server_Status(self,msg):
        self.text_server.AppendText(msg)
        
    def Upd_Client_Status(self,msg):
        self.text_client.AppendText(msg)                
        
    def OnBack(self, evt):
        self.Parent.Parent.OnCloseWindow(None)
        
    def Destroy(self):
        if (self.server_proc is not None):
            self.Server_thread_active_flag=0

            if (self.client_proc is not None):
                self.Client_thread_active_flag=0
                print("Client Thread Active..killing it: %d \n" % self.client_proc.pid)
                kill_child_processes(self.client_proc.pid)
                self.client_proc.terminate()
                self.client_proc.wait()
                self.client_proc = None                

            print("Server Thread Active..killing it: %d \n" % self.server_proc.pid)
            kill_child_processes(self.server_proc.pid)
            
            self.server_proc.terminate()
            self.server_proc.wait()
            self.server_proc = None        
    
    def OnFlushClient(self, evt):
        self.text_client.Clear()

    def OnFlushServer(self, evt):
        self.text_server.Clear()

    def OnGenServerPrivateKey(self, evt):      
        self.text_server.AppendText("Creating Server ECC Private Key... \n")
        command_output = exec_cmd.execCLI([
                             "openssl", "ecparam",
                             "-out", "server1_privkey.pem",
                             "-name", "prime256v1",
                             "-genkey"         
                         ])
        self.text_server.AppendText(command_output)
        self.text_server.AppendText("'openssl ecparam -out server1_privkey.pem -name prime256v1 -genkey' executed \n")
        self.text_server.AppendText("+++++++++++++++++++++++++++++++++++++++++++\n")
        
    def OnGenServerKeyCSR(self, evt):
        self.text_server.AppendText("Creating Server ECC Keys CSR... \n")
        command_output = exec_cmd.execCLI([
                             "openssl", "req",
                             "-new", 
                             "-key", "server1_privkey.pem",
                             "-subj", "/CN=Server1/O=Infineon/C=SG",
                             "-out", "server1.csr",
                         ])
        self.text_server.AppendText(command_output)
        self.text_server.AppendText("'openssl req -new -key server1_privkey.pem -subj /CN=Server1/O=Infineon/C=SG -out server1.csr' executed \n")
        self.text_server.AppendText("+++++++++++++++++++++++++++++++++++++++++++\n")
        
    def OnGenServerCert(self, evt):
        self.text_server.AppendText("Creating Server Certificate by using CA...\n")
        command_output = exec_cmd.execCLI([
                             "openssl", "x509",
                             "-req",
                             "-in", "server1.csr",
                             "-CA", config.CERT_PATH + "/OPTIGA_Trust_M_Infineon_Test_CA.pem",
                             "-CAkey", config.CERT_PATH + "/OPTIGA_Trust_M_Infineon_Test_CA_Key.pem",
                             "-CAcreateserial",
                             "-out", "server1.crt",
                             "-days", "365",
                             "-sha256",
                             "-extfile", "openssl.cnf",
                             "-extensions", "cert_ext",
                         ])
        self.text_server.AppendText(command_output)
        self.text_server.AppendText("+++++++++++++++++++++++++++++++++++++++++++\n")

    def OnGenClientKeyCSR1(self, evt):
        wx.CallAfter(self.OnGenClientKeyCSR)
        self.text_client.AppendText("Creating new ECC 256 key length with Auth/Enc/Sign usage and creating a certificate request...\n")
    
    def OnGenClientKeyCSR(self):
        command_output = exec_cmd.execCLI([
                             "openssl", "req",
                             "-keyform", "engine",
                             "-engine", "trustm_engine",
                             "-key", "0xe0f3:^:NEW:0x03:0x13",
                             "-new", 
                             "-out", "client1_e0f3.csr",
                             "-subj", "/CN=Client1",
                         ])
        self.text_client.AppendText(command_output)
        self.text_client.AppendText("'openssl req -keyform engine -engine trustm_engine -key 0xe0f3:^:NEW:0x03:0x13 -new -out client1_e0f3.csr -subj /CN=Client1' executed \n")
        command_output = exec_cmd.execCLI([
                             "openssl", "req",
                             "-in", "client1_e0f3.csr",
                             "-text",
                         ])
        self.text_client.AppendText(command_output)
        self.text_client.AppendText("'openssl req -in client1_e0f3.csr -text' executed \n")
        self.text_client.AppendText("+++++++++++++++++++++++++++++++++++++++++++\n")
        
    def OnExtractPublicKey(self, evt):
        self.text_client.AppendText("Extracting Public Key from CSR...\n")
        command_output = exec_cmd.execCLI([
                             "openssl",
                             "req",
                             "-in", "client1_e0f3.csr",
                             "-out", "client1_e0f3.pub",
                             "-pubkey",
                         ])
        self.text_client.AppendText(command_output)
        self.text_client.AppendText("'openssl req -in client1_e0f3.csr -out client1_e0f3.pub -pubkey' executed \n")
        self.text_client.AppendText("+++++++++++++++++++++++++++++++++++++++++++\n")
    
    def OnGenClientCert(self, evt):
        self.text_client.AppendText("Creating Client Certificate by using CA...\n")
        command_output = exec_cmd.execCLI([
                             "openssl", "x509",
                             "-req",
                             "-in", "client1_e0f3.csr",
                             "-CA", config.CERT_PATH + "/OPTIGA_Trust_M_Infineon_Test_CA.pem",
                             "-CAkey", config.CERT_PATH + "/OPTIGA_Trust_M_Infineon_Test_CA_Key.pem",
                             "-CAcreateserial",
                             "-out", "client1_e0f3.crt",
                             "-days", "365",
                             "-sha256",
                             "-extfile", "openssl.cnf",
                             "-extensions", "cert_ext1",
                         ])
        self.text_client.AppendText(command_output)
        self.text_client.AppendText("+++++++++++++++++++++++++++++++++++++++++++\n")
            
    def OnStartServer(self, evt):
        #if server thread is still running, terminate it
        if (self.server_proc is not None):
            self.Server_thread_active_flag=0
            #if client thread is still running, terminate it
            if (self.client_proc is not None):
                self.Client_thread_active_flag=0
                print("Client Thread Active..killing it: %d \n" % self.client_proc.pid)
                kill_child_processes(self.client_proc.pid)
                self.client_proc.terminate()
                self.client_proc.wait()
                self.client_proc = None
                
            print("Server Thread Active..killing it: %d \n" % self.server_proc.pid)
            kill_child_processes(self.server_proc.pid)
            self.server_proc.terminate()
            self.server_proc.wait()
            self.server_proc = None

        #if server thread is not running
        else: 
            openssl_cmd="openssl s_server -cert server1.crt -key server1_privkey.pem -accept 5000 -verify_return_error -Verify 1 -CAfile " + config.CERT_PATH + "/OPTIGA_Trust_M_Infineon_Test_CA.pem"
#             openssl_cmd="echo Hello World!"
            self.server_proc = exec_cmd.createProcess(openssl_cmd, None)
            self.Server_thread_active_flag=1
            #start a server daemon thread and run server_thread function
            s_thread = threading.Thread(name='Server-daemon', target=self.server_thread)
            s_thread.setDaemon(True)
            s_thread.start()
            #this message is sent first
            wx.CallAfter(Publisher.sendMessage, "ECC_Server_Text", msg="\n\n" + openssl_cmd +"\n\n")     
    
    def OnStartClient(self, evt):
        if (self.client_proc is not None):
            self.Client_thread_active_flag=0
            print("Client Thread Active..killing it: %d \n" % self.client_proc.pid)
            kill_child_processes(self.client_proc.pid)
            self.client_proc.terminate()
            self.client_proc.wait()
            self.client_proc = None
        else:
            openssl_cmd="openssl s_client -connect localhost:5000 -client_sigalgs ECDSA+SHA256 -keyform engine -engine trustm_engine -cert client1_e0f3.crt -key 0xe0f3:^ -tls1_2 -CAfile " + config.CERT_PATH + "/OPTIGA_Trust_M_Infineon_Test_CA.pem"
            if (self.server_proc is not None):
                self.client_proc = exec_cmd.createProcess(openssl_cmd, None)

                self.Client_thread_active_flag=1
                c_thread = threading.Thread(name='Client-daemon', target=self.client_thread)
                c_thread.setDaemon(True)
                c_thread.start()                
                wx.CallAfter(Publisher.sendMessage, "ECC_Client_Text", msg="\n\n" +openssl_cmd+"\n\n")
            else:
                wx.CallAfter(Publisher.sendMessage, "ECC_Client_Text",msg="Server is not active..\n")   
    
    def OnWriteToServer(self, evt):
        global server_proc
        if (self.server_proc is None):
            self.text_server.AppendText("Server is not running!\n")
            return
        write_value = self.input_client.GetValue()
        if (write_value == ""):
            self.text_server.AppendText("I need something to write!\n")
            return
        self.client_proc.stdin.write((write_value+"\n").encode())
        self.client_proc.stdin.flush()

    def OnWriteToClient(self, evt):
        if (self.client_proc is None):
            self.text_client.AppendText("Client is not running!\n")
            return
        write_value = self.input_server.GetValue()
        if (write_value == ""):
            self.text_client.AppendText("I need something to write!\n")
            return
        self.server_proc.stdin.write((write_value+"\n").encode())
        self.server_proc.stdin.flush()

class Tab_RNG(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        
        textctrlfont = wx.Font()
        textctrlfont.SetPointSize(11)
        
        enctypelist = ['Base64','Hex',]
        
        buttonfont = wx.Font(14, wx.ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        textfont = wx.Font(14, wx.ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        
        # declare the sizers
        mainsizer = wx.BoxSizer(wx.VERTICAL)
        input_sizer = wx.BoxSizer(wx.VERTICAL)
        mainhorisizer = wx.BoxSizer(wx.HORIZONTAL)
        
        midsizer = wx.BoxSizer(wx.VERTICAL)
        
        gdsizer2 = wx.GridSizer(rows=2, cols=1, vgap=30, hgap=10)
        gdsizer3 = wx.GridSizer(rows=3, cols=1, vgap=30, hgap=10)
        
        
        #leftsizer = wx.BoxSizer(wx.VERTICAL)
        backbuttonsizer = wx.BoxSizer(wx.HORIZONTAL)
        
        # declare sizers that will be in the grid1
        enctypesizer = wx.BoxSizer(wx.VERTICAL)
        
        # instantiate the objects
        inputtext = wx.StaticText(self, 1, "No. of bytes to be generated :")
        self.input_display = wx.TextCtrl(self, 1 , value="1024", size = wx.Size(170,30))
        inputtext.SetFont(textfont)
        self.input_display.SetFont(textctrlfont)
        
        self.button_genkey = wx.Button(self, 1, 'Generate RNG', size = wx.Size(300, 50))
        self.button_genkey.SetFont(buttonfont)
        
        text_enctype = wx.StaticText(self, 1, "Encoding type :")
        self.enctype = wx.ComboBox(self, 1 ,choices=enctypelist ,size = wx.Size(170, 30) ,style=wx.CB_READONLY)
        text_enctype.SetFont(textfont)
        self.enctype.SetFont(textctrlfont)
        
        self.command_display = wx.TextCtrl(self, -1, style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.command_display.SetFont(wx.Font(11, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))


        clearimage = wx.Image(config.IMAGEPATH + "/images/clear.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        clearbutton = wx.BitmapButton(self, -1, clearimage)
        
        backimage = wx.Image(config.IMAGEPATH + "/images/back.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        backbutton = wx.BitmapButton(self, -1, backimage)
       
        #Add mainhorisizer to mainsizer
        mainsizer.AddSpacer(5)
        
        
        mainsizer.Add(mainhorisizer, 1, wx.EXPAND)
       
        # Add Sub Sizers to the mainhorisizer
        mainhorisizer.Add(midsizer, 1, wx.EXPAND)
        mainhorisizer.Add(self.command_display, 2, wx.EXPAND | wx.ALL, 5)
      
        backbuttonsizer.Add(backbutton, 0, wx.ALIGN_LEFT, 0)
        backbuttonsizer.AddSpacer(10)
        backbuttonsizer.Add(clearbutton, 0, wx.EXPAND, 0)

        # Add sizers to midsizer
        midsizer.AddSpacer(30)
        
        
        midsizer.AddSpacer(10)
        midsizer.Add(gdsizer2, 0, wx.ALIGN_CENTRE | wx.ALL, 10)
        
        
        midsizer.AddSpacer(30)
        midsizer.Add(gdsizer3, 0, wx.ALIGN_CENTRE | wx.ALL, 10)
        
        midsizer.AddSpacer(120)
        midsizer.Add(backbuttonsizer,0,wx.LEFT | wx.BOTTOM, 5)
        
        
        #add buttons into gdsizer3
        gdsizer3.AddMany([
           
           (self.button_genkey),
        
       ])
        
        gdsizer2.AddMany([
                 (input_sizer , 0, wx.EXPAND),
                 (enctypesizer, 0, wx.EXPAND),
              
        ])
         
        
        #add objects into sizers in gdsizer2
        
        enctypesizer.Add(text_enctype, 1, wx.ALIGN_CENTRE | wx.ALL, 0)
        enctypesizer.Add(self.enctype, 1, wx.ALIGN_CENTRE | wx.ALL, 0)

        input_sizer.Add(inputtext, 1 , wx.ALIGN_CENTRE | wx.ALL,0)
        input_sizer.Add(self.input_display, 1 ,wx.ALIGN_CENTRE | wx.ALL, 0)
        
        
        self.enctype.SetSelection(0)
        
        
        #bind events
        self.button_genkey.Bind(wx.EVT_BUTTON, self.OnGenRNG)
        clearbutton.Bind(wx.EVT_BUTTON, self.OnClear)
        backbutton.Bind(wx.EVT_BUTTON, self.OnBack)
        
        
        # Set tooltips
        
        self.button_genkey.SetToolTip(wx.ToolTip("Generate a Random Number"))
        clearbutton.SetToolTip(wx.ToolTip("Clear all textboxes."))
        backbutton.SetToolTip(wx.ToolTip("Go back to main page.")) 

        self.SetSizer(mainsizer)
        mainsizer.Fit(self)
     
    def OnClear(self, evt):
        self.command_display.Clear()

    # Calling parent of the parent, as direct parent is the notebook,
    # then the second parent is the frame, from which we call the destruction
    def OnBack(self, evt):
        self.Parent.Parent.OnCloseWindow(None)

    def OnGenRNG(self, evt):
        enctype = self.enctype.GetValue()
        
        self.command_display.AppendText("Generating Random Number in " + enctype + " encoding....\n\n")
        wx.CallLater(20, self.OnGenRNG1)

    def OnGenRNG1(self):
        no_bytes = self.input_display.GetValue()
        
        #enctype = self.enctype.GetValue()
        
        if (self.enctype.GetSelection() == 0):
            enctype = "base64"
        
        else:
            enctype = "hex"
        
        try:
            no_bytes = abs(int(no_bytes))
        except ValueError:
            self.command_out.AppendText("Number of bytes is not an integer, try again.\n")
            return
     
        else :
            command_output = exec_cmd.execCLI([
                "openssl", "rand",
                "-engine", "trustm_engine",
                "-" + enctype, str(no_bytes),
            ])
            self.command_display.AppendText("=========================================================================\n")
            self.command_display.AppendText(command_output)
            self.command_display.AppendText("\n=========================================================================")
            self.command_display.AppendText("\n'openssl rand -engine trustm_engine -" + enctype + " " + str(no_bytes) + " executed'\n")
            self.command_display.AppendText("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n\n")      

class Tab3Frame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title="OpenSSL Engine", size=(1280, 720), style=(wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX)))
        self.Centre(wx.BOTH)
        main_menu_font = wx.Font(14, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.SetFont(main_menu_font)

        # Instantiate all objects
        self.tab_base = wx.Notebook(self, id=wx.ID_ANY, style=wx.NB_TOP)
        self.tab2_ecc_cs = Tab_ECC_CS(self.tab_base)
        self.tab4_rng = Tab_RNG(self.tab_base)
        

        # Add tabs
        self.tab_base.AddPage(self.tab2_ecc_cs, 'ECC (Client/Server)')
        self.tab_base.AddPage(self.tab4_rng, 'RNG')

        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        self.Show(True)
        
        if (self.tab_base.GetSelection() == 0):
            self.tab_base.ChangeSelection(0)

    def OnCloseWindow(self, evt):
        #checkProcesses()
        self.tab2_ecc_cs.Destroy()
        self.Parent.Show()
        self.Destroy()
