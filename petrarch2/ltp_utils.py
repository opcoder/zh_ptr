# -*- coding:utf8 -*-
import pyltp
import sys
import os

reload(sys)
sys.setdefaultencoding('utf-8')

class LTP:
    def __init__(self):
        model_dir = r'C:\Users\wcbao\Desktop\eventext\evernote\ltp.model'
        self.sentenceSplitter = pyltp.SentenceSplitter
        self.segmentor = pyltp.Segmentor()
        self.segmentor.load(os.path.join(model_dir,'cws.model'))
        self.postagger = pyltp.Postagger()
        self.postagger.load(os.path.join(model_dir, 'pos.model'))
        self.parser = pyltp.Parser()
        self.parser.load(os.path.join(model_dir, 'parser.model'))
        self.srl = pyltp.SementicRoleLabeller()
        self.srl.load(os.path.join(model_dir, 'srl'))
        self.ner = pyltp.NamedEntityRecognizer()
        self.ner.load(os.path.join(model_dir, 'ner.model'))
        print 'pyltp models loaded done!'

    def sentenceSplit(self, text):
        return list(self.sentenceSplitter.split(text))

    def segment(self, sents):
        if isinstance(sents, list):
            return [list(self.segmentor.sengment(sent)) for sent in sents]
        if isinstance(sents, unicode):
            sents = str(sents)
        return list(self.segmentor.segment(sents))

    def postag(self, words):
        return list(self.postagger.postag(words))

    def recognize(self, words, postags = None):
        if isinstance(words, str) or isinstance(words, unicode):
            words = self.segment(words)
        if postags:
            return list(self.ner.recognize(words, postags))
        return list(self.ner.recognize(words, self.postag(words)))

    def parse(self, words, postags = None):
        if postags:
            return self.parser.parse(words, postags)
        return self.parser.parse(words, self.postag(words))

    def label(self, **kwargs):
        # parameters: {'words','postags', 'netags', 'arcs', 'sentense'}
        assert('words' in kwargs or 'sentenses' in kwargs)
        words = kwargs['words'] if 'words' in kwargs else self.segment(kwargs['sentenses'])
        postags = kwargs['postags'] if 'postags' in kwargs else self.postag(words)
        netags = kwargs['netags'] if 'netags' in kwargs else self.recognize(words, postags)
        arcs = kwargs['arcs'] if 'arcs' in kwargs else self.parse(words, postags)
        roles = self.srl.label(words, postags, netags, arcs)
        return roles

    def __del__(self):
        self.segmentor.release()
        self.postagger.release()
        self.parser.release()
        self.srl.release()

ltp_api = LTP()
if __name__ == '__main__':
    ltp = LTP()
    sent = '国务院总理李克强调研上海外高桥时提出，支持上海积极探索新机制。'
    words = ltp_api.segment(sent)
    ner = ltp.recognize(words)
    text = '报道称，强大的中国军队7月11日可能在南海西沙群岛周边实施军事演习。'
    sentenses = ltp_api.sentenceSplit(text)[0]
    roles = ltp_api.label(**{'sentenses': sentenses})
    for role in roles:
        print role.index, "".join(
            ["%s:(%d,%d)" % (arg.name, arg.range.start, arg.range.end) for arg in role.arguments])



