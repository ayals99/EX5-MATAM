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
    assert vigenere.encrypt("we wish you the best of luck in all of your exams") == "ya isbq akg dqn daed xo nqou rw chx yo hqqd ogjoo"
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
           files = set(os.listdir(expected) + os.listdir(curr_dir))
           for file in files:
                total_tests += 1
                expected_file = os.path.join(expected, file)
                if not os.path.isfile(expected_file):
                    print(f"Test #{total_tests} Failed: your code created an unexpected file: '{expected_file}'")
                    failures.append((total_tests, expected_file))
                    continue
                output = os.path.join(curr_dir, file)
                if not os.path.isfile(output):
                    print(f"Test #{total_tests} Failed: your code did not create the following file: '{file}'")
                    failures.append((total_tests, output))
                    continue
                if not filecmp.cmp(output, expected_file):
                    print(f"Test #{total_tests} Failed: file content does not match for '{expected_file}' and '{output}'")
                    failures.append((total_tests, expected_file))
                    continue

                print(f"Test #{total_tests} Passed: '{file}'")
                successes += 1

    print(f"\nTotal number of tests passed: {successes} out of {total_tests}")
    print("\nFailed tests:")
    for test_num, failed_test in failures:
        print(f"Test #{test_num} - '{failed_test}'")

if __name__ == "__main__":
    test_process_directory()

