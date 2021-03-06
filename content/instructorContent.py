'''
Created on Jun 12, 2015

@author: Daniel
'''
import csv
import sys
import re
from collections import defaultdict
import datetime
import plotly.plotly as py
from plotly.graph_objs import *
from lib2to3.fixer_util import Newline

def main(total_zyBooks, file, stop_words_file, live_zyBooks):
    zyBooks = read_file(file)
    live_zyBooks = int(live_zyBooks)
    
    character_distribution_keys = [10, 20, 50, 100, 150, 200, 'above']
    character_distribution = {}
    for key in character_distribution_keys:
        character_distribution[key] = 0
    
    all_notes = ''
    most_notes = 0
    notated_zyBooks = 0
    total_notes = 0
    number_of_public_zyBooks = 0
    length_of_instructor_notes = 0
    zyBooks_and_notes = {}
    public_zyBooks = {}
    
    for zyBook_id in sorted(zyBooks.keys()):
        number_of_notes = len(zyBooks[zyBook_id]['instructor_content'])
        zyBooks_and_notes[zyBook_id] = number_of_notes
        if number_of_notes >= most_notes:
            most_notes = number_of_notes
            zyBook_title_with_most_notes = zyBooks[zyBook_id]['title']
            zyBook_code_with_most_notes = zyBooks[zyBook_id]['code']
        notated_zyBooks += 1
        total_notes += number_of_notes
        if zyBooks[zyBook_id]['public'] == True:
            public_zyBooks[zyBook_id] = zyBooks[zyBook_id]
            number_of_public_zyBooks += 1
        for instructor_content in zyBooks[zyBook_id]['instructor_content']:
            all_notes += instructor_content + ' '
            length = len(instructor_content)
            length_of_instructor_notes += length
            for key in character_distribution_keys:
                if key == character_distribution_keys[-1]:
                    character_distribution[key] += 1
                    break
                elif length < key:
                    character_distribution[key] += 1
                    break
    
    note_date_distribution = {}
    for book in zyBooks:
        note_date_distribution[zyBooks[book]['title']] = sorted(zyBooks[book]['note dates'])
    
    stop_words = add_stop_words(stop_words_file)
    
    word_count = defaultdict(int)
    all_notes = re.split(r'[\s.():/\n,]', all_notes)
    all_notes = [element.lower() for element in all_notes]
    words_to_print = []
    for word in all_notes:
        if (len(word) > 1 and word not in stop_words):
            word_count[word] += 1
            words_to_print.append(word)
    word_count = sorted(word_count.items(), key=lambda x: x[1], reverse=True)
    print_to_file(words_to_print)
     
    average_size_of_notes = length_of_instructor_notes / total_notes
    average_notes_per_zyBook = total_notes / notated_zyBooks
    average_notes_per_all = total_notes / total_zyBooks
    percent_of_zyBooks_with_notes = (notated_zyBooks / total_zyBooks) * 100
    
    percent_of_live_zyBooks = 100 * number_of_public_zyBooks / live_zyBooks
    live_number_of_notes = 0
    live_all_notes = ""
    live_zyBooks_and_notes = {}
    for zyBook_id in public_zyBooks.keys():
        live_number_of_notes += zyBooks_and_notes[zyBook_id]
        live_zyBooks_and_notes[zyBook_id] = zyBooks_and_notes[zyBook_id]
        for instructor_content in public_zyBooks[zyBook_id]['instructor_content']:
            live_all_notes += instructor_content
    live_average_instructor_notes = live_number_of_notes/number_of_public_zyBooks
    find_median_average(live_zyBooks_and_notes)
    print()
    print(live_number_of_notes)
    print(live_average_instructor_notes)
    
    books = {}
    for book in zyBooks:
        books[zyBooks[book]['title']] = len(zyBooks[book]['instructor_content'])
    
    most_notes = {
                  'title': zyBook_title_with_most_notes,
                  'code': zyBook_code_with_most_notes,
                  'value': most_notes
                  }
    
    notated = {
               'public': number_of_public_zyBooks,
               'evals': notated_zyBooks - number_of_public_zyBooks
               }
    
    characters = {
                  'distribution': character_distribution,
                  'keys': character_distribution_keys
                  }
    
    data = {
            'books': books,
            'note data': zyBooks_and_notes,
            'word count': word_count,
            'most notes': most_notes,
            'notated': notated,
            'total notes': total_notes,
            'average size of notes': average_size_of_notes,
            'average notes per zyBook': average_notes_per_zyBook,
            'average notes per all zyBooks': average_notes_per_all,
            'total zyBooks': total_zyBooks,
            'percent of zyBooks with notes': percent_of_zyBooks_with_notes,
            'characters': characters,
            'note dates': note_date_distribution
            }
    
    # For printing out to excel
    
    x_locations = []
    y_locations = []
    num_elements = 0
    date_distributions = compute_date_difference(note_date_distribution)
    date_distributions = sorted(date_distributions, key=lambda x: x[1], reverse=True)
    for book, time in date_distributions:
        if time > 0:
            x_locations.append(book)
            y_locations.append(time)
            num_elements += 1
    graph_line(x_locations, y_locations, 'date distribution', 'books', 'days between first and last note')
    print_to_excel(x_locations, y_locations, num_elements, 'date_distribution.csv')
    
    x_locations = []
    y_locations = []
    num_elements = 0
    for item in word_count:
        if item[1] > 20:
            x_locations.append(item[0])
            y_locations.append(item[1])
            num_elements += 1
    graph_line(x_locations, y_locations, 'most used words', 'words', 'times used')
    print_to_excel(x_locations, y_locations, num_elements, 'most_used_words.csv')
    
    x_locations = []
    y_locations = []
    num_elements = 0
    for title in books.keys():
        x_locations.append(title)
        y_locations.append(books[title])
        num_elements += 1
