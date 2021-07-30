import html
import time
from datetime import datetime
import sys
import re
import requests

""" # This file will serve as the word of the day grab, and that will be its job. """


class WordOfTheDay:
    word, url = "", ""
    part_of_speech, definitions, examples, source_texts, source_links, date = [], [], [], [], [], []

    def initialize(self, word, part_of_speech, definitions, examples, source_texts, source_links, url, date):
        self.word = word
        self.part_of_speech = part_of_speech
        self.definitions = definitions
        self.examples = examples
        self.source_texts = source_texts
        self.source_links = source_links
        self.url = url
        self.date = date
        return self

    def __iter__(self):
        return iter((self.word, self.part_of_speech, self.definitions,
                     self.examples, self.source_texts, self.source_links, self.url, self.date))


# This function parses the request text of the page and will return the 'Word' part of the word of the day.
# No errors here.
def grab_word(request_text):
    try:
        match = re.search(r"<div class=\"content_column\">[\s]*<h1><a href=[^>]*>[^<]*<", request_text).group(0)
        word = match.split(">")[3].split("<")[0]
        return word
    except:
        print("WOTD: Error", sys.exc_info()[0], "\n")


# This function will grab all the definitions and parts of speech from the word of the day.
# No errors here.
def grab_definitions(request_text):
    try:
        match = re.findall(r"(<li><abbr title=\"partOfSpeech\">[\w\s].*</abbr>.*</li>)", request_text)

        definitions, part_of_speech = [], []
        for raw_ in match:
            raw = str(raw_).split("partOfSpeech\">")[1].split("</li>")[0].split("</abbr> ")
            part_of_speech.append(raw[0])
            definitions.append(raw[1])
        return part_of_speech, definitions
    except:
        print("WOTD: Error", sys.exc_info()[0], "\n")


# This function parses the request text of the page and will return the examples of the word of the day.
# No errors here.
def grab_examples(request_text):
    try:
        match = re.findall(r"<li class=\"exampleItem\">\s*<p class=\"text\">.*\s*.*\s*</li>",
                           request_text)
        examples, source_text, source_link = [], [], []
        for raw_ in match:
            text = re.search(r"<p class=\"text\">.*<", raw_).group(0).split("<")[1].split("p class=\"text\">")[1]
            source = re.search(r"<p class=\"source\">.*<", raw_).group(0).split("href=\"")[1].split("</a><")[0].split(
                "\" target=\"_blank\">")
            examples.append(text)
            source_link.append(source[0])
            source_text.append(source[1])
        return examples, source_text, source_link
    except:
        print("WOTD: Error", sys.exc_info()[0], "\n")


# This grabs the word of the day from Merriam Webster's Word Of The Day using the helper functions and returns an
# object containing all the information we need to make a message.
# Note: We include the sleep to make sure we can reach the status_code and text of the request...
# ... Weird issue arise otherwise.
# For errors: 200 = Bad request, 201 = No 'Word' found, 202 = No 'Definitions/Parts of Speech' found
def word_of_the_day(date):
    url = "https://www.wordnik.com/word-of-the-day/"
    if date:
        url += str(date[0]) + "/" + str(date[1]) + "/" + str(date[2])

    request = requests.get(url)
    time.sleep(0.2)

    if request.status_code != 200:
        print("WOTD: Did not receive 200 response from request.\n")
        return 200

    word = grab_word(request.text)
    if not word:
        print("WOTD: Did not find the 'Word' section of Word Of The Day.\n")
        return 201

    part_of_speech, definitions = grab_definitions(request.text)
    if len(part_of_speech) == 0 | len(definitions) == 0:
        print("WOTD: Did not find the 'Definition' and 'Part Of Speech' section/s of Word Of The Day")
        return 202

    examples, source_texts, source_links = grab_examples(request.text)
    if len(examples) == 0 | len(source_links) == 0 | len(source_texts) == 0:
        print("WOTD: Did not find 'Examples' and 'Sources' section/s of Word Of The Day\n"
              "*Note that it is possible to not find any Examples for some words.*")
        return WordOfTheDay().initialize(word, part_of_speech, definitions, examples, source_texts, source_links, url,
                                         date)

    return WordOfTheDay().initialize(word, part_of_speech, definitions, examples, source_texts, source_links, url, date)


# Here we can make our string from our object and return the str/list of str we want to send to each channel..
# Return None if we somehow receive an error.
def handle_and_send(word_of_the_day_Obj):
    word, part_of_speech, definitions, examples, source_texts, source_links, url, date = word_of_the_day_Obj

    defs, part_of_speeches = [], []

    if date:
        str_build = (
            "__Word of the Day,{0}/{1}__\n".format(date[1], date[2]))
    else:
        str_build = (
            "__Word of the Day,{0}/{1}__\n".format(datetime.now().strftime("%m"), datetime.now().strftime("%d")))

    str_build += ("`{0}`\n\n".format(word))
    str_build += "__**Definitions**__\n"
    # Safe to assume we will have as many definitions as parts of speech and vice versa.
    for definition in definitions:
        defs.append(definition)
    for pos in part_of_speech:
        part_of_speeches.append(pos)

    for i in range(len(definitions)):
        str_build += ("**->Definition {0}**\n> (__**{1}**__) : {2}\n\n".format(i + 1, part_of_speeches[i], defs[i]))

    if examples:
        if len(examples) > 5:
            examples = examples[0:5]
            source_texts = source_texts[0:5]
            source_links = source_links[0:5]
        exs, src_texts, src_links = [], [], []

        for example in examples:
            exs.append(example)
        for source_text in source_texts:
            src_texts.append(source_text)
        for source_link in source_links:
            src_links.append(source_link)

        str_build += "__**Examples**__\n"

        for i in range(len(examples)):
            str_build += ("**->Example {0}**\n```\n{1}\n```**Source** : *{2}*\n**Link** : `'{3}'`\n\n"
                          .format(i + 1, exs[i], src_texts[i], src_links[i]))

    str_build += (
        "> __**Word of the Day Webpage Link**__\n> __*{0}*__\n> __**Courtesty of Wordnik.com**__\n".format(url))
    str_build = html.unescape(str_build)

    # If we get a long message, lets split it and separate the message.
    if len(str_build) <= 2000:
        return str_build
    elif (len(str_build) <= 4000) and (len(str_build) > 2000):
        return handle_long_message(str_build, url)
    else:
        return None


