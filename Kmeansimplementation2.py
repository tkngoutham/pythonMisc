import math


#words={'w1':{'d1':1,'d2':5},'w2':{'d1':2,'d2':6},'w3':{'d1':5,'d2':7},'w4':{'d1':6,'d2':9},'w5':{'d1':8,'d2':2},'w6':{'d1':9,'d2':1}}
#words={'w1':{'d1':1,'d2':1},'w2':{'d1':1.5,'d2':2.0},'w3':{'d1':3.0,'d2':4.0},'w4':{'d1':5.0,'d2':7.0},'w5':{'d1':3.5,'d2':5.0},'w6':{'d1':4.5,'d2':5.0},'w7':{'d1':3.5,'d2':4.5}}
words={'w1':{'d1':2,'d2':10},'w2':{'d1':2,'d2':5},'w3':{'d1':8.0,'d2':4.0},'w4':{'d1':5.0,'d2':8.0},'w5':{'d1':7,'d2':5.0},'w6':{'d1':6,'d2':4},'w7':{'d1':1,'d2':2},'w8':{'d1':4,'d2':9}}
#A1=(2,10), A2=(2,5), A3=(8,4), A4=(5,8), A5=(7,5), A6=(6,4), A7=(1,2), A8=(4,9). 
dimensions=['d1','d2']


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
        if current_square_error==previous_square_error:
            break
    return clusters
    #return inital_centers
     
    

print kmeans(3,2)




    
    
    

#print euclidean_distance({'d1':1,'d4':1,'d3':5},{'d1':2,'d4':1,'d2':6})
        
        
        
    

