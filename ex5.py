
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
        CaesarCipher.key = keyInput

    # def encrypt(self, stringToEncrypt):
    #     encryptedString = for all letters in stringToEncrypt, (letter += key) % alphabetSize
    #     return encryptedString

    # def decrypt(self, encryptedString):
    #     decryptedString = for all letters in stringToEncrypt, (letter -= key) % alphabetSize
    #     return decryptedString
    

class VigenereCipher:
    def __init__(self, listOfNumbers):
        self.keyList = listOfNumbers

    # def encrypt(self, stringToEncrypt):
    #     encryptedString = for all letters in stringToEncrypt and for all numbers in self.keyList, letter = shift(letter, number) 
    #     return encryptedString
    
    # def decrypt(self, encryptedString):
    #     decryptedString = for all letters in stringToEncrypt and for all numbers in self.keyList, letter = shift(letter, -1*number) 
    #     return decryptedString
    
# Part 2:
def getVigenereFromStr(key):
    # keyList = [for all letters in key, if letter is a char, then letter -= 'a']
    # return keyList
