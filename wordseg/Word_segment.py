#encoding=utf-8
__author__ = 'mgchbot'

import math

class Word_segment:

    def __init__(self):

        self.result=[]
        self.dict_tree={"root":[{},[]]}
        self.mincount=1000
        self.sum=0

    def load_dict(self,dict_path="./wordseg/dict.txt"):
        print "Loading dict..."
        for line in open(dict_path):

            words=line.decode("utf-8").split()
            self.mincount=min(self.mincount,int(words[1]))
            self.sum+=int(words[1])
            currentdict=self.dict_tree["root"][0]
            for ct,char in enumerate(words[0]):
                if currentdict.has_key(char):
                    currentdict=currentdict[char][0]
                else:
                    if ct==len(words[0])-1:
                        currentdict[char]=[{},[int(words[1])]]
                    else:
                        currentdict[char]=[{},[]]
                    currentdict=currentdict[char][0]

    def Generate_DAG(self,sentence=""):

        if len(self.dict_tree["root"])<3:
            self.load_dict()

        result={}
        for i,word in enumerate(sentence):
            currentdict=self.dict_tree["root"][0]
            j=i
            result[i]={}
            # print ""
            while(word in currentdict):

                # print word,currentdict[word][1]
                if len(currentdict[word][1])==0:
                    result[i][j+1]=math.log(self.mincount/float(self.sum))
                else:
                    # print math.log(currentdict[word][1][0]/float(self.sum))
                    result[i][j+1]=math.log(currentdict[word][1][0]/float(self.sum))
                if j==len(sentence)-1:
                    break
                j+=1
                currentdict=currentdict[word][0]
                word=sentence[j]
        # print result
        return result


    def word_seg(self,sentence=""):

        if len(sentence)==0:
            return self.result

        sentence=sentence.decode("utf-8")
        if len(self.dict_tree["root"])==0:
            self.load_dict()
        dist=[]
        temp=[]

        DAG=self.Generate_DAG(sentence)
        router=[]
        for i in range(len(sentence)):
            temp=[]
            temp2=[]
            for j in range(len(sentence)+1):
                temp2.append([str(i)+" "+str(j)])
                if DAG[i].has_key(j):
                    temp.append(DAG[i][j])
                else:
                    temp.append(-100000000)
            router.append(temp2)
            dist.append(temp)

        for i in range(len(sentence)):
          for j in range(len(sentence)+1):
            for k in range(len(sentence)):
              if (dist[i][k] + dist[k][j] > dist[i][j] ):
                dist[i][j] = dist[i][k] + dist[k][j];
                router[i][j]=router[i][k]+router[k][j]
        # print dist[0][len(sentence)]

        for word in router[0][len(sentence)]:
            ws=word.split()
            temp=""
            for i in range(int(ws[0]),int(ws[1])):
                temp+=sentence[i]
            self.result.append(temp)
        return self.result

if __name__=="__main__":

    print " ".join(Word_segment().word_seg("我们都是中国人"))
