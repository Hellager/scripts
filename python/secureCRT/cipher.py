#!/usr/bin/env python3
import os
from Crypto.Hash import SHA256
from Crypto.Cipher import AES, Blowfish

# Reference link
# https://blog.csdn.net/ly4983/article/details/131528552

# 使用 os.path.expandvars 获取当前用户的 AppData 路径
session_store_folder = os.path.join(
    os.path.expandvars("%APPDATA%"),
    "VanDyke",
    "Config",
    "Sessions"
)


class SecureCRTCrypto:

    def __init__(self):
        '''
        Initialize SecureCRTCrypto object.
        '''
        self.IV = b'\x00' * Blowfish.block_size
        self.Key1 = b'\x24\xA6\x3D\xDE\x5B\xD3\xB3\x82\x9C\x7E\x06\xF4\x08\x16\xAA\x07'
        self.Key2 = b'\x5F\xB0\x45\xA2\x94\x17\xD9\x16\xC6\xC6\xA2\xFF\x06\x41\x82\xB7'

    def Encrypt(self, Plaintext: str):
        '''
        Encrypt plaintext and return corresponding ciphertext.

        Args:
            Plaintext: A string that will be encrypted.

        Returns:
            Hexlified ciphertext string.
        '''
        plain_bytes = Plaintext.encode('utf-16-le')
        plain_bytes += b'\x00\x00'
        padded_plain_bytes = plain_bytes + os.urandom(Blowfish.block_size - len(plain_bytes) % Blowfish.block_size)

        cipher1 = Blowfish.new(self.Key1, Blowfish.MODE_CBC, iv=self.IV)
        cipher2 = Blowfish.new(self.Key2, Blowfish.MODE_CBC, iv=self.IV)
        return cipher1.encrypt(os.urandom(4) + cipher2.encrypt(padded_plain_bytes) + os.urandom(4)).hex()

    def Decrypt(self, Ciphertext: str):
        '''
        Decrypt ciphertext and return corresponding plaintext.

        Args:
            Ciphertext: A hex string that will be decrypted.

        Returns:
            Plaintext string.
        '''

        cipher1 = Blowfish.new(self.Key1, Blowfish.MODE_CBC, iv=self.IV)
        cipher2 = Blowfish.new(self.Key2, Blowfish.MODE_CBC, iv=self.IV)
        ciphered_bytes = bytes.fromhex(Ciphertext)
        if len(ciphered_bytes) <= 8:
            raise ValueError('Invalid Ciphertext.')

        padded_plain_bytes = cipher2.decrypt(cipher1.decrypt(ciphered_bytes)[4:-4])

        i = 0
        for i in range(0, len(padded_plain_bytes), 2):
            if padded_plain_bytes[i] == 0 and padded_plain_bytes[i + 1] == 0:
                break
        plain_bytes = padded_plain_bytes[0:i]

        try:
            return plain_bytes.decode('utf-16-le')
        except UnicodeDecodeError:
            raise (ValueError('Invalid Ciphertext.'))


