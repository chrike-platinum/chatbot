__author__ = 'christiaan'
import json
import os.path


def constructIntentRequest(listOfSentencesAndLabels,outPutfilename,write=True):
    with open(outPutfilename,'w') as file:
        jasonString = [{"name": item[1],
                        } for item in listOfSentencesAndLabels]
        j = json.dumps(jasonString,indent=4)
        if write:
                file.write(j)
        return j




def constructTrainingRequest(listOfSentencesAndLabels,outPutfilename,write=True):

    with open(outPutfilename,'w') as file:
        jasonString = [{"text": item[0],
                    "intentName": item[1],
                    "entityLabels":[]} for item in listOfSentencesAndLabels]

        j = json.dumps(jasonString,indent=4)
        if write:
            file.write(j)
        return j



def constructRequestsForLUIS(inputFileName,outputFolder,outPutfilenameIntents,outPutfilenameUtterances,write=True):
    with open(inputFileName) as f:
        lines = f.read().splitlines()

    listOfSentencesAndLabels=[(item[0].strip(),item[1].strip()) for item in  [tuple(l) for l in [line.split('|') for line in lines]]]


    outPutfilePathIntents = os.path.join(outputFolder, outPutfilenameIntents)
    outPutfilePathUtterances = os.path.join(outputFolder, outPutfilenameUtterances)


    intentRequest = constructIntentRequest(listOfSentencesAndLabels,outPutfilePathIntents,write=write)
    trainingRequest = constructTrainingRequest(listOfSentencesAndLabels,outPutfilePathUtterances,write=write)
    return intentRequest,trainingRequest

