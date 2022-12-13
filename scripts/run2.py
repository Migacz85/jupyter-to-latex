# This file is runing latex in main directory
import subprocess
import os

def run_latex():

    # set your path to latex folder\n",
    cwd = os.getcwd()
    pdftex = cwd + "/latex/"

    command = ["bash", "-c"]
    command.append("pdflatex -shell-escape -interaction=nonstopmode main.tex")
    command[2] = command[2] + " && biber main && "
    command[2] = command[2] + " pdflatex -shell-escape -interaction=nonstopmode main.tex"

    subprocess.call(command, cwd=pdftex, stdout=open(os.devnull, 'wb'))

    #other command
    #latexmk -cd -lualatex main.tex

run_latex()