#     graph_bar(x_locations, y_locations, 'notes and books', 'books', 'number of notes')
    print_to_excel(x_locations, y_locations, num_elements, 'notes_and_books.csv')
    
    x_locations = []
    y_locations = []
    num_elements = 0
    for key in data['characters']['keys']:
        average = (data['characters']['distribution'][key] / data['total notes']) * 100
        x_locations.append(key)
        percent = str(average) + '%'
        y_locations.append(percent)
        num_elements += 1
#     graph_line(x_locations, y_locations, 'note sizes', 'size of note', 'percent between numbers')
    print_to_excel(x_locations, y_locations, num_elements, 'character_distribution.csv')
    
    x_locations = []
    y_locations = []
    note_count = []
    for book in zyBooks:
        note_count.append(zyBooks[book]['number of notes'])
    note_count = sorted(note_count, key=lambda x: x[1], reverse=True)
    num_elements = 0
    for book, number in note_count:
        x_locations.append(book)
        y_locations.append(number)
        num_elements += 1
    print_to_excel(x_locations, y_locations, num_elements, 'books_note_counts.csv')

#     find_median_average(zyBooks_and_notes)
    
    return data
    
def print_all(data):
    # receives dictionary and prints out values
#     print('Most used words:')
#     for (item, num) in data['word count']:
#         if num >= 50:
#             print('"%s": %d' % (item, num))
#       
#     print()
    print('"%s" (%s) has the most instructor notes at %d.' % (data['most notes']['title'], data['most notes']['code'], data['most notes']['value']))
    
    total_notated = data['notated']['public'] + data['notated']['evals']
    print('There are %d zyBooks with instructor notes.' % total_notated)
    print('Of those %d notated zyBooks %d of them are public' % (total_notated, data['notated']['public']))
    print('There are a total of %d instructor notes.' % data['total notes'])
    print('Each instructor note is, on average, %d characters long.' % data['average size of notes'])
    print('There are %d instructor notes on average per zyBooks that have instructor notes.' % data['average notes per zyBook'])
    print('There are %.2f instructor notes per all zyBooks on average.' % data['average notes per all zyBooks'])
    for key in data['characters']['keys']:
        average = (data['characters']['distribution'][key] / data['total notes']) * 100
        if key != data['characters']['keys'][-1]:
            print('%.2f%% of the instructor notes are less than %s.' % (average, key))
        else:
            print('%.2f%% of the instructor notes are greater than %s.' % (average, data['characters']['keys'][-2]))
    print('%d out of %d zyBooks use instructor notes.  That is %d%%.' % (total_notated, data['total zyBooks'], data['percent of zyBooks with notes']))
    print()
#     for book in data['note dates'].keys():
#         print("%r: %r" % (book, data['note dates'][book]))
    date_differences = compute_date_difference(data['note dates'])
    one_note = 0
    for book, time in date_differences:
        if time != 0:
            print('Book %r: days between first and last note: %r' % (book, time))
        elif time == 0:
            one_note += 1
    print("Number of zyBooks with notes only on one day: %d" % one_note)    

