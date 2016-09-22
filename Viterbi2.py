def prepare_unigram_bigram_trigram_word_dictionaries(file_path):
    with open(file_path,'r') as fp:
        count=0
        for line in fp:
            if count==0:
                count+=1
                continue
            decoded_line=line.decode('utf-8')
            tokens=decoded_line.split()
            Before_Previous_Tag=None
            Previous_Tag=None 
            Current_Tag=None
            Current_Word=None
            Bigram=None
            Trigram=None
            for token in tokens:
                token=token.strip()
                word_tag=token.split('/')
                if(len(word_tag)<2):
                    Current_Tag=token
                else:                
                    Current_Tag=word_tag[1].strip()
                    Current_Word=word_tag[0].strip()
                    try:
                        Word_Dictionary[Current_Word]+=1
                    except:
                        temp_dict={Current_Word:1}
                        Word_Dictionary.update(temp_dict)
                try:
                    Unigram_Dictionary[Current_Tag]+=1
                except:
                    temp_dict={Current_Tag:1}
                    Unigram_Dictionary.update(temp_dict)
                if Before_Previous_Tag==None and Previous_Tag==None:
                    Previous_Tag=Current_Tag
                    continue
                elif Before_Previous_Tag==None and Previous_Tag!=None:
                    Before_Previous_Tag=Previous_Tag
                    Bigram=Previous_Tag+' '+Current_Tag
                    Previous_Tag=Current_Tag
                    try:
                        BiGram_Dictionary[Bigram]+=1
                    except:
                        temp_dict={Bigram:1}
                        BiGram_Dictionary.update(temp_dict)
                else:
                    Trigram=Before_Previous_Tag+' '+Previous_Tag+' '+Current_Tag
                    Before_Previous_Tag=Previous_Tag
                    Bigram=Previous_Tag+' '+Current_Tag
                    Previous_Tag=Current_Tag
                    try:
                        BiGram_Dictionary[Bigram]+=1
                    except:
                        temp_dict={Bigram:1}
                        BiGram_Dictionary.update(temp_dict)
                    try:
                        TriGram_Dictionary[Trigram]+=1
                    except:
                        temp_dict={Trigram:1}
                        TriGram_Dictionary.update(temp_dict)
  

def build_bigram_transition_matrix(Unigram_Dictionary,BiGram_Dictionary,PreDefined_Tags):
    bigram_transition_matrix={}
    second_level_tags=PreDefined_Tags
    for PreDefined_Tag in PreDefined_Tags:
        temp={PreDefined_Tag:{}}
        bigram_transition_matrix.update(temp)
        try:
            count_of_current_unigram=Unigram_Dictionary[PreDefined_Tag]
        except:
            count_of_current_unigram=0
        #print PreDefined_Tag+' '
        for second_level_tag in second_level_tags:
            current_bigram=PreDefined_Tag+' '+second_level_tag
            try:
                count_of_current_bigram=BiGram_Dictionary[current_bigram]
            except:
                count_of_current_bigram=0
            if count_of_current_unigram==0:
                bigram_transition_matrix[PreDefined_Tag][second_level_tag]=0.0
            else:
                bigram_transition_matrix[PreDefined_Tag][second_level_tag]=(float(float(count_of_current_bigram)/float(count_of_current_unigram)))
            #print second_level_tag+'\n'   
    return bigram_transition_matrix


def smoothing(Word_Dictionary,training_data_path,smoothed_training_data_path):
    smoothed_training_data_pointer=open(smoothed_training_data_path,'w')
    with open(training_data_path,'r') as fp:
        count=0
        Current_Sentence='   '
        for line in fp:
            if count==0:
                smoothed_training_data_pointer.write(Current_Sentence.encode('utf-8')+'\n')
                count+=1
                continue
            decoded_line=line.decode('utf-8')
            tokens=decoded_line.split()
            Current_Sentence=''
            Current_Word=None
            for token in tokens:
                token=token.strip()
                word_tag=token.split('/')
                if(len(word_tag)<2):
                    Current_Sentence=Current_Sentence+str(token).encode('utf-8')+' '
                    continue
                else:
                    Current_Word=word_tag[0].strip()
                    Current_Tag=word_tag[1].strip()
                    try:
                        if Word_Dictionary[Current_Word]<2:
                            Current_Word='_RARE_'
                    except:
                        continue
                Current_Sentence+=Current_Word+'/'+Current_Tag+' '
            smoothed_training_data_pointer.write(Current_Sentence.encode('utf-8')+'\n')


