
import os
import sys
import json

# import unittest
# class TestCeaserShift(unittest.TestCase):
#     def testLowerCase(self):
#         caesar1 = CaesarCipher('abc', 3,)
#         self.assertEqual(caesar1.encrypt, "cde", "Should be 'cde'")

#     def testTupleLowerCase(self):
#         self.assertEqual()

# Part 1:
lowerCaseList = "abcdefghijklmnopqrstuvwxyz"
alphabetSize = len(lowerCaseList)

def shift(letter, shiftAmount):
    if not(letter.isalpha):
        return letter
    alphabet = lowerCaseList
    if letter.isupper:
        isUpper = True
        alphabet = lowerCaseList.upper
    else:
        isUpper = False
    shiftedLetterIndex = (alphabet.find(letter) + shiftAmount) % alphabetSize
    return alphabet[shiftedLetterIndex]
 
class CaesarCipher:
    def __init__(self, keyInput):
        CaesarCipher.key = keyInput

    def encrypt(self, stringToEncrypt):
        encryptedString = ""
        for character in stringToEncrypt:
            encryptedString += shift(character)
        return encryptedString

    def decrypt(self, encryptedString):
        reverseCypher = CaesarCipher(-1 * self.key) 
        return reverseCypher.encrypt(encryptedString)  #use encryt in order to not duplicate code 
    
class VigenereCipher:
    def __init__(self, listOfNumbers):
        self.keyList = listOfNumbers
        self.amountOfKeys = len(listOfNumbers)

    def encrypt(self, stringToEncrypt):
        encryptedString = ""
        indexInList = 0
        for character in stringToEncrypt:
            encryptedString += shift(character, self.keyList[indexInList])
            if character.isalpa:
                indexInList = (self.keyList + 1) % self.amountOfKeys
        return encryptedString
    
    def decrypt(self, encryptedString):
        reverseCypher = VigenereCipher([-1*key for key in self.keyList])
        return reverseCypher.encrypt(encryptedString) # in order to avoid code duplication
    
# Part 2:
def getVigenereFromStr(key):
    keyIntList = []
    for character in key:
        if not character.isalpha:
            continue
        #assuming character is an uppercase of lowercase letter
        base = ""
        if character.isupper:
            base = "A"
        if character.islower:
            base = "a"
        keyIntList.append( (ord(character) - ord(base) ) % alphabetSize)


def createDictionary(listOfFiles, dir_path):
    for file in listOfFiles:
        if file.endswith(".json"):
            fileName = os.path.join(dir_path, file)
            with open(fileName, 'r') as JSONfile:
                loaded_dict = json.load(JSONfile)
                return loaded_dict

def createEncryptorInstance(dictionary):
    if dictionary["type"] == "Vigenere":
        return VigenereCipher(dictionary["key"])
    if dictionary["type"] == "Ceaser":
        return CaesarCipher(dictionary["key"])
    
def isEncryptOn(dictionary):
    if dictionary["encrypt"] == "True":
        return True
    else:
        return False

def encryptFile(fileToEncrypt, functionToPerform, outFile):
    for line in fileToEncrypt:
        outFile.write(outputLine = functionToPerform(line))

def loadEncryptionSystem(dir_path):
    listOfFiles = os.listdir(dir_path)
    dictionary = createDictionary(listOfFiles, dir_path)
    
    encryptBool = isEncryptOn(dictionary)
    encryptionType = createEncryptorInstance(dictionary)

    if encryptBool == True:
        desiredFileSuffix = ".enc"
        outFileSuffix = ".txt"
        functionToPerform = encryptionType.encrypt
    else:
        desiredFileSuffix = ".txt"
        outFileSuffix = ".enc"
        functionToPerform = encryptionType.decrypt

    for file in listOfFiles and fileName.endswith(desiredFileSuffix):
        fileName = os.path.join(dir_path, file)
        with open(fileName, 'r') as fileToRead:
            with open(os.path.join(dir_path, fileName.os.path.splitext(), outFileSuffix), 'w') as outFile:
                encryptFile(fileToRead, functionToPerform, outFile)