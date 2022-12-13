#!/bin/bash
pdflatex -shell-escape -interaction=nonstopmode main.tex && biber main
