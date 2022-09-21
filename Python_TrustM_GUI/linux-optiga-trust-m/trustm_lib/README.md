# OPTIGA&trade; Trust M Software Framework

## Quick navigation

<a href="https://github.com/Infineon/optiga-trust-m#description"><img src="https://github.com/Infineon/Assets/blob/master/Pictures/optiga_trust_x_gitrepo_tile_1.jpg" width="256" height="192"></a> <a href="https://github.com/Infineon/optiga-trust-m#examples"><img src="https://github.com/Infineon/Assets/blob/master/Pictures/optiga_trust_x_gitrepo_tile_2.jpg" width="256" height="192"></a>  <a href="https://github.com/Infineon/optiga-trust-m#get-started"><img src="https://github.com/Infineon/Assets/blob/master/Pictures/optiga_trust_x_gitrepo_tile_3.jpg" width="256" height="192"></a>

<a href="https://github.com/Infineon/optiga-trust-m#documentation"><img src="https://github.com/Infineon/Assets/blob/master/Pictures/optiga_trust_x_gitrepo_tile_4.jpg" width="256" height="192"></a> <a href="https://github.com/Infineon/optiga-trust-m/wiki/Crypto-Performance"><img src="https://github.com/Infineon/Assets/blob/master/Pictures/optiga_trust_x_gitrepo_tile_5.jpg" width="256" height="192"></a>  <a href="https://github.com/Infineon/optiga-trust-m/wiki/Trust-M-Crypt-API"><img src="https://github.com/Infineon/Assets/blob/master/Pictures/optiga_trust_x_gitrepo_tile_6.jpg" width="256" height="192"></a>

## Security Chip

### <a name="description"></a>Description

<img src="https://github.com/Infineon/Assets/blob/master/Pictures/optiga_trust_m_uson10.png" width="300" >

