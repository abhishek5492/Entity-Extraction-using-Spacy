
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

    def NER(self,doc):
        NerList=[]
        html = displacy.render(doc, style="ent", page=True)
        for ent in doc.ents:
            print(str(ent.label_)+' : '+ str(ent.lower_))
            NerList.append(str(ent.label_)+' : '+ str(ent.lower_))
        return NerList


'''Main Api handler'''
app = Flask(__name__)

@app.route("/heartbeat",methods=["GET"])
def heartbeat():
    print("HeartBeat")
    return 'Service is up again n again'

@app.route("/GetNER", methods=["GET"])
def StartNLPService():
   List_of_Entity=[]   
   DirectDependencies=[]
   IndirectDependencies=[]   
   sent = request.args['sent']     
   result = []
   doc = nlp(sent)
   ObjForInformationExtraction = GetInfo()
   List_of_Entity = ObjForInformationExtraction.NER(doc)        
   DirectDependencies = ObjForInformationExtraction.GetDirectDependencyForNLP(doc)
   IndirectDependencies = ObjForInformationExtraction.GetIndirectDependencyForNLP(doc)
        
   return jsonify({'NERList': List_of_Entity,
                   'DirectDependencies' : DirectDependencies,
                   'IndirectDependencies': IndirectDependencies                  
                })

@app.route("/GetDependencyList", methods=["GET"])
def GetDependency():
    sent = request.args['sent']
    doc = nlp(sent)
    html = displacy.render(doc, style="dep", page=True)
    print("hello")

if __name__=="__main__":
    app.run()



