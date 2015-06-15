'''
Created on Jun 12, 2015

@author: Daniel
'''
import csv

i = 0
list_of_book_nums = []
line = 1
book_num = 0
number_of_book = 0

file = "instructor-content-zyBooks.csv"

with open(file, 'r') as zyBookContent:
        fileReader = csv.reader(zyBookContent, delimiter=',')
        for row in fileReader:
            if (line == 1):
                line += 1            
            elif (row and len(row) >= 5 and len(row[0]) > 0 and len(row[4]) <= 6):
#                 print('Row #%d: zyBook id: ' % line, row[4])
                list_of_book_nums.append(int(row[4]))
                line += 1
                i += 1
            else:
                line += 1
                
        
        list_of_book_nums.sort()
        i = 0
        for x in list_of_book_nums:
            temp = list_of_book_nums[i]
            if (i == 0 or number_of_book == 0):
                book_num = list_of_book_nums[i]
                number_of_book += 1
            else:
                if (temp == list_of_book_nums[i-1]):
                    number_of_book += 1
                else:
                    print("Book %d has %d teacher notes" % (book_num, number_of_book))
                    number_of_book = 0
            i += 1
        
        
        