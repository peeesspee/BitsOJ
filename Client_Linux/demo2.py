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
    ip = input('Enter New IP : ')
    with open('./config.json','r') as read:
        sampleString =json.load(read)
    # sampleString = "GeeksforGeeks"; 
  
    sampleString = encryptDecrypt(sampleString)
    sampleString = eval(sampleString)
    sampleString["host"] = ip
    sampleString = str(sampleString) 
    sampleString = encryptDecrypt(sampleString)

    
    with open('./config.json', 'w') as write:
        json.dump(sampleString, write, indent = 4)
