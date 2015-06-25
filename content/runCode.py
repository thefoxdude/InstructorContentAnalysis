'''
Created on Jun 18, 2015

@author: Daniel
'''
import content.instructorContent
import sys

def main(total_zyBooks, content_file, stop_words_file):
    results = content.instructorContent.main(total_zyBooks, content_file, stop_words_file)
    print(results['word count'])
    
if __name__ == '__main__':
    main(int(sys.argv[1]), sys.argv[2], sys.argv[3])