
import os
import sys


import unittest
class TestCeaserShift(unittest.TestCase):
    def testLowerCase(self):
        caesar1 = CaesarCipher('abc', 3,)
        self.assertEqual(caesar1.encrypt, "cde", "Should be 'cde'")

    def testTupleLowerCase(self):
        self.assertEqual()


# Part 1:
class CaesarCipher:
    def __init__(self, keyInput):
        if not isinstance(keyInput, str):
            raise TypeError
        CaesarCipher.key = keyInput

    # def encrypt(self, stringToEncrypt):
    #     encryptedString = for all letters in stringToEncrypt, (letter += key) % alphabetSize
    #     return encryptedString

    # def decrypt(self, encryptedString):
    #     decryptedString = for all letters in stringToEncrypt, (letter -= key) % alphabetSize
    #     return decryptedString
    

class VigenereCipher:
    def __init__(self, keyList):
        self.keyList = keyList

    # def encrypt(self, stringToEncrypt):
    #     encryptedString = "a"
    #     return encryptedString
    
    # def decrypt(self, encryptedString):
    #     decryptedString = "a"
    #     return decryptedString
    
# Part 2:
def getVigenereFromStr(key):
    # keyList = [for all letters in key, letter -= 'a']
    # return keyList