This repository contains a target-agnostic Software Framework for the [OPTIGA™ Trust M](https://www.infineon.com/optiga-trust) security chip. It is a base for other application notes. **Be aware that this software comes without any security claims and shall be used for evaluation purpose.**

### <a name="key_features_and_benefits"></a>Key Features and Benefits
* High-end security controller
* Common Criteria Certified EAL6+ (high) hardware
* Turnkey solution
* Up to 10kB user memory
* PG-USON-10 package (3 x 3 mm)
* Temperature range (−40°C to +105°C)
* I2C interface with Shielded Connection (encrypted communication)
* Cryptographic support: 
  * ECC : NIST curves up to P-521, Brainpool r1 curve up to 512,
  * RSA® up to 2048
  * AES key up to 256 , HMAC up to SHA512
  * TLS v1.2 PRF and HKDF up to SHA512
* Crypto ToolBox commands for SHA-256, ECC and RSA® Feature, AES, HMAC and Key derivation
* Configurable device security monitor, 4 Monotonic up counters
* Protected(integrity and confidentiality) update of data, key and metadata objects
* Hibernate for zero power consumption
* Lifetime for Industrial Automation and Infrastructure is 20 years and 15 years for other Application Profiles  

### OPTIGA&trade; Trust M features table

<table class="tg">
  <tr>
    <th class="tg-fymr">Features</th>
    <th class="tg-fymr">Supported Curve/Algorithm</th>
    <th class="tg-fymr">V1</th>
    <th class="tg-fymr">V3</th>
  </tr>
  <tr>
    <td class="tg-c3ow" rowspan="2">ECC</td>
    <td class="tg-0pky">ECC NIST P256/384 </td>
    <td class="tg-0pky">✓</td>
    <td class="tg-0pky">✓</td>
  </tr>
  <tr>
    <td class="tg-0pky">ECC NIST P521, ECC Brainpool P256/384/512 r1</td>
    <td class="tg-0pky"></td>
    <td class="tg-0pky">✓</td>
  </tr>
  <tr>
    <td class="tg-c3ow">RSA</td>
    <td class="tg-0pky">RSA® 1024/2048 </td>
    <td class="tg-0pky">✓</td>
    <td class="tg-0pky">✓</td>
  </tr>
  <tr>
    <td class="tg-c3ow" rowspan="3">Key Derivation</td>
    <td class="tg-0pky">TLS v1.2 PRF SHA 256 </td>
    <td class="tg-0pky">✓</td>
    <td class="tg-0pky">✓</td>
  </tr>
  <tr>
    <td class="tg-0pky">TLS v1.2 PRF SHA 384/512 </td>
    <td class="tg-0pky"> </td>
    <td class="tg-0pky">✓</td>
  </tr>
  <tr>
    <td class="tg-0pky">HKDF SHA-256/384/512  </td>
    <td class="tg-0pky"> </td>
    <td class="tg-0pky">✓</td>
  </tr>
  <tr>
    <td class="tg-c3ow">AES</td>
    <td class="tg-0pky">Key size - 128/192/256 (ECB, CBC, CBC-MAC, CMAC)</td>
    <td class="tg-0pky"> </td>
    <td class="tg-0pky">✓</td>
  </tr>
  <tr>
    <td class="tg-c3ow">Random Generation</td>
    <td class="tg-0pky">TRNG, DRNG, Pre-Master secret for RSA® Key exchange</td>
    <td class="tg-0pky">✓</td>
    <td class="tg-0pky">✓</td>
  </tr>
  <tr>
    <td class="tg-c3ow">HMAC</td>
    <td class="tg-0pky">HMAC with SHA256/384/512 </td>
    <td class="tg-0pky"> </td>
    <td class="tg-0pky">✓</td>
  </tr>
  <tr>
    <td class="tg-c3ow">Hash </td>
    <td class="tg-0pky">SHA256 </td>
    <td class="tg-0pky">✓</td>
    <td class="tg-0pky">✓</td>
  </tr>
  <tr>
    <td class="tg-c3ow" rowspan="2">Protected data (object) update (Integrity)</td>
    <td class="tg-0pky">ECC NIST P256/384</br>RSA® 1024/2048 </br>Signature scheme as ECDSA FIPS 186-3/RSA SSA PKCS#1 v1.5 without hashing </td>
    <td class="tg-0pky">✓</td>
    <td class="tg-0pky">✓</td>
  </tr>
  <tr>
    <td class="tg-c3ow">ECC NIST P521,</br>ECC Brainpool P256/384/512 r1</br>Signature scheme as ECDSA FIPS 186-3/RSA SSA PKCS#1 v1.5 without hashing</td>
    <td class="tg-0pky"> </td>
    <td class="tg-0pky">✓</td>
  </tr>
  <tr>
    <td class="tg-c3ow">Protected Data/key/metadata update (Integrity and/or confidentiality)</td>
    <td class="tg-0pky">ECC NIST P256/384/521</br>ECC Brainpool P256/384/512 r1</br>RSA® 1024/2048</br>Signature scheme as ECDSA FIPS 186-3/RSA SSA PKCS#1 v1.5 without hashing</td>
    <td class="tg-0pky"> </td>
    <td class="tg-0pky">✓</td>
  </tr>
</table>

## Get Started

### Boards

| [OPTIGA&trade; Trust M Evaluation Kit](https://github.com/Infineon/getstarted-optiga-trust-m/wiki/Get-Started-with-OPTIGA%E2%84%A2-Trust-M-Evaluation-Kit) | [OPTIGA&trade; Trust IoT Security Development Kit](https://github.com/Infineon/getstarted-optiga-trust-m/wiki/Get-Started-with-OPTIGA%E2%84%A2-Trust-M-IoT-Security-Development-Kit) |
|     :---:      |     :---:      |
| <a href="https://github.com/Infineon/getstarted-optiga-trust-m/wiki/Get-Started-with-OPTIGA%E2%84%A2-Trust-M-Evaluation-Kit"><img src="https://github.com/Infineon/Assets/raw/master/Pictures/OPTIGA_Trust_M_Eval_Kit%2002.jpg" width="480" height="326"></a>   | <a href="https://github.com/Infineon/getstarted-optiga-trust-m/wiki/Get-Started-with-OPTIGA%E2%84%A2-Trust-IoT-Security-Development-Kit"><img src="https://github.com/Infineon/Assets/raw/master/Pictures/optiga_trust_iot_secdevkit.png" width="480" height="318"></a>     |

Get started with the [OPTIGA™ Trust M evaluation kit](https://www.infineon.com/cms/en/product/evaluation-boards/optiga-trust-m-eval-kit/) or with the [OPTIGA™ Trust IoT Security Development kit](https://www.infineon.com/cms/en/product/evaluation-boards/optiga-trust-m-iot-kit/) using [this](https://github.com/Infineon/getstarted-optiga-trust-m) Application Note

### <a name="examples"></a>Examples

1. [Get started guide](https://github.com/Infineon/getstarted-optiga-trust-m)
1. [Off-Chip TLS example (mbedTLS)](https://github.com/Infineon/mbedtls-optiga-trust-m)
1. Cloud:
    1. [AWS FreeRTOS example](https://github.com/Infineon/amazon-freertos-optiga-trust)
    1. [Microsoft Azure IoT example](https://github.com/Infineon/azure-optiga-trust-m)
1. [Zephyr OS driver](https://github.com/Infineon/zephyr)
1. Secure Firmware Update and Secure Boot (link is pending)
1. [Arduino library](https://github.com/Infineon/arduino-optiga-trust-m)
1. [Personalize OPTIGA™ Trust](https://github.com/Infineon/personalize-optiga-trust)
1. [OpenSSL Engine Command Line Interface and AWS IoT C SDK (for RPi3)](https://github.com/Infineon/cli-optiga-trust-m)
1. [Python package](https://github.com/Infineon/python-optiga-trust)
1. [I2C Utilities](https://github.com/Infineon/i2c-utils-optiga-trust)

### <a name="software_framework_oveview"></a>Software Framework overview

![](https://github.com/Infineon/Assets/raw/master/Pictures/optiga_trust_m_system_block_diagram_v3.png)

1. See [Trust M Crypt API](https://github.com/Infineon/optiga-trust-m/wiki/Trust-M-Crypt-API) and [Trust M Util API](https://github.com/Infineon/optiga-trust-m/wiki/Trust-M-Util-API)  to know more about CRYPT and UTIL modules
2. Information about the OPTIGA™ Trust M Command Library (CMD) can be found in the [Solution Reference Manual](documents/OPTIGA_Trust_M_Solution_Reference_Manual_v3.00.pdf)
    In the same document you can find explanation of all Object IDs (OIDs) available for users as well as detailed technical explanation for all features and envisioned use cases.
3. Infineon I<sup>2</sup>C Protocol implementation details can be found [here](documents/Infineon_I2C_Protocol_v2.02.pdf)
4. Platform Abstraction Layer (PAL) overview and Porting Guide are presented in the [Wiki](https://github.com/Infineon/optiga-trust-m/wiki/Porting-Guide)

For more information please refer to the [Wiki page](https://github.com/Infineon/optiga-trust-m/wiki) of this project

### <a name="evaluation_development_kits"></a>Evaluation and developement kits

External links, open in the same tab.
* [OPTIGA™ Trust M evaluation kit](https://www.infineon.com/cms/en/product/evaluation-boards/optiga-trust-m-eval-kit/)
* [OPTIGA™ Trust M Shield2Go](https://www.infineon.com/cms/en/product/evaluation-boards/s2go-security-optiga-m/)
  Notes to the S2Go Security OPTIGA M:
  * Supply voltage VCC is max. 5.5 V, please refer to the OPTIGA™ Trust M datasheet for more details about maximum ratings
  * Ensure that no voltage applied to any of the pins exceeds the absolute maximum rating of VCC + 0.3 V
  * Pin out on top (head) is directly connected to the pins of the OPTIGA™ Trust M
  * If head is broken off, only one capacitor is connected to the OPTIGA™ Trust M

  <details>
  <summary> S2Go Security OPTIGA M Pinout</summary>
  <img src="https://github.com/Infineon/Assets/blob/master/Pictures/optiga_trust_m_shield2go_pinout.png" alt="drawing"/>
  </details>

  <details>
  <summary> S2Go Security OPTIGA M Schematic</summary>
  <img src="https://github.com/Infineon/Assets/blob/master/Pictures/optiga_trust_m_shield2go_schematics.png" alt="drawing"/>
  </details>

## <a name="documentation"></a>Documentation

### Usefull articles

  * [Initialisation hints (Wiki)](https://github.com/Infineon/optiga-trust-m/wiki/Initialisation-hints)
  * [Porting guide (Wiki)](https://github.com/Infineon/optiga-trust-m/wiki/Porting-Guide)
  * [Crypto performance (Wiki)](https://github.com/Infineon/optiga-trust-m/wiki/Crypto-Performance)
  * [In which form does OPTIGA return keys and signatures? (Wiki)](https://github.com/Infineon/optiga-trust-m/wiki/Data-format-examples)
  * [Code Footprint (Wiki)](https://github.com/Infineon/optiga-trust-m/wiki/Code-Footprint)
  * [Device Error Codes (Wiki)](https://github.com/Infineon/optiga-trust-m/wiki/Device-Error-Codes)
  * [Protected Update for Data Objects](https://github.com/Infineon/optiga-trust-m/wiki/Protected-Update-for-Data-Objects)
  * [Shielded Connection (Wiki)](https://github.com/Infineon/optiga-trust-m/wiki/Shielded-Connection-101)
  * **User API**
      * [Crypt API (Wiki)](https://github.com/Infineon/optiga-trust-m/wiki/Trust-M-Crypt-API)
      * [Util API (Wiki)](https://github.com/Infineon/optiga-trust-m/wiki/Trust-M-Util-API)
      
  * [Hardware-Security: "Einfach (und) Sicher" (external link, opens in the same tab)](https://vimeo.com/279839814) in German, [Slides](https://github.com/Infineon/Assets/blob/master/PDFs/2018-06-04_Building-IoT_HW-Sec_Lesjak_vFinal.pdf) in English

### Datasheet and Co.

For high level description and some important excerpts from the documentation please refer to [Wiki page](https://github.com/Infineon/optiga-trust-m/wiki)

Other downloadable PDF documents can be found below:
1. [OPTIGA™ Trust M Datasheet v3.10](documents/OPTIGA_Trust_M_Datasheet_v3.10.pdf) (PDF)
2. [OPTIGA™ Trust M Solution Reference Manual v3.15](documents/OPTIGA_Trust_M_Solution_Reference_Manual_v3.15.pdf) (PDF)
3. [OPTIGA™ Trust M Keys and Certificates v3.10](documents/OPTIGA_Trust_M_Keys_And_Certificates_v3.10.pdf) (PDF)
4. [Infineon I2C protocol specification v2.03](documents/Infineon_I2C_Protocol_v2.03.pdf) (PDF)

### Board assembly recommendations

If you are planning to integrate OPTIGA™ Trust M in your PCB design have a look at the recommendations found [here (external, opens in the same tab)](https://www.infineon.com/dgdl/Infineon-Additional_product_information_SON_packages-AN-v00_01-EN.pdf?fileId=db3a30433e82b1cf013e82faab2000e5).


## <a name="contributing"></a>Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## <a name="license"></a>License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
