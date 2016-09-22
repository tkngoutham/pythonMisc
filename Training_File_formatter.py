
file_path='/home/gowtham/eclipse/A2/txtfiles/tam_full'
current_sent=''
destination_file_path='/home/gowtham/eclipse/A2/txtfiles/tam_tagged'
destination_file=open(destination_file_path,'w')
with open(file_path,'r') as fp:
    for line in fp:
        decoded_line=line.replace('\n','')
        decoded_line=decoded_line.decode('utf-8')
        if line.find('line_break')==0:
           destination_file.write(current_sent.encode('utf-8')+'\n')
           current_sent=''
        else:
            current_sent=current_sent+decoded_line+' '
            
    
            
        
        