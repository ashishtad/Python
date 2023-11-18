"""
Source code.
Author: Ashish Tad
Date: 18/11/2023
"""

import json
import difflib

def read_logfile(file_path):
    with open(file_path,'r') as file:
        return file.readlines()

def extract_messages(log_entries):
    messages =[]
    for entry in log_entries:
        message_start = entry.find('Message:') + len ('Message:')
        message = entry[message_start:].strip()
        messages.append(message)
    
    return messages

def create_diffFile(messages1,messages2,
                    input_log_file1,input_log_file2,
                    output_log_file):

    html_diff = difflib.HtmlDiff()
    diff_result = html_diff.make_file(messages1,messages2,fromdesc=input_log_file1,todesc=input_log_file2)

    with open(output_log_file,'w') as file:
        file.write(diff_result)



if __name__ == "__main__":

    #Parse the config json file
    with open("config.json","r") as config_file:
        config = json.load(config_file)
    
    for log_block in config['logs']:
        input_log_files = log_block['input_log_files']
        output_log_file = log_block['output_log_file']

        #There should be 2 input log files
        if (2 != len(input_log_files)) :
            print("Error in input log file count!!. Please check the config file")
            continue
        #check for output file html extension
        if not output_log_file.endswith('.html'):
            print("Output diff file extension is not correct!!. Output diff file should be html file")
            continue
        input_log_file1= input_log_files[0]
        input_log_file2 = input_log_files[1]
        file1_log_entries = read_logfile(input_log_file1)
        file2_log_entries = read_logfile(input_log_file2)

        #Extract message part from logfiles.
        file1_messages = extract_messages(file1_log_entries)
        file2_messages = extract_messages(file2_log_entries)

        create_diffFile(file1_messages,file2_messages,input_log_file1,input_log_file2,output_log_file)