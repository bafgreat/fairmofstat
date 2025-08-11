#!/usr/bin/python
from __future__ import print_function
__author__ = "Dr. Dinga Wonanke"
__status__ = "production"
import os
import pickle
import csv
import json
import codecs
from zipfile import ZipFile
import numpy as np

import pandas as pd
import msgpack
from importlib.resources import files


def numpy_to_json(ndarray, file_name):
    '''
    Serialise a numpy object
    '''
    json.dump(ndarray.tolist(), codecs.open(file_name, 'w',
              encoding='utf-8'), separators=(',', ':'), sort_keys=True)
    return


def write_json(json_obj, file_name):
    '''
    write a python dictionary object to json
    '''
    # Serializing json
    json_object = json.dumps(json_obj, indent=4, sort_keys=True)
    with open(file_name, "w", encoding='utf-8') as outfile:
        outfile.write(json_object)


def json_to_numpy(json_file):
    '''
    serialised a numpy array to json
    '''
    json_reader = codecs.open(json_file, 'r', encoding='utf-8').read()
    json_reader = np.array(json.loads(json_reader))
    return read_json


def append_json(new_data, filename):
    '''
    append a new data in an existing json file
    '''
    if not os.path.exists(filename):
        with open(filename, 'w', encoding='utf-8') as file:
            file.write('{}')
    elif os.path.getsize(filename) == 0:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write('{}')
    with open(filename, 'r+', encoding='utf-8') as file:
        # First we load existing data into a dict.
        file_data = json.load(file)
        # Overwrite existing keys with new_data
        file_data.update(new_data)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent=4, sort_keys=True)


def read_json(file_name):
    '''
    load a json file
    '''
    with open(file_name, 'r', encoding='utf-8') as f_obj:
        data = json.load(f_obj)

    return data


def csv_read(csv_file):
    '''
    Read a csv file
    '''
    f_obj = open(csv_file, 'r', encoding='utf-8')
    data = csv.reader(f_obj)
    return data


def get_contents(filename):
    '''
    Read a file and return a list content
    '''
    with open(filename, 'r', encoding='utf-8') as f_obj:
        contents = f_obj.readlines()
    return contents


def put_contents(filename, output):
    '''
    write a list object into a file
    '''
    with open(filename, 'w', encoding='utf-8') as f_obj:
        f_obj.writelines(output)
    return


def append_contents(filename, output):
    '''
    append contents into a file
    '''
    with open(filename, 'a', encoding='utf-8') as f_obj:
        f_obj.writelines(output)
    return


def pickle_load(filename):
    '''
    load a pickle file
    '''
    data = open(filename, 'rb')
    data = pickle.load(data)
    return data


def read_zip(zip_file):
    '''
    read a zip file
    '''
    content = ZipFile(zip_file, 'r')
    content.extractall(zip_file)
    content.close()
    return content


def save_dict_msgpack(data: dict, filename: str) -> None:
    """Save a dictionary to a file using MessagePack."""
    with open(filename, "wb") as f:
        msgpack.pack(data, f, use_bin_type=True)


def load_dict_msgpack(filename: str) -> dict:
    """Load a dictionary from a MessagePack file."""
    with open(filename, "rb") as f:
        return msgpack.unpack(f, raw=False, strict_map_key=False)


def convert_numpy_types(data):
    '''
    A function that jsonifies a dictionary by removing numpy data types.

    **parameter:**
        data (dict): data to jsonify

    **return:**
        data (dic): jsonified data
    '''
    if isinstance(data, dict):
        return {key: convert_numpy_types(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [convert_numpy_types(element) for element in data]
    elif isinstance(data, np.integer):
        return int(data)
    elif isinstance(data, np.floating):
        return float(data)
    else:
        return data


def get_section(contents, start_key, stop_key, start_offset=0, stop_offset=0):
    all_start_indices = []
    for i, line in enumerate(contents):
        if start_key in line:
            all_start_indices.append(i + start_offset)
    start_index = all_start_indices[-1]
    for i in range(start_index, len(contents)):
        line = contents[i]
        if stop_key in line:
            stop_index = i + 1 + stop_offset
            break
    data = contents[start_index:stop_index]
    return data


def load_data(filename):
    '''
    function that recognises file extenion and chooses the correction
    function to load the data.
    '''
    # file_ext = filename[filename.rindex('.')+1:]
    basename = os.path.basename(filename)
    file_ext = basename.split('.')[-1]

    if file_ext == 'json':
        data = read_json(filename)
    elif file_ext == 'csv':
        data = pd.read_csv(filename)
    elif file_ext == 'p':
        data = pickle_load(filename)
    elif file_ext == 'xlsx':
        data = pd.read_excel(filename)
    elif file_ext == 'msgpack':
        data = load_dict_msgpack(filename)
    else:
        data = get_contents(filename)
    return data

def load_iupac_names():
    msgpack_path = files("mofstructure").joinpath("db/iupacname.msgpack")
    return load_data(msgpack_path)