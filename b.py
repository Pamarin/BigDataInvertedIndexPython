#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright (2017) Hochschule Karlsruhe - Technik und Wirtschaft
Jean-Luc Burot <jburot@gmail.com>
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

    def intersect(self,wordA,wordB):
        # Prüfen, ob beide Wörter im Index existieren.
        if len(wordA) > 0 and len(wordB) > 0:
            # Intersect Index erstellen.
            intersectIndex = []
            if wordA in self.words and wordB in self.words:
                # Indexe für die beiden Wörter holen.
                wordAIndex = self.words[wordA]
                wordBIndex = self.words[wordB]
                # Listenpositionen festhalten, um zeitlich linear bleiben zu können.
                posA = 0
                posB = 0
                # Zeitlich linear aufwärts iterieren, bis beide Listen einmalig durchlaufen sind.
                while posA < len(wordAIndex) and posB < len(wordBIndex):
                    if wordAIndex[posA] == wordBIndex[posB]:
                        # Intersection hinzufügen, da beide Wörter denselben Document Identifier haben.
                        intersectIndex.append(posA)
                        # Beide Positionspointer anheben.
                        posA += 1
                        posB += 1
                    elif wordAIndex[posA] < wordBIndex[posB]:
                        # Positionspointer von wordA anheben, da der Index hier kleiner ist.
                        posA += 1
                    elif wordAIndex[posA] > wordBIndex[posB]:
                        # Positionspointer von wordB anheben, da der Index hier kleiner ist.
                        posB += 1
            else:
                # Ausgabe über nicht im Index gefundene Wörter generieren.
                if wordA not in self.words:
                    print("\"" + wordA + "\" could not be found in the index.")
                if wordB not in self.words:
                    print("\"" + wordB + "\" could not be found in the index.")
            # Rückgabe der Intersection Indexliste.
            return intersectIndex

        else:
            print("Bad input! Intersection computation cannot be started.")

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

    wordA = wordB = "input"

    # Intersections solange anfragen, solange der User etwas eingibt.
    while len(wordA) > 0 and len(wordB) > 0:
        # Userinput holen.
        print()
        print("Compute intersection between two words!")
        print("Word A:")
        wordA = input()
        print("Word B:")
        wordB = input()

        # Intersection berechnen.
        intersectionList = wa.intersect(wordA, wordB)

        if intersectionList is None:
            print("No intersection found.")
        else:
            # Ausgabe des Index.
            indexString = "[" + ", ".join(str(e) for e in intersectionList) + "]"

            # Bildschirmausgabe.
            print("The words \"" + wordA + "\" and \"" + wordB + "\" have intersections at " + indexString + ".")
