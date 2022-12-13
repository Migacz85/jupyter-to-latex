
# This file is runing latex in build directory
import subprocess
import os

def run_latex():
    # set your path to latex folder
    cwd = os.getcwd()
    pdftex = cwd + "/latex/"

    # specify the output directory for LaTeX and Biber
    output_dir = "build"

    command = ["bash", "-c"]
    command.append("pdflatex -shell-escape -interaction=nonstopmode -output-directory=" + output_dir + " main.tex")
    command[2] = command[2] + " && biber --output_directory " + output_dir + " main && "
    command[2] = command[2] + " pdflatex -shell-escape -interaction=nonstopmode -output-directory=" + output_dir + " main.tex"

    subprocess.call(command, cwd=pdftex, stdout=open(os.devnull, 'wb'))
    # subprocess.call(command, cwd=pdftex )

run_latex()