def read_file(file):
    # reads in csv file and returns dictionary of zyBooks
    zyBooks= {}
    note_addition_date_location = 2
    instructor_note_location = 3
    zyBook_id_location = 4
    zyBook_title_location = 6
    zyBook_code_location = 7
    zyBook_public_location = 18
    zyBook_dev_location = 19
    
    with open(file, 'r') as instructorContent:
        fileReader = csv.reader(instructorContent, delimiter=',')
        next(fileReader)
        for row in fileReader:
            note_addition_date = convert_to_date(row[note_addition_date_location])
            zyBook_id = int(row[zyBook_id_location])
            instructor_note = row[instructor_note_location]
            zyBook_title = row[zyBook_title_location]
            zyBook_code = row[zyBook_code_location]
            zyBook_public = int(row[zyBook_public_location]) == 1
            zyBook_dev = int(row[zyBook_dev_location]) == 0

            if zyBook_dev:
                try:
                    zyBooks[zyBook_id]['instructor_content'].append(instructor_note)
                    zyBooks[zyBook_id]['note dates'].append(note_addition_date)
                    zyBooks[zyBook_id]['number of notes'][1] += 1
                except KeyError:
                    zyBooks[zyBook_id] = {
                                          'id': zyBook_id,
                                          'instructor_content': [instructor_note],
                                          'title': zyBook_title,
                                          'code': zyBook_code,
                                          'public': zyBook_public,
                                          'note dates': [note_addition_date],
                                          'number of notes': [zyBook_title, 1]
                                          }
    return zyBooks

def add_stop_words(file):
    # reads in csv file and returns a list of stop words
    stop_words = []
    with open(file, 'r') as stopWords:
        fileReader = csv.reader(stopWords, delimiter=',')
        for row in fileReader:
            for x in row:
                stop_words.append(x)
    return stop_words

def convert_to_date(date_string):
    # reads in string and returns a date object
    date_string = date_string.split(' ')[0]
    date_string = re.split(r'[/\s]', date_string)
    date_string = [int(i) for i in date_string]
    date_string = datetime.date(date_string[2], date_string[0], date_string[1])
    return date_string

def compute_date_difference(dictionary):
    # recieves a dictionary of books and times and returns the time between
    # the first note and the last note in days
    differences = []
    seconds_in_day = 86400
    for book in dictionary.keys():
        time = int((dictionary[book][-1] - dictionary[book][0]).total_seconds() / seconds_in_day)
        times = [book, time]
        differences.append(times)
    return differences

def graph_line(x_locations, y_locations, name_of_graph, x_axis, y_axis):
    line1 = Scatter(
        x = x_locations,
        y = y_locations
    )
 
    data = Data([line1])
     
    layout = Layout(
        title = name_of_graph,
        xaxis=XAxis(
            title = x_axis,
            titlefont=Font(
                family='Courier New, monospace',
                color='#7f7f7f'
            )
        ),
        yaxis = YAxis(
            title = y_axis,
            titlefont=Font(
                family='Courier New, monospace',
                color='#7f7f7f'
            )
        )
    )
    fig = Figure(data=data, layout=layout)
#     py.plot(fig, filename = name_of_graph)
    
def graph_bar(x_locations, y_locations, name_of_graph, x_axis, y_axis):
    bar1 = Bar(
               x = x_locations,
               y = y_locations
               )
 
    data = Data([bar1])
     
    layout = Layout(
        title = name_of_graph,
        xaxis=XAxis(
            title = x_axis,
            titlefont=Font(
                family='Courier New, monospace',
                color='#7f7f7f'
            )
        ),
        yaxis = YAxis(
            title = y_axis,
            titlefont=Font(
                family='Courier New, monospace',
                color='#7f7f7f'
            )
        )
    )
    fig = Figure(data=data, layout=layout)
#     py.plot(fig, filename = name_of_graph)
    
def print_to_file(words):
    with open('allWords.txt', 'w') as w:
        for word in words:
            w.write(word + ' ')
    
def print_to_excel(x_locations, y_locations, num_elements, file_name):
    with open(file_name, 'w+', newline = "") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter = ',')
        i = 0
        while i < num_elements:
            csv_writer.writerow([x_locations[i], y_locations[i]])
            i += 1

def find_median_average(dictionary):
    median = 0;
    all_values = []
    total = 0
    average = 0
    for value in dictionary.values():
        all_values.append(value)
    all_values = sorted(all_values, reverse = True)
    if (len(all_values) % 2 == 0):
        middle = int(len(all_values) / 2)
        median = int((all_values[middle] + all_values[middle - 1]) / 2)
    else:
        middle = int(len(all_values) / 2)
        median = all_values[middle]
    print(median)
    total = 0
    for element in all_values:
        total += element
    average = total / len(all_values)
    print(average)

    del all_values[0]
    del all_values[0]
    total = 0
    for element in all_values:
        total += element
    average = total / len(all_values)
    print(average)
        

if __name__ == '__main__':
#     print_all(main(int(sys.argv[1]), sys.argv[2], sys.argv[3]), sys.argv[4])
    main(int(sys.argv[1]), sys.argv[2], sys.argv[3], sys.argv[4])
    
    