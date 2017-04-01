#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright (2017) Hochschule Karlsruhe - Technik und Wirtschaft
Jean-Luc Burot <jburot@gmail.com>
Jean-Pierre Bourhis <jp.bourhis@gmail.com>
"""

import re
import sys
import time

def intersect(list1,list2):
    interesect_inverted_lists = {}		
    l1=len(list1.inverted_lists)
    l2 = len(list2.inverted_lists)
    if l1>=l2:
       l = l1
       mybiglist=list1
       mysmalllist=list2
    else :
       l=l2
       mybiglist=list2
       mysmalllist=list1
    
    for word, inversted_list in mysmalllist.inverted_lists.items():	
        if word in mybiglist.inverted_lists:
           #add the list because its common to both list
           interesect_inverted_lists[word] = []
           #Now we need to do the linear time search
           x=0
           z=0
           wl1=len(mybiglist.inverted_lists[word])
           wl2 = len(mysmalllist.inverted_lists[word])
           if wl1>=wl2:
              wl = wl1
              wbiglist=mybiglist.inverted_lists[word]
              wsmalllist=mysmalllist.inverted_lists[word]
           else :
              wl=wl2
              wbiglist=mysmalllist.inverted_lists[word]
              wsmalllist=mybiglist.inverted_lists[word]

           stop="false"
           while stop=="false": 
              if wbiglist[x] == wsmalllist[z]:
              #Match found with the same index value
                  interesect_inverted_lists[word].append(wbiglist[x])
                  if len(wsmalllist)> z+1 and len(wbiglist)> x+1:
                    z+=1
                    x+=1
                  else:
                     # Both list can't be incremented
                     stop="true"
              elif wbiglist[x] > wsmalllist[z]:
                  if len(wsmalllist)> z+1:
                     z+=1
                  else:
                      #If we reached the limit of the smaller list, we increment the index of the bigger one
                      if len(wbiglist)> x+1:
                         x+=1
                      else:
                         #Both list can't be incremented
                         stop="true"
              elif wbiglist[x] < wsmalllist[z]:
                   if len(wbiglist)> x+1:
                         x+=1
                   else:
                     #If we reached the limit of the bigger list, we increment the index of the smaller one
                     if len(wsmalllist)> z+1:
                        z+=1
                     else:
                        #Both list can't be incremented
                        stop="true"

       #If the common word between both list don't have common id, we remove it from the dictionary
        if len(interesect_inverted_lists[word]) == 0:
            del interesect_inverted_lists[word]

       #End of for word

    #Print the result			
    for word, inverted_list in interesect_inverted_lists.items():
        print(word, len(inverted_list), '[%s]' % ', '.join(map(str, inverted_list)))



class InvertedIndex:
    """ Ein sehr einfacher Invertierter Index. """

    def __init__(self):
        """ Erstelle leeren Index. """
        self.inverted_lists = {}
        self.document_id_lists = []
        self.doc_id=0
        self.document_line = []
        self.intersect_id = []


    def read_from_file(self,file_name):
        """ Erstelle Index aus File mit 1 Dokument pro Zeile.
        >>> ii = InvertedIndex()
        >>> ii.read_from_file("sample-documents.txt")
        >>> sorted(ii.inverted_lists.items())
        [('again', [3]), ('document', [1, 2, 3]), ('one', [1, 3]), ('second', [2])]
        """
        
        with open(file_name) as file:
            for line in file:		
                self.doc_id += 1
                self.document_line.append(line) 	
                for word in re.split("\W+",line):
                    word = word.lower()
                    if len(word)>0:
                        # wenn Wort zum ersten Mal, neue Liste
                        if word not in self.inverted_lists:
                            self.inverted_lists[word] = []
                        # fuege doc_id zur Liste hinzu
                        if self.doc_id not in self.inverted_lists[word]:			   			
                           self.inverted_lists[word].append(self.doc_id)
                        if self.doc_id not in self.document_id_lists:
                           self.document_id_lists.append(self.doc_id)

    def search_word(self):
        """ Such nach Woerter """
        userinput = raw_input("Please write up to two words separated by a space to find relevant document(s) \n")
        print("Please standby..")
        time.sleep(1)
        word_list = []

    # Function to save up to two valid words given by the user
        for word in re.split("\W+",userinput):
            word = word.lower()
            if len(word)>0 and len(word_list)<2:
               word_list.append(word)
            elif len(word)>0 and len(word_list)==2:
                 print("\n")
                 print("Error Order 66: Hack detected")
                 time.sleep(1)
                 print("Running trace......")
                 time.sleep(4)
                 print("...Social security number acquired")
                 time.sleep(1)
                 print("You are now put in the relevant list")
                 time.sleep(2)
                 print("Contacting human asset number AF00MCD1....")
                 time.sleep(4)
                 print("Authorities have been alerted.. please stay still until they arrest you")
                 time.sleep(2)
                 print("And have a pleasant day :)")
                 print("\n")
                 sys.exit()
            elif len(word)==0 and len(word_list)==0:
                 print("Why call me if you are not looking for something? I go back to sleep")
                 sys.exit()
        # End of function

        # This Print the result if any match is found without specific order
        #for word in word_list:
            #if word in self.inverted_lists:
               #print("Match found in inverted list for the term ", word , " id : " , self.inverted_lists[word])
            #else:
               #print("No Match found")

         # This Print the result if any match is found without specific order
        #print("Now Sorted")
        match_list = []
        relevant_id_list= []
        common_id_list = []

        for word in word_list:
             if word in self.inverted_lists:
                match_list.append(word)



         # If Two words given are somewhere in the file, we need to check if they have common ids
        if len(match_list) == 2:
              #print(match_list[0])
              #print(match_list[1])
              #for ids in self.inverted_lists[match_list[0]]:
                  #print ("Myids " , ids)

              # This works
              self.intersect_word(self.inverted_lists[match_list[0]], self.inverted_lists[match_list[1]])


              # Intersect id was put as self , because return list won t work
              common_id_list = self.intersect_id
              #print("Common")
              #for id in common_id_list:
                 # print(id)
              # its possible they have something in common or nothing at all
              if len(common_id_list) > 0:
                 # its possible they have something in common
                 #print("Common Match found for two words")
                 relevant_id_list = common_id_list
                 #for id in relevant_id_list:
                     #print(self.document_line[id - 1])
                 # Need to add the other uncommon ids for list 1
                 for other_ids in self.inverted_lists[match_list[0]]:
                     if other_ids not in relevant_id_list:
                        relevant_id_list.append(other_ids)
                 # Need to add the other uncommon ids for list 1
                 for other_ids in self.inverted_lists[match_list[1]]:
                     if other_ids not in relevant_id_list:
                        relevant_id_list.append(other_ids)

              else:
                 #print("No Common Match found for two words")
                 relevant_id_list = self.inverted_lists[match_list[0]] + self.inverted_lists[match_list[1]]
        elif len(match_list) == 1:
             #print("Only one word Match found")
             relevant_id_list = self.inverted_lists[match_list[0]]
        #print("relevant ids")
        #for id in relevant_id_list:
            #print(id)
        #print("..")

        print("Document Matched:")
        if len(relevant_id_list) > 0:
           nb_loop=0
           while nb_loop < len(relevant_id_list) and nb_loop<3:
                 nb_loop+=1		 	
                 print(self.document_line[relevant_id_list[nb_loop-1]-1])
        else:
            print("I am sorry but there is no match")













    def intersect_word(self,list1,list2):
       self.intersect_id = []
       x=0
       z=0
       wl1=len(list1)
       wl2 = len(list2)
       if wl1>=wl2:
          wl = wl1
          wbiglist=list1
          wsmalllist=list2
       else :
          wl=wl2
          wbiglist=list2
          wsmalllist=list1

       stop="false"
       while stop=="false":
           #print("Looping")
           if wbiglist[x] == wsmalllist[z]:
              #print("wbiglist ", wbiglist[x], " == wsmalllist ", wsmalllist[z])
              #Match found with the same index value
              self.intersect_id.append(wbiglist[x])
              if len(wsmalllist)> z+1 and len(wbiglist)> x+1:
                 z+=1
                 x+=1
              else:
                 #Both list can't be incremented
                 #print("Stop at len(wsmalllist)> z+1 and len(wbiglist)> x+1")
                 stop="true"
           elif wbiglist[x] > wsmalllist[z]:
                #print("wbiglist " , wbiglist[x] , " > wsmalllist " , wsmalllist[z] )
                if len(wsmalllist)> z+1:
                   z+=1
                else:
                   #If we reached the limit of the smaller list, we increment the index of the bigger one
                   if len(wbiglist)> x+1:
                      x+=1
                   else:
                      #Both list can't be incremented
                      #print("Stop at wbiglist[x] > wsmalllist[z]")
                      stop="true"
           elif wbiglist[x] < wsmalllist[z]:
                   #print("wbiglist ", wbiglist[x], " < wsmalllist ", wsmalllist[z])
                   if len(wbiglist)> x+1:
                      x+=1
                   else:
                     #If we reached the limit of the bigger list, we increment the index of the smaller one
                     if len(wsmalllist)> z+1:
                        z+=1
                     else:
                       #Both list can't be incremented
                       #print("wbiglist[x] < wsmalllist[z]")
                       stop="true"

           #return intersect_id
           #for id in self.intersect_id:
               ##print(id)
           #return  intersect_id this doesnt work for unknown reasons


if __name__ == "__main__":
    """ Ausgabe: Laenge der Invertierten Listen (Haeufigkeit der Woerter) im Input File. """
    # File als Argument
    if (len(sys.argv) != 2):
        print("Run: python3 inverted_index.py <file with 1 doc per line> ")
        sys.exit()
    
    file_name=sys.argv[1]
   

    # Ausgabe    
    ii = InvertedIndex()
    ii.read_from_file(file_name)
    
    
    print("file1 Inverted list:")
    for word, inverted_list in ii.inverted_lists.items():
        print(word, len(inverted_list), '[%s]' % ', '.join(map(str, inverted_list)))
  
    

    ii.search_word()




