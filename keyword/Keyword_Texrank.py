__author__ = 'mgchbot'

class Keyword_Texrank:

    def __init__(self):

        self.wordgraph={}
        self.result={}

    def gernerate_wordgraph(self,sentence="",wordwindow=5):

        words=sentence.split()
        for word in words:
            if not self.wordgraph.has_key(word):
                self.wordgraph[word]=[set(),set()]

        for i,word in enumerate(words):
            for j in range(max(0,i-wordwindow),min(len(words),i+wordwindow)):
                self.wordgraph[word][0].add(words[j])
                self.wordgraph[words[j]][1].add(word)

    def get_keywords(self,sentence="",number=5,wordwindow=2,iter=100):
        words=sentence.split()
        for word in words:
            if not self.result.has_key(word):
                self.result[word]=float(1)/words.count(word)
        self.gernerate_wordgraph(sentence,wordwindow)

        for i in range(iter):
            for word in words:
                sum=0
                for j in self.wordgraph[word][1]:
                    sum+=self.result[j]/float(len(self.wordgraph[j][0]))
                self.result[word]=0.15+0.85*sum
        result=sorted(self.result.iteritems(), key=lambda d:d[1], reverse = True)
        return result
