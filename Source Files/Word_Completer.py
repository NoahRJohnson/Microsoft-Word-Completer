import cPickle
import os
from sets import Set

class WordCompleter(object):
    '''
    Word Completer.
    This class will create the database necessary to complete words based off
    of some characters inputted so far, i.e. the prefix of letters.
    '''

    def __init__(self, pkl_filename, prefix_number):
        self.pkl_filename = pkl_filename
        self.current_words = set()
        self.prefix = () #Empty tuple
        self.prefix_num = prefix_number

        pkl_path = os.getcwd() + "/" + self.pkl_filename
        if os.path.exists(pkl_path):
            with open(self.pkl_filename, 'rb') as f:
                self.word_freq, self.prefix_freq = cPickle.load(f)
        else:
            try:
                with open("words.txt", 'r') as f:
                    word_list = f.read().lower().split()
            except:
                raise IOError("Failed to open the words file.")
            
            self.word_freq = {}
            for word in word_list:
                self.word_freq[word] = 1
            self.prefix_freq = {}
        

    def find_mfw(self, string):
        # Of the words that the string could become, this method returns
        # the word which the user has typed most frequently. Now takes into
        # account previous words typed, i.e. the prefix.
        # Lots of heavy logic here.
        
        
        if self.prefix_num == 0:

            mfw = self.basic_mfw_search(string)

        else:
            '''
            I choose not to optimize this section with another set, e.g.
            self.current_tuples, for tuples to be added to and then run
            through, in order to reduce the number of loops the for loop
            has to run through, as is implemented above. I do this because
            although the number of prefixes may get huge, I find it unlikely
            that any one prefix will have a huge number of word tuples that
            come after it. It seems to run fast enough as is. I can always
            optimize it later, but if you think it would be worth it, e.g.
            if you like to set the prefix number to 1 and type 100 different
            variations after one word, then feel free to add such a set and
            implement it.
            '''  
            if self.prefix in self.prefix_freq.keys():
                mfw = ""
                highest_freq = 0
                for t in self.prefix_freq[self.prefix]:
                    if t[0].startswith(string):
                        if t[1] > highest_freq:
                            highest_freq = t[1]
                            mfw = t[0]
                if mfw == "": #If none of the tuples match the word:
                    mfw = self.basic_mfw_search(string)
    
            else:
                mfw = self.basic_mfw_search(string)
                            
        return mfw

    def basic_mfw_search(self, string):
        if string == "":
            return ""
        
        mfw = ""
        highest_freq = 0
        
        if len(self.current_words) == 0:
            for word in self.word_freq.keys():
                if word.startswith(string):
                    self.current_words.add(word)
                    if self.word_freq[word] > highest_freq:
                        highest_freq = self.word_freq[word]
                        mfw = word
        else:
            next_set = set()
            for word in self.current_words:
                if word.startswith(string):
                    next_set.add(word)
                    if self.word_freq[word] > highest_freq:
                        highest_freq = self.word_freq[word]
                        mfw = word
            self.current_words = next_set

        return mfw
        


    
    def add_word(self, word):
        self.word_freq[word] = self.word_freq.get(word, 0) + 1

        if len(self.prefix) == self.prefix_num and self.prefix_num != 0:
            
            values = self.prefix_freq.get(self.prefix, [])
            if values == []:
                tup = (word, 1)
                values = [tup] #Put tuple into a list, as a tuple.
            else:
                match = False
                for t in values:
                    if t[0] == word:
                        num = t[1] + 1
                        updated_t = (word, num)
                        values.remove(t)
                        values.append(updated_t)
                        match = True
                        break
                if match == False:
                    t = (word, 1)
                    values.append(t)

            self.prefix_freq[self.prefix] = values


        if self.prefix_num != 0:
            self.prefix = self.prefix + (word,)
            if len(self.prefix) > self.prefix_num:
                self.prefix = self.prefix[(len(self.prefix)-self.prefix_num):]

        
        self.clear_current_words()


    def set_prefix_number(self, num):
        self.prefix_num = num
        self.clear_current_words()

    def clear_current_words(self):
        self.current_words.clear()

    def end(self):
        # Dump dict into pickle file.
        with open(self.pkl_filename, 'wb') as f:
            data = [self.word_freq, self.prefix_freq]
            cPickle.dump(data, f)

