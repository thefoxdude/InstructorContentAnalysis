'''
Created on Jun 12, 2015

@author: Daniel
'''
import csv
import sys
import re
from collections import defaultdict

def main(total_zyBooks, file, stop_words_file):
    zyBooks = {}
    # index of instructor notes and zyBook ids in the rows of the excel spreadsheet
    instructor_note_location = 3
    zyBook_id_location = 4
    zyBook_title_location = 7
    zyBook_code_location = 8
    zyBook_public_location = 18
    
    with open(file, 'r') as instructorContent:
        fileReader = csv.reader(instructorContent, delimiter=',')
        next(fileReader)
        for row in fileReader:
    #       print('Row #%d: zyBook id: ' % line, row[4])
            zyBook_id = int(row[zyBook_id_location])
            instructor_note = row[instructor_note_location]
            zyBook_title = row[zyBook_title_location]
            zyBook_code = row[zyBook_code_location]
            zyBook_public = int(row[zyBook_public_location]) == 1

            try:
                zyBooks[zyBook_id]["instructor_content"].append(instructor_note)
            except KeyError:
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
                all_notes += instructor_content + " "
                length = len(instructor_content)
                length_of_instructor_notes += length
                for key in character_distribution_keys:
                    if key == character_distribution_keys[-1]:
                        character_distribution[key] += 1
                        break
                    elif length < key:
                        character_distribution[key] += 1
                        break
        
        stop_words = []
        with open(stop_words_file, 'r') as stopWords:
            fileReader = csv.reader(stopWords, delimiter=',')
            for row in fileReader:
                for x in row:
                    stop_words.append(x)
        
        word_count = defaultdict(int)
        all_notes = re.split(r'[\s.():/\n]', all_notes)
        all_notes = [element.lower() for element in all_notes]
        for word in all_notes:
            if (len(word) > 1 and word not in stop_words):
                word_count[word] += 1
        word_count = sorted(word_count.items(), key=lambda x: x[1], reverse=True)
         
        average_size_of_notes = length_of_instructor_notes / total_notes
        average_notes_per_zyBook = total_notes / notated_zyBooks
        average_notes_per_all = total_notes / total_zyBooks
        percent_of_zyBooks_with_notes = (notated_zyBooks / total_zyBooks) * 100
        
        data = {
                'word count': word_count,
                'zyBook title with most notes': zyBook_title_with_most_notes,
                'zyBook code with most notes': zyBook_code_with_most_notes,
                'most notes': most_notes,
                'notated zyBooks': notated_zyBooks,
                'public zyBooks': number_of_public_zyBooks,
                'total notes': total_notes,
                'average size of notes': average_size_of_notes,
                'average notes per zyBook': average_notes_per_zyBook,
                'average notes per all zyBooks': average_notes_per_all,
                'total zyBooks': total_zyBooks,
                'percent of zyBooks with notes': percent_of_zyBooks_with_notes,
                'character distribution': character_distribution
                }
        return data
    
        
def print_all(data):
    print("Most used words:")
    for (item, num) in data['word count']:
        if num >= 50:
            print("%s: %d" % (item, num))
      
    print()
    print("'%s' (%s) has the most instructor notes at %d." % (data['zyBook title with most notes'], data['zyBook code with most notes'], data['most notes']))
    print("There are %d zyBooks with instructor notes." % data['notated zyBooks'])
    print("Of those %d notated zyBooks %d of them are public" % (data['notated zyBooks'], data['public zyBooks']))
    print("There are a total of %d instructor notes." % data['total notes'])
    print("Each instructor note is, on average, %d characters long." % data['average size of notes'])
    print("There are %d instructor notes on average per zyBooks that have instructor notes." % data['average notes per zyBook'])
    print("There are %.2f instructor notes per all zyBooks on average." % data['average notes per all zyBooks'])
    for (key, value) in data['character distribution'].items():
        average = (value / data['total notes']) * 100
        if key != list(data['character distribution'].keys())[-1]:
            print("%.2f%% of the instructor notes are less than %d." % (average, key))
        else:
            print("%.2f%% of the instructor notes are greater than %d." % (average, list(data['character distribution'].keys())[-2]))
    print("%d out of %d zyBooks use instructor notes.  That is %d%%." % (data['notated zyBooks'], data['total zyBooks'], data['percent of zyBooks with notes']))
    
if __name__ == '__main__':
    print_all(main(int(sys.argv[1]), sys.argv[2], sys.argv[3]))
    
    