#!/usr/bin/env python
# coding: utf-8

# # Splitting Large Files #
# 
# <strong>Author:</strong> David Liau <br />
# <strong>Date:</strong> 9/18/2019 <br />
# <strong>Purpose:</strong> This script serves to take in a large file of size > 1GB, and split it into multiple files of size ~1GB. Any suggestions to improve speed/efficiency would be greatly appreciated. <br />
# <strong>Version:</strong> 0.0.0

# In[1]:


# Necessary Imports
from tkinter import Tk
from tkinter.filedialog import asksaveasfilename, askopenfilename


# In[2]:


def y_n_question(question):
    while True:
        # Ask question
        answer = input(question)
        if not answer or answer == '':
            continue
        answer_cleaned = answer[0].lower()
        if answer_cleaned == 'y' or answer_cleaned == 'n':
            if answer_cleaned == 'y':
                return True
            if answer_cleaned == 'n':
                return False
        else:
            print("Invalid input, please try again.")

def select_file_in(title):
    file_in = askopenfilename(initialdir="../", title=title,
                              filetypes=(("Comma Separated Values", "*.csv"), ("all files", "*.*")))
    if not file_in:
        input("Program Terminated. Press Enter to continue...")
        exit()

    return file_in


# In[3]:


# Confirmation question
confirm_q = "Press y/n to confirm/re-choose size of "

# Hide Tkinter GUI
Tk().withdraw()

print("Please select the file to split.")

# Find input file
file_in = select_file_in("Select file input")

# Ask for file size, catching any errors
while True:
    try:
        size = input("Enter file size (in bytes):") 
        
        # Checking that size is a string
        size = int(size)

        # Checking for 0 < size < 1000000000
        if size < 1 or size > 1000000000:
            raise AssertionError
        
        # Asking confirmation question
        question = confirm_q + str(size) + ": "
        confirmation = y_n_question(question)
        
        if confirmation:
            break
        else:
            continue
            
    except AssertionError:
        print("Not a valid size. Please enter an integer between 1 byte and 1GB (1,000,000,000 bytes).")
    except ValueError:
        print("Not a valid type. Please input an integer.")
        
# Writing to multiple files
with open(file_in, encoding='utf-8') as f:
    header = f.readline()
    part = 0
    total = 0
    
    # Create filename, in the format of: filename_{part}.{file type}
    period_i = file_in.rfind('.')
    file_name = file_in[:period_i] + '_' + str(part) + file_in[period_i:]
    output_file = open(file_name, 'a+', encoding='utf-8')
    output_file.write(header)
    
    # Reading from input file
    while 1:
        # Trying to read
        try:
            chunk = f.readline()

            # If end of input file, break
            if not chunk:
                output_file.close()
                f.close()
                print("Writing to", file_name, "complete!")
                break

            # Write to output file while size is still less than limit
            if total + len(chunk) <= int(size):
                output_file.write(chunk)
                total += len(chunk)

            # Close output file and open a new one
            else:
                output_file.close()
                print("Writing to", file_name, "complete!")

                # Updating variables for new otuput file
                total = 0
                part += 1
                file_name = file_in[:period_i] + '_' + str(part) + file_in[period_i:]
                output_file = open(file_name, 'a+', encoding='utf-8')
                output_file.write(header)
        # Catching any exception and printing it, as well as closing files
        except Exception as exp:
            print("Program failed with exception: %s" % (exp))
            output_file.close()
            f.close()


# In[ ]:




