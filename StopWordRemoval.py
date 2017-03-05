__author__ = 'kushwanth'


from nltk.corpus import stopwords;
sentences=["I want to go out for dinner","I am interested in Indian Food","I like sea food","Price of food should not be more than 1000/- per person"];
stop=stopwords.words('english');

bufferArray=[];

def buildCombination(n,k):
    if n<1: return;
    j=0;
    while j<k:
        bufferArray.append(j);
        buildCombination(n-1,k);
        j=j+1;
    return


for sent in sentences:
    A=[i for i in sent.split() if i not in stop];
    bufferArray=[];
    buildCombination(len(A),2);
    print bufferArray;
print A







#stopwordremov=["I want go dinner","I interested Indian Food","I like sea food","Price food more 1000/- person"];

#how to link indian food and sea food ie entity linking comes into picture
