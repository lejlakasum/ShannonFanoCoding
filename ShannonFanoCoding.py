from collections import namedtuple
import tkinter as tk
from tkinter import filedialog, Text
import os
from datetime import datetime

Symbol = namedtuple("Symbol", "Symbol, Count, Coding, NumberOfBits")


def CreateSymbolTuple(sortedSymbols):
    symTuple = list()
    for sym in sortedSymbols:
        symTuple.append(Symbol(sym[0], sym[1], "", 0))
    return symTuple


def SortByFrequency(inputSymbols):
    symbolsFrequency = dict()
    for symbol in inputSymbols:
        if symbol in symbolsFrequency:
            symbolsFrequency[symbol] += 1
        else:
            symbolsFrequency[symbol] = 1

    symbolsFrequency = sorted(symbolsFrequency.items(),
                              key=lambda x: x[1], reverse=True)

    return symbolsFrequency


def findDivideingElement(symTuple, first, last):
    if abs(first-last) == 1:
        return 0

    differenceList = list()

    for i in range(first, last):
        sumA = 0
        sumB = 0
        for j in range(i+1):
            sumA += symTuple[j].Count
        for j in range(i+1, last):
            sumB += symTuple[j].Count

        differenceList.append(abs(sumA-sumB))

    if len(differenceList) == 0:
        return 0
    return differenceList.index(min(differenceList))+1+first


def ShannonFanoCoding(symTuple, first, last):
    if (len(symTuple) == 1):
        symTuple[0] = Symbol(symTuple[0].Symbol,
                             symTuple[0].Count, "0", 1)

    dividingElement = findDivideingElement(symTuple, first, last)
    if dividingElement != 0:
        for i in range(first, dividingElement):
            newCoding = symTuple[i].Coding + '0'
            symTuple[i] = Symbol(symTuple[i].Symbol,
                                 symTuple[i].Count, newCoding, symTuple[i].NumberOfBits+1)
        for i in range(dividingElement, last):
            newCoding = symTuple[i].Coding + '1'
            symTuple[i] = Symbol(symTuple[i].Symbol,
                                 symTuple[i].Count, newCoding, symTuple[i].NumberOfBits+1)

        ShannonFanoCoding(symTuple, first, dividingElement)
        ShannonFanoCoding(symTuple, dividingElement, last)

    return symTuple


def ShannonFanoDecod(input, dictionary):
    result = []
    work = ""
    for symbol in input:
        work += symbol
        for x, y in dictionary.items():
            if (y == work):
                result.append(x)
                work = ""
                break

    return result


def guiCode(inputSymbols):
    sortedSymbols = SortByFrequency(inputSymbols)
    symTuple = CreateSymbolTuple(sortedSymbols)
    symTuple = ShannonFanoCoding(symTuple, 0, len(symTuple))

    result = dict()
    for sym in symTuple:
        result[sym.Symbol] = sym.Coding

    coded = ""
    for x in inputSymbols:
        coded += result[x]

    labelCompresed.configure(text=coded)

    bitsNonCommpresed = len(inputSymbols) * 8

    bitsResult = dict()
    for sym in symTuple:
        bitsResult[sym.Symbol] = sym.NumberOfBits
    bitsCommpresed = 0
    for x in inputSymbols:
        bitsCommpresed += bitsResult[x]

    labelStepen.configure(text=bitsNonCommpresed/bitsCommpresed)

    return coded, result


def btnCodeClick():
    try:
        guiCode(e1.get())
        infoLabel.configure(text="Uspjesno izvrsena kompresija", fg="green")
    except:
        infoLabel.configure(text="Doslo je do greske", fg="red")


def btnLoadFileClick():
    try:
        filename = filedialog.askopenfilename(
            initialdir="/", title="Select File", filetypes=(("Textual", "*.txt"), ("All Files", "*.*")))
        f = open(filename, "r")
        coded, result = guiCode(f.read())
        name = filename.split("/")[-1]
        f = open("coded_" + name, "w")
        f.write(coded)
        f.close()
        sifarnik = ""
        for x, y in result.items():
            sifarnik += x + ":" + y + "\n"
        f = open("codes_"+name, "w")
        f.write(sifarnik)
        f.close()
        infoLabel.configure(
            text="Uspjesno izvrsena kompresija i kreirani fajlovi", fg="green")
    except:
        infoLabel.configure(text="Doslo je do greske", fg="red")


def btnLoadFileDecodeClick():
    try:
        filename = filedialog.askopenfilename(
            initialdir="/", title="Select File", filetypes=(("Textual", "*.txt"), ("All Files", "*.*")))

        f = open(filename, "r")
        name = filename.split("/")[-1].split("_")[-1]
        f2 = open("codes_" + name, "r")
        lines = f2.readlines()
        codes = dict()
        for line in lines:
            if (len(line) > 2):
                splited = line.split(":")
                codes[splited[0]] = splited[1].split("\n")[0]

        decoded = ShannonFanoDecod(f.read(), codes)
        decodedString = ""
        for x in decoded:
            decodedString += x

        f = open("decoded_"+filename.split("/")
                 [-1].split(".")[0] + ".txt", "w")
        f.write(decodedString)
        f.close()
        infoLabel.configure(
            text="Uspjesno izvrsena dekompresija i kreiran fajl", fg="green")
    except:
        infoLabel.configure(text="Doslo je do greske", fg="red")

    labelDeCompresed.configure(text=decodedString)


root = tk.Tk()

canvas = tk.Canvas(root, height=400, width=400, bg="white")
canvas.pack()

frame = tk.Frame(canvas, bg="white")
frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)

infoLabel = tk.Label(frame, text="", bg="white")
infoLabel.pack()
emptyLabel = tk.Label(frame, text="", bg="white")

l1 = tk.Label(frame,
              text="Unesite simbole za kodiranje", bg="white", padx=5, pady=5)
l1.pack()

e1 = tk.Entry(frame)
e1.pack()

btnCode = tk.Button(frame, text="Kopresuj", command=btnCodeClick)
btnCode.pack()

labelCompresed = tk.Label(
    frame, text="Kompresovani tekst", bg="white", padx=1, pady=1, wraplength=400)
labelCompresed.pack()

labelStepen = tk.Label(
    frame, text="Stepen kompresije", bg="white", padx=1, pady=1)
labelStepen.pack()

btnLoadFile = tk.Button(frame, text="Ucitaj txt fajl",
                        command=btnLoadFileClick)
btnLoadFile.pack()


btnLoadFileDecode = tk.Button(
    frame, text="Ucitaj fajl za dekompresiju", command=btnLoadFileDecodeClick)
btnLoadFileDecode.pack()

labelDeCompresed = tk.Label(
    frame, text="Dekompresovani tekst", bg="white", padx=1, pady=1, wraplength=300)
labelDeCompresed.pack()

root.mainloop()
