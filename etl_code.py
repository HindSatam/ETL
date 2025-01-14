import glob
import pandas as pd
import xml.etree.ElementTree as ET
from datetime import datetime

#global file paths one to store final output data and another to store all logs
log_file = "log_file.txt"
target_file = "transformed_data.csv"

#Extrac

#Extract CSV
def extract_from_csv(file_to_process):
    df = pd.read_csv(file_to_process)
    return df 

#Extract JSON
def extract_from_json(file_to_process):
    df = pd.read_json(file_to_process, lines=True)
    return df

#Extract XML
#header must be known: name, height, weight
def extract_from_xml(file_to_process):
    df = pd.DataFrame(columns=["name", "height", "weight"])
    tree = ET.parse(file_to_process)
    root = tree.getroot()

    for person in root:
        name = person.find("name").text
        height = float(person.find("height").text)
        weight = float(person.find("weight").text)

        df = pd.concat([df, pd.DataFrame([{"name":name, "height":height, "weight":weight}])], ignore_index=True)
    return df

#function to identify which function to call based on the filetype
def extract():

#empty df to hold the data
    extracted_data = pd.DataFrame(columns=['name','height','weight'])

    #csv files
    for csvfile in glob.glob("*.csv"):
        extracted_data = pd.concat([extracted_data, pd.DataFrame(extract_from_csv(csvfile))], ignore_index=True)

    #json files
    for jsonfile in glob.glob("*.json"):
        extracted_data = pd.concat([extracted_data, pd.DataFrame(extract_from_json(jsonfile))], ignore_index=True)

    #xml files
    for xmlfile in glob.glob("*.xml"):
        extracted_data = pd.concat([extracted_data, pd.DataFrame(extract_from_xml(xmlfile))], ignore_index=True)
        
    return extracted_data


#Transform

def transform(data):
  #'''Convert inches to meters and round off to two decimals 
    #1 inch is 0.0254 meters '''
    data['height'] = round(data.height * 0.0254,2) 
 
    #'''Convert pounds to kilograms and round off to two decimals 
    #1 pound is 0.45359237 kilograms '''
    data['weight'] = round(data.weight * 0.45359237,2) 
    
    return data   

#Load & Log

#transform data to CSV
def load_data(target_file, transformed_data):
    transformed_data.to_csv(target_file)

#to record logging
def log_progress(message): 
    timestamp_format = '%Y-%h-%d-%H:%M:%S' # Year-Monthname-Day-Hour-Minute-Second 
    now = datetime.now() # get current timestamp 
    timestamp = now.strftime(timestamp_format) 
    with open(log_file,"a") as f: 
        f.write(timestamp + ',' + message + '\n') 


#Testing

log_progress("ETL Job Started")

log_progress("Extract Phase Started")
extracted_data = extract()

log_progress("Extrcat Phase Ended")

log_progress("Transform Phase Started")
transformed_data = transform(extracted_data)
print("Transformed Data")
print(transformed_data)

log_progress("Transforme Phase Ended")

log_progress("Load Phase Started")
load_data(target_file, transformed_data)

log_progress("Load Phase Ended")

log_progress("ETL Jop Ended")
