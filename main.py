import random, nltk, pygame
import parameters
nltk.data.path.append('.venv/nltk_data')
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
        self.initialState = True
        self.start_game()
        
    def start_game(self) -> None:
        pygame.init()
        pygame.font.init()
        self.resolution = parameters.SCREEN_DATA["RESOLUTION"]
        self.screen_size = parameters.SCREEN_DATA["SCREEN_SIZE"]
        self.canvas = pygame.Surface(self.resolution)
        self.screen = pygame.display.set_mode(self.screen_size)
        self.x_screen_scale = self.resolution[0] / self.screen_size[0]
        self.y_screen_scale = self.resolution[1] / self.screen_size[1]
        self.fps_cap = parameters.SCREEN_DATA["FPS_CAP"]
        pygame.display.set_caption("POEM GENERATOR")        
        self.exit = False
        self.clock = pygame.time.Clock()     
        #------
        font = pygame.font.Font(None,20)
        askSpace = font.render("Loading...",True, (255,255,255))
        self.canvas.blit(askSpace,(25,45))
        self.update_screen()
        
        self.adjectives, self.nouns, self.adverbs = self.get_adjectives_nouns_adverbs_list()
        self.colors = self.get_colors_list()
        self.d = cmudict.dict()
        #------
        self.poems = ""
        self.author = ""
        self.borderColor = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
        
        self.game_loop()   
        
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

        s1 = f"Roses are {self.get_color()}. Violets are {rhyme1}."
        s2 = f"{self.get_noun()} is {self.get_adjective()}, and so is {rhyme2}."
        s3 = f"Never optimize the {self.get_noun()} out of your life."
        s4 = f"Always do things in a {self.get_adverb()} way to people."
        s5 = f"{self.get_adjective()} acts always generates {self.get_adjective()} acts."
        s6 = f"Brace yourselves. {self.get_noun()} is coming."
        return random.choice([s1,s2,s3,s4,s5,s6])

    def game_loop(self) -> None:
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.type == pygame.QUIT:
                        running = False
                    if event.key == pygame.K_SPACE:
                        if self.initialState:
                            self.initialState = False
                        self.poems = self.get_sentence()
                        self.author = random.choice(parameters.EMOJI_LIST)
                        self.borderColor = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
                    elif (event.key == pygame.K_q) or (event.key == pygame.K_ESCAPE):
                        running = False
            if running:
                self.canvas.fill((0, 0, 0)) 
                self.draw()
                self.update_screen()
                
    def draw(self) -> None:
        pygame.draw.rect(self.canvas, self.borderColor, pygame.Rect(0,0,self.screen_size[0],self.screen_size[1]),3)
        
        if (self.initialState):
            font = pygame.font.Font(None,20)
            askSpace = font.render("Press 'SPACE' to get new poems",True, (255,255,255))
            self.canvas.blit(askSpace,(25,45))
        else:
            font = pygame.font.Font(None,20)
            poems2screen = font.render(self.poems,True, (255,255,255))
            author2screen = font.render(self.author, True, (125,125,125))
            self.canvas.blit(poems2screen,(25,45))
            self.canvas.blit(author2screen,(370,75))

        
        
            
    def update_screen(self) -> None:
        scaled_canvas = pygame.transform.scale(self.canvas, self.screen_size)
        self.screen.blit(scaled_canvas, (0, 0))  # Draw scaled canvas on the screen
        pygame.display.update()  # atualiza a tela
        

def execute():
    myGrammarGame = MyFirstGrammar()

if __name__ == "__main__":
    execute()