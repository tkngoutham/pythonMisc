import MySQLdb,os
from ClassifyMLN import ClassifyMLN
from LearnMLN import LearnMLN








class S_DolphinNavigator:
    
    def __init__(self):
        self.sDolphin_Home=os.getenv("HOME")+'/'+'sDolphin'
        self.MLN="""HasWord(word, page)\n
                    Topic(class, page)\n
                    HasWord(+w, p) => Topic(+c, p)"""
        return
    
    
    def initiate_learning(self,Domain_Name):
        db = MySQLdb.connect(host="192.168.10.100", port=3306, user="root", passwd="123456", db="sDolphin")
        cur=db.cursor()
        cur.execute("select max(Domain_ID) from Domain_Name_Resolution;")
        a=cur.fetchall()
        current_index=a[0][0]+1
        cur.execute("insert into Domain_Name_Resolution(Domain_Name,Reference_ID) values("+Domain_Name+","+Domain_Name+"_"+current_index+")")
        os.chdir(self.sDolphin_Home)
        os.system(str("mkdir "+Domain_Name+"___"+current_index+"___Test"))
        os.chdir(self.sDolphin_Home+'/'+Domain_Name+"___"+current_index+"___Test")
        mln=open('basic.mln','w')
        mln.write(self.MLN)
        mln.close()
        
        LearnMLN(self.sDolphin_Home+'/'+Domain_Name+"___"+current_index+"___Data",self.sDolphin_Home+'/'+Domain_Name+"___"+current_index+"___Test").run_mln_learning()
        ClassifyMLN(self.sDolphin_Home+'/'+Domain_Name+"___"+current_index+"___Test",0.8)
        return
    
    def get_sDolphin_Home(self):
        return self.sDolphin_Home
        
S_DolphinNavigator().initiate_learning()