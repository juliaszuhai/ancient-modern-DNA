class BlastData:

    def __init__(self,title:str,length:str,score:str,gaps:str,eValue:str,query:str,match:str,sbjct:str):
        self.title=title
        self.length=length
        self.score=score
        self.gaps=gaps
        self.eValue=eValue
        self.query=query
        self.match=match
        self.sbjct=sbjct

    def __str__(self):
        return "Allignment:"+self.title+"\n"+"seq"+str(self.sbjct)






