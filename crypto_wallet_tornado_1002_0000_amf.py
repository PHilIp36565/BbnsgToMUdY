# 代码生成时间: 2025-10-02 00:00:42
import os
from hashlib import sha256
from base64 import b64encode
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidSignature
from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application


class CryptoWallet:
    """
    A simple class to simulate a cryptocurrency wallet
    using RSA encryption algorithm.
    """
    def __init__(self):
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        self.public_key = self.private_key.public_key()

    def generate_keypair(self):
        """
        Generate a public-private key pair using RSA.
        Returns the private and public keys as PEM formatted strings.
        """
        return self.private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ), self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

    def sign_message(self, message):
        """
        Sign a message using the private key.
        Returns the signature as a base64 encoded string.
        """
        signature = self.private_key.sign(
            message.encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return b64encode(signature).decode('utf-8')

    def verify_signature(self, message, signature):
        """
        Verify a message signature using the public key.
        Returns True if the signature is valid, False otherwise.
        """
        try:
            self.public_key.verify(
                base64.b64decode(signature),
                message.encode(),
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except InvalidSignature:
            return False


class WalletHandler(RequestHandler):
    """
    A Tornado handler to interact with the CryptoWallet class.
    """
    def initialize(self, wallet):
        self.wallet = wallet

    def get(self):
        """
        Provide the public key and private key.
        """
        self.write({"public_key": self.wallet.public_key, "private_key": self.wallet.private_key})

    def post(self):
        """
        Process a POST request to sign a message.
        """
        try:
            data = self.get_json_body()
            message = data.get('message')
            if not message:
                raise ValueError("No message provided")
            signature = self.wallet.sign_message(message)
            self.write({"signature": signature})
        except Exception as e:
            self.write({"error": str(e)})

    def put(self):
        """
        Process a PUT request to verify a message signature.
        """
        try:
            data = self.get_json_body()
            message = data.get('message')
            signature = data.get('signature')
            if not message or not signature:
                raise ValueError("No message or signature provided")
            is_valid = self.wallet.verify_signature(message, signature)
            self.write({"is_valid": is_valid})
        except Exception as e:
            self.write({"error": str(e)})


def make_app():
    """
    Create a Tornado application.
    """
    wallet = CryptoWallet()
    return Application(
        [('/wallet', WalletHandler, {'wallet': wallet})],
        debug=True
    )

if __name__ == '__main__':
    app = make_app()
    app.listen(8888)
    print("Wallet server running on http://localhost:8888")
    IOLoop.current().start()
