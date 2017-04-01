#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright (2017) Hochschule Karlsruhe - Technik und Wirtschaft
Jean-Luc Burot <jburot@gmail.com>
Jean-Pierre Bourhis <jp.bourhis@gmail.com>
"""

import re
import sys
import operator
import os

class WordAggregator:
    def __init__(self,sourceAddress):
        # Quell-Dokument-Adresse merken.
        self.sourceAddress = sourceAddress
        # Erstelle leeren Index.
        self.words = {}

    def run(self):
        # Dokument Id erstellen.
        doc_id = 0
        # Prüfe, ob Datei existiert.
        if os.path.isfile(self.sourceAddress):
            # Datei in den Zwischenspeicher laden.
            with open(self.sourceAddress) as file:
                # Dateiinhalt zeilenweise durchlaufen.
                for line in file:
                    # Anzahl Durchläufe merken.
                    doc_id += 1
                    # Einzelne Wörter durchlaufen.
                    for word in re.split("\W+",line):
                        # Alle Großbuchstaben in Kleinbuchstaben umwandeln.
                        word = word.lower()
                        # Wort hat mindestens 1 Buchstabe.
                        if len(word)>0:
                            # Wenn Liste leer.
                            if word not in self.words:
                                # Erstelle neue Liste.
                                self.words[word] = []

                            # Nur Wort einfügen, wenn in doc_id nicht doppelt.
                            if not ((len(self.words[word]) > 0) and not (doc_id not in self.words[word])):
                                # Füge doc_id zur Liste hinzu.
                                self.words[word].append(doc_id)
        else:
            print("The file '" + self.sourceAddress + "' could not be found.")
            # Exit program.
            sys.exit()


class IndexWriter:
    def __init__(self,targetAddress,wordsIndex):
        # Ziel-Dokument-Adresse merken.
        self.targetAddress = targetAddress
        # Wörter-Intex merken.
        self.wordsIndex = wordsIndex

    def run(self):
        # Sortiere den 'dict' nach seiner ersten Spalte.
        self.wordsIndexSorted = sorted(self.wordsIndex.items(), key=operator.itemgetter(0))
        # Ausgabe-Datei öffnen.
        targetFile = open(self.targetAddress,"w")
        # Index in die Ausgabe-Datei schreiben.
        for word, inverted_list in self.wordsIndexSorted:
            # Ausgabe des Index.
            indexString = "[" + ", ".join(str(e) for e in inverted_list) + "]"
            # Wort und indexString in Datei schreiben.
            targetFile.write(word + " " + indexString + os.linesep)
            # Bildschirmausgabe.
            print(word, indexString)

if __name__ == "__main__":
    print("Welcome to WordAggregator (Python3 Version)!")
    print()

    # Quell-Datei-Adresse muss als Argument mitgegeben werden.
    if (len(sys.argv) != 3):
        print("Error: Missing arguments -> sourceAddress, targetAddress.")
        # Exit program.
        sys.exit()

    
    # Get address argument from command line.
    sourceAddress=sys.argv[1]
    targetAddress=sys.argv[2]
    
    # Dateianalyse.
    wa = WordAggregator(sourceAddress)
    wa.run()

    # Speichern des Inhalts in eine Datei.
    iw = IndexWriter(targetAddress,wa.words)
    iw.run()
