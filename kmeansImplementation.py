import math


#words={'w1':{'d1':1,'d2':5},'w2':{'d1':2,'d2':6},'w3':{'d1':5,'d2':7},'w4':{'d1':6,'d2':9},'w5':{'d1':8,'d2':2},'w6':{'d1':9,'d2':1}}
words={'w1':{'d1':1,'d2':1},'w2':{'d1':1.5,'d2':2.0},'w3':{'d1':3.0,'d2':4.0},'w4':{'d1':5.0,'d2':7.0},'w5':{'d1':3.5,'d2':5.0},'w6':{'d1':4.5,'d2':5.0},'w7':{'d1':3.5,'d2':4.5}}
dimensions=['d1','d2']

def euclidean_distance(vector1,vector2):
    intersection = set(vector1.keys()) & set(vector2.keys())
    vector1min=set(vector1.keys()) - set(vector2.keys())
    vector2min=set(vector2.keys()) - set(vector1.keys())
    common_sum = sum([(vector1[x] - vector2[x])**2 for x in intersection])
    vector1sum = sum([(vector1[x])**2 for x in vector1min])
    vector2sum = sum([(vector2[x])**2 for x in vector2min])
    return math.sqrt(common_sum+vector1sum+vector2sum)


    
def assign_words_to_clusters(distances,k,inital_centers):
    word_distance_array=[]
    cluster={}
    for center in inital_centers:
        cluster.update({center:{}})
    for word in words:
        word_distance_array=[]
        for center in inital_centers:
            word_distance_array.append(distances[center][word])
        cluster[word_distance_array.index(min(word_distance_array))].update({word:None})
    return cluster

def centroid(vectors,words,dimensions,k):
    no_of_vectors=len(vectors)
    centroid_vector={}
    if no_of_vectors==0:
        for dimension in dimensions:
            centroid_vector[dimension]=0
    else:
        for vector in vectors:
            for dimension in words[vector]:
                try:
                    temp=centroid_vector[dimension]
                except:
                    centroid_vector[dimension]=0
                centroid_vector[dimension]+=words[vector][dimension]
        for dimension in dimensions:
            current_sum=0
            try:
                current_sum+=centroid_vector[dimension]
            except:
                continue
            centroid_vector[dimension]=float(current_sum)/float(k)
    return centroid_vector
            
def find_centroids(clusters,k,words):
    centroids={}
    for cluster in range(0,k):
        centroids.update({cluster:{}})
        centroids[cluster]=centroid(clusters[cluster],words,dimensions,k)
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
        for dimension in range(1,dimensions+1):
            inital_centers[center]['d'+str(dimension)]=words[words.keys()[center]]['d'+str(dimension)]
    distances={}
    count=0
    current_square_error=None
    previous_square_error=None
    while True:
        for center in inital_centers:
            distances.update({center:{}})
            for word in words:
                distances[center][word]=euclidean_distance(inital_centers[center],words[word])
        clusters=assign_words_to_clusters(distances,k,inital_centers)
        inital_centers=find_centroids(clusters,k,words)
        #count+=1
        previous_square_error=current_square_error
        current_square_error=square_error(distances,clusters)
        print clusters
        print distances
        if current_square_error==previous_square_error:
            break
        if count == 10:
            break
        
        
        
    
    
    
    #print distances
    
    return inital_centers
     
    

print kmeans(2,2)




    
    
    

#print euclidean_distance({'d1':1,'d4':1,'d3':5},{'d1':2,'d4':1,'d2':6})
        
        
        
    

