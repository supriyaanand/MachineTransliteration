__author__ = 'supriya'

import sys
import re
import nltk
from nltk.collocations import *

def readAnnotationFile(filename):
    nere = re.compile(r"\[[^\]\\]+\]");
    fid = open(filename, 'r');
    data = [];
    isTokType = re.compile("^[A-Z]{1,3}$");
    neTokTypes = set(["P", "L", "A"]);

    for line in fid:
        line = line.replace("\n", "").replace("\r", "").decode('utf-8').replace(u"\ufeff", "").strip();
        # print [line]
        if line == "":
            continue;
        neLocs = [];
        it = re.finditer(nere, line);
        for match in it:
            neLocs.append([match.start(), match.end()]);
        fields = line.split(" ");
        st = 0;
        entry = [];
        for f in fields:
            inNe = False;
            rloc = [];
            for loc in neLocs:
                if st >= loc[0] and st <= loc[1]:
                    rloc = loc;
                    inNe = True;
                    break;
            tok = "";
            tokType = "";
            translit = "";
            if inNe:
                tok = f;
                if rloc[0] == st and rloc[1] <= st + len(f):
                    tok = line[st + 1:rloc[1] - 1];
                # if rloc[0]==st:
                # tok = tok[1:];
                # if rloc[1]==st+len(f)-1:
                #    tok = tok[:-2];
                postfix = line[rloc[1]:];
                if len(postfix) > 0:
                    temp = postfix.split(" ");  # translit of multi-token ne not handled here...
                    if len(temp) > 0:
                        if "=" in temp[0]:
                            tokTypes = temp[0].split("=")[0];
                            if (tokTypes == ""):
                                tokType = "NE_?";
                            else:
                                tokType = "NE_%s" % (tokTypes);
                            translit = temp[0].split("=")[1];
                        else:
                            if temp[0] == "":
                                tokType = "NE_?";
                            else:
                                tokType = "NE_%s" % (temp[0]);
                    else:
                        if "=" in postfix:
                            tokTypes = postfix.split("=")[0];
                            if tokTypes == "":
                                tokType = "NE_?";
                            else:
                                tokType = "NE_%s" % (tokTypes);
                            translit = postfix.split("=")[1];
                        else:
                            if postfix == "":
                                tokType = "NE_?";
                            else:
                                tokType = "NE_%s" % (postfix);
                """
                if len(postfix)==0:
                    tokType = "NE_GENERIC";
                elif postfix[0]==" ":
                    tokType = "NE_GENERIC";
                elif not postfix[0] in ["P","O","L","A"]:
                    tokType = "NE_?";
                else:
                    tokType = "NE_%s" %(postfix[0]);
                """

            else:
                if "\\" in f:
                    temp = f.split("\\");
                    tok = temp[0];
                    if "=" in temp[1]:
                        translit = temp[1].split("=")[1];
                        tokType = temp[1].split("=")[0];
                    else:
                        tokType = temp[1];

                    if re.match(isTokType, tokType) == None:
                        tokType = "";
                        tok = f;
                        translit = "";
                else:
                    tok = f;
            st += len(f) + 1;

            # Fixes to convert NE naming inconsistencies
            if tokType[0:3] != "NE_":
                if len(set(tokType).intersection(neTokTypes)) > 0:
                    tokType = "NE_%s" % (tokType);
                if tokType == "N":
                    tokType = "NE_?";

            entry.append([tok, tokType, translit]);
        data.append(entry);
    return data;


def check_seq(pat, token):
    if pat.search(token) != None:
        return 1
    else:
        return 0


def read_freq(filename):
    FH = open(filename)
    words = {}
    data = FH.readlines()
    FH.close()

    for line in data:
        line = line.replace("\n", "")
        word, freq = line.split()
        if int(freq) >= 3:
            words[word] = int(freq)
    return words


def check_in_n(pat, token):
    if pat.search(token) != None:
        return True
    else:
        return False


def check_ends_with_in(pat, token):
    if pat.search(token) != None:
        return True
    else:
        return False


def check_ends_with_n(pat, token):
    if pat.search(token) != None:
        return True
    else:
        return False


def check_ends_with_i(pat, token):
    if pat.search(token) != None:
        return True
    else:
        return False


def check_contains_in(pat, token):
    if pat.search(token) != None:
        return True
    else:
        return False


def check_ends_with_o(pat, token):
    if pat.search(token) != None:
        return True
    else:
        return False


def check_is_punct(pat, token):
    if pat.search(token) != None:
        return True
    else:
        return False


def check_is_smiley(pat, token):
    if pat.search(token) != None:
        return True
    else:
        return False

def check_is_stopword(token):
    stop_word_list = ["a","able","about","across","after","all","almost","also","am","among","an","and","any","are","as","at","be","because","been","but","by","can","cannot","could","dear","did","do","does","either","else","ever","every","for","from","get","got","had","has","have","he","her","hers","him","his","how","however","i","if","in","into","is","it","its","just","least","let","like","likely","may","me","might","most","must","my","neither","no","nor","not","of","off","often","on","only","or","other","our","own","rather","said","say","says","she","should","since","so","some","than","that","the","their","them","then","there","these","they","this","tis","to","too","twas","us","wants","was","we","were","what","when","where","which","while","who","whom","why","will","with","would","yet","you","your","ain't","aren't","can't","could've","couldn't","didn't","doesn't","don't","hasn't","he'd","he'll","he's","how'd","how'll","how's","i'd","i'll","i'm","i've","isn't","it's","might've","mightn't","must've","mustn't","shan't","she'd","she'll","she's","should've","shouldn't","that'll","that's","there's","they'd","they'll","they're","they've","wasn't","we'd","we'll","we're","weren't","what'd","what's","when'd","when'll","when's","where'd","where'll","where's","who'd","who'll","who's","why'd","why'll","why's","won't","would've","wouldn't","you'd","you'll","you're","you've"]
    if token in stop_word_list:
        return True
    else:
        return False

