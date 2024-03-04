import random
from nltk.corpus import cmudict, wordnet

#nltk.download('cmudict')
#nltk.download('punkt')
#nltk.download('wordnet')

# wordnet doc: https://wordnet.princeton.edu/documentation/wngloss7wn
# Synset: A set of synonyms that share a common meaning.
# Hypernym: A more general term that encompasses a broader category in which a specific word belongs. (ex: hyper of dog: animal, mammal, canine)
# Hyponym: A more specific term that fall under the category of a broader term (hypernym) (ex: hypo of dog: golden retriver, poodle, pincher)

class MyFirstGrammar():

    def __init__(self) -> None:
        self.adjectives, self.nouns, self.adverbs = self.get_adjectives_nouns_adverbs_list()
        self.colors = self.get_colors_list()
        self.d = cmudict.dict()

    def get_phoneme(self, word: str) -> list:
        """input: a word (string)
        output: a list of phonemes of said word, empty list if word doesnt exist"""
         # the cmudict lexicon as a dictionary, whose keys are lowercase words and whose values are lists of pronunciations.
        phonemes = self.d[word]
        if phonemes:
            phonemes = phonemes[0]
            return phonemes
        else: 
            return [] 

    def get_adjectives_nouns_adverbs_list(self) -> list:
        """output: a list of adjectives and a list of nouns with 4 phonemes maximum"""
        adjs = []
        nouns = [] 
        adverbs = []
        w = cmudict.entries() # a list of all words defined in the cmudict lexicon.
        for word in w:
            synsets = wordnet.synsets(word[0]) 
            for synset in synsets:
                if synset.pos()=="a":
                    adjs.append(word[0])
                elif synset.pos()=="n":
                    nouns.append(word[0])
                elif synset.pos()=="r":
                    adverbs.append(word[0])

        #adjs = random.sample(adjs,100)
        #nouns = random.sample(nouns,100)
        return [adjs,nouns,adverbs]

    def get_name_from_synset(self, synset_name: str):
        """used by get_colors() to return just the color name from a synset"""
        output = synset_name[:synset_name.find(".n")]
        return output

    def get_colors_list(self) -> list:
        """output: returns a list of colors"""
        colors = []
        achromatic_color = wordnet.synset('achromatic_color.n.01')
        achromatic_color = achromatic_color.hyponyms()
        for color in achromatic_color:
            colors.append(self.get_name_from_synset(color.name()))

        chromatic_color = wordnet.synset('chromatic_color.n.01')
        chromatic_color = chromatic_color.hyponyms()
        for color in chromatic_color:
            color = self.get_name_from_synset(color.name())
            if (color != "complementary_color") and (color not in colors): 
                colors.append(color)
        return colors
    
    def get_word(self, wordlist:list) -> str:
        return random.choice(wordlist)
    
    def get_adjective(self) -> str:
        return random.choice(self.adjectives)
    
    def get_noun(self) -> str:
        return random.choice(self.nouns)
    
    def get_color(self) -> str:
        return random.choice(self.colors)
    
    def get_adverb(self) -> str:
        return random.choice(self.adverbs)

    def rhyme_options(self, w1:str, t:str) -> list:
        """returns a list of words of type t that rhyme with w1
        t = a (adjectives), n (nouns)"""
        phoneme = self.get_phoneme(w1)
        output = []

        if t=="a": words_space = self.adjectives
        elif t=="n": words_space = self.nouns
        else: words_space = self.adjectives+self.nouns

        for word in words_space:
            word_phoneme = self.get_phoneme(word)
            if (word_phoneme[-2:] == phoneme [-2:]):
                output.append(word)
        return output

    def get_sentence(self) -> str:
        rhyme1 = self.get_adjective()
        rhyme2 = self.get_word(self.rhyme_options(rhyme1,"b"))

        s1 = f"\n--\nRoses are {self.get_color()}. Violets are {rhyme1}."
        s2 = f"\n{self.get_noun()} is {self.get_adjective()}, and so is {rhyme2}."
        s3 = f"\n--\n Never optimize the {self.get_noun()} out of your life."
        s4 = f"\n--\n Always do things in a {self.get_adverb()} way to people."
        s5 = f"\n--\n {self.get_adjective()} acts always generates {self.get_adjective()} acts."
        s6 = f"\n--\n Brace yourselves. {self.get_noun()} is coming."
        return s1+s2+s3+s4+s5+s6

def demo():
    myGrammar = MyFirstGrammar()
    print(myGrammar.get_sentence())
    
if __name__ == "__main__":
    demo()