class SecureCRTCryptoV2:

    def __init__(self, ConfigPassphrase: str = ''):
        '''
        Initialize SecureCRTCryptoV2 object.

        Args:
            ConfigPassphrase: The config passphrase that SecureCRT uses. Leave it empty if config passphrase is not set.
        '''
        self.IV = b'\x00' * AES.block_size
        self.Key = SHA256.new(ConfigPassphrase.encode('utf-8')).digest()

    def Encrypt(self, Plaintext: str):
        '''
        Encrypt plaintext and return corresponding ciphertext.

        Args:
            Plaintext: A string that will be encrypted.

        Returns:
            Hexlified ciphertext string.
        '''
        plain_bytes = Plaintext.encode('utf-8')
        if len(plain_bytes) > 0xffffffff:
            raise OverflowError('Plaintext is too long.')

        plain_bytes = \
            len(plain_bytes).to_bytes(4, 'little') + \
            plain_bytes + \
            SHA256.new(plain_bytes).digest()
        padded_plain_bytes = \
            plain_bytes + \
            os.urandom(AES.block_size - len(plain_bytes) % AES.block_size)
        cipher = AES.new(self.Key, AES.MODE_CBC, iv=self.IV)
        return cipher.encrypt(padded_plain_bytes).hex()

    def Decrypt(self, Ciphertext: str):
        '''
        Decrypt ciphertext and return corresponding plaintext.

        Args:
            Ciphertext: A hex string that will be decrypted.

        Returns:
            Plaintext string.
        '''
        cipher = AES.new(self.Key, AES.MODE_CBC, iv=self.IV)
        padded_plain_bytes = cipher.decrypt(bytes.fromhex(Ciphertext))

        plain_bytes_length = int.from_bytes(padded_plain_bytes[0:4], 'little')
        plain_bytes = padded_plain_bytes[4:4 + plain_bytes_length]
        if len(plain_bytes) != plain_bytes_length:
            raise ValueError('Invalid Ciphertext.')

        plain_bytes_digest = padded_plain_bytes[4 + plain_bytes_length:4 + plain_bytes_length + SHA256.digest_size]
        if len(plain_bytes_digest) != SHA256.digest_size:
            raise ValueError('Invalid Ciphertext.')

        if SHA256.new(plain_bytes).digest() != plain_bytes_digest:
            raise ValueError('Invalid Ciphertext.')

        return plain_bytes.decode('utf-8')


def find_session_files(folder_path, hostname):
    """
    Find configuration files containing the specified hostname in the given folder
    
    Args:
        folder_path: Sessions folder path
        hostname: Hostname to search for
        
    Returns:
        List of matching files
    """
    matching_files = []
    try:
        for file in os.listdir(folder_path):
            if file.lower().endswith('.ini') and hostname.lower() in file.lower():
                matching_files.append(file)
    except Exception as e:
        print(f"Error searching files: {e}")
    return matching_files

def process_session_file(file_path):
    """
    Process a single session configuration file, decrypt password
    
    Args:
        file_path: Full path to the configuration file
    """
    try:
        with open(file_path, 'r') as file:
            for line in file:
                raw_pwd = ""
                crypto = None
                if line.startswith('S:"Password"'):
                    raw_pwd = line.strip()
                    crypto = SecureCRTCrypto()
                elif line.startswith('S:"Password V2"'):
                    raw_pwd = line.strip()
                    crypto = SecureCRTCryptoV2('')

                if raw_pwd != "" and crypto is not None:
                    parts = line.strip().split(":")
                    if len(parts) > 2:
                        pwd_string = "".join(parts[2:]).strip()
                        pwd = crypto.Decrypt(pwd_string)
                        print(f"Decrypted password: {pwd}")
    except Exception as e:
        print(f"Error processing file: {e}")

if __name__ == '__main__':
    while True:
        # Get hostname from user input
        hostname = input("Enter hostname to search (enter 'q' to quit): ").strip()
        if hostname.lower() == 'q':
            break
            
        # Find matching files
        matching_files = find_session_files(session_store_folder, hostname)
        
        if not matching_files:
            print(f"No configuration files found containing '{hostname}'")
            continue
            
        # Display list of found files
        print("\nFound matching configuration files:")
        for i, file in enumerate(matching_files, 1):
            print(f"{i}. {file}")
            
        # Let user select a file
        while True:
            choice = input("\nSelect file number to process (enter 'b' to go back): ").strip()
            if choice.lower() == 'b':
                break
                
            try:
                choice_num = int(choice)
                if 1 <= choice_num <= len(matching_files):
                    selected_file = matching_files[choice_num - 1]
                    print(f"\nProcessing file: {selected_file}")
                    file_path = os.path.join(session_store_folder, selected_file)
                    process_session_file(file_path)
                    break
                else:
                    print("Invalid selection, please try again")
            except ValueError:
                print("Please enter a valid number")
