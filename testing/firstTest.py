'''
Created on Jun 12, 2015

@author: Daniel
'''
import csv
import sys
from collections import defaultdict

zyBooks = {}
# index of instructor notes and zyBook ids in the rows of the excel spreadsheet
instructor_note_location = 3
zyBook_id_location = 4
zyBook_title_location = 7
zyBook_code_location = 8
zyBook_public_location = 18
line = 1

file = sys.argv[2]

with open(file, 'r') as instructorContent:
    fileReader = csv.reader(instructorContent, delimiter=',')
    
    for row in fileReader:
        if line == 1:
            line += 1
        else:
    #       print('Row #%d: zyBook id: ' % line, row[4])
            zyBook_id = int(row[zyBook_id_location])
            instructor_note = row[instructor_note_location]
            zyBook_title = row[zyBook_title_location]
            zyBook_code = row[zyBook_code_location]
            zyBook_public = int(row[zyBook_public_location])
            if zyBook_public == 0:
                zyBook_public = False
            elif zyBook_public == 1:
                zyBook_public = True
            if zyBook_id in zyBooks:
                zyBooks[zyBook_id]["instructor_content"].append(instructor_note)
            else:
                zyBooks[zyBook_id] = {
                              "id": zyBook_id,
                              "instructor_content": [instructor_note],
                              "title": zyBook_title,
                              "code": zyBook_code,
                              "public": zyBook_public
                              }
                    
    most_notes = 0
    notated_zyBooks = 0
    total_notes = 0
    number_of_public_zyBooks = 0
    length_of_instructor_notes = 0
    character_distribution_keys = [10, 20, 50, 100, 150, 200, "above"]
    character_distribution = {}
    for key in character_distribution_keys:
        character_distribution[key] = 0
    all_notes = ""
    for zyBook_id in sorted(zyBooks.keys()):
        number_of_notes = len(zyBooks[zyBook_id]["instructor_content"])
#         print("Book %d has %d teacher notes" % (zyBook_id, number_of_notes))
        if number_of_notes >= most_notes:
            most_notes = number_of_notes
            zyBook_title_with_most_notes = zyBooks[zyBook_id]['title']
            zyBook_code_with_most_notes = zyBooks[zyBook_id]['code']
        notated_zyBooks += 1
        total_notes += number_of_notes
        if zyBooks[zyBook_id]['public'] == True:
            number_of_public_zyBooks += 1
        for instructor_content in zyBooks[zyBook_id]['instructor_content']:
            all_notes += instructor_content
            length = len(instructor_content)
            length_of_instructor_notes += length
            for key in character_distribution_keys:
                if key == character_distribution_keys[-1]:
                    character_distribution[key] += 1
                    break
                elif length < key:
                    character_distribution[key] += 1
                    break
    
      
    word_count = defaultdict(int)
    all_notes = all_notes.split()
    for word in all_notes:
        if len(word) > 3:
            word_count[word] += 1
    for key in word_count.keys():
        if word_count[key] > 50:
            print(key + ": %d" % word_count[key])
            
    total_zyBooks = int(sys.argv[1])
    
#     print("'%s' (%s) has the most instructor notes at %d." % (zyBook_title_with_most_notes, zyBook_code_with_most_notes, most_notes))
#     print("There are %d zyBooks with instructor notes." % notated_zyBooks)
#     print("Of those %d notated zyBooks %d of them are public" % (notated_zyBooks, number_of_public_zyBooks))
#     print("There are a total of %d instructor notes." % total_notes)
#     average_size_of_notes = length_of_instructor_notes / total_notes
#     print("Each instructor note is, on average, %d characters long." % average_size_of_notes)
#     average_notes_per_zyBook = total_notes / notated_zyBooks
#     average_notes_per_all = total_notes / total_zyBooks
#     print("There are %d instructor notes on average per zyBooks that have instructor notes." % average_notes_per_zyBook)
#     print("There are %.2f instructor notes per all zyBooks on average." % average_notes_per_all)
    for key in character_distribution_keys:
        average = (character_distribution[key] / total_notes) * 100
        if key != character_distribution_keys[-1]:
            print("%.2f%% of the instructor notes are less than %d." % (average, key))
        else:
            print("%.2f%% of the instructor notes are greater than %d." % (average, character_distribution_keys[-2]))
#     percent_of_zyBooks_with_notes = (notated_zyBooks / total_zyBooks) * 100
#     print("%d out of %d zyBooks use instructor notes.  That is %d%%." % (notated_zyBooks, total_zyBooks, percent_of_zyBooks_with_notes))
    
        
        
        