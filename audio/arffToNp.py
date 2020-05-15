#########################################
# Project   : ARFF to CSV converter     #
# Created   : 10/01/17 11:08:06         #
# Author    : haloboy777                #
# Licence   : MIT                       #
#########################################

# Importing library
import os
import pandas as pd
import numpy as np

def convert(input_path):
    # Getting all the arff files from the current directory

    # Main loop for reading and writing files

    output_array = [[]]

    with open(input_path , "r") as inFile:
        content = inFile.readlines()
        name,ext = os.path.splitext(input_path)
        new = toCsv(content)
        with open(name+".csv", "w") as outFile:

            outFile.writelines(new)
            outFile.close()
            df = pd.read_csv(name+".csv")
            df = df.drop(columns=['name', 'class'])
            output_array = np.asarray(df , dtype=np.float32)

        print("Finished converting!")

        return output_array




# Function for converting arff list to csv list
def toCsv(content):
    data = False
    header = ""
    newContent = []
    for line in content:
        if not data:
            if "@attribute" in line:
                attri = line.split()
                columnName = attri[attri.index("@attribute")+1]
                header = header + columnName + ","
            elif "@data" in line:
                data = True
                header = header[:-1]
                header += '\n'
                newContent.append(header)
        else:
            newContent.append(line)
    return newContent