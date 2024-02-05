# comfyui-enable-tls
Overrides to enable tls for https:// and wss:// for comfyui
Take these files and put them in the root of the project.  
install cryptography package in your venv for generate_certificate to work
python -m pip install cryptography

i.e.- main_https.py next to main.py
override_server.py next to server.py
generate_certificate.py in same folder  

A .bat file is included for an example, where it will take in the flag "--http" to launch the standard main.py
When no flag is included, launches the main_https.py file instead.  

These files rely on the originals, they provide some overrides and rewrites on the fly.  
If these functions/methods that this overrides changes, they will need to be updated.  

The generate_certificate.py is mostly boilerplate. Please review it and make changes.  
It generates a minimal self signed certificate every launch, and uses your local in network ip address as the common name.  
This will likely change, it was enough to get all of my connections from the front-end using https and wss, tested using wireshark.  

Please verify if you intend to forward outside of your private network.  
My objective is to create a tool that has user login, authentication tokens, and has encryption by default.  
It's not there yet.  
I felt the need to make this, after I had made some apps that utilize comfyui, wanted to share them, but without tls support, it could expose users to risk.  
