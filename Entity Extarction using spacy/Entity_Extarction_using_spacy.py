
from flask import Flask,jsonify
import re, spacy, os
from flask import request
import json
from spacy import displacy

nlp = spacy.load('en_core_web_lg')

class GetInfo:    
    def GetDirectDependencyForNLP(self, doc):        
        GetDirectDep = []
        for item in doc:
            GetDirectDep.append([item.text, item.dep_, item.head.text, item.head.pos_])
        return GetDirectDep

    def GetIndirectDependencyForNLP(self, doc):        
        IndirectDep = []
        for token in doc:
            ancestors = []
            for ancestor in token.ancestors:
                ancestors.append(ancestor.text)
            IndirectDep.append([token.text, token.dep_, ancestors])
            # print(token.text,token.dep_,[ancestor.text for ancestor in token.ancestors])
        return IndirectDep

    def NER(self,sentrecived,nlp):
        doc = nlp(sent)        
        for ent in doc.ents:
            print("hello")
    
    def ShowDependency(self, sentence, nlp):
        doc = nlp(sent)
        displacy.serve(doc, style="dep")


'''Main Api handler'''
app = Flask(__name__)

@app.route("/heartbeat",methods=["GET"])
def heartbeat():
    print("HeartBeat")
    return 'Service is up again n again'

@app.route("/GetDependencyList", methods=["GET"])
def StartNLPService():
   Possible_List_of_Org=[]   
   DirectDependencies=[]
   IndirectDependencies=[]
   PurchaseAmount=''
   ClosingDate=''
   InitialEarnestMoney=''
   AdditionalEarnestMoney=''
   TIN=''
   InspectionPeriod=''
   sent = request.args['sent']
   keyword=request.args['key']
   sent=sent.replace('URISEPEREATOR','&')   
   result = []   
   

   if keyword=='Buyer' or keyword=='Seller':
        doc = nlp(sent)
        ObjForInformationExtraction = GetInfo()
        Possible_List_of_Org = ObjForInformationExtraction.NER(sent,nlp)        
        DirectDependencies = ObjForInformationExtraction.GetDirectDependencyForNLP(doc)
        IndirectDependencies = ObjForInformationExtraction.GetIndirectDependencyForNLP(doc)
        
   return jsonify({'NERList': Possible_List_of_Org,
                   'DirectDependencies' : DirectDependencies,
                   'IndirectDependencies': IndirectDependencies                  
                })

if __name__=="__main__":
    app.run()



