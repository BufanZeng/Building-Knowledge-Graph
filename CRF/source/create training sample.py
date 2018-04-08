import string
# import nltk
from sklearn.externals import joblib
clf = joblib.load('postagger.pkl') 

breeds = "Akita, American Staffordshire Terrier, Bull Terrier, Chow, Doberman, German Shepherd, Husky, Pit Bull, Presa Canario, Rottweiler, Wolf Hybrid".translate(None, string.punctuation).split( )
breeds = set(breeds)

def features(sentence, index):
    """ sentence: [w1, w2, ...], index: the index of the word """
    return {
        'word': sentence[index],
        'is_first': index == 0,
        'is_last': index == len(sentence) - 1,
        'is_capitalized': sentence[index][0].upper() == sentence[index][0],
        'is_all_caps': sentence[index].upper() == sentence[index],
        'is_all_lower': sentence[index].lower() == sentence[index],
        'prefix-1': sentence[index][0],
        'prefix-2': sentence[index][:2],
        'prefix-3': sentence[index][:3],
        'suffix-1': sentence[index][-1],
        'suffix-2': sentence[index][-2:],
        'suffix-3': sentence[index][-3:],
        'prev_word': '' if index == 0 else sentence[index - 1],
        'next_word': '' if index == len(sentence) - 1 else sentence[index + 1],
        'has_hyphen': '-' in sentence[index],
        'is_numeric': sentence[index].isdigit(),
        'capitals_inside': sentence[index][1:].lower() != sentence[index][1:]
    }
def pos_tag(sentence):
    tagged_sentence = []
    tags = clf.predict([features(sentence, index) for index in range(len(sentence))])
    return zip(sentence, tags)

with open("/Users/bufan/inf558/HW/Bufan_Zeng_hw4/test_no_tags.txt", "r") as f:
	with open("/Users/bufan/inf558/HW/Bufan_Zeng_hw4/taggedtest.txt", "w") as f1:
		# read and split lines
		txt = f.read().splitlines()
		# print pos_tag(word_tokenize())
		# remove unicode, lowercase, split into list
		l = [s.decode('utf-8').replace(u"\u2022"," ").encode('ascii').split(" ") for s in txt]

		# flatten list
		l = [item for items in l for item in items]
		# remove empty items
		l = filter(None, l)
		# tag the chars
		t = pos_tag(l)
		for i in range(0,len(t)-1):
			w = t[i][0].translate(None, string.punctuation).lower()
			w1 = t[i+1][0].translate(None, string.punctuation).lower()
			if w == "allowed":
				t[i] = list(t[i])
				t[i][1] ='VBD'
			elif w == "welcome" or w == "welcomes":
				t[i] = list(t[i])
				t[i][1] ='VB'
			label = 'IR'
			if t[i][1] == 'CD':
				if w1 == 'deposit':
					label = 'DP'
				elif w1 == 'monthly':
					label = 'MN'
				elif w1 == 'fee':
					label = "FE"
				elif w1 == 'lb':
					label = 'WT'
				elif w1 == 'pet':
					label = 'LM'
  			f1.write(' '.join(str(s).encode('ascii') for s in t[i]) + ' ' + label + '\n')
  		f1.write("\n")
  			

		
		# print l