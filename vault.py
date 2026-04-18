from Crypto.Protocol.KDF import PBKDF2
from db_base import DBbase
from Crypto.Cipher import AES
from Crypto import Random


class Vault(DBbase):
    """
    Gets API keys, encrypts them, then writes them to a local SQLite file
    """
    def __init__(self):
        super().__init__("vault.sqlite")
        # Necessary for encryption/decryption purposes
        # TODO: Try to find a method that will persist across runs without hard-coding the key or IV
        self.iv = Random.new().read(AES.block_size)
        salt = Random.new().read(8)
        password = input("Enter password: ")
        self.key = PBKDF2(password, salt, 16)

    def get_apikey_from_user(self):
        # Asks the user to enter their API key
        key = input("Enter your API key: ")
        return key

    def get_apikey_from_db(self, app):
        # Fetches API key for specific app. If found then decrypts it, otherwise prompt for a new key
        super().connect()
        output = super().get_cursor.execute("""SELECT api_key FROM Vault WHERE app = ?;""", (app,)).fetchone()
        if output is None:
            super().close_db()
            raise Exception("Key does not exist.")
        else:
            return self.decrypt_key(output[0])

    def get_raw(self, app):
        # Fetches API key for specific app. If found then decrypts it, otherwise prompt for a new key
        super().connect()
        output = super().get_cursor.execute("""SELECT api_key FROM Vault WHERE app = ?;""", (app,)).fetchone()
        if output is None:
            super().close_db()
            raise Exception("Key does not exist.")
        else:
            return output

    def encrypt_key(self, message):
        # Takes a message, encrypts it, and returns the ciphertext
        obj = AES.new(self.key, AES.MODE_CBC, self.iv)
        message = message.encode("utf8")
        length = 16 - (len(message) % 16)
        message += bytes([length])*length
        ciphertext = obj.encrypt(message)
        return ciphertext

    def decrypt_key(self, message):
        # Takes an encrypted API key and decrypts it
        obj = AES.new(self.key, AES.MODE_CBC, self.iv)
        decrypted = obj.decrypt(message)
        cleaned = decrypted[:-decrypted[-1]].decode("utf8", "ignore")
        return cleaned

    def store_key(self, key, app):
        # Takes an API key and application then writes it to SQLite
        key.decode("utf8", "ignore")
        try:
            super().connect()
            super().get_cursor.execute("""insert or ignore into Vault (api_key, app)
                                    values (?,?);""", (key, app))
            super().get_connection.commit()
            super().close_db()
            print("Added API key successfully.")
        except Exception as e:
            print("An error has occurred while adding the API key.", e)

    def reset_database(self):
        # Wipes out the entire table and starts fresh
        sql = """
        DROP TABLE IF EXISTS Vault;
        
        CREATE TABLE Vault (
            id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            app TEXT UNIQUE,
            api_key VARCHAR(50) UNIQUE
        );"""
        super().connect()
        super().execute_script(sql)
        super().close_db()
