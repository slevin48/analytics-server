from os import scandir
from hurry.filesize import size
import pandas as pd
import json

# Create a handler for our read (GET) dataset
def read():
    """
    This function responds to a request for /api/dataset
    with the complete lists of dataset

    :return:        sorted list of dataset
    """
    
    df = pd.DataFrame(columns= ['name','lastModified','filesize'])

    # Data to serve with our API
    dir_entries = scandir('data/')
    for entry in dir_entries:
        df = df.append({'name' : entry.name, 'lastModified' : entry.stat().st_mtime, 'filesize' : size(entry.stat().st_size)}, ignore_index=True)

    # Create the list of dataset from our data
    return json.loads(df.to_json(orient='records'))