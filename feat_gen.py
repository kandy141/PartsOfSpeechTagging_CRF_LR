#!/bin/python
import feats
def preprocess_corpus(train_sents):
    """Use the sentences to do whatever preprocessing you think is suitable,
    such as counts, keeping track of rare features/words to remove, matches to lexicons,
    loading files, and so on. Avoid doing any of this in token2features, since
    that will be called on every token of every sentence.

    Of course, this is an optional function.

    Note that you can also call token2features here to aggregate feature counts, etc.
    """
    
    #Checking with removing duplicates in words. Ex: yaaaaaaaaaaaay -> yay   | drawbacks are: books->boks
    # import itertools
    # def remove_adj_dupes(s):
    #     return ''.join(i for i, _ in itertools.groupby(s))
    # for i in range(len(train_sents)):
    #     train_sents[i] = [remove_adj_dupes(x) for x in train_sents[i]]


    #Checking by doing spell correct for each word
    # from autocorrect import spell
    # for i in range(len(train_sents)):
    #     train_sents[i] = [spell(x) for x in train_sents[i]]    
    #     print (train_sents[i])
    #**************BAD CHOICE
    # Token-wise accuracy 72.09082308420058
    # Token-wise F1 (macro) 71.83677488712381
    # Token-wise F1 (micro) 72.09082308420058
    # Sentence-wise accuracy 3.571428571428571

    #USELESS
    # mhash = {'yaaaayyy': 'yay', 'Weeeeee': 'we', 'goosh':'gosh', 'Wkwkwk':'wk', 'Sighhhhh':'Sigh', 'longggggg':'long', '!!':'!', "'ll":"'l", '!!!!':'!', 'xHahaa':'haha', '???':'?', '...':'.', '!...':'!', 'awwwwwwww':'aw'}
    # for i in range(len(train_sents)):
    #     for j in range(len(train_sents[i])):
    #         if train_sents[i][j] in mhash:
    #             print ('****************CHANGED', train_sents[i][j], mhash[train_sents[i][j]])
    #             train_sents[i][j] = mhash[train_sents[i][j]]


    # hash_counts = [0]*len(train_sents)
    # for i in range(len(train_sents)):
    #     hash_count = 0
    #     for j in range(len(train_sents[i])):
    #         if train_sents[i][j].startswith(('#', '$', '@'))
    #             hash_count += 1
    #     hash_counts[i] = hash_count
    # return hash_counts


    #1000 clusters
    # clusterIDs = []
    # clusterWords = []
    # with open('clusterIDs.txt') as f:
    #     lines = f.readlines()
    #     for line in lines:
    #         clusterIDs.append([x.strip() for x in line.split(' ')])

    # with open('clusterWords.txt') as f:
    #     lines = f.readlines()
    #     for line in lines:
    #         clusterWords.append([x.strip() for x in line.split(' ')])    

    
    # for i in range(len(clusterWords)):
    #     for j in range(len(clusterWords[i])):
    #         if clusterWords[i][j] not in feats.clusterHash:
    #             feats.clusterHash[clusterWords[i][j]] = [clusterIDs[i]]
    #         else:
    #             feats.clusterHash[clusterWords[i][j]].append(clusterIDs[i])


    ##750kpaths.txt / 6mpaths.txt
    with open('6mpaths.txt') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            sp=' '
            if '    ' in line:
                sp = '    '
            if '\t' in line:
                sp = '\t'
            split = line.split(sp)
            feats.clusterHash[split[1].strip()] = split[0]
            
    pass

def token2features(sent, i, add_neighs = True):
    """Compute the features of a token.

    All the features are boolean, i.e. they appear or they do not. For the token,
    you have to return a set of strings that represent the features that *fire*
    for the token. See the code below.

    The token is at position i, and the rest of the sentence is provided as well.
    Try to make this efficient, since it is called on every token.

    One thing to note is that it is only called once per token, i.e. we do not call
    this function in the inner loops of training. So if your training is slow, it's
    not because of how long it's taking to run this code. That said, if your number
    of features is quite large, that will cause slowdowns for sure.

    add_neighs is a parameter that allows us to use this function itself in order to
    recursively add the same features, as computed for the neighbors. Of course, we do
    not want to recurse on the neighbors again, and then it is set to False (see code).
    """
    ftrs = []
    # bias
    ftrs.append("BIAS")
    # position features
    if i == 0:
        ftrs.append("SENT_BEGIN")
    if i == len(sent)-1:
        ftrs.append("SENT_END")

    # the word itself
    word = unicode(sent[i])
    ftrs.append("WORD=" + word)
    ftrs.append("LCASE=" + word.lower())
    # some features of the word
    if word.isalnum():
        ftrs.append("IS_ALNUM")
    if word.isnumeric():
        ftrs.append("IS_NUMERIC")
    if word.isdigit():
        ftrs.append("IS_DIGIT")
    if word.isupper():
        ftrs.append("IS_UPPER")
    if word.islower():
        ftrs.append("IS_LOWER")


    
    #my features
    common_feature = 'IS_TWEETLANGUAGE'
    
    #Useless
    # if word.istitle():
    #     ftrs.append('IS_TITLE')

    #is_hashtag / username
    if word.startswith(('#', '$', '@', '*', '%')):
        #ftrs.append('IS_HASHTAG')
        ftrs.append(common_feature)

    #is_emoji
    common_emojis = [':)', ':-)', ':]', ':-]', ';)', ';-)', ':d', ':-d', ';p', ';-p', ';p', ';-p', ':p', ':-p', ':p', ':-p', '8)', '8-)', ':|', ':-|', ':(', ':-(', 
                     'o_o', 'o.o', 'o_o', 'o.o', ':/', ':-/', ':o', ':-o', ':o', ':-o', 'o_o', 'o.o', 'o_o', 'o.o', '#)', '#-)', '^.^', '^_^', '^^', ':x', ':-x', '<3', '#(', '#-(', '', 'm)', 'm-)', 'xd', 'xd', ":'(", ":'-(", '=)', '=]', '=d', '=p', '=p', '=/', '=o', "='(", '\\o/', ":')", ":'-)", '>:(', '>:-(', '>=(', 'xoxo']
    if word.lower() in common_emojis:
        #ftrs.append('IS_EMOJI')
        ftrs.append(common_feature)

    #is_internet_slang
    common_internetslangs = ['afaic', 'afaik', 'haha', 'hahaha', 'biotch', 'urgh', 'fuck', 'oh', 'afair', 'afk', 'asap', 'bbl', 'bbs', 'bfd', 'brb', 'btw', 'b2b', 
                             'c&v', 'c|n>k', 'cya', 'cu', 'cys', 'faq', 'ffs', 'foaf', 'fyi', 'g2g', 'gagf', 'gfy', 'gg', 'gj', 'hand', 'hth', 'ianal', 'ianars', 
                             'ic', 'icydk', 'icydn', 'icudk', 'iirc', 'ik', 'imho', 'imo', 'imnsho', 'irc', 'irl', 'istr', 'iydmma', 'jj', 'jk', 'joo', 'jooc', 'k', 
                             'l8', 'l8r', 'liek', 'lmao', 'lol', 'myob', 'nm', 'noyb', 'np', 'nsfw', 'nt', 'o', 'oic', 'omg', 'omfg', 'omfl', 'ooc', 'ot', 'otoh', 
                             'own', 'pfo', 'pita', 'po', "po'd", 'prog', 'prolly', 'plz', 'pwn', 'p2p', 'qoolz', 'r', 'rl', 'rofl', 'rotfl', 'roflmao', 'rotflmao', 
                             'r0x0rz', 'rtfa', 'rtfm', 'ru', 'r8', 'sfw', 'stfu', 'sux0rs', 'tbh', 'thx', 'ttfn', 'tia', 'ttyl', 'u', 'ur', 'w/e', 'w/o', 'wduwta', 
                             'wtf', 'ymmv', 'w00t', 'w8', 'x > *', '<3', '2b', '4']
    if word.lower() in common_internetslangs:
        #ftrs.append('IS_INTERNETSLANG')
        ftrs.append(common_feature)

    #is_URL
    if word.lower().startswith(('https://', 'http://', 'www.')) or word.lower().endswith(('.com')):
        #ftrs.append('IS_URL')
        ftrs.append(common_feature)

    punc_list = ['!', '.', '-', ',', '.', '/', ':', '"', "'", '?', '>', '<', ';', ']', '[', '}', '{', ')', '(', '@', '#', '$', '%', '^', '&', '*', '_','+']
    if word.strip() in punc_list:
        #ftrs.append('IS_PUNCTUATION')
        ftrs.append(common_feature)

    # if word.strip().startswith(('(','[','{')): 
    #     ftrs.append('IS_STARTBRACE')

    # if word.strip().endswith((')','}',']')):
    #     ftrs.append('IS_ENDBRACE')

    def camel(s):
        return s != s.lower() and s != s.upper() and "_" not in s
    if camel(word):
        ftrs.append('IS_CAMELCASE')

    # #Including 1000 clusters
    # if word.strip() in feats.clusterHash:
    #     temp = [' '.join(x) for x in feats.clusterHash[word.strip()]]
    #     ftrs.extend(temp)



    #750k.txt / 6mpaths.txt clusters
    if word.strip() in feats.clusterHash:
        ftrs.append('CLUSTER_' + feats.clusterHash[word])


    #Including suffixes
    NOUN = set(['acy', 'cy', 'ade', 'ad', 'age', 'al', 'ial', 'an', 'ian', 'ate', 'dom', 'en', 'et', 'ette', 'let', 'hood', 'ice', 'ic', 'tic', 'ics',
                'ine', 'in', 'ing', 'ism', 'ist', 'ive', 'ment', 'ness', 'ship', 'th', 'tude', 'ure', 'ance', 'ence', 'ancy', 'ency', 'ant', 'ent', 
                'ary', 'ery', 'ry', 'ory', 'er', 'or', 'ar', 'eer', 'ier', 'ee', 'ess', 'ion', 'ity'])
    ADJ = set(['able', 'ible', 'al', 'ial', 'an', 'ian', 'ant', 'ent', 'ary', 'ory', 'ar', 'ate', 'ful', 'ic', 'ical', 'istic', 'istical', 'ish', 'ive', 
            'less', 'ly', 'eous', 'ious', 'uous', 'ing', 'ed', 'y', 'en', 'er', 'or', 'ern', 'ese', 'id', 'ile', 'ine', 'ist', 'ite', 'like', 'some', 'th', 'eth', 'ward'])
    VERB = set(['ate', 'en', 'ify', 'efy', 'ish', 'ize', 'ise', 'er'])
    ADV = set(['ly', 'ward', 'wards', 'ways', 'wise', 'ely', 'ilely', 'lily', 'ply', 'bly', 'tly', 'dly', 'ably', 'ibly', 'ally', 'ially', 'antly', 'ently', 'arily',
                'arly', 'orily', 'ately', 'fully', 'icly', 'ically', 'isticly', 'istically', 'ingly', 'edly', 'ishly', 'ively', 'lessly', 'ously', 'eously', 'iously', 'uously', 'ily'])

    temp = word.lower().strip()
    for val in NOUN:
        if temp.endswith(val):
            ftrs.append('NOUN_'+val)
    for val in ADJ:
        if temp.endswith(val):
            ftrs.append('ADJ_'+val)
    for val in VERB:
        if temp.endswith(val):
            ftrs.append('VERB_'+val)
    for val in ADV:
        if temp.endswith(val):
            ftrs.append('ADV_'+val)
    

    # previous/next word feats
    if add_neighs:
        if i > 0:
            for pf in token2features(sent, i-1, add_neighs = False):
                ftrs.append("PREV_" + pf)
        if i < len(sent)-1:
            for pf in token2features(sent, i+1, add_neighs = False):
                ftrs.append("NEXT_" + pf)
    # return it!
    return ftrs

if __name__ == "__main__":
    sents = [
    [ "I", "love", "food", "lol", "LOL", ":)"]
    ]
    preprocess_corpus(sents)
    for sent in sents:
        for i in xrange(len(sent)):
            print sent[i], ":", token2features(sent, i)

    '''f = open('emojis_list.txt')
    ls = f.readlines()
    out = []
    for l in ls:
        out.append(l.strip().lower())
    print out
    '''