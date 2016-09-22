import os,re,subprocess


class LearnMLN:
    stop_words=['i','me','my','myself','we','our','ours','ourselves','you','your','yours','yourself','yourselves','he','him','his',
                'himself','she','her','hers','herself','it','its','itself','they','them','their','theirs','themselves','what','which',
                'who','whom','this','that','these','those','am','is','are','was','were','be','been','being','have','has','had','having',
                'do','does','did','doing','a','an','the','and','but','if','or','because','as','until','while','of','at','by','for','with',
                'about','against','between','into','through','during','before','after','above','below','to','from','up','down','in','out',
                'off','over','under','again','further','then','once','here','there','when','where','why','how','all','any','both','each',
                'few','on','more','most','some','such','only','own','so','than','too','very','can','will','just','should','now']
    
    
    def __init__(self,Training_Folder_Name,mln_folder):
        self.MLN_folder=mln_folder
        self.MLN_DB_File_Name='train.db'
        self.MLN_File_Name='basic'
        open(os.path.join(self.MLN_folder, self.MLN_DB_File_Name),'w').write('\n')
        self.preprocess_file(Training_Folder_Name)
        return #self.run_mln_learning()
    
    def createMLN(self,MailID,Words,MailName):
        Mln_File=open(os.path.join(self.MLN_folder, self.MLN_DB_File_Name),'a')
        for Word in Words:
            hasword_string="HasWord(\""+Word+"\",\""+MailName+"\")"
            Mln_File.write(hasword_string+"\n") 
        topic_string="Topic("+MailID+",\""+MailName+"\")"
        Mln_File.write(topic_string+"\n")
        return
    
    
    def preprocess_file(self,Training_Folder_Name):
        BucketDictionary={}
        for dir_entry in os.listdir(Training_Folder_Name):
            Training_File_Path = os.path.join(Training_Folder_Name, dir_entry)
            if os.path.isfile(Training_File_Path):
                with open(Training_File_Path, 'r') as Training_File:
                    BucketName=dir_entry
                    BucketName=re.sub("[0-9]", "", BucketName)
                    BucketName=BucketName.split(' ')
                    BucketName=BucketName[0]
                    BucketName=BucketName.replace('.','_')
                    Training_File_Data=re.sub('[^a-zA-Z\n\.]',' ',Training_File.read())
                    Training_File_Data=Training_File_Data.replace('.',' ')
                    tokens=Training_File_Data.split()
                    Modified_Filename=dir_entry.replace('.','_')
                    for token in tokens:
                        if token in self.stop_words:
                            tokens.remove(token)
                    try:
                        BucketDictionary[BucketName]+=1
                        self.createMLN(BucketName,tokens,Modified_Filename)
                    except:
                        temp_Dict={BucketName:1}
                        BucketDictionary.update(temp_Dict)
                        self.createMLN(BucketName,tokens,Modified_Filename)
        print 'Buckets are : '
        for k,v in BucketDictionary.items():
            print k+' '+str(v)
        return
    
    
    
    def run_mln_learning(self):
        print 'learning MLN.....!'
        os.chdir(self.MLN_folder)
        command_string=str('~/alchemy/bin/learnwts -d -i basic.mln -o basic-out.mln -t train.db -ne Topic')
        status=subprocess.check_output(command_string,shell=True)
        print status
        print 'Learning done successfully......!'
        return 
    
        


    
    
    







    





    




    





    
    

    
    

    
    
    