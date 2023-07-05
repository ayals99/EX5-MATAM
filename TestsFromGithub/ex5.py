
import os
import sys
import json
alphabetSize = 26
 

def shift(letter, shiftAmount):
    """shifts a letter forwards or backwards in the ABC.
    if input is not a letter, it will be returned untouched"""
    if not(letter.isalpha()):
        return letter
    baseASCIIValue = ord('a')
    if letter.isupper():
        baseASCIIValue = ord('A')
    shiftedLetterASCII = (ord(letter) - baseASCIIValue + shiftAmount) % alphabetSize
    return chr(shiftedLetterASCII + baseASCIIValue)

class CaesarCipher:
    """holds a key (int) and shifts all characters that are alpha by the key."""
    def __init__(self, keyInput):
        self.key = keyInput

    def encrypt(self, stringToEncrypt):
        encryptedString = ""
        for character in stringToEncrypt:
            encryptedString += shift(character, self.key)
        return encryptedString

    def decrypt(self, encryptedString):
        reverseCypher = CaesarCipher(-1 * self.key) 
        return reverseCypher.encrypt(encryptedString)  #use encryt in order to not duplicate code 
    
class VigenereCipher:
    """holds a key (list of ints) and shifts all characters in the string.
    The shifting occurs by index, so the first letter will be shifted according to the first value in keyList
    and so forth."""
    def __init__(self, listOfNumbers):
        self.keyList = listOfNumbers
        self.amountOfKeys = len(listOfNumbers)

    def encrypt(self, stringToEncrypt):
        encryptedString = ""
        indexInList = 0
        for character in stringToEncrypt:
            encryptedString += shift(character, self.keyList[indexInList])
            if character.isalpha():
                indexInList = (indexInList + 1) % self.amountOfKeys
        return encryptedString
    
    def decrypt(self, encryptedString):
        reverseCypher = VigenereCipher([-1*key for key in self.keyList])
        return reverseCypher.encrypt(encryptedString) # in order to avoid code duplication
    
# Part 2:
def getVigenereFromStr(key):
    """turns a string into a list of ints, that is a key. Treats lowercase and uppercase the same.
    Disregards characters that are not alpha."""
    keyIntList = []
    for character in key:
        if character.isalpha():
            base = "a"
            if character.isupper():
                base = "A"
            keyIntList.append(ord(character) - ord(base))
    return VigenereCipher(keyIntList)


def createDictionary(listOfFiles, dir_path):
    """loads the .json file into a dictionary."""
    for file in listOfFiles:
        if os.path.splitext(file)[1] == ".json":
            fileName = os.path.join(dir_path, file)
            with open(fileName, 'r') as jsonfile:
                loadedDictionary = json.load(jsonfile)
                return loadedDictionary

def createEncryptorInstance(dictionary):
    """reads from the dictionary what kind of encryption we are using and reads the key.
    Returns an instance of the cipher we want to use."""
    typeOfEncryption = dictionary["type"]
    cipher = None
    if typeOfEncryption == "Vigenere":
        if isinstance(dictionary['key'], str): 
            cipher = getVigenereFromStr(dictionary['key'])
        else:
            cipher = VigenereCipher(dictionary['key'])
    elif typeOfEncryption == "Caesar":
        cipher = CaesarCipher(dictionary['key'])
    return cipher

def isEncryptOn(dictionary):
    return dictionary.get('encrypt') == "True"

def encryptFile(fileToEncrypt, functionToPerform, outFile):
    wholeFileLine = fileToEncrypt.read()
    outFile.write(functionToPerform(wholeFileLine))

def loadEncryptionSystem(dir_path):
    """goes through all files that end with ".enc" or ".txt" in the directory and encrypts/decrypts them,
    accoring to the instructions in the config.json file.
    We then write them to a file with the same name (and create it if doesn't exist) but opposite suffix"""
    listOfFiles = os.listdir(dir_path)
    dictionary = createDictionary(listOfFiles, dir_path)

    encryptBool = isEncryptOn(dictionary)
    encryptorInstance = createEncryptorInstance(dictionary)

    functionToPerform = encryptorInstance.encrypt if encryptBool else encryptorInstance.decrypt
    desiredFileSuffix = ".txt" if encryptBool else ".enc"
    outFileSuffix = ".enc" if encryptBool else ".txt"

    for file in listOfFiles:
        if os.path.splitext(file)[1] == desiredFileSuffix:
            fileName = os.path.join(dir_path, file)
            with open(fileName, 'r') as fileToRead:
                outFilePath = os.path.splitext(fileName)[0] + outFileSuffix 
                with open(outFilePath, 'w') as outFile:
                    encryptFile(fileToRead, functionToPerform, outFile)