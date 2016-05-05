__author__ = 'mgchbot'

class KeyWord_TFIDF:

    def __init__(self):
        self.idf_path="./Keyword/idf.txt"
        self.idf_dict={}

    def load_idf(self):
        print "Loading IDF dict..."
        for line in open(self.idf_path):
            word=line.split()
            self.idf_dict[word[0]]=float(word[1])

    def get_keywords(self,sentence="",number=5):

        if len(self.idf_dict)==0:
            self.load_idf()
        dict_result={}
        temp_set=set()
        sentencelen=len(sentence.split())

        for word in sentence.split():
            temp_set.add(word)

        for word in temp_set:
            if self.idf_dict.has_key(word):
                dict_result[word]=sentence.count(word)*self.idf_dict[word]
            else:
                dict_result[word]=sentence.count(word)*5
        dict_result=sorted(dict_result.iteritems(), key=lambda d:d[1], reverse = True)

        if number>sentencelen:
            return dict_result[:sentencelen]
        else:
            return dict_result[:number]