def build_wordtag_dictionary_after_smoothing(smoothed_training_data_path):
    Smoothed_Word_Dictionary={}
    with open(smoothed_training_data_path,'r') as fp:
        count=0
        for line in fp:
            if count==0:
                count+=1
                continue
            decoded_line=line.decode('utf-8')
            tokens=decoded_line.split()
            Current_Word=None
            for token in tokens:
                token=token.strip()
                try:
                    Word_Tag_Dictionary[token]+=1
                except:
                    temp_dict={token:1}
                    Word_Tag_Dictionary.update(temp_dict)
                word_tag=token.split('/')
                if(len(word_tag)<2):
                    continue
                    #Current_Tag=token
                else:                
                    #Current_Tag=word_tag[1].strip()
                    Current_Word=word_tag[0].strip()
                    try:
                        Smoothed_Word_Dictionary[Current_Word]+=1
                    except:
                        temp_dict={Current_Word:1}
                        Smoothed_Word_Dictionary.update(temp_dict)
    return Smoothed_Word_Dictionary
            
    
def build_emission_matrix(Tag_Dictionary,Word_Tag_Dictionary,Smoothed_Word_Dictionary,PreDefined_Tags):
    count_of_tag=0.0
    emission_matrix={}
    for PreDefined_Tag in PreDefined_Tags:
        try:
            count_of_tag=Tag_Dictionary[PreDefined_Tag]
        except:
            count_of_tag=0.0
        temp={PreDefined_Tag:{}}
        emission_matrix.update(temp)
            
        for word in Smoothed_Word_Dictionary:
            current_wordtag=word+'/'+PreDefined_Tag
            if count_of_tag==0.0:
                emission_matrix[PreDefined_Tag][word]=0.0
                continue
            try:
                count_of_wordtag=Word_Tag_Dictionary[current_wordtag]
            except:
                count_of_wordtag=0.0
            emission_matrix[PreDefined_Tag][word]=float(float(count_of_wordtag)/float(count_of_tag))
    return emission_matrix
                
def bigram_transition(curr_pos_tag,prev_pos_tag):
    return bigram_transition_matrix[prev_pos_tag][curr_pos_tag]

def emission(word,tag):
    return emission_matrix[tag][word]
              
                
def find_returning_tags(backtracking_Dictionary,sentence_length):
    returning_tags=range(sentence_length)
    current_position=sentence_length-1
    returning_tags[current_position]=backtracking_Dictionary[sentence_length].keys()[0]
    current_pos_tag=backtracking_Dictionary[sentence_length].keys()[0]
    current_position=current_position-1
    for index in range(-current_position,1):
        if -index+1==sentence_length:
            returning_tags[-index]=backtracking_Dictionary[-index+1][current_pos_tag]
        else:
            returning_tags[-index]=backtracking_Dictionary[-index+1][current_pos_tag][0]
        current_pos_tag=returning_tags[-index]
    return returning_tags


def pi(position,curr_pos_tag,smoothed_sentence):
    if position==0:
        return emission(smoothed_sentence[position],curr_pos_tag)
        #return bigram_transition(curr_pos_tag,'<START>')*emission(smoothed_sentence[position],curr_pos_tag)
    else:
        probability_buffer=[]
        probability_buffer=range(len(Taggable_Tags))
        emission_prob=emission(smoothed_sentence[position],curr_pos_tag)
        try:
            temp=backtracking_Dictionary[position]
        except:
            backtracking_Dictionary.update({position:{}})
        for index in range(0,len(Taggable_Tags)):
            pi_from_backtrack=0.0
            try:
                pi_from_backtrack=backtracking_Dictionary[position-1][Taggable_Tags[index]][1]
            except:
                pi_from_backtrack=pi(position-1,Taggable_Tags[index],smoothed_sentence)
            probability_buffer[index]=pi_from_backtrack*bigram_transition(curr_pos_tag,Taggable_Tags[index])*emission_prob
        backtracking_Dictionary[position][curr_pos_tag]=(Taggable_Tags[probability_buffer.index(max(probability_buffer))],max(probability_buffer))
        return max(probability_buffer)
    
def viterbi(words_in_sent):
    position=len(words_in_sent)-1
    probability_buffer=range(len(Taggable_Tags))
    backtracking_Dictionary.update({len(words_in_sent):{}})
    for Tag in Taggable_Tags:
        probability_buffer[Taggable_Tags.index(Tag)]=bigram_transition('<STOP>',Tag)*pi(position,Tag,words_in_sent)
    backtracking_Dictionary[len(words_in_sent)].update({Taggable_Tags[probability_buffer.index(max(probability_buffer))]:None})
    print backtracking_Dictionary
    returning_tags=find_returning_tags(backtracking_Dictionary,len(words_in_sent)) 
    return returning_tags  




def initiate_viterbi(sentence_file_path):
    count=0
    with open(sentence_file_path,'r') as fp:
        for line in fp:
            if count==0:
                count+=1
                continue
            current_line=line.decode('utf-8')
            words_in_sent=current_line.split()
            smoothed_sentence=''
            output_file=open('/home/gowtham/eclipse/A2/results/kan_result','a')
            for word in words_in_sent:
                smoothed_word=''
                word=word.strip()
                word=word.replace('\n','')
                dummy_num=0
                try:
                    dummy_num=Smoothed_Word_Dictionary[word]
                    smoothed_word=word
                except:
                    smoothed_word='_RARE_'
                smoothed_sentence+=smoothed_word+' '
            backtracking_Dictionary.clear()
            output_file.write(build_returning_sentence(words_in_sent,viterbi(smoothed_sentence.split())))
            
      
    return
            
    
    
def initiation():
    sentence_file_path=''
    while True:
        sentence_file_path=input('enter sentence file path :' )
        initiate_viterbi(sentence_file_path)
        choice=input('if you want to exit press y else n :' )
        if choice == 'y':
            break
    return

def build_returning_sentence(words_in_sent,returning_tags):
    indexes=range(len(words_in_sent))
    words_with_tag=range(len(words_in_sent))
    returning_sent=''
    for index in indexes:
        words_with_tag[index]=words_in_sent[index]+'_'+returning_tags[index]
        returning_sent=returning_sent+words_with_tag[index]+' '
    return (returning_sent+'\n').encode('utf-8')

PreDefined_Tags=['<START>',
                 'NN','NST','NNP','PRP',
              'DEM','VM','VAUX','JJ',
              'RB','PSP','RP','CC',
              'WQ','QF','QC','QO',
              'CL','INTF','INJ','NEG',
              'UT','SYM','*C','RDP',
              'ECH','UNK','<STOP>']

Taggable_Tags=['NN','NST','NNP','PRP',
              'DEM','VM','VAUX','JJ',
              'RB','PSP','RP','CC',
              'WQ','QF','QC','QO',
              'CL','INTF','INJ','NEG',
              'UT','SYM','*C','RDP','ECH','UNK']




Word_Tag_Dictionary={}
Unigram_Dictionary={}
BiGram_Dictionary={}
TriGram_Dictionary={}
Word_Dictionary={}
emission_matrix={}
backtracking_Dictionary={}
training_data_path='/home/gowtham/eclipse/A2/txtfiles/kan_tagged'
smoothed_training_data_path='/home/gowtham/eclipse/A2/txtfiles/kan_tagged_smoothed.txt'
prepare_unigram_bigram_trigram_word_dictionaries(training_data_path)
bigram_transition_matrix=build_bigram_transition_matrix(Unigram_Dictionary,BiGram_Dictionary,PreDefined_Tags)
smoothing(Word_Dictionary,training_data_path,smoothed_training_data_path)
Smoothed_Word_Dictionary=build_wordtag_dictionary_after_smoothing(smoothed_training_data_path)
emission_matrix=build_emission_matrix(Unigram_Dictionary,Word_Tag_Dictionary,Smoothed_Word_Dictionary,PreDefined_Tags)

initiation()








#emission_matrix=build_emission_matrix()
#print Word_Dictionary
# f=open(r'C:\Users\innoveta\Desktop\PGMs\testwords.txt','w')
# for key,value in emission_matrix.iteritems():
#     if key==None:
#         continue
#     f.write(key.encode('utf-8')+' '+str(value)+'\n')
    

# print bigram_transition_matrix['<START>']['DEM']
# print bigram_transition_matrix['DEM']['NST']
# print bigram_transition_matrix['NNP']['NN']
# print bigram_transition_matrix['VM']['<STOP>']
# print emission_matrix['VAUX']
print bigram_transition_matrix['NN']['VM']