
import os
import sys
import json
alphabetSize = 26
 
def shift(letter, shiftAmount):
    if not(letter.isalpha()):
        return letter
    baseASCIIValue = ord('a')
    if letter.isupper():
        baseASCIIValue = ord('A')
    shiftedLetterASCII = (ord(letter) - baseASCIIValue + shiftAmount) % alphabetSize
    return chr(shiftedLetterASCII + baseASCIIValue)

class CaesarCipher:
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
    keyIntList = []
    for character in key:
        if character.isalpha():
            if character.isupper():
                base = "A"
            else:
                base = "a"
            keyIntList.append(ord(character) - ord(base))
    return VigenereCipher(keyIntList)


def createDictionary(listOfFiles, dir_path):
    for file in listOfFiles:
        if os.path.splitext(file)[1] == ".json":
            fileName = os.path.join(dir_path, file)
            with open(fileName, 'r') as jsonfile:
                loadedDictionary = json.load(jsonfile)
                return loadedDictionary

def createEncryptorInstance(dictionary):
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