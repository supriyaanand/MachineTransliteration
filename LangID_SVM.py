import sys
import re;


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
    FH = open(sys.argv[2])
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
        return 1
    else:
        return 0


def check_ends_with_in(pat, token):
    if pat.search(token) != None:
        return 1
    else:
        return 0


def check_ends_with_n(pat, token):
    if pat.search(token) != None:
        return 1
    else:
        return 0


def check_ends_with_i(pat, token):
    if pat.search(token) != None:
        return 1
    else:
        return 0


def check_contains_in(pat, token):
    if pat.search(token) != None:
        return 1
    else:
        return 0


def check_ends_with_o(pat, token):
    if pat.search(token) != None:
        return 1
    else:
        return 0


def check_is_punct(pat, token):
    if pat.search(token) != None:
        return 1
    else:
        return 0


def check_is_smiley(pat, token):
    if pat.search(token) != None:
        return 1
    else:
        return 0


if __name__ == "__main__":

    FH = open("op.txt", 'a')
    datastr = ""
    u = readAnnotationFile(sys.argv[1])
    #print u
    word_freq = read_freq(sys.argv[2])
    p_seq = re.compile(r'(\w)\1{1,}')
    p_in = re.compile(r'\w+in$|\w+i$|\w?in\w?|\w?n$|\w+o$')
    p_ends_with_in = re.compile(r'\w+in$')
    p_ends_with_n = re.compile(r'\w+n$')
    p_ends_with_o = re.compile(r'\w+o$')
    p_contains_in = re.compile(r'\w+in\w+')
    p_ends_with_i = re.compile(r'\w+i$')
    p_is_punct = re.compile(r'\W|\D|\?|\.|\"|\'|:|;|!')
    p_is_smiley = re.compile(r'^:-?\w+$')
    func_dict = {check_seq: p_seq, check_ends_with_in: p_ends_with_in, check_ends_with_n: p_ends_with_n,
                 check_ends_with_i: p_ends_with_i, check_ends_with_o: p_ends_with_o,
                 check_contains_in: p_contains_in, check_is_smiley: p_is_smiley, check_is_punct: p_is_punct}
    func_list = [check_seq, check_ends_with_in, check_ends_with_n, check_ends_with_i, check_ends_with_o,
                 check_contains_in, check_is_smiley, check_is_punct]
    datastr = ''
    for line in u[600:]:
        for token in line:
            count = 1
            if token[1] == 'H':
                datastr = datastr + str(1) + " "
            else:
                datastr = datastr + str(-1) + ' '
            for func in func_list:
                print "func name " + str(func)
                val = func(func_dict[func], token[0])
                datastr = datastr + str(count) + ':' + str(val) + ' '
                count += 1
            freq = word_freq[token[0]] if token[0] in word_freq else 1
            # freq = 1
            datastr = datastr + str(count) + ':' + str(freq) + " #" + token[0] + "\n"
            print datastr

    FH.write(datastr.encode('utf-8'))
    FH.close()

