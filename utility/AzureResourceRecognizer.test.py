import spacy
import plac
from spacy.lang.en import English
from spacy.tokens import Doc, Span, Token
from AzureResourceRecognizer import AzureResourceRecognizer

nlp = spacy.load('en_core_web_lg')

def test(text):
    doc = nlp(text)
    print('Tokens', [t.text for t in doc]) 
    # print('Doc has_azure_resource', doc._.has_azure_resource)
    # print('Token 0 is_azure_resource', doc[1]._.is_azure_resource)
    # print('Token 1 is_azure_resource', doc[2]._.is_azure_resource)
    print('Entities', [(e.text, e.label_) for e in doc.ents])

def run():
    text = "How to start my vm and virtual machine?"
    test(text)
    azureResourceRecognizer = AzureResourceRecognizer(nlp)
    nlp.add_pipe(azureResourceRecognizer, last=True)
    test(text)

run()