import os
import tempfile
import shutil
import filecmp
import difflib
import ex5


class Playground():
    def __init__(self, path):
        self.path = path

    def __enter__(self):
        temp_dir = "./tmpdir/"
        os.mkdir(temp_dir)
        self.temp_dir = temp_dir
        return temp_dir

    def __exit__(self, *_):
        shutil.rmtree(self.temp_dir)


def format_error_message(f1, f2):
    ret = f"'{f1}' and '{f2}' do not match:\n"
    with open(f1, "r") as f1:
        text1 = f1.readlines()
    with open(f2, "r") as f2:
        text2 = f2.readlines()
    diff = "\n".join(difflib.unified_diff(text1, text2))
    return ret + diff


def test_vigenere_cipher():
    vigenere = ex5.VigenereCipher([3])
    assert vigenere.encrypt("l") == "o"
    vigenere = ex5.VigenereCipher([2, -4, -14, -16, -17, -17])
    assert vigenere.encrypt(
        "we wish you the best of luck in all of your exams") == "ya isbq akg dqn daed xo nqou rw chx yo hqqd ogjoo"
    vigenere = ex5.VigenereCipher([1, 2, 3, 4, -5])
    assert vigenere.encrypt("Hello World!") == "Igopj Xqupy!"


def test_vigenere_from_str():
    vigenere = ex5.getVigenereFromStr("python rules, C drools")
    assert vigenere.encrypt("JK, C is awesome") == "YI, V pg nnydseg"
    assert vigenere.decrypt("YI, V pg nnydseg") == "JK, C is awesome"


def test_process_directory():
    total_tests = 0
    successes = 0
    failures = []

    for expected, output in zip(os.listdir("tests/expected"), os.listdir("tests/output")):
        if expected.startswith("."):
            continue
        curr_dir = os.path.join("tests/output", output)

        with Playground(curr_dir) as pg:
            ex5.loadEncryptionSystem(curr_dir)
            expected = os.path.join("tests/expected", expected)
            files = list(set(os.listdir(expected)).union(set(os.listdir(curr_dir))))
            total_tests += 1
            success_flag = True
            for file in files:
                expected_file = os.path.join(expected, file)
                if not os.path.isfile(expected_file):
                    print(
                        f"Test Failed: your code created an unexpected file: '{expected_file}' in directory '{curr_dir}'")
                    success_flag = False
                    break
                output = os.path.join(curr_dir, file)
                if not os.path.isfile(output):
                    print(
                        f"Test Failed: your code did not create the following file: '{file}' in directory '{curr_dir}'")
                    success_flag = False
                    break
                if not filecmp.cmp(output, expected_file):
                    print(
                        f"Test Failed: file content does not match for '{expected_file}' and '{output}' in directory '{curr_dir}'")
                    success_flag = False
                    break
            if success_flag:
                print(f"Test Passed for directory: '{curr_dir}'")
                successes += 1
