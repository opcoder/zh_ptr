import jpype
from standoff import TextStandoff
import sys, os
class ParserError(Exception):
    def __init__(self, *args, **margs):
        Exception.__init__(self, *args,**margs)


def standoffFromToken(txt, token):
    return TextStandoff(txt, (token.beginPosition(), token.endPosition()))

class Dependencies:
    def __init__(self, sentence, tokens, posTags, dependencies):
        self.sentence = sentence

        self.posTags = posTags        
        
        self.tokens = tokens

        self.tokensToPosTags = dict(zip(self.tokens, self.posTags))

        self.dependencies = dependencies
        
        self.govToDeps = {}
        self.depToGov = {}
        self.constituentsToRelation = {}

        # there is a bug where sometimes there is a self dependency.
        self.dependencies = [(relation, gov, dep) for relation, gov, dep in self.dependencies
                             if gov != dep]


        for relation, gov, dep in self.dependencies:

            self.govToDeps.setdefault(gov, [])
            self.govToDeps[gov].append(dep)
            assert not dep in self.depToGov, (dep.text, [(key.text, value.text)
                                                         for key, value in self.depToGov.iteritems()])
            self.depToGov[dep] = gov
            self.constituentsToRelation[(gov,dep)] = relation
            
        self.checkRep()

    def tagForTokenStandoff(self, tokenStandoff):
        return self.tokensToPosTags[tokenStandoff]
        
        
    def checkRep(self):
        assert len(self.posTags) == len(self.posTags)        
        for t in self.tokens:
            assert t.entireText == self.sentence



    def govForDep(self, dep):
        return self.depToGov[dep]
    def depsForGov(self, gov):
        return self.govToDeps[gov]

    def relForConstituents(self, gov, dep):
        return self.constituentsToRelation((gov, dep))
    
    def __str__(self):
        result = ""
        result += "sentence=" + repr(self.sentence) + "\n"
        for relation, gov, dep in self.dependencies:
            result += relation + "(" + gov.text + ", " + dep.text + ")\n"
        return result

stanford_parser_home = None

def startJvm():
    import os
    os.environ.setdefault("STANFORD_PARSER_HOME", r"E:\stanford-parser-full-2016-10-31")
    global stanford_parser_home
    stanford_parser_home = os.environ["STANFORD_PARSER_HOME"]
    stanford_parser_jar = os.path.join(stanford_parser_home, 'stanford-parser.jar')
    assert(os.path.exists(stanford_parser_jar))
    jpype.startJVM(jpype.getDefaultJVMPath(),
                   "-ea",
                   "-Djava.class.path={}".format(stanford_parser_jar),)
startJvm() # one jvm per python instance.

class Parser:

    def __init__(self, pcfg_model_fname=None):
        # if pcfg_model_fname == None:
        #     #self.pcfg_model_fname = "%s/englishPCFG.ser" % stanford_parser_home
        #     #self.pcfg_model_fname = "%s/englishFactored.ser" % stanford_parser_home
        #     self.pcfg_model_fname = os.path.join(stanford_parser_home,
        #                                          'stanford-parser-3.7.0-models',
        #                                          'edu/stanford/nlp/models/lexparser',
        #                                          'chinesePCFG.ser.gz')
        # else:
        #     self.pcfg_model_fname = pcfg_model_fname
        # assert(os.path.exists(self.pcfg_model_fname))

        zip_path = os.path.join(stanford_parser_home, 'stanford-parser-3.7.0-models.jar')
        model_path = 'edu/stanford/nlp/models/lexparser/chinesePCFG.ser.gz'
        # model_path = 'edu/stanford/nlp/models/lexparser/chineseFactored.ser.gz'
        self.package_lexparser = jpype.JPackage("edu.stanford.nlp.parser.lexparser")
        # self.parser = self.package_lexparser.LexicalizedParser.loadModelFromZip(jar_path, model_path)

        # zip_path = r'E:\stanford-parser-full-2016-10-31\model.zip'
        # model_path = 'chinesePCFG.ser.gz'

        self.parser = self.package_lexparser.LexicalizedParser.loadModelFromZip(zip_path, model_path)

        # self.package = jpype.JPackage("edu.stanford.nlp")

        # tokenizerFactoryClass = self.package.process.__getattribute__("PTBTokenizer$PTBTokenizerFactory")
        # self.tokenizerFactory = tokenizerFactoryClass.newPTBTokenizerFactory(True, True)
        #
        # self.documentPreprocessor = self.package.process.DocumentPreprocessor(self.tokenizerFactory)


        # self.parser.setOptionFlags(["-retainTmpSubcategories"])




    def printInfo(self):

        Numberer = self.package.util.Numberer
        print ("Grammar\t" +
               `Numberer.getGlobalNumberer("states").total()` + '\t' +
               `Numberer.getGlobalNumberer("tags").total()` + '\t' +
               `Numberer.getGlobalNumberer("words").total()` + '\t' +
               `self.parser.pparser.ug.numRules()` + '\t' +
               `self.parser.pparser.bg.numRules()` + '\t' +
               `self.parser.pparser.lex.numRules()`)

        print "ParserPack is ", self.parser.op.tlpParams.getClass()
        print "Lexicon is ", self.parser.pd.lex.getClass()        
        print "Tags are: ", Numberer.getGlobalNumberer("tags")
        self.parser.op.display()
        print "Test parameters"
        self.parser.op.tlpParams.display();
        self.package_lexparser.Test.display()
    # def parse(self, sentence):
    #     """
    #     Parses the sentence string, returning the tokens, and the parse tree as a tuple.
    #     tokens, tree = parser.parse(sentence)
    #     """
    #
    #     tokens = self.documentPreprocessor.getWordsFromString(sentence)
    #     for token in tokens:
    #         if token.word() in ["down"]:
    #             print "setting tag"
    #             token.setTag("IN")
    #             pass
    #         if token.word().lower() in ["bot"]:
    #             token.setTag("NN")
    #             pass
    #
    #     wasParsed = self.parser.parse(tokens)
    #     if not wasParsed:
    #         raise ParserError("Could not parse " + sentence)
    #     return tokens, self.parser.getBestParse()
    #
    # def parseToStanfordDependencies(self, sentence):
    #
    #     tokens, tree = self.parse(sentence)
    #     standoffTokens = [standoffFromToken(sentence, token)
    #                       for token in tokens]
    #     posTags = [token.tag() for token in tree.taggedYield()]
    #     print " ".join(["%s/%s" % (word.text, tag) for word, tag in zip(standoffTokens, posTags)])
    #     #print tree.taggedYield().toString(False)
    #     result = self.package.trees.EnglishGrammaticalStructure(tree)
    #
    #     returnList = []
    #     for dependency in result.typedDependenciesCollapsedTree():
    #
    #         govStandoff = standoffTokens[dependency.gov().index() - 1]
    #         depStandoff = standoffTokens[dependency.dep().index() - 1]
    #
    #         returnList.append((str(dependency.reln()),
    #                            govStandoff,
    #                            depStandoff))
    #
    #
    #
    #     return Dependencies(sentence, standoffTokens, posTags, returnList)
                              
if __name__ == '__main__':
    par = Parser()
    print 'done'