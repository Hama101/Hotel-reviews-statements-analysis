'''
    this file analyzes the text and returns the summary of the text with the details of the text
'''

from summarizer import text_summarizer
import re 
import string
#import issues dummy data
from issues import ISSUES_CATEGORIES , NEGATION_ATTRUIBUITES , NEGATION_WORDS

s = """
The environment of the hotel was really cool. But when talking
about the hotel in our room the table lamp was broken. The room is
quite smelly as well and room-boys service was terrible. And there
was only cold water in bathroom. There was also no enough space
in luggage to keep our belongings. The price is a bit high when
compared to other hotels in the area. But the Swimming pool is
pretty large and I really like that. Huge parking space is also
available which is really good. There were two issues which
surprised me that could work to make the hotel perfect. One is that
WIFI connection was weak sometimes. And the other is the food as
its not tasty bad food. I don’t expect to come back unless y’all
correct this things which I experienced during my stay.
"""

#*a text cleaner helper fn
def clean_text(text):
    text = text.lower()
    text = re.sub('\[.*?\]', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\w*\d\w*', '', text)
    text = text.replace('\n', '')
    text = text.replace('\t', '')
    text = text.replace('\r', '')
    return text

#*split list of sentences to list of words with . or , or ? or ! or : or ;
def split_sentences(text):
    # text to lowwer
    text = text.lower()
    punctuation = ['.'  , '?' , '!' ]
    statements = []
    for char in text:
        if char in punctuation:
            statements.append(text[:text.index(char)])
            text = text[text.index(char)+1:]

    return statements if len(statements) > 0 else [text]

#*flatten list of lists
def flatten_list(list_of_lists):
    return [item for sublist in list_of_lists for item in sublist]

#*this function take issue phrase and category keyword and return the score
def get_score_for_issue_by_category(issue , category_keywords):
    score = 0
    words_founded = []
    for keyword in list(set(category_keywords)):
        if keyword in issue:
            # print(f"{keyword} founded in {issue}")
            score += 1
            words_founded.append(keyword)

    return score , words_founded

#*this function loops throw category issues and get the most scored catgory for each issue
def get_most_scored_category(issue):
    category_scores = {}
    for category in ISSUES_CATEGORIES:
        score , words_founded = get_score_for_issue_by_category(issue, ISSUES_CATEGORIES[category])
        category_scores[category] = score
    
    # return the category with the highest score using max function
    category = max(category_scores, key=category_scores.get)
    return  category , category_scores[category] , words_founded

#*loop throw the list of issues and for each issue loop throw ISSUES
def identity_issues(list_of_issues):
    issues = {
        category : [] for category in ISSUES_CATEGORIES
    }
    #loop throw the list of issues and get the most scored category for each issue
    for issue in list_of_issues:
        values = flatten_list(list(issues.values()))
        if issue not in values:
            most_scored_category , score , words_founded = get_most_scored_category(issue)
            # print(f"{issue} ---> {most_scored_category} with score {score} and words founded {words_founded}")
            #che
            if score > 0 :
                issues[most_scored_category].append(issue)
            else :
                issues["other"].append(issue)

    return issues

# * this function takes a text and the loaded model and return if the passed text happy or not!
def analyse_text(text = s , model = None):

    text = split_sentences(text)
    result = list(model.predict(text))
    print("i m here")
    not_happy_occ = 0
    happy_occ = 0
    list_of_positive_statements = []
    list_of_negative_statements = []
    #loop throw the list of results and check if the result is happy or not
    for i in range(len(result)):
        #check if the result[i] is happy
        if result[i] == "happy":
            is_trully_happy = True
            #loop NEGATION_WORDS and check if the word is in the text[i]
            for word in NEGATION_WORDS:
                if word in text[i]:
                    not_happy_occ += 1
                    list_of_negative_statements.append(clean_text(text[i]))
                    is_trully_happy = False
                    break
            #loop NEGATION_ATTRUIBUITES and check if the word is in the text[i]
            for word in NEGATION_ATTRUIBUITES:
                if word in text[i]:
                    not_happy_occ += 1
                    list_of_negative_statements.append(clean_text(text[i]))
                    is_trully_happy = False
                    break
            #if the result[i] is happy and is_trully_happy is True
            if is_trully_happy:
                list_of_positive_statements.append(clean_text(text[i]))
                happy_occ += 1
        else:
            not_happy_occ += 1
            list_of_negative_statements.append(clean_text(text[i]))

    # print(text)
    print(len(list_of_positive_statements))
    print(len(list_of_negative_statements))

    is_happy = True if happy_occ > not_happy_occ else False
    if is_happy:
        return {
            "is_happy" : is_happy,
        }

    return {
        "is_happy" : is_happy,
        "list_of_positive_statements" : list(set(list_of_positive_statements)),
        "list_of_negative_statements" : list(set(list_of_negative_statements)),
        "list_of_negative_statements_by_category" : identity_issues(list(set(list_of_negative_statements))),
        }


def analyse(text = s , model= None):
    #run the variables checks
    if not model :
        return "Error Model not loded!"
    
    if not text :
        return "Empty text"
    
    #run the is happy fn and the summarizer
    return analyse_text(text , model)