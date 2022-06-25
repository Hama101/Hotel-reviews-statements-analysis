'''
    in this module we summraize the text than analyze the phrases 
    (this file is not optimal for now !!)
'''

import re
import string
import asyncio
# Load Pkgs
import spacy 
# Text Preprocessing Pkg
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
# Import Heapq 
from heapq import nlargest , nsmallest
#import issues dummy data
from issues import ISSUES_CATEGORIES


# Build a List of Stopwords
stopwords = list(STOP_WORDS)
#load the english model
nlp = spacy.load('en_core_web_sm')

#inital test value
test = """
        Worst hotel ive stayed in. 
- The lock housing was exposed meaning it wasnt difficult to break into our room. 
- No safety deposit boxes in rooms. - Hot water constantly running out.
- No ventilation in bathroom (No window or extractor fan) leaving the bathroom misty after taking a shower and leaving it smelly after using the loo. - Virtually no cooking utensils, making a basic task such as hard boiling an egg extremely difficult. No sponge to clean any dishes. - Beds were extremely uncomfortable, may as well of slept on their sun loungers. - Pillows were solid hurting your neck when you slept. - Room was dust central, dust had settled everywhere and even after us wiping it off with some baby wipes it would re settle. Under the bed was filthy with dirt and dust looked like it had been forgotten about by the cleaner. - Bed sheets were filled with dust when we asked Dimitri (the owner) if we could have them changed he replied "well the cleaner has finished whos going to do it?" - Fridge was dirty and horrible and the bottom of it was rusty. - Staff funny when you leave hotel to eat or drink out.
A little two faced. I could go on but im not going to waste any more time. 
I have honestly never been anywhere and met such rude two faced staff 
    """

#a text cleaner helper fn
def clean_text(text):
    text = text.lower()
    text = re.sub('\[.*?\]', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\w*\d\w*', '', text)
    return text


#this function take issue phrase and category keyword and return the score
def get_score_for_issue_by_category(issue , category_keywords):
    score = 0
    for keyword in list(set(category_keywords)):
        if keyword in issue:
            score += 1
    return score


#this function loops throw category issues and get the most scored catgory for each issue
def get_most_scored_category(issue):
    category_scores = {}
    for category in ISSUES_CATEGORIES:
        score = get_score_for_issue_by_category(issue, ISSUES_CATEGORIES[category])
        category_scores[category] = score if score > 0 else 0
    # return the category with the highest score using max function
    return max(category_scores, key=category_scores.get)


#loop throw the list of issues and for each issue loop throw ISSUES
def identity_issues(list_of_issues):
    issues = {
        category : [] for category in ISSUES_CATEGORIES
    }
    #loop throw the list of issues and get the most scored category for each issue
    for issue in list_of_issues:
        most_scored_category = get_most_scored_category(issue)
        issues[most_scored_category].append(issue)

    return issues


# text preprocessing function
def text_summarizer(raw_docx = test):
    raw_text = raw_docx
    docx = nlp(raw_text)
    stopwords = list(STOP_WORDS)
    # Build Word Frequency
    # word.text is tokenization in spacy
    word_frequencies = {}  
    for word in docx:  
        if word.text not in stopwords:
            if word.text not in word_frequencies.keys():
                word_frequencies[word.text] = 1
            else:
                word_frequencies[word.text] += 1

    maximum_frequncy = max(word_frequencies.values())

    for word in word_frequencies.keys():  
        word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)
    # Sentence Tokens
    sentence_list = [ sentence for sentence in docx.sents ]

    # Calculate Sentence Score and Ranking
    sentence_scores = {}  
    for sent in sentence_list:  
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                if len(sent.text.split(' ')) < 30:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word.text.lower()]
                    else:
                        sentence_scores[sent] += word_frequencies[word.text.lower()]

    # Find N Largest
    summary_sentences = nlargest(10, sentence_scores, key=sentence_scores.get)
    final_sentences = [ w.text for w in summary_sentences ]
    summary = ' '.join(final_sentences)
    
    #clear summary to have one space between sentences and words and \n
    summary = summary.replace('\n', ' ')
    summary = summary.replace('\r', ' ')
    summary_list = summary.split(' ')
    summary_list = [x for x in summary_list if x != '' and x != ' ']
    summary = ' '.join(summary_list)

    #split list of sentences to list of words with . or , or ? or ! or : or ;
    punctuation = ['.' , ',' , '?' , '!' , ':' , ';']
    list_of_issues = []
    for char in summary:
        if char in punctuation:
            list_of_issues.append(summary[:summary.index(char)])
            summary = summary[summary.index(char)+1:]

    list_of_issues = [clean_text(x) for x in list_of_issues if x != '' and len(x.split(' ')) > 2]

    obj = {
        "length": len(summary),
        "list_of_issues": list_of_issues,
        "list_of_issues_for_each_category": identity_issues(list_of_issues)
    }
    return obj


if __name__=="__main__":
    print(text_summarizer())