import pickle

def is_int(string):
  '''Checks if a string can be converted to an int
  
  Arguments:
    string {String} -- The string to be checked
  
  Returns:
    Boolean -- If the string can be or not converted to an int
  '''

  try: 
    int(string)
    return True
  except ValueError:
    return False

def save_list_to_file(list, file_name):
  '''Saves a list to a file using the pickle serialization format
  
  Arguments:
    list {List} -- List to be saved
    file_name {String} -- Name of the file to be saved to
  '''

  with open(file_name, 'wb') as fp:
    pickle.dump(list, fp)

def load_list_from_file(file_name):
  '''Loads a list from a file that was saved using the pickle serialization format
  
  Arguments:
    file_name {String} -- Name of the file to be saved from
  
  Returns:
    List -- The list loaded from the file
  '''

  with open (file_name, 'rb') as fp:
    return pickle.load(fp)