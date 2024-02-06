from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.serialization import Encoding, PrivateFormat, NoEncryption
import datetime

import socket

from certificate_authority import CertificateAuthority

##! For dev purpose to regenerate the CA on each launch
#CertificateAuthority.generate_ca()


def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("10.255.255.255", 1))
    ip_address = s.getsockname()[0]
    s.close()
    return ip_address

# Get the IP address of the machine
ip_address = get_ip_address()

# Generate private key
private_key = ec.generate_private_key(
    ec.SECP384R1()
)

# Minimal subject and issuer details
subject = x509.Name([
    x509.NameAttribute(NameOID.COMMON_NAME, u"{ip_address}".format(ip_address=ip_address)),
])

issuer = CertificateAuthority.get_ca_cert().subject


# Generate a basic certificate
cert = x509.CertificateBuilder().subject_name(
    subject
).issuer_name(
    issuer
).public_key(
    private_key.public_key()
).serial_number(
    x509.random_serial_number()
).not_valid_before(
    datetime.datetime.utcnow()
).not_valid_after(
    datetime.datetime.utcnow() + datetime.timedelta(days=2)
).add_extension(
    x509.SubjectAlternativeName([
        x509.DNSName(u"localhost"),
        x509.IPAddress(ip_address),
        x509.IPAddress('0.0.0.0'),
    ])
).sign(CertificateAuthority.get_ca_key(), hashes.SHA256())

# Write servers private key and certificate
with open("server_private_key.pem", "wb") as f:
    f.write(private_key.private_bytes(
        encoding=Encoding.PEM,
        format=PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=NoEncryption()
    ))

with open("server_certificate.pem", "wb") as f:
    f.write(cert.public_bytes(Encoding.PEM))

#Assign into variables generate_certificate.CERT_FILE, generate_certificate.KEY_FILE

CERT_FILE = "./server_certificate.pem"
KEY_FILE = "./server_private_key.pem"