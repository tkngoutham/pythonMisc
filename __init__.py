#!flask/bin/python
from flask import Flask, jsonify, abort, make_response, request,url_for,request
import re,os,subprocess

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class ClassifyMLN:
    
    stop_words=['i','me','my','myself','we','our','ours','ourselves','you','your','yours','yourself','yourselves','he','him','his',
                'himself','she','her','hers','herself','it','its','itself','they','them','their','theirs','themselves','what','which',
                'who','whom','this','that','these','those','am','is','are','was','were','be','been','being','have','has','had',
                'do','does','did','doing','a','an','the','and','but','if','or','because','as','until','while','of','at','by','for','with',
                'about','against','between','into','through','during','before','after','above','below','to','from','up','down','in','out',
                'off','over','under','again','further','then','once','here','there','when','where','why','how','all','any','having','both',
                'few','on','more','most','some','such','only','own','so','than','too','very','can','will','just','should','now','each']
    def __init__(self,mln_folder,threshold):
        self.MLN_folder=mln_folder
        self.MLN_Test_DB_File_Name='test.db'
        self.threshold=threshold
        self.result_file='basic.result'
        Mln_File=open(os.path.join(self.MLN_folder, self.MLN_Test_DB_File_Name),'w')
        Mln_File.write('')
        Mln_File.close()
        return
    
    def process_file(self,Mail_Data):
        Training_File_Data=re.sub('[^a-zA-Z\n\.]',' ',Mail_Data)
        Training_File_Data=Training_File_Data.replace('.',' ')
        tokens=Training_File_Data.lower().split()
        Modified_Filename='test_mail'
        for token in tokens:
            if token.strip().lower() in self.stop_words:
                tokens.remove(token)
        self.createMLN(tokens,Modified_Filename)
        self.run_mln_inference()
        return self.output_bucket(Modified_Filename)
    
    def createMLN(self,Words,MailName):
        Mln_File=open(os.path.join(self.MLN_folder, self.MLN_Test_DB_File_Name),'w')
        for Word in Words:
            hasword_string="HasWord(\""+Word+"\",\""+MailName+"\")"
            Mln_File.write(hasword_string+"\n")
        Mln_File.close()
        return
    
    def run_mln_inference(self):
        os.chdir(self.MLN_folder)
        print 'running inference.....!'
        command_string=str('/home/gowtham/alchemy/bin/infer -i basic-out.mln -r basic.result -e test.db -q Topic')
        status=subprocess.check_output(command_string,shell=True)
        print status
        return
    
    def output_bucket(self,Input_File_Name):
        output=''
        result_File=open(os.path.join(self.MLN_folder, self.result_file),'r')
        lines=result_File.readlines()
        probs=list()
        probs_source=list()
        for line in lines:
            toks=line.split(" ")
            probs.append(float(re.sub('\n','',toks[1])))
            probs_source.append(toks[0])
        try:
            for prob in probs:
                if prob!=0:
                    raise Exception
            output=str(Input_File_Name+' : Not matched to any of the buckets')
            return output
        except:
            pass
        if max(probs)<self.threshold:
            output=str(Input_File_Name+' : Not matched to any of the buckets')
            return output
        output=probs_source[probs.index(max(probs))]
        output=output[6:output.index(',')]
        return output
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class S_DolphinNavigator:
    
    def __init__(self):
        self.sDolphin_Home=os.getenv("HOME")+'/'+'sDolphin'
        self.MLN="""HasWord(word, page)\n
                    Topic(class, page)\n
                    HasWord(+w, p) => Topic(+c, p)"""
        return
    
    def get_sDolphin_Home(self):
        return self.sDolphin_Home
    
    

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


app = Flask(__name__)

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web', 
        'done': False
    }
]


@app.route("/")
def hello():
    return "Hello, I love Digital Appachi!"

@app.route('/todo/api/v1.0/tasks', methods = ['GET'])
def get_tasks():
    return jsonify( { 'tasks': tasks } )

@app.route('/sDolphin/beta/v1.0/classifyMail', methods = ['POST'])
def create_task():
    if not request.json or not 'mail_body' in request.json:
        abort(400)
    classifyMLN=ClassifyMLN('/home/gowtham/sDolphin/DellTest',0.8)
    result=classifyMLN.process_file(request.json['mail_body'])
    return jsonify( { 'Bucket': result } ), 201

@app.route('/upload', methods= ['POST'])
def upload_file():
    domain_name=request.form['domain_name']
    email=request.form['email']
    f = request.files['files']
    
    
    f.save('/home/gowtham/sDolphin/DellTest/newTest.txt')
    
    
    return jsonify( { 'domain_name': domain_name,'email':email } )


if __name__ == "__main__":
    app.run(debug = True)