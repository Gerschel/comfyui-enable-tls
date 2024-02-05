import sys

#main is import first because it sets up the environment (cli-args, etc...)
from main import *
# reimports server, but customized for tls support
import override_server as server
#declares it as the server module, so when other scripts import server, they get the tls version
sys.modules['server'] = server


#generates the self-signed certificate
import generate_certificate
import ssl

async def run(server, address='', port=8188, verbose=True, call_on_start=None):
    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_context.load_cert_chain(generate_certificate.CERT_FILE, generate_certificate.KEY_FILE)
    await asyncio.gather(server.start(address, port, verbose, call_on_start, ssl_context), server.publish_loop())

with open("main.py", 'r') as main_file:
    main_file_lines = main_file.readlines()

#Iterate backwards through file to find the last occurence of "if __name__ == '__main__'" becuase there are more than one
start_line = len(main_file_lines) - next(i for i, line in enumerate(main_file_lines) if line.startswith("if __name__ =="))
#I know there is no ws:// in this section, but I'm replacing it just in case it gets added in the future
code_to_exec = "".join(main_file_lines[start_line - 1:]).replace("http://", "https://").replace("ws://", "wss://")

exec(code_to_exec)
