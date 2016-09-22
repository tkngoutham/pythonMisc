import operator


def customized_window_creation(window_dictionary,sentence,dimension_dictionary,window_size):
    tokens_of_sentence=sentence.split()
    for token in tokens_of_sentence:
        try:
            temp=window_dictionary[token]
        except:
            temp={token:{}}
            window_dictionary.update(temp)
           
    sentence_size=len(tokens_of_sentence)
    previous_token_index=-1    
    for token in tokens_of_sentence:
        token_index=tokens_of_sentence.index(token)
        try:
            temp=dimension_dictionary[token]
            if(token_index<previous_token_index):
                token_index=tokens_of_sentence.index(token,previous_token_index)
            if(token_index<=window_size):
                left_threshold=token_index
            else:
                left_threshold=window_size
            if(window_size<=(sentence_size-1)-token_index):
                right_threshold=window_size
            else:
                right_threshold=(sentence_size-1)-token_index
              
            for iteration in range(1,right_threshold+1):
                required_index=token_index+iteration
                required_key=('right_'+tokens_of_sentence[required_index])
                try:
                    window_dictionary[token][required_key]+=1
                except:
                    temp_dict={required_key:1}
                    window_dictionary[token].update(temp_dict)
  
            for iteration in range(-left_threshold,0):
                required_index=token_index+iteration
                required_key=('left_'+tokens_of_sentence[required_index])
                try:
                    window_dictionary[token][required_key]+=1
                except:
                    temp_dict={required_key:1}
                    window_dictionary[token].update(temp_dict)
            previous_token_index=token_index
        except:
            continue
        #print 'done customized_window_creation'
    return 
    
def prepare_word_dictionary(file_path,Word_Dictionary):
    with open(file_path,'r') as fp:
            for line in fp:
                decoded_line=line
                tokens=decoded_line.split()
                Current_Word=None
                for token in tokens:
                    token=token.strip()
                    
                    
                    Current_Word=token
                    try:
                        Word_Dictionary[Current_Word]+=1
                    except:
                        temp_dict={Current_Word:1}
                        Word_Dictionary.update(temp_dict)
                        


def store_word_dictionary(file_path,Word_Dictionary):
    file_pointer=open(file_path,'w')
    for key,value in Word_Dictionary.iteritems():
        file_pointer.write((key+' : '+str(value)+'\n'))
    
def convert_dictionary_to_list(Word_Dictionary):
    list=[]
    for key,value in Word_Dictionary.iteritems():
        list.append((key,value))
    return list

def build_dimensions(Word_List):
    dimension_count=0.5*len(Word_List)
    Sorted_Word_Dictionary = sorted(Word_List.iteritems(), key=operator.itemgetter(1),reverse=True)
    #Sorted_Word_list=convert_dictionary_to_list(Sorted_Word_Dictionary)
    dimensions={}
    for item in range(0,int(dimension_count)):
        dimensions.update({Sorted_Word_Dictionary[item][0]:Sorted_Word_Dictionary[item][1]})
    return dimensions
        
    
def build_window_dictionary(dimension_dictionary,window_size,file_path):
    window_dictionary={}
    with open(file_path,'r') as fp:
            for line in fp:
                decoded_line=line
                customized_window_creation(window_dictionary,decoded_line,dimension_dictionary,window_size)
    return window_dictionary


    
     

Word_Dictionary={}
file_path='/home/gowtham/Desktop/Sample_Text'
prepare_word_dictionary(file_path,Word_Dictionary)
file_path='/home/gowtham/Desktop/Sample_Text_result'                  
store_word_dictionary(file_path,Word_Dictionary)
file_path='/home/gowtham/Desktop/Sample_Text'
dimension_dict=build_dimensions(Word_Dictionary)
window_dictionary=build_window_dictionary(dimension_dict,2,file_path)
print dimension_dict.keys()
file_path='/home/gowtham/Desktop/Sample_Text_dim_vect'
store_word_dictionary(file_path,window_dictionary)
#print window_dictionary
    
