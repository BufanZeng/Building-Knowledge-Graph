source.py		use xpath to extract the pet policy text from webpages
trainpostag.py	refered 'http://nlpforhackers.io/training-pos-tagger/' train pos_tagger using decision tree
postagger.pkl	predictive model for postagger
create training sample.py 	tag and label the words
chunking.py & crfutils.py 	set features for crfsuite training





# command used in command line
cd ~/inf558/HW/Bufan_Zeng_hw4
gzip tmp.txt
gunzip -c tmp.txt.gz | ./chunking.py > tmp1.txt

install crfsuite on mac
https://stackoverflow.com/questions/25838517/how-to-get-crfsuite-to-work-on-mac-os-x

brew tap brewsci/science
brew install crfsuite
