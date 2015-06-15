'''
Created on Jun 12, 2015

@author: Daniel
'''
import csv


zyBooks = {}
# index of instructor notes and zyBook ids in the rows of the excel spreadsheet
instructor_note_location = 3
zyBook_id_location = 4
line = 1

file = "instructor-content-zyBooks.csv"

with open(file, 'r') as instructorContent:
    fileReader = csv.reader(instructorContent, delimiter=',')
    
    for row in fileReader:
        if line == 1:
            line += 1
        else:
    #       print('Row #%d: zyBook id: ' % line, row[4])
            zyBook_id = int(row[zyBook_id_location])
            instructor_note = row[instructor_note_location]
            if zyBook_id in zyBooks:
                zyBooks[zyBook_id]["instructor_content"].append(instructor_note)
            else:
                zyBooks[zyBook_id] = {}
                zyBooks[zyBook_id]["zyBook_id"] = zyBook_id
                zyBooks[zyBook_id]["instructor_content"] = []
                zyBooks[zyBook_id]["instructor_content"].append(instructor_note)
    
    most_notes = 0
    notated_zyBooks = 0
    total_notes = 0
    for zyBook_id in sorted(zyBooks.keys()):
        number_of_notes = len(zyBooks[zyBook_id]["instructor_content"])
#         print("Book %d has %d teacher notes" % (zyBook_id, number_of_notes))
        if number_of_notes >= most_notes:
            most_notes = number_of_notes
            zyBook_with_most_notes = zyBook_id
        notated_zyBooks += 1
        total_notes += number_of_notes
        
    print("Please enter the total number of zyBooks")
    total_zyBooks = int(input())
    print("%d has the most notes at %d" % (zyBook_with_most_notes, most_notes))
    print("There are %d zyBooks with notes" % notated_zyBooks)
    average_note_per_zyBook = total_notes / notated_zyBooks
    print("There are %d notes per zyBook on average" % average_note_per_zyBook)
    percent_of_zyBooks_with_notes = (notated_zyBooks / total_zyBooks) * 100
    print("%d out of %d zyBooks use teacher notes. That is %d%%" % (notated_zyBooks, total_zyBooks, percent_of_zyBooks_with_notes))
    
        
        
        