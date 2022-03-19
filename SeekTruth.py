# SeekTruth.py : Classify text objects into two categories
#
# Yash Pratap Solanky - ysolanky
#
# Based on skeleton code by D. Crandall, October 2021
#

import sys
import math


def load_file(filename):
    objects = []
    labels = []
    with open(filename, "r") as f:
        for line in f:
            parsed = line.strip().split(' ', 1)
            labels.append(parsed[0] if len(parsed) > 0 else "")
            objects.append(parsed[1] if len(parsed) > 1 else "")

    return {"objects": objects, "labels": labels, "classes": list(set(labels))}


# classifier : Train and apply a bayes net classifier
#
# This function should take a train_data dictionary that has three entries:
#        train_data["objects"] is a list of strings corresponding to reviews
#        train_data["labels"] is a list of strings corresponding to ground truth labels for each review
#        train_data["classes"] is the list of possible class names (always two)
#
# and a test_data dictionary that has objects and classes entries in the same format as above. It
# should return a list of the same length as test_data["objects"], where the i-th element of the result
# list is the estimated classlabel for test_data["objects"][i]
#
# Do not change the return type or parameters of this function!
#
def classifier(train_data, test_data):
    # This is just dummy code -- put yours here!

    deceptive = []
    truthful = []

    d_tokens = []
    t_tokens = []

    countd = 0
    countt = 0

    # The following list of stopwords was taken by importing nltk and running the command nltk.corpus.stopwords.words('english').
    # Checking for stop words increased the accuracy of my model by 1.25% and reduced runtime
    stop = ['.', 'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll",
            "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her',
            'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what',
            'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be',
            'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and',
            'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against',
            'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down',
            'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when',
            'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no',
            'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don',
            "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't",
            'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven',
            "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan',
            "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn',
            "wouldn't"]

    for i, j in enumerate(train_data["objects"]):

        # Creating 2 lists based on the label
        if train_data["labels"][i] == "deceptive":
            deceptive.append(j)
            countd += 1
        elif train_data["labels"][i] == "truthful":
            truthful.append(j)
            countt += 1

    # Creating lists with single words rather than list of lists with separate reviews
    for word in deceptive:
        d_tokens.extend(word.split())

    for word in truthful:
        t_tokens.extend(word.split())

    # Code to perform strip in place was taken from https://stackoverflow.com/questions/46769063/python-strip-doesnt-work-in-for-in
    for i in range(0, len(d_tokens)):
        # End of code taken from stack overflow
        # Performing data cleaning on the words inside our bag of words
        word = d_tokens[i]
        word = word.lower()
        word = word.strip()
        word = word.strip(" ")
        word = word.strip("$")
        word = word.strip("!")
        word = word.strip(",")
        word = word.strip(".")
        word = word.strip("?")
        word = word.strip("...")
        word = word.strip(")")
        word = word.strip("(")
        word = word.strip("'")
        word = word.strip("*")
        word = word.strip(";")
        d_tokens[i] = word

    # Code to perform strip in place was taken from https://stackoverflow.com/questions/46769063/python-strip-doesnt-work-in-for-in
    for i in range(0, len(t_tokens)):
        # End of code taken from stack overflow
        # Performing data cleaning on the words inside our bag of words
        word = t_tokens[i]
        word = word.lower()
        word = word.strip()
        word = word.strip(" ")
        word = word.strip("$")
        word = word.strip("!")
        word = word.strip(",")
        word = word.strip(".")
        word = word.strip("?")
        word = word.strip("...")
        word = word.strip(")")
        word = word.strip("(")
        word = word.strip("'")
        word = word.strip("*")
        word = word.strip(";")
        t_tokens[i] = word

    result = []

    for i in test_data["objects"]:
        # Looping through the reviews in test set

        i = i.split()

        p_a = math.log(countd / len(train_data["labels"]))
        p_b = math.log(countt / len(train_data["labels"]))

        for j in i:
            # Looping through the words in each review and cleaning them
            j = j.lower()
            j = j.strip()
            j = j.strip(" ")
            j = j.strip("$")
            j = j.strip("!")
            j = j.strip(",")
            j = j.strip(".")
            j = j.strip("?")
            j = j.strip("...")
            j = j.strip(")")
            j = j.strip("(")
            j = j.strip("'")
            j = j.strip("*")
            j = j.strip(";")

            count_d = 0
            count_t = 0

            if j in stop or j.isnumeric() is True:
                # We are not calculating the count or the likelihood for stop words or numbers
                continue
            else:
                # Following method to count occurence was taken from stack overflow
                # https://stackoverflow.com/questions/2600191/how-can-i-count-the-occurrences-of-a-list-item
                # It helped me to cut down on running time
                count_d = d_tokens.count(j)
                count_t = t_tokens.count(j)
                # End of code from stack overflow

                # for k in d_tokens:
                #     if j == k:
                #         count_d += 1
                # for k in t_tokens:
                #     if j == k:
                #         count_t += 1

            # To avoid log(0) calculation, I added one to both counts of labels A and B. This helps avoid math domain
            # error in the cases when either of the count is equal to 0. Now the count is at least 1,
            # even for the words that are in test set but not in train set.
            count_d += 1
            count_t += 1

            # Likelihood is calculated by dividing the number of times a word appears in the training set by the number
            # of the different words in the respective label
            likelihood_d = count_d / len(d_tokens)
            likelihood_t = count_t / len(t_tokens)

            # We are looping over the likelihoods of all the words in a single review and adding them to the prior +
            # the likelihood of previous words.
            p_a = p_a + math.log(likelihood_d)
            p_b = p_b + math.log(likelihood_t)

        if p_a > p_b:
            result.append("deceptive")
        else:
            result.append("truthful")

    return result


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise Exception("Usage: classify.py train_file.txt test_file.txt")

    (_, train_file, test_file) = sys.argv
    # Load in the training and test datasets. The file format is simple: one object
    # per line, the first word one the line is the label.
    train_data = load_file(train_file)
    test_data = load_file(test_file)
    if (sorted(train_data["classes"]) != sorted(test_data["classes"]) or len(test_data["classes"]) != 2):
        raise Exception("Number of classes should be 2, and must be the same in test and training data")

    # make a copy of the test data without the correct labels, so the classifier can't cheat!
    test_data_sanitized = {"objects": test_data["objects"], "classes": test_data["classes"]}

    results = classifier(train_data, test_data_sanitized)

    # calculate accuracy
    correct_ct = sum([(results[i] == test_data["labels"][i]) for i in range(0, len(test_data["labels"]))])
    print("Classification accuracy = %5.2f%%" % (100.0 * correct_ct / len(test_data["labels"])))
