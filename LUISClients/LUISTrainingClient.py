__author__ = 'christiaan'
########### Python 3.6 #############
# -*- coding: utf-8 -*-

import http.client, sys, os.path, json
from LUISClients import JSONrequestCreator
import http.client, urllib.request, urllib.parse, urllib.error, base64
import time

# Programmatic key, available in luis.ai under Account Settings
LUIS_programmaticKey  = "e5cbf16a13654d09ad2d016db3fe1ef9"

# ID of your LUISClients app to which you want to add an utterance
LUIS_APP_ID      = "3331538a-ba60-4b5a-b42c-db851937185d"

# The version number of your LUISClients app
LUIS_APP_VERSION = "0.1"

# Update the host if your LUISClients subscription is not in the West US region
LUIS_HOST       = "westus.api.cognitive.microsoft.com"

# uploadFile is the file containing JSON for utterance(s) to add to the LUISClients app.
# The contents of the file must be in this format described at: https://aka.ms/add-utterance-json-format
UTTERANCE_FILE   = "utterances.json"
RESULTS_FILE     = "utterances.results.json"

INTENT_FILE= "intents.json"
RESULTS_INTENT_FILE    = "intents.results.json"

REQUEST_FOLDER='./JSONRequests/'
REQUEST_LOGS_FOLDER='./JSONRequests/LOGS/'

PUBLISH_INFO="publish.json"




# LUISClients client class for adding and training utterances
class LUISClient:

    # endpoint method names
    TRAIN    = "train"
    EXAMPLES = "examples"
    ADD_INTENT="intents"
    PUBLISH ="publish"

    # HTTP verbs
    GET  = "GET"
    POST = "POST"

    # Encoding
    UTF8 = "UTF8"

    # path template for LUISClients endpoint URIs
    PATH     = "/luis/api/v2.0/apps/{app_id}/versions/{app_version}/"
    PUBLISHPATH= "/luis/api/v2.0/apps/{app_id}/"



    # default HTTP status information for when we haven't yet done a request
    http_status = 200
    reason = ""
    result = ""

    def __init__(self, host, app_id, app_version, key):
        if len(key) != 32:
            raise ValueError("LUISClients subscription key not specified in " +
                             os.path.basename(__file__))
        if len(app_id) != 36:
            raise ValueError("LUISClients application ID not specified in " +
                             os.path.basename(__file__))
        self.key = key
        self.host = host
        self.path = self.PATH.format(app_id=app_id, app_version=app_version)
        self.publishPath = self.PUBLISHPATH.format(app_id=app_id)

    def call(self, luis_endpoint, method, data=""):
        path = self.path + luis_endpoint
        if luis_endpoint == self.PUBLISH:
            path = self.publishPath + luis_endpoint
        print('calling: '+str(path))
        headers = {'Ocp-Apim-Subscription-Key': self.key}
        conn = http.client.HTTPSConnection(self.host)
        conn.request(method, path, data.encode(self.UTF8) or None, headers)
        response = conn.getresponse()
        self.result = json.dumps(json.loads(response.read().decode(self.UTF8)),
                                 indent=2)
        self.http_status = response.status
        self.reason = response.reason
        print("HTTP RESPONSE: "+str(response.status)+' '+str(response.reason)+'('+str(json.loads(self.result))+')')
        return self

    def add_utterances(self, filename=REQUEST_FOLDER+UTTERANCE_FILE):
        with open(filename, encoding=self.UTF8) as utterance:
            data = utterance.read()
        return self.call(self.EXAMPLES, self.POST, data)

    def add_intents(self, filename=REQUEST_FOLDER+INTENT_FILE):
        print('JSONfile: '+str(filename))
        with open(filename, encoding=self.UTF8) as intents:
            data = json.loads(intents.read())
            for request in data:
                try:
                    self.call(self.ADD_INTENT, self.POST, str(request))
                except:
                    print(str(request)+' already in list of indents')


    def train(self):
        return self.call(self.TRAIN, self.POST)

    def getTrainingStatus(self):
        return self.call(self.TRAIN, self.GET)

    def publish(self,filename=REQUEST_FOLDER+PUBLISH_INFO):
        with open(filename, encoding=self.UTF8) as publishSpecs:
            data = publishSpecs.read()
        return self.call(self.PUBLISH, self.POST,data)

    def status(self):
        return self.call(self.TRAIN, self.GET)

    def write(self, filename=REQUEST_LOGS_FOLDER+RESULTS_FILE):
        if self.result:
            with open(filename, "w", encoding=self.UTF8) as outfile:
                outfile.write(self.result)
        return self

    def print(self):
        if self.result:
            print(self.result)
        return self

    def raise_for_status(self):
        if 200 <= self.http_status < 300:
            return self
        raise http.client.HTTPException("{} {}".format(
            self.http_status, self.reason))



def trainApplication():
        headers = {
            # Request headers
            'Ocp-Apim-Subscription-Key': '{subscription key}',
        }

        params = urllib.parse.urlencode({
        })
        try:
            conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
            conn.request("POST", "/luis/api/v2.0/apps/{appId}/versions/{versionId}/train?%s" % params, "{body}", headers)
            response = conn.getresponse()
            data = response.read()
            print(data)
            conn.close()
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))





def trainLUIS(inputFile):
        LUIS = LUISClient(LUIS_HOST, LUIS_APP_ID, LUIS_APP_VERSION,
                      LUIS_programmaticKey)

        JSONrequestCreator.constructRequestsForLUIS(inputFile,REQUEST_FOLDER,INTENT_FILE,UTTERANCE_FILE,write=True)
        print('adding intents...')
        LUIS.add_intents()
        print('Intents added...')
        print('adding utterances...')
        LUIS.add_utterances()
        print('Utterances added...')
        print('Retraining app...')
        LUIS.train()
        time.sleep(10)
        print('Training status:')
        LUIS.getTrainingStatus()
        print('Publishing app...')
        LUIS.publish()


if __name__ == "__main__":
    trainLUIS('./trainingSentences')



'''
if __name__ == "__main__":

    # uncomment a line below to simulate command line options
    # sys.argv.append("-train")
    # sys.argv.append("-status")

    luis = LUISClient(LUIS_HOST, LUIS_APP_ID, LUIS_APP_VERSION,
                      LUIS_programmaticKey)

    try:
        if len(sys.argv) > 1:
            option = sys.argv[1].lower().lstrip("-")
            if option == "train":
                print("Adding Intent(s).")
                luis.add_intents().write(filename=RESULTS_INTENT_FILE).raise_for_status()
                print("Adding utterance(s).")
                luis.add_utterances()   .write().raise_for_status()
                print("Added utterance(s). Requesting training.")
                luis.train()            .write().raise_for_status()
                print("Requested training. Requesting training status.")
                luis.status()           .write().raise_for_status()
            elif option == "status":
                print("Requesting training status.")
                luis.status().write().raise_for_status()
        else:
            print("Adding Intent(s).")
            luis.add_intents().write(filename=RESULTS_INTENT_FILE).raise_for_status()
            print("Adding utterance(s).")
            luis.add_utterances().write().raise_for_status()
    except Exception as ex:
        luis.print()    # JSON response may have more details
        print("{0.__name__}: {1}".format(type(ex), ex))
    else:
        print("Success: results in", RESULTS_FILE)
'''