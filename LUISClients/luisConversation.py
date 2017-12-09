__author__ = 'christiaan'

#import the luis client and open the luis app
import luis
l = luis.Luis(url='https://westus.api.cognitive.microsoft.com/luis/v2.0/apps/3331538a-ba60-4b5a-b42c-db851937185d?subscription-key=e5cbf16a13654d09ad2d016db3fe1ef9&staging=true&verbose=true&timezoneOffset=0&q=')



def analyseQuestion(question,verbose=False):
    r = l.analyze(question)
    best = r.best_intent()
    command = best.intent
    score=best.score
    print('FOUND: '+str(command)+' with accuracy of '+str(score)+'.')
    parameters = [(item.resolution,item.start_index,item.end_index) for item in r.entities]
    print('PARAMETERS: '+str(parameters))
    print(r)
    returnSet = command,parameters
    if verbose:
        returnSet.append(score)
    return returnSet






#'show top three customers 4 days ago?'

analyseQuestion('show top three customers of november last year')