# This function will try various methods in order to most efficiently split our string into two messages.
# Note: Deprecated now that we check for the count of examples and limit them to 5. But comes in handy sometimes.
# Return None if it cannot return a split list containing two messages
def handle_long_message(str_builder, url):
    method = 1
    while True:
        if method == 1:
            split = str_builder.split("**->Example 1")
            if (len(split[0]) <= 2000) and (len(split[1]) <= 1987):
                split[1] = "**->Example 1{0}".format(split[1])
                return split
            method += 1
        elif method == 2:
            split = str_builder.split("**->Definition 1")
            if (len(split[0]) <= 2000) and (len(split[1]) <= 1984):
                split[1] = "**->Definition 1{0}".format(split[1])
                return split
            method += 1
        elif method == 3:
            split = str_builder.split("**->Example 2")
            if (len(split[0]) <= 2000) and (len(split[1]) <= 1987):
                split[1] = "**->Example 2{0}".format(split[1])
                return split
            method += 1
        elif method == 4:
            split = str_builder.split("**->Definition 2")
            if (len(split[0]) <= 2000) and (len(split[1]) <= 1984):
                split[1] = "**->Definition 2{0}".format(split[1])
                return split
            method += 1
        elif method == 5:
            split = str_builder.split("**->Example 3")
            if (len(split[0]) <= 2000) and (len(split[1]) <= 1987):
                split[1] = "**->Example 3{0}".format(split[1])
                return split
            method += 1
        elif method == 6:
            split = str_builder.split("**->Definition 3")
            if (len(split[0]) <= 2000) and (len(split[1]) <= 1984):
                split[1] = "**->Definition 3{0}".format(split[1])
                return split
            method += 1
        elif method == 7:
            split = str_builder.split("**->Example 4")
            if (len(split[0]) <= 2000) and (len(split[1]) <= 1987):
                split[1] = "**->Example 4{0}".format(split[1])
                return split
            method += 1
        elif method == 8:
            split = str_builder.split("**->Definition 4")
            if (len(split[0]) <= 2000) and (len(split[1]) <= 1984):
                split[1] = "**->Definition 4{0}".format(split[1])
                return split
            method += 1
        elif method == 9:
            split = str_builder.split("**->Example 5")
            if (len(split[0]) <= 2000) and (len(split[1]) <= 1987):
                split[1] = "**->Example 5{0}".format(split[1])
                return split
            method += 1
        elif method == 10:
            split = str_builder.split("**->Definition 5")
            if (len(split[0]) <= 2000) and (len(split[1]) <= 1984):
                split[1] = "**->Definition 5{0}".format(split[1])
                return split
            method += 1
        elif method == 11:
            split = str_builder.split("**->Example 6")
            if (len(split[0]) <= 2000) and (len(split[1]) <= 1987):
                split[1] = "**->Example 6{0}".format(split[1])
                return split
            method += 1
        elif method == 12:
            split = str_builder.split("**->Definition 6")
            if (len(split[0]) <= 2000) and (len(split[1]) <= 1984):
                split[1] = "**->Definition 6{0}".format(split[1])
                return split
            method += 1
        elif method == 13:
            split = str_builder.split("**->Example 7")
            if (len(split[0]) <= 2000) and (len(split[1]) <= 1987):
                split[1] = "**->Example 7{0}".format(split[1])
                return split
            method += 1
        elif method == 14:
            split = str_builder.split("**->Definition 7")
            if (len(split[0]) <= 2000) and (len(split[1]) <= 1984):
                split[1] = "**->Definition 7{0}".format(split[1])
                return split
            method += 1
        elif method == 15:
            split = str_builder.split("**->Example 8")
            if (len(split[0]) <= 2000) and (len(split[1]) <= 1987):
                split[1] = "**->Example 8{0}".format(split[1])
                return split
            method += 1
        elif method == 16:
            split = str_builder.split("**->Definition 8")
            if (len(split[0]) <= 2000) and (len(split[1]) <= 1984):
                split[1] = "**->Definition 8{0}".format(split[1])
                return split
            method += 1
        elif method == 17:
            split = str_builder.split("**->Example 9")
            if (len(split[0]) <= 2000) and (len(split[1]) <= 1987):
                split[1] = "**->Example 9{0}".format(split[1])
                return split
            method += 1
        elif method == 18:
            split = str_builder.split("**->Definition 9")
            if (len(split[0]) <= 2000) and (len(split[1]) <= 1984):
                split[1] = "**->Definition 9{0}".format(split[1])
                return split
            method += 1
        elif method == 19:
            split = str_builder.split("**->Example 10")
            if (len(split[0]) <= 2000) and (len(split[1]) <= 1986):
                split[1] = "**->Example 10{0}".format(split[1])
                return split
            method += 1
        elif method == 20:
            split = str_builder.split("**->Definition 10")
            if (len(split[0]) <= 2000) and (len(split[1]) <= 1983):
                split[1] = "**->Definition 10{0}".format(split[1])
                return split
            method += 1
        elif method == 21:
            print("[ERROR] : NO SUPPORTED METHOD")
            return None
