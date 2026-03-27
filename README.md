[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Python version](https://img.shields.io/badge/Python-3-green?logo=python)](https://www.python.org/)

# **OPTIGA™ Trust M Explorer**

The OPTIGA™ Trust M Explorer is a GUI-based tool for users to familiarize themselves with Trust M quickly and easily using Infineon's OPTIGA™ Trust M solution for Raspberry Pi. In addition, the OPTIGA™ Trust M Explorer demonstrates how the OPTIGA™ Trust M can be used to increase security and trust for data sharing across different networking and cloud platforms.

Using this tool, you can instantly experience the benefits that OPTIGA™ Trust M will bring to IoT devices and network equipment.

![](docs/images/Setup/MainScreen.png)

Tool highlights include the opportunity to explore OPTIGA™ Trust M features and use cases faster - without having to familiarize yourself with Trust M or various command sets. You simply select a button to activate the relevant function or task. Once you select a button, the view menu gives you instant visual feedback, showing the commands that have been executed and the corresponding responses. This easy-to-use GUI makes it possible for all users - regardless of their level of experience or knowledge - to effortlessly access different OPTIGA™ Trust M features and explore common use cases.

## Features

-   Shows OPTIGA™ Trust M commands executed and the corresponding responses on the display screen or the terminal in the background
-   Displays all properties defined within an OPTIGA™ Trust M
-   Read/Write data/Certificate into OPTIGA™ Trust M
-   Cryptographic support:
    ECC : NIST curves up to P-521, Brainpool r1 curve up to 512,
    RSA® up to 2048
    AES key up to 256 ,
-   Encrypts and decrypts data using ECC/RSA/AES
-   Signs and verifies data with ECC/RSA

## Use cases

-   Secure Storage
-   Protected Update
-   Cryptographic operations using OpenSSL library
-   Secured communications with OpenSSL library

## Setup environment

This tool was tested on a Raspberry Pi  4 Model B with Raspbian Linux release version 12 (Bookworm) and kernel version 6.6.31+rpt-rpi-v8.

For more information on how to setup the tool environment, refer to the [OPTIGA™ Trust M Setup Guide](./Setup%20Guide.md)

![](docs/images/Setup/bookworm.png)

## User guide

Learn more about the tool, how it works and OPTIGA™ Trust M functionality by the following example illustrations and simple step-by-step instructions;  see the [OPTIGA™ Trust M Explorer User Guide](./User%20Guide.md) for details.

To update Platform Binding Secret (PBS) for OPTIGA™ Trust M V3/MTR/Express, please refer to [README.md](https://github.com/Infineon/linux-optiga-trust-m/blob/feature/mtr_express/pbs/README.md)  

## Resources

You will find relevant resources (tools, open source host code and application notes) to help you study OPTIGA™ Trust M and learn more about it on [Infineon OPTIGA™ Trust M GitHub](https://github.com/Infineon/optiga-trust-m) and [Infineon OPTIGA™ Trust M Linux tools GitHub](https://github.com/Infineon/linux-optiga-trust-m)

## License

The OPTIGA™ Trust M Explorer is released under the MIT License; see the [LICENSE](LICENSE) file for details.

