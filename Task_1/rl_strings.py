#! python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 10:00:56 2019

@author: jltsa
"""

import re
import pandas as pd
import sys

def main():
    """
    To run script open commond line and path into directory containing
    this script.  Type python rl_strings.py <file_of_mined_data> <save_path>
    Ex) python Distict_Brands.txt rl_strings.csv
    
    First argument: path to .txt filewith mined data
    Second argument: path of where to save a .csv file with Ralph Lauren strings
    
    """
    script = sys.argv[0]
    file_path = sys.argv[1]
    save_file_path = sys.argv[2]
    
    #validate user input
    while file_path[-4:] != '.txt':
        response = input("Please enter complete path with file extension .txt: ")
        if response[-4:] == '.txt':
            file_path = response
            print('Accepted')
        else:
            print('Try Again.')
            continue
        
    while save_file_path[-4:] != '.csv':
        save_response = input("Please enter complete path with file extension .csv: ")
        if save_response[-4:] == '.csv':
            save_file_path = save_response
            print('Accepted')
        else:
            print('Try Again.')
            continue
        
    #handle UnicodeDecodeError when reading in .txt file
    try:
        with open(file_path, mode='r') as file:
            items = file.read()
            
    except UnicodeDecodeError:     
        with open(file_path, encoding = 'latin-1', mode='r') as file:
            items = file.read()
    
    #List comprehension to get list of names in .txt file
    names = [re.sub('[\\\(){}<>/|]', '', x.replace('"', '').strip()) \
             for x in items.split(',')]
    
    #use regular expression to search for Ralph Lauren assocications
    #Create empty list to store matches, ignore case
    rl = []
    regex = re.compile(r'(r+a+u*l+p+h+)\s*\W*(l+a+u+r+e+n+)', re.IGNORECASE)

    #Append matches to rl
    for text in names:
        if re.search(regex, text):
            rl.append(text)
    
    #Cast to DataFrame so we can save to .csv
    rl_ser = pd.DataFrame(rl)
    rl_ser.to_csv(str(save_file_path), index=False)
    
    print('Sucess!')
    print('Check path to find file saved as a <file name>.csv or in the ' +\
          'current directory if only file name was given and no path was specifed.')
    
if __name__ == '__main__':
    main()