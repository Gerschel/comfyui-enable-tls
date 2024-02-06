import os
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import Encoding, PrivateFormat, NoEncryption, load_pem_private_key
import datetime

class CertificateAuthority:
    CA_CERT_FILE = "./ca_certificate.pem"
    CA_KEY_FILE = "./ca_private_key.pem"

    @staticmethod
    def get_ca_cert():
        if os.path.exists(CertificateAuthority.CA_CERT_FILE):
            with open(CertificateAuthority.CA_CERT_FILE, "rb") as f:
                return x509.load_pem_x509_certificate(f.read())
        else:
            return CertificateAuthority.generate_ca()[1]

    @staticmethod
    def get_ca_key():
        if os.path.exists(CertificateAuthority.CA_KEY_FILE):
            with open(CertificateAuthority.CA_KEY_FILE, "rb") as f:
                return load_pem_private_key(f.read(), password=None)
        else:
            return CertificateAuthority.generate_ca()[0]

    @staticmethod
    def generate_ca():
        # Generate CA's private key
        ca_private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=4096,
        )

        # CA's subject and issuer details
        print("************ Generating Central Authority Certificate ************")
        common_name = input("Enter the common name for the CA (Enter whatever you want): ")
        organization_name = input("Enter the organization name for the CA (Enter whatever you want): ")
        organizational_unit_name = input("Enter the organizational unit name for the CA (Enter whatever you want): ")
        ca_subject = ca_issuer = x509.Name([
            x509.NameAttribute(NameOID.COMMON_NAME, common_name),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, organization_name),
            #x509.NameAttribute(NameOID.COUNTRY_NAME, u"US"),
            #x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"California"),
            #x509.NameAttribute(NameOID.LOCALITY_NAME, u"San Francisco"),
            x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME, organizational_unit_name),
            #x509.NameAttribute(NameOID.EMAIL_ADDRESS, u"ca@example.com"),
        ])

        # Generate CA's certificate
        ca_cert = x509.CertificateBuilder().subject_name(
            ca_subject
        ).issuer_name(
            ca_issuer
        ).public_key(
            ca_private_key.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.datetime.utcnow()
        ).not_valid_after(
            # CA's certificate valid for 5 years
            datetime.datetime.utcnow() + datetime.timedelta(days=5*365)
        ).add_extension(
            x509.BasicConstraints(ca=True, path_length=None), critical=True,
        ).sign(ca_private_key, hashes.SHA256())

        # Write CA's private key and certificate
        with open(CertificateAuthority.CA_KEY_FILE, "wb") as f:
            f.write(ca_private_key.private_bytes(
                encoding=Encoding.PEM,
                format=PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=NoEncryption()
            ))

        with open(CertificateAuthority.CA_CERT_FILE, "wb") as f:
            f.write(ca_cert.public_bytes(Encoding.PEM))

        return ca_private_key, ca_cert

#    @staticmethod
#    def sign_cert(cert_to_sign):
#        ca_key, ca_cert = CertificateAuthority.get_ca_key(), CertificateAuthority.get_ca_cert()
#        return cert_to_sign.sign(ca_key, hashes.SHA256())