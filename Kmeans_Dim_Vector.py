import operator
import math


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
                decoded_line=line.decode('utf-8')
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
    Word_Dictionary=sorted(Word_Dictionary.iteritems(), key=operator.itemgetter(1),reverse=True)    
    return Word_Dictionary
                        


def store_word_dictionary(file_path,Word_Dictionary):
    file_pointer=open(file_path,'w')
    for key,value in Word_Dictionary.iteritems():
        file_pointer.write(str(key)+' : '+str(value)+'\n')
 

def store_cluster_dictionary(file_path,Word_Dictionary):
    file_pointer=open(file_path,'w')
    for key,value in Word_Dictionary.iteritems():
        for k,v in value.iteritems():
            file_pointer.write(str(key)+' : '+str(k).encode('utf-8')+'\n')

    
    
def store_word_list(file_path,Word_Dictionary):
    file_pointer=open(file_path,'w')
    for item in Word_Dictionary:
        file_pointer.write(str(item[0])+' : '+str(item[1])+'\n')


def convert_dictionary_to_list(Word_Dictionary):
    list=[]
    for key,value in Word_Dictionary.iteritems():
        list.append((key,value))
    return list

def build_dimensions(Word_List):
    dimension_count=0.15*len(Word_List)
    
    dimensions={}
    for item in range(30,int(dimension_count)+30):
        dimensions.update({Word_List[item][0]:Word_List[item][1]})
    return dimensions
        
    
def build_window_dictionary(dimension_dictionary,window_size,file_path):
    window_dictionary={}
    with open(file_path,'r') as fp:
            for line in fp:
                decoded_line=line.decode('utf-8')
                customized_window_creation(window_dictionary,decoded_line,dimension_dictionary,window_size)
    return window_dictionary



def euclidean_distance(vector1,vector2):
    intersection = set(vector1.keys()) & set(vector2.keys())
    vector1min=set(vector1.keys()) - set(vector2.keys())
    vector2min=set(vector2.keys()) - set(vector1.keys())
    common_sum = sum([(vector1[x] - vector2[x])**2 for x in intersection])
    vector1sum = sum([(vector1[x])**2 for x in vector1min])
    vector2sum = sum([(vector2[x])**2 for x in vector2min])
    return math.sqrt(common_sum+vector1sum+vector2sum)
    
def assign_word_to_clusters(distances,k,inital_centers,word,clusters):
    word_distance_array=[]
    if clusters==None:
        clusters={}
        for center in inital_centers:
            clusters.update({center:{}})
    for center in inital_centers:
        word_distance_array.append(distances[center][word])
    for cluster in clusters:
        try:
            del clusters[cluster][word]
        except:
            continue
    clusters[word_distance_array.index(min(word_distance_array))].update({word:None})
    
    return word_distance_array.index(min(word_distance_array)),clusters

def centroid(cluster,words,dimensions,words_in_cluster):
    no_of_words=len(words_in_cluster)
    centroid_vector={}
    for wordname in words_in_cluster:
        for dimension in words[wordname]:
            try:
                temp=centroid_vector[dimension]
            except:
                centroid_vector[dimension]=0
            centroid_vector[dimension]+=words[wordname][dimension]
    for dimension in dimensions:
        current_sum=0
        try:
            current_sum+=centroid_vector[dimension]
        except:
            continue
        centroid_vector[dimension]=float(current_sum)/float(no_of_words)
    return centroid_vector
            
def find_centroids(cluster,k,inital_centers,clusters):
    centroids={}
    for cluster_index in range(0,k):
        if cluster_index==cluster:
            centroids.update({cluster:{}})
            centroids[cluster]=centroid(cluster,words,dimensions,clusters[cluster])
        else:
            centroids.update({cluster_index:inital_centers[cluster_index]})
    return centroids

def square_error(distances,clusters):
    square_error=0
    for cluster in clusters:
        words_in_cluster=clusters[cluster]
        for word in words_in_cluster:
            square_error+=distances[cluster][word]
    return square_error



def kmeans(k,dimensions):
    inital_centers={}
    for center in range(0,k):
        inital_centers.update({center:{}})
        inital_centers[center].update(words[words.keys()[center]])
        distances={}
    for center in inital_centers:
        distances.update({center:{}})
    clusters=None
    current_square_error=None
    previous_square_error=None
    count=0
    errors=range(50)
    while True:
        current_words={}
        for word in words:
            for centroid_name in range(0,k):
                distances[centroid_name][word]=euclidean_distance(inital_centers[centroid_name],words[word])
            changed_cluster_name,clusters=assign_word_to_clusters(distances,k,inital_centers,word,clusters)
            current_words.update({word:words[word]})
            inital_centers=find_centroids(changed_cluster_name,k,inital_centers,clusters)
        previous_square_error=current_square_error
        current_square_error=square_error(distances,clusters)
        errors[count]=current_square_error
        count+=1
        if current_square_error==previous_square_error or count==11:
            break
    #print clusters
    print errors
    return clusters
     
 
 
Word_Dictionary={}
file_path='/home/gowtham/eclipse/A2/txtfiles/tam'
Word_Dictionary=prepare_word_dictionary(file_path,Word_Dictionary)
file_path='/home/gowtham/eclipse/A2/txtfiles/tam_dict'                  
store_word_list(file_path,Word_Dictionary)
file_path='/home/gowtham/eclipse/A2/txtfiles/tam'
dimension_dict=build_dimensions(Word_Dictionary)
window_dictionary=build_window_dictionary(dimension_dict,4,file_path)
file_path='/home/gowtham/eclipse/A2/txtfiles/tam_dim_dict'
store_word_dictionary(file_path,window_dictionary)
dimensions=dimension_dict.keys()
words=window_dictionary

# words={'w1':{'d1':2,'d2':10},'w2':{'d1':2,'d2':5},'w3':{'d1':8.0,'d2':4.0},'w4':{'d1':5.0,'d2':8.0},'w5':{'d1':7,'d2':5.0},'w6':{'d1':6,'d2':4},'w7':{'d1':1,'d2':2},'w8':{'d1':4,'d2':9}}
# #A1=(2,10), A2=(2,5), A3=(8,4), A4=(5,8), A5=(7,5), A6=(6,4), A7=(1,2), A8=(4,9). 
# dimensions=['d1','d2']

 
file_path='/home/gowtham/eclipse/A2/txtfiles/tam_2_cluster'                  
store_cluster_dictionary(file_path,kmeans(10,len(dimensions)))



