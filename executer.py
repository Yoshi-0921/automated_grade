import csv
import glob
import os
import subprocess

from inputs import INPUTS
from outputs import OUTPUTS


def execute(root):
    students_directory = sorted(glob.glob(f'{root}/*[!.csv]'))
    summary = [["Student ID"]]
    for i in range(len(INPUTS[root])):
        summary[0] += [f"compile_{i}", f"execution_{i}", f"result_{i}"]

    unexpected_files = []
    for directory_i, directory in enumerate(students_directory):
        result = [directory[len(root)+1:]] + ["×", "×", "×"] * len(INPUTS[root])
        output_files = glob.glob(f'{directory}/*[!.c]')
        output_files = sorted(output_files)
        for file in output_files:
            ex_skip = False
            file_skip = False

            print(f"({directory_i+1} / {len(students_directory)}) {file}====================")
            cmd = [fr"{file}"]

            try:
                ex = file[len(root)+10:]
                assert ex in INPUTS[root].keys()
            except AssertionError:
                print(f"unexpected file name: {file}")
                unexpected_files.append(file)
                while 1:
                    ex = input("Type the appropriate file name like 'ex1', 'ex2', ... or 'skip: ")
                    if ex in INPUTS[root].keys():
                        break
                    elif ex == 'skip':
                        ex_skip = True
                        break

            if not ex_skip:
                result[(int(ex[2:])-1) * 3 + 1] = "○"
                outputs = []
                for input_text in INPUTS[root][ex]:
                    try:
                        output = subprocess.run(cmd, input=input_text, encoding='UTF-8', timeout=20, capture_output=True)
                    except subprocess.TimeoutExpired as e:
                        output = e
                        setattr(output, 'returncode', 1)
                        output.stdout = "Timeout Error occurred."
                    except UnicodeDecodeError as e:
                        output = e
                        setattr(output, 'returncode', 1)
                        output.stdout = "Unicode Decode Error occurred."
                    outputs.append(output)
                if all(out.returncode == 0 for out in outputs):
                    result[(int(ex[2:])-1) * 3 + 2] = "○"

                if ex in OUTPUTS[root].keys():
                    for file_name in OUTPUTS[root][ex]:
                        while not file_skip:
                            try:
                                f = open(file_name, 'r', encoding='UTF-8')
                                data = f.read()
                                print(data)
                                f.close()
                                os.remove(file_name)
                                break
                            except FileNotFoundError:
                                file_name = input("Type the appropriate file name like 'hoge.txt', 'hoge', ... or 'skip': ")
                                if file_name == 'skip':
                                    file_skip = True

                while not file_skip:
                    corrects = [input(out.stdout + "\nType 'y' if correct else 'n': ") for out in outputs]
                    if all(correct == "y" for correct in corrects):
                        result[(int(ex[2:])-1) * 3 + 3] = "○"
                    if all(correct in ["y", "n"] for correct in corrects): break
                print()
        summary.append(result)

    print(f"Not executed: {unexpected_files}")

    with open(root+"/results.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerows(summary)
