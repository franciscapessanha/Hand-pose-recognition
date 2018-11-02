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