import json
def encryptDecrypt(inpString): 
  
    # Define XOR key 
    # Any character value will work 
    xorKey = '/'; 
  
    # calculate length of input string 
    length = len(inpString); 
  
    # perform XOR operation of key 
    # with every caracter in string 
    for i in range(length): 
      
        inpString = (inpString[:i] + 
             chr(ord(inpString[i]) ^ ord(xorKey)) +
                     inpString[i + 1:]); 
      
    return inpString; 
  
# Driver Code 
if __name__ == '__main__': 
    with open('./config.json','r') as read:
        sampleString =json.load(read)
  
    sampleString = encryptDecrypt(sampleString)
    sampleString = eval(sampleString)
    sampleString["Contest"] = "START"

    
    with open('./config_reader.json', 'w') as write:
        json.dump(sampleString, write, indent = 4)
