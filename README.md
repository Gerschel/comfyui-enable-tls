# comfyui-enable-tls
Overrides to enable tls for https:// and wss:// for comfyui  


This project uses a script to generate a Certificate Authority certificate and server certificate.  
The Certificate Authority certificate will be your own, you take a copy of the CA certificate and put
on your device you would like to have connect with https.  

Both pem and der format are created. You will have to look up how to install on your device, I welcome guides from the community.


Each time the server (comfyui) is started, it will generate a certificate for the session.  
This certificate will stay on your comfyui instance.  


The private key for the CA certificate will be used to sign the server certificate.  


Then when your device is connecting to your server, it will use the CA cert you gave to your device, to verify the signature.  


If you forget to copy the CA cert to your device, you will get a warning from your browser, invalid authority, but encryption will still work.  


But forgetting to do so, can you leave you open to a man in the middle attack.  


By default, the CA certificate will not expire for 5 years, you can change this in the code, you can always regenerate it using the provided code.  
Keep in mind, whenever you create a new CA certificate, you'll need to move it to the device that you want having recognize your signed certs.  


I opted to use pythons cryptography library, since users of comfyui will have it installed, and not everyone will have openssl installed.  
##  Installing
```python
python3 -m pip install cryptography
```


All of these files will live in comfyui's root directory, the same directory where you will find main.py


## Running  


Instead of launching main.py, launch main_https.py instead.  
If it is first run, some questions will pop up, asking you to enter some information for your Certificate Authority certificate.  


A .bat file is included for an example, where it will take in the flag "--http" to launch the standard main.py
When no flag is included, launches the main_https.py file instead.  


## Notes:  
These files rely on the originals, they provide some overrides and rewrites on the fly.  
If the functions/methods that these overrides change, then the files in this project will need to be updated.  


The generate_certificate.py is mostly boilerplate. Please review it and make changes depending on your need such as `exteranl ip address if wanting to connect remotely`.  
It generates a minimal self signed certificate every launch, and uses your local in network ip address as the common name.  
This will likely change, it was enough to get all of my connections from the front-end using https and wss, tested using wireshark.  


Please verify if you intend to forward outside of your private network.  
My objective is to create a tool that has user login, authentication tokens, and has encryption by default.  
It's not there yet.  
I felt the need to make this, after I had made some apps that utilize comfyui, wanted to share them, but without tls support, it could expose users to risk.  
