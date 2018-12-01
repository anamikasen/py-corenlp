import json, requests

class StanfordCoreNLP:

    def __init__(self, server_url):
        if server_url[-1] == '/':
            server_url = server_url[:-1]
        self.server_url = server_url

    def annotate(self, text, properties=None):
        assert isinstance(text, str)
        if properties is None:
            properties = {}
        else:
            assert isinstance(properties, dict)

        # Checks that the Stanford CoreNLP server is started.
        try:
            requests.get(self.server_url)
        except requests.exceptions.ConnectionError:
            raise Exception('Check whether you have started the CoreNLP server e.g.\n'
            '$ cd stanford-corenlp-full-2015-12-09/ \n'
            '$ java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer')

        data = text.encode()
        r = requests.post(
            self.server_url, params={
                'properties': str(properties)
            }, data=data, headers={'Connection': 'close'})
        output = r.text
        if ('outputFormat' in properties
             and properties['outputFormat'] == 'json'):
            try:
                output = json.loads(output, encoding='utf-8', strict=True)
            except:
                pass
        return output

    def tokensregex(self, text, pattern, filter):
        return self.regex('/tokensregex', text, pattern, filter)

    def semgrex(self, text, pattern, filter):
        return self.regex('/semgrex', text, pattern, filter)

    def regex(self, endpoint, text, pattern, filter):
        r = requests.get(
            self.server_url + endpoint, params={
                'pattern':  pattern,
                'filter': filter
            }, data=text)
        output = r.text
        try:
            output = json.loads(r.text)
        except:
            pass
        return output

    def sentiment_analysis_on_sentence(sentence):
    # The StanfordCoreNLP server is running on http://127.0.0.1:9000
        nlp = StanfordCoreNLP('http://127.0.0.1:9000')
    # Json response of all the annotations
        output = nlp.annotate(sentence, properties={
            "annotators": "tokenize,ssplit,parse,sentiment",
            "outputFormat": "json",
        # Only split the sentence at End Of Line. We assume that this method only takes in one single sentence.
            "ssplit.eolonly": "true",
        # Setting enforceRequirements to skip some annotators and make the process faster
            "enforceRequirements": "false"
            })
    # Only care about the result of the first sentence because we assume we only annotate a single sentence in this method.
        return int(output['sentences'][0]['sentimentValue'])
