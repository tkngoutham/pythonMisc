from os import listdir

dir_path='/home/gowtham/DellData/'

dirs=listdir(dir_path)

dest_file_path='/home/gowtham/total_dell_data.txt'
dest_file=open(dest_file_path,'a')
for file in dirs:
    current_file_path=dir_path+'/'+file
    with open(current_file_path,'r') as fp:
        #current_data=fp.read().decode('utf-8')
	current_data=current_data.split()
        processed_data=''
	for datum in current_data:
	    processed_data=processed_data+' '+datum
        #dest_file.write(processed_data.encode('utf-8'))
        dest_file.write(processed_data.encode('utf-8'))

 