def check_bigram_presense(word_list,token):
    for bigrams in word_list:
        if token == bigrams[0] or token == bigrams[1]:
            ret_val = True
        else:
            ret_val = False
    return ret_val


word_freq = read_freq(sys.argv[5])
p_seq = re.compile(r'(\w)\1{1,}')
p_in = re.compile(r'\w+in$|\w+i$|\w?in\w?|\w?n$|\w+o$')
p_ends_with_in = re.compile(r'\w+in$')
p_ends_with_n = re.compile(r'\w+n$')
p_ends_with_o = re.compile(r'\w+o$')
p_contains_in = re.compile(r'\w+in\w+')
p_ends_with_i = re.compile(r'\w+i$')
p_is_punct = re.compile(r'\W|\D|\?|\.|\"|\'|:|;|!')
p_is_smiley = re.compile(r'^:-?\w+$|^;-?\w+$')
bigram_list_training_corpus = []
bigram_list_brown_corpus = []
bigram_list_nps_chat_corpus = []



def language_features(token):
    #print "ive got token " + token
    features = {}

    func_dict = {'check_seq' :check_seq, 'check_ends_with_in' : check_ends_with_in, 'check_ends_with_n' : check_ends_with_n,
                 'check_ends_with_i' : check_ends_with_i, 'check_ends_with_o' : check_ends_with_o,
                 'check_contains_in' : check_contains_in, 'check_is_smiley' : check_is_smiley, 'check_is_punct' : check_is_punct}

    pat_dict = {'check_seq' : p_seq, 'check_ends_with_in' : p_ends_with_in, 'check_ends_with_n' : p_ends_with_n,
                 'check_ends_with_i' : p_ends_with_i, 'check_ends_with_o' : p_ends_with_o,
                 'check_contains_in' : p_contains_in, 'check_is_smiley' : p_is_smiley, 'check_is_punct' : p_is_punct}

    func_list = ['check_seq', 'check_ends_with_in', 'check_ends_with_n', 'check_ends_with_i','check_ends_with_o',
                 'check_contains_in', 'check_is_smiley', 'check_is_punct']
    count = 1
    for func in func_list:
        # print "func name " + str(func)
        func_name = func_dict[func]
        val = func_name(pat_dict[func],token)
        features[func] = val
    freq = word_freq[token] if token in word_freq else 1
    features['freq'] = freq
    features['check_is_stopword'] = check_is_stopword(token)
    #features['bigram_in_training'] = check_bigram_presense(bigram_list_training_corpus,token)
    features['bigram_in_brown_corpus'] = check_bigram_presense(bigram_list_brown_corpus,token)
    features['bigram_in_nps_chat_corpus'] = check_bigram_presense(bigram_list_nps_chat_corpus,token)
    #features['word_length'] = len(token)
    #print features
    return features


if __name__ == "__main__":

    # Training data sets
    train_featuresets = []
    test_features = []
    all_tokens = []
    u = readAnnotationFile(sys.argv[1])
    u.extend(readAnnotationFile(sys.argv[2]))
    u.extend(readAnnotationFile(sys.argv[3]))

    for line in u:
        all_tokens.extend(token[0].lower() for token in line)

    bigram_measures = nltk.collocations.BigramAssocMeasures()
    finder = BigramCollocationFinder.from_words(all_tokens)
    finder.apply_freq_filter(3)
    bigram_list_training_corpus = finder.nbest(bigram_measures.pmi, 500)

    bigram_measures = nltk.collocations.BigramAssocMeasures()
    finder = BigramCollocationFinder.from_words(nltk.corpus.brown.words())
    finder.apply_freq_filter(3)
    bigram_list_brown_corpus = finder.nbest(bigram_measures.pmi, 500)

    bigram_measures = nltk.collocations.BigramAssocMeasures()
    finder = BigramCollocationFinder.from_words(nltk.corpus.nps_chat.words())
    finder.apply_freq_filter(3)
    bigram_list_nps_chat_corpus = finder.nbest(bigram_measures.pmi, 500)

    print "bigram_list_brown_corpus " + str(bigram_list_brown_corpus[:500])


    for line in u:
        train_featuresets.extend([(language_features(token[0].lower()), token[1]) for token in line])
    #print featuresets

    print "size " + str(len(train_featuresets))

    print train_featuresets[:5]

    # Test data sets
    t = readAnnotationFile(sys.argv[4])
    test_tags = []
    for line in t:
        #print line
        test_features.extend([(language_features(token[0]), 'H') for token in line])
    for line in t:
        test_tags.extend([[token[0], token[1]] for token in line])
    print "size test " + str(len(test_tags))

    classifier = nltk.NaiveBayesClassifier.train(train_featuresets)
    print(nltk.classify.accuracy(classifier, test_features))
    print classifier.show_most_informative_features(15)

    errors = []
    for tok,tag in test_tags:
        guess = classifier.classify(language_features(tok))
        if guess != tag:
            errors.append( (tag, guess, tok) )

    for (tag, guess, tok) in sorted(errors):
        print "guess " + guess.encode('utf-8') + " tok " + tok.encode('utf-8')

    





