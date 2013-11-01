# coding: latin1
import random
import time
            


VOCAB_M = ('rock', 'dagger', 'sword', 'cloak', 'boulder', 'cave', 'flint', 'fire', 'shield', 'spear', 'chariot', 'axe', 'stone', 'iron')
VOCAB_F = ('flower', 'dye', 'berry', 'fruit', 'jewel', 'diamond', 'crystal', 'cloud', 'ice', 'linen', 'moon', 'sun', 'star', 'bead', 'shell')
VOCAB_N = ('city', 'site', 'place', 'river', 'forest', 'wood', 'plains', 'hill', 'mountain', 'ocean', 'lake', 'horse', 
            'earth', 'planet', 'continent', 'path', 'desert', 'death', 'life', 'dog', 'rat', 'temple', 'market', 'wheat',
            'tavern', 'inn', 'hall', 'room', 'pillar', 'village', 'pot', 'crate', 'barrel', 'bronze', 'copper')
VOCAB_FUNC = ('the', 'a', 'of')


NO_ONSET_C_CHANCE = 70 # Chance of language being a language with a high amount of "no onset consonant" syllables
NO_CODA_C_CHANCE = 70 # Chance of language being a language with a high amount of "no coda consonant" syllables

## Same thing for onsets
HIGH_ONSET_C_FREQS = (2000, 2500)
LOW_ONSET_C_FREQS = (50, 75)    

# "Frequency" values for high-coda-consonant-chance languages will be between these two values            
HIGH_CODA_C_FREQS = (2000, 2500)
# "Frequency" values for low-coda-consonant-chance languages will be between these two values
LOW_CODA_C_FREQS = (50, 75)    
            
## "Frequency" values for "common" onsets of a language will be somewhere in this range            
COMMON_ONSET_FREQS = (50, 75)
## "Frequency" values for onsets of a language which are not "common" will be somewhere in this range
REG_ONSET_FREQS = (5, 15)

## "Frequency" values for "common" codas of a language will be somewhere in this range            
COMMON_CODA_FREQS = (50, 75)
## "Frequency" values for codas of a language which are not "common" will be somewhere in this range
REG_CODA_FREQS = (5, 15)

## The number of "common" onsets for a language will be between these two numbers
COMMON_ONSET_NUMS = (4, 6)
## The number of "common" codas for a language will be between these two numbers
COMMON_CODA_NUMS = (4, 6)


NUM_COMMON_VOWELS = (2, 3)

COMMON_VOWEL_FREQS = (50, 100)
REG_VOWEL_FREQS = (1, 20)
## Eliminate some possibilities so each lang is more distinct
MIN_VOWEL_INVENTORY = 4
VOWEL_CUTOFF_FREQ = 8
            
            
# Chance of dropping a consonant from the full list of consonants
PHONOLOGICAL_INV_DROP_CHANCES = {'all':100, 'large':80, 'medium':60, 'small':40, 'tiny':30}

# use weird thing in place of... I don't know
WEIRD_CONS_LIST = ( chr(237), chr(227), chr(234), chr(231), chr(225) )
'''
# Possible use?            
dead_language_cons = [chr(247), chr(243), chr(242), chr(240), chr(226), chr(215), chr(212), chr(213), chr(217), chr(218), 
                chr(198), chr(197), chr(196), chr(180), chr(179), chr(191), chr(192), chr(174), chr(175),
                chr(169), chr(170), '/', '\\', chr(61), '+', chr(16), chr(17), chr(21)]

dead_language_vowels = ['^', ':', ';', '*', chr(96), '-',  chr(7), chr(126), chr(157), chr(169), chr(170), chr(173), chr(236), 
                chr(237), chr(244), chr(245), chr(248)]            
'''            
            

# No W for now ...            
ALL_CONSONANTS = [201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213,
                214, 215, 216, 217, 218, 219, 220, 221, 222, 224] #223, 224]
            
ALL_VOWELS = [101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111]


PHON_TO_ENG_EXAMPLES = {201:'"p"', 
                        202:'"b"', 
                        203:'"t"',
                        204:'"d"',
                        205:'"k"',
                        206:'hard "g", as in "girl"',
                        207:'"ch", as in "chest"',
                        208:'"j", as in "join"',
                        209:'"f"',
                        210:'"v"',
                        211:'soft "th", as in "thin"',
                        212:'hard "th", as in "that"',
                        213:'"s"',
                        214:'"z"',
                        215:'"sh", as in "shore"',
                        216:'"zh", as the "s" in "treasure"',
                        217:'"h"',
                        218:'"m"',
                        219:'"n"',
                        220:'"ng", as in "thing"',
                        221:'"r"',
                        222:'"y" consonant, as in "yes"',
                        223:'"w"',
                        224:'"l"', 
                        
                        101:'short "i", as in "sit"',
                        102:'long "e", as in "see"',
                        103:'short "u", as in "up"',
                        104:'short "e", as in "beg"',
                        105:'short "a", as in "bad"',
                        106:'long "a", as in "gate"',
                        107:'flat "a", as in "ah"',
                        108:'long "i", as in "hide"',
                        109:'long "o", as in "toe"',
                        110:'short "oo", as in "good"',
                        111:'long "u", as in "blue"',
                        112:'diphthong "au", as in "auburn"',
                        113:'diphthong "ou", as in "out"',
                        114:'diphthong "oi", as in "toil"'
                        }
                        
# 103    u        up        |    104    e        beg
# 105    a        bad        |    106    ae        sundae
# 107    aa        Saab    |    108    ie        pie
# 109    oe        toe        |    110    oo        good
# 111    ue        blue    |    112    au        auger
# 113    ou        out        |    114    oi        toil
                        
                        

## Vowels: English mapping
# 101    i        sit        |    102    ee        see
# 103    u        up        |    104    e        beg
# 105    a        bad        |    106    ae        sundae
# 107    aa        Saab    |    108    ie        pie
# 109    oe        toe        |    110    oo        good
# 111    ue        blue    |    112    au        auger
# 113    ou        out        |    114    oi        toil

## ASCI#: characters
#128 Ç 135 ç
#144 É            130 é 136 ê 137 ë 138 è
#142 Ä 143 Å    131 â 132 ä 133 à 134 å 160 á
#                139 ï 140 î 141 ì 161 í
#153 Ö            147 ô 148 ö 149 ò 162 ó
#154 Ü            129 ü 150 û 151 ù 163 ú
#146 Æ            145 æ
#152 ÿ
#165 Ñ            164 ñ


SYMB_TO_CAPITAL = {chr(139):'I', chr(140):'I', chr(141):'I', chr(161):'I',
                    chr(130):chr(144), chr(136):'E', chr(137):'E', chr(138):chr(144), chr(141):'I', chr(161):'I',
                    chr(129):chr(154), chr(150):'U', chr(151):'U', chr(163):'U',
                    chr(145):chr(146),  chr(131):'A', chr(132):chr(142), chr(133):'A', chr(134):chr(143), chr(160):'A',
                    chr(147):'O', chr(148):chr(153), chr(149):'O', chr(162):'O',
                    chr(152):'Y',
                    chr(135):chr(128), 
                    chr(164):chr(165)
                    }
            
VOWEL_WRITTEN = {101:['i', 'i', 'i', chr(139), chr(140), chr(141), chr(161)], 
                102:['e', 'e', 'ea', 'ea', chr(130), chr(136), chr(137), chr(138), chr(141), chr(161)], 
                103:['u', 'u', 'u', chr(129), chr(150), chr(151), chr(163)], 
                104:['e', 'e', 'e', chr(130), chr(136), chr(137), chr(138)], 
                105:['a', 'a', 'a', chr(145),  chr(131), chr(132), chr(133), chr(134), chr(160)], 
                106:['ae', 'ae', 'ae', chr(131), chr(132), chr(133), chr(134), chr(160)],
                107:['a', 'a', 'aa', 'aa', chr(131), chr(132), chr(133), chr(134), chr(160)],  
                108:['ie', 'i', 'i', chr(139), chr(140), chr(141), chr(161)], 
                109:['oe', 'oe', 'o', chr(147), chr(148), chr(149), chr(162)], 
                110:['u', 'eu', 'eu', 'eo', 'eo', chr(129), chr(150), chr(151), chr(163)], 
                111:['ue', 'ue', chr(129), chr(150), chr(151), chr(163)], 
                112:['au'],
                113:['ou'], 
                114:['oi']
                }
            
CONSONANT_WRITTEN = {300:[''],
                    301:[''],
                    
                    201:['p'], 
                    202:['b'], 
                    203:['t'],
                    204:['d'],
                    205:['k', 'k', 'k', 'k', 'q', 'c', 'c'],
                    206:['g'],
                    207:['ch', 'ch', 'ch', 'ch', 'c'],
                    208:['j', 'g'],
                    209:['f', 'f', 'f', 'f', 'ph'],
                    210:['v'],
                    211:['th'],
                    212:['th'],
                    213:['s'],
                    214:['z'],
                    215:['sh'],
                    216:['zh', 'z', 'z', chr(135)],
                    217:['h'],
                    218:['m'],
                    219:['n'],
                    220:['ng', 'ng', chr(237), chr(238)],
                    221:['r'],
                    222:['y'],
                    223:['w'],
                    224:['l']
                    }            

            
POSSIBLE_ONSETS = [
                [[201, None, []] ],
                [[202, None, []] ],
                [[203, None, []] ],
                [[204, None, []] ],
                [[205, None, []] ],
                [[206, None, []] ],
                [[207, None, []] ],
                [[208, None, []] ],
                [[209, None, []] ],
                [[210, None, []] ],
                [[211, None, []] ],
                [[212, None, []] ],
                [[213, None, []] ],
                [[214, None, []] ],
                [[215, None, []] ],
                [[217, None, []] ],
                [[218, None, []] ],
                [[219, None, []] ],
                [[221, None, []] ],
                [[222, None, []] ],
                #[[223, None, []] ],
                [[224, None, []] ],
                [['plosive', None, []], ['approximant', None, [222, 223]] ],
                [['fricative', 0, []], ['approximant', None, [222, 223]] ],
                [[213, None, []], ['plosive', 0, []] ],
                [[213, None, []], ['nasal', None, [220]] ],
                [[213, None, []], ['fricative', 0, [211, 212, 213, 215, 216]] ],
                [[213, None, []], ['plosive', 0, []], ['approximant', None, [222, 223]] ]
                ]
            
POSSIBLE_CODAS =  [ 
                [[201, None, []], ],
                [[202, None, []], ],
                [[203, None, []], ],
                [[204, None, []], ],
                [[205, None, []], ],
                [[206, None, []], ],
                [[207, None, []], ],
                [[209, None, []], ],
                [[210, None, []], ],
                [[211, None, []], ],
                [[212, None, []], ],
                [[213, None, []], ],
                [[214, None, []], ],
                [[215, None, []], ],
                [[216, None, []], ], # "zh"
                [[217, None, []], ], # "h"
                [[218, None, []], ],
                [[219, None, []], ],
                [[220, None, []], ], ## ng
                [[221, None, []], ],
                [[222, None, []], ],
                #[[223, None, []], ],
                [[224, None, []], ],
                [[224, None, []], ['plosive', None, []] ],
                [[224, None, []], ['affricate', None, []] ],
                [[221, None, []], ['plosive', None, []] ],
                [[221, None, []], ['affricate', None, []] ],
                [[224, None, []], ['fricative', None, [216, 217]] ],
                [[221, None, []], ['fricative', None, [216, 217]] ],
                [[224, None, []], ['nasal', None, [220]] ],
                [[221, None, []], ['nasal', None, [220]] ],
                [[221, None, []], ['lateral', None, []] ],
                [['nasal', None, [220]], ['plosive', None, []] ],  ## homorganic?
                [['nasal', None, [220]], ['affricate', None, []] ],## homorganic?
                [['nasal', None, [220]], ['fricative', None, [216, 217]] ],
                [['fricative', 0, [216]], ['plosive', 0, []] ],
                [['plosive', 0, []], ['plosive', 0, []] ],
                [['plosive', None, []], ['fricative', 0, [216]] ],
                ]             
            
            
def roll(a, b):
    return random.randint(a, b)
    
    
def spec_cap(word):
    # We need a way to capitalize special characters
    if word[0].isalpha():
        return word.capitalize()
    try:
        word = ''.join( [ SYMB_TO_CAPITAL[word[0]], word[1:] ] )
        return word
    except:
        return word
            
            
class Consonant:
    def __init__(self, phon, num, location, method, voicing):
        self.phon = phon
        self.num = num
        self.location = location
        self.method = method
        self.voicing = voicing
        self.freq = None
        
        CONSONANTS.append(self)
        
        
# List of consonants - should be added to Language class to be language-specific
CONSONANTS = []
'''    
# Create the consonants
p  = Consonant('p',  201, 'bilabial', 'plosive', 0, 33)
b  = Consonant('b',  202, 'bilabial', 'plosive', 1, 17)
t  = Consonant('t',  203, 'alveolar', 'plosive', 0, 68)
d  = Consonant('d',  204, 'alveolar', 'plosive', 1, 40)
k  = Consonant('k',  205, 'velar', 'plosive', 0, 41)
g  = Consonant('g',  206, 'velar', 'plosive', 1, 26)
ch = Consonant('ch', 207, 'post-alveolar', 'affricate', 0, 5)
j  = Consonant('j',  208, 'post-alveolar', 'affricate', 1, 8)
f  = Consonant('f',  209, 'labio-dental', 'fricative', 0, 17)
v  = Consonant('v',  210, 'labio-dental', 'fricative', 1, 12)
th = Consonant('th', 211, 'dental', 'fricative', 0, 3)
tz = Consonant('th', 212, 'dental', 'fricative', 1, 1)
s  = Consonant('s',  213, 'alveolar', 'fricative', 0, 68)
z  = Consonant('z',  214, 'alveolar', 'fricative', 1, 37)
sh = Consonant('sh', 215, 'post-alveolar', 'fricative', 0, 12)
zh = Consonant('zh', 216, 'post-alveolar', 'fricative', 1, 1)
h  = Consonant('h',  217, 'glottal', 'fricative', 3, 7)
m  = Consonant('m',  218, 'bilabial', 'nasal', 3, 30)
n  = Consonant('n',  219, 'alveolar', 'nasal', 3, 68)
ng = Consonant('ng', 220, 'velar', 'nasal', 3, 10)
r  = Consonant('r',  221, 'alveolar', 'approximant', 3, 39) # R - should be also post-alveolar?
y  = Consonant('y',  222, 'palatal', 'approximant', 3, 16) # J - really Y
w  = Consonant('w',  223, 'velar', 'approximant', 3, 12) 
l  = Consonant('l',  224, 'alveolar', 'lateral', 3, 54) 
'''    

p  = Consonant('p',  201, 'bilabial', 'plosive', 0)
b  = Consonant('b',  202, 'bilabial', 'plosive', 1)
t  = Consonant('t',  203, 'alveolar', 'plosive', 0)
d  = Consonant('d',  204, 'alveolar', 'plosive', 1)
k  = Consonant('k',  205, 'velar', 'plosive', 0)
g  = Consonant('g',  206, 'velar', 'plosive', 1)
ch = Consonant('ch', 207, 'post-alveolar', 'affricate', 0)
j  = Consonant('j',  208, 'post-alveolar', 'affricate', 1)
f  = Consonant('f',  209, 'labio-dental', 'fricative', 0)
v  = Consonant('v',  210, 'labio-dental', 'fricative', 1)
th = Consonant('th', 211, 'dental', 'fricative', 0)
tz = Consonant('th', 212, 'dental', 'fricative', 1)
s  = Consonant('s',  213, 'alveolar', 'fricative', 0)
z  = Consonant('z',  214, 'alveolar', 'fricative', 1)
sh = Consonant('sh', 215, 'post-alveolar', 'fricative', 0)
zh = Consonant('zh', 216, 'post-alveolar', 'fricative', 1)
h  = Consonant('h',  217, 'glottal', 'fricative', 3)
m  = Consonant('m',  218, 'bilabial', 'nasal', 3)
n  = Consonant('n',  219, 'alveolar', 'nasal', 3)
ng = Consonant('ng', 220, 'velar', 'nasal', 3)
r  = Consonant('r',  221, 'alveolar', 'approximant', 3) # R - should be also post-alveolar?
y  = Consonant('y',  222, 'palatal', 'approximant', 3) # J - really Y
w  = Consonant('w',  223, 'velar', 'approximant', 3) 
l  = Consonant('l',  224, 'alveolar', 'lateral', 3)     

REG_CONS_COMBOS = [('bilabial', 'plosive'), ('alveolar', 'plosive'), ('velar', 'plosive'),
                    ('post-alveolar', 'affricate'), ('labio-dental', 'fricative'), 
                    ('dental', 'fricative'), ('alveolar', 'fricative'), ('post-alveolar', 'fricative')
                    ]

WEIRD_CONS_COMBOS = [                    
                    ('glottal', 'fricative'), ('bilabial', 'nasal'), ('alveolar', 'nasal'),
                    ('velar', 'nasal'), ('alveolar', 'approximant'), ('palatal', 'approximant'),
                    ('velar', 'approximant'), ('alveolar', 'lateral')
                    ]
        
        
        
class Orthography:
    ''' Class to map phonemes to letters. Very shallow at the moment '''
    def __init__(self, possible_vowels, possible_consonants, nordic_i=None, use_weird_symbols=None):
        # Allow specification of any symbols that are predefined
        self.mapping = {}
        
        
        potential_v_rep = {}
        for vowel in possible_vowels:
            potential_v_rep[vowel] = VOWEL_WRITTEN[vowel][:]

        potential_c_rep = {}
        for consonant in possible_consonants:
            potential_c_rep[consonant] = CONSONANT_WRITTEN[consonant][:]
    
        
        ## Sort of silly, but it we allow "y" to be used in place of "i", we need
        ## to make sure that "y" cannot also be a consonant (we'll replace with J for now)
        use_nordic_i = 0
        if (nordic_i == None and roll(1, 5) == 1) or nordic_i == 1:
            use_nordic_i = 1
            
        if use_nordic_i:
            if 101 in potential_v_rep.keys():
                potential_v_rep[101].append('y')
                potential_v_rep[101].append(chr(152))
            if 108 in potential_v_rep.keys():
                potential_v_rep[108].append('y')
                potential_v_rep[108].append(chr(152))
            
            potential_c_rep = self.replace_grapheme(mapping=potential_c_rep, phoneme=222, old='y', new='j')

        # If we want to (possibly) use non-english symbols in place of some of the consonants        
        if (use_weird_symbols == None and roll(1, 5) == 1) or use_weird_symbols == 1:
            # Use "thorn"/"eth" (sigma symbol? haha)
            if roll(0, 1) == 1:
                potential_c_rep = self.replace_grapheme(mapping=potential_c_rep, phoneme=211, old='th', new=chr(235))
                potential_c_rep = self.replace_grapheme(mapping=potential_c_rep, phoneme=212, old='th', new=chr(235))
            # Use ç in place of ch
            if roll(0, 1) == 1:
                potential_c_rep = self.replace_grapheme(mapping=potential_c_rep, phoneme=207, old='ch', new=chr(135))
            # Use ƒ instead of sh
            if roll(0, 1) == 1:
                potential_c_rep = self.replace_grapheme(mapping=potential_c_rep, phoneme=215, old='sh', new=chr(159))
                potential_c_rep = self.replace_grapheme(mapping=potential_c_rep, phoneme=216, old='zh', new=chr(159))

            for i in WEIRD_CONS_LIST:
                if roll(1, 5) == 1:
                    cons = random.choice(potential_c_rep.keys())
                    # Lazy for now - but can't replace empty
                    if cons < 300:
                        potential_c_rep[cons] = [i]
        
        
        for consonant, grapheme_list in potential_c_rep.iteritems():
            if not consonant in self.mapping.keys():
                grapheme = random.choice(grapheme_list)
                self.mapping[consonant] = grapheme
        ## Transcribe vowels
        for vowel, grapheme_list in potential_v_rep.iteritems():
            if not vowel in self.mapping.keys():
                grapheme = random.choice(grapheme_list)
                self.mapping[vowel] = grapheme
                

        
    def replace_grapheme(self, mapping, phoneme, old, new):
        if phoneme in mapping.keys():
            num_graphemes = mapping[phoneme].count(old)
            for g in xrange(num_graphemes):
                mapping[phoneme].remove(old)
                mapping[phoneme].append(new)
            
            return mapping
        else:
            return mapping
        
class Language:
    ''' Basically a set of rules for what phonemes are in the language, 
        what valid syllable onsets and codas exist, and their frequencies '''
    def __init__(self):    
        
        phonological_inventory_size=random.choice(PHONOLOGICAL_INV_DROP_CHANCES.keys())
        # Generate a phonological inventory - but make sure it leaves us with valid onsets/offsets
        while 1:
            self.gen_structs(phonological_inventory_size)
            if len(self.valid_onsets) > 0 and len(self.valid_codas) > 0:
                break
        
        self.set_onsets()
        self.set_codas()
        self.set_vowels()
        
        ## Create transcription - map letters to writing symbols
        self.create_script()
        
        self.name = spec_cap( self.gen_word( syllables=roll(2, 3), num_phonemes=(3, 20) ) )
        
        self.gen_vocabulary()
        
        
    def gen_structs(self, phonological_inv_size):
        ## Generate possible structures (consonants, syllables, codas) for the language
        ## based on size of phonological inventory

        consonant_drop_chance = PHONOLOGICAL_INV_DROP_CHANCES[phonological_inv_size]    
        # Start with empty list of consonants, will build up over time
        self.consonants = []
        
        consonant_possibilities = []
        
        # Now we check to see which ones (if any) are dropped
        for consonant in CONSONANTS[:]:
            if roll(1, 100) <= consonant_drop_chance:
                consonant_possibilities.append(consonant)
        # Give each one a frequency. Currently very weird because
        # the only time this frequency is really used is computing
        # consonants that make up a syllable onset or coda
        # The onset and coda structures themselves have their own frequencies
        for cons in consonant_possibilities:
            cons.freq = roll(1, 70)
            self.consonants.append(cons)
        
        
        self.valid_onsets = []
        self.valid_codas = []
        
        # Now it's time to use brute force and see which of all possible 
        # onsets/codas can  be used. If phon_list returns empty, it means
        # our language can't find phonemes for that onset/coda, and so must be discarded
        #
        # Tricky here - need to copy all of the sublists to make sure original lists aren't modified
        for onset in POSSIBLE_ONSETS[:]:
            all_valid_phonemes = 1
            for phoneme_properties in onset[:]:
                phon_list = self.find_phoneme(phoneme_properties[0], phoneme_properties[1], phoneme_properties[2]) 
                if phon_list == []:
                    all_valid_phonemes = 0

            if all_valid_phonemes:
                self.valid_onsets.append(onset[:])
    
        # Same for codas
        for coda in POSSIBLE_CODAS[:]:
            all_valid_phonemes = 1
            for phoneme_properties in coda[:]:
                phon_list = self.find_phoneme(phoneme_properties[0], phoneme_properties[1], phoneme_properties[2]) 
                if phon_list == []:
                    all_valid_phonemes = 0
            
            if all_valid_phonemes:
                self.valid_codas.append(coda[:])

                
        
    def set_vowels(self):
        self.vowel_freqs = []
        # Copy all vowels
        vowels = ALL_VOWELS[:]
        ## Make a list of common vowels
        common_vowels = []
        for i in xrange(roll(NUM_COMMON_VOWELS[0], NUM_COMMON_VOWELS[1])):
            common_vowel = vowels.pop(roll(0, len(vowels)-1) )
            common_vowels.append(common_vowel)
        
            freq = roll(COMMON_VOWEL_FREQS[0], COMMON_VOWEL_FREQS[1])
            self.vowel_freqs.append( (common_vowel, freq) )
        
        ## Shuffle the remaining list
        random.shuffle(vowels)
        # Generate frequencies for remaining vowels - if they're low enough, remove them entirely from the inventory
        for vowel in vowels:
            freq = roll(REG_VOWEL_FREQS[0], REG_VOWEL_FREQS[1])
            # If frequency is low enough, we'll drop it from the language
            # Make sure that the frequency is high enough, and that we have a min number of vowels
            if freq > VOWEL_CUTOFF_FREQ or len(self.vowel_freqs) < MIN_VOWEL_INVENTORY:
                self.vowel_freqs.append( (vowel, freq) )
                    
        
        # Weird, but some vowels associated more with males, or females
        # Hopefully will help distinguish male/female names
        vf_ind = roll(1, len(self.vowel_freqs)-1)
        self.vowel_F = self.vowel_freqs[vf_ind][0]
        self.vowel_M = self.vowel_freqs[vf_ind-1][0]
        
    
    def set_onsets(self, onsets=None, no_onset_chance=NO_ONSET_C_CHANCE):
        ## You can feed the function a list of your own valid onsets
        ## if you want to specify.
        if onsets != None:
            self.valid_onsets = onsets
        ## Otherwise, create the possible onsets randomly
        else:
            random.shuffle(self.valid_onsets)
            
            common_onset_nums = min(roll(COMMON_ONSET_NUMS[0], COMMON_ONSET_NUMS[1]), len(self.valid_onsets) )
                
            for i, onset in enumerate(self.valid_onsets):
                if i <= common_onset_nums:
                    freq = roll(COMMON_ONSET_FREQS[0], COMMON_ONSET_FREQS[1])
                    onset.append(freq)
                
                else:
                    freq = roll(REG_ONSET_FREQS[0], REG_ONSET_FREQS[1])
                    onset.append(freq)
                    
            ## Some languages have a high occurance of syllables with no onset consonant
            if roll(1, 100) >= no_onset_chance:
                perc_sylls_with_no_onset = roll(HIGH_ONSET_C_FREQS[0], HIGH_ONSET_C_FREQS[1])
                self.valid_onsets.append( [(300, None, []), perc_sylls_with_no_onset] )
            else:
                perc_sylls_with_no_onset = roll(LOW_ONSET_C_FREQS[0], LOW_ONSET_C_FREQS[1])
                self.valid_onsets.append( [(300, None, []), perc_sylls_with_no_onset] )
    
        # Now get a list of tuples, only containing the valid onsets (in num or long form) and their freqs (out of 1000, roughly?) 
            self.valid_onset_freqs = []
            for entry in range(0, len(self.valid_onsets)):
                self.valid_onset_freqs.append((entry, self.valid_onsets[entry][-1]))
    
    
    def set_codas(self, codas=None, no_coda_chance=NO_CODA_C_CHANCE):
        ## You can feed the function a list of your own valid codas
        ## if you want to specify.
        if codas != None:
            self.valid_codas = codas
        ## Otherwise, create the possible codas randomly
        else:
            random.shuffle(self.valid_codas)
            
            common_coda_nums = min(roll(COMMON_CODA_NUMS[0], COMMON_CODA_NUMS[1]), len(self.valid_codas) )
            
            for i, coda in enumerate(self.valid_codas):
                if i < common_coda_nums:
                    freq = roll(COMMON_CODA_FREQS[0], COMMON_CODA_FREQS[1])
                    coda.append(freq)
                
                else:
                    freq = roll(REG_CODA_FREQS[0], REG_CODA_FREQS[1])
                    coda.append(freq)
            
            ## Some languages have a high occurance of syllables with no coda consonant
            if roll(1, 100) >= no_coda_chance:
                perc_sylls_with_no_coda = roll(HIGH_CODA_C_FREQS[0], HIGH_CODA_C_FREQS[1])
                self.valid_codas.append( [(301, None, []), perc_sylls_with_no_coda] )
            else:
                perc_sylls_with_no_coda = roll(LOW_CODA_C_FREQS[0], LOW_CODA_C_FREQS[1])
                self.valid_codas.append( [(301, None, []), perc_sylls_with_no_coda] )
            
        self.valid_coda_freqs = []
        for entry in range(0, len(self.valid_codas)):
            self.valid_coda_freqs.append((entry, self.valid_codas[entry][-1]))
            
            
    def create_script(self):
        possible_vowels = [vowel for (vowel, freq) in self.vowel_freqs]
        possible_consonants = [consonant.num for consonant in self.consonants]
        possible_consonants.append(300)
        possible_consonants.append(301)

        self.orthography = Orthography(possible_vowels=possible_vowels, possible_consonants=possible_consonants)
    
            
    def gen_vocabulary(self):
        self.vocabulary = {}
        
        self.vocab_m = {}
        self.vocab_f = {}
        self.vocab_n = {}
        self.vocab_function = {}
        
        # Generate some "Masculine", "Feminine", and "neutral" words
        word_lists = ( (VOCAB_M, 'm', self.vocab_m), (VOCAB_F, 'f', self.vocab_f), (VOCAB_N, None, self.vocab_n) )
        for (eng_list, vowel_pref, append_list) in word_lists:
            # Basically, make sure the word is "valid" (not too short), and if so, use it
            for eng_word in eng_list: 

                syllables = roll(1, 2)
                # Here's where the "Masculine" or "feminine" words come into play
                word = self.gen_word(syllables, num_phonemes=(3, 20), use_onset=1, onset_can_have_no_consonant=1, use_coda=1, vowel_pref=vowel_pref)
                
                self.vocabulary[eng_word] = word
                append_list[eng_word] = word
        
        # Generate function words
        for eng_word in VOCAB_FUNC:
            use_onset, use_coda = random.choice( ( (0, 1), (1, 0) ) )
            onset_cons = roll(0, 1)
            word = self.gen_word(syllables=1, num_phonemes=(1, 4), use_onset=use_onset, onset_can_have_no_consonant=onset_cons, use_coda=use_coda, vowel_pref=None)
            self.vocab_function[eng_word] = word

    
    def gen_phon(self, freqlist, desclist):
        # Return part of a word - onset, offset, vowel - that draws from input list 
        chunk_phon = [] # The list that gets returned            
        
        #Start by finding onset/offset/whatever by weighted random item in list
        chunk = w_rand(freqlist)
        
        for entry in xrange(len(desclist[chunk])-1):
            # Check if entry is directly a phoneme; else make weighted choice from list
            chunk_entry = desclist[chunk][entry]
            
            # Ugly check to see how to proceed:
            if type(chunk_entry[0]) == type(int()):
                # Append it since we already chose it based on frequency
                chunk_phon.append(chunk_entry[0])
                
            else:
                # Awkward solution for now: This particular word-opening combo has been chosen by frequency
                # of the ENTIRE opening combo (arbitrary), but now we'll choose each of these numbers individually
                
                # Gets a list of phon nums
                phon_list = self.find_phoneme(chunk_entry[0], chunk_entry[1], chunk_entry[2])
                
                choice = w_rand(phon_list)
                chunk_phon.append(choice)

        #print chunk_phon
        return chunk_phon

    
    def get_vowel(self, vowel_pref=None):
        ## Weird little function. Here I'm attempting to bypass the normal
        ## weighted vowel thing in favor of the masc or fem vowel.
        ## The main reason to do this is try to distinguish masc or fem names
        num = roll(1, 9)
        if num >= 5 and vowel_pref == 'f':
            return self.vowel_F
        elif num >= 5 and vowel_pref == 'm':
            return self.vowel_M
        else:
            return w_rand(self.vowel_freqs)
    
    def gen_word(self, syllables, num_phonemes, use_onset=1, onset_can_have_no_consonant=1, use_coda=1, vowel_pref=None):
        ''' Generate a word containing specified # of syllables '''
        
        while 1:
            # List of phonemes in the word. Phonemes are represented by numbers
            # The numbers later get converted to letters
            word = []
            # Actual letters of the word; starts off as an empty string
            wordphon = '' 
            

            onset_can_have_no_consonant = 1
            for syllable in range(syllables):
                if use_onset:
                    use_onset = 0
                    # Sort of a bad way to solve this issue. Issue is that we don't want a syllable with an empty
                    # coda to have a syllable with an empty onset following it. 
                    # Rules (currently) here are:
                    #    Onsets occur at the beginning of a word, with no restriction as to whether it starts with a consonant
                    #     If the preceding coda did not end with a consonant, we MUST have a consonant at the beginning of the onset
                    #    This breaks up words like "guud" which would otherwise happen
                    while 1:
                        onset = self.gen_phon(freqlist=self.valid_onset_freqs, desclist=self.valid_onsets)
                        if onset_can_have_no_consonant or onset[0] != 300:
                            break
                    
                    for entry in onset:
                        word.append(entry)
                
                # Vowels in the middle
                vowel = self.get_vowel(vowel_pref=vowel_pref)
                word.append(vowel)
                
                # codas after every syllable
                if use_coda:
                    coda = self.gen_phon(freqlist=self.valid_coda_freqs, desclist=self.valid_codas)
                    
                    for entry in coda:
                        word.append(entry)
                    # Special case - if the coda didn't end with a consonant, we
                    # want the next syllable to start with an onset, and that onset MUST have a consonant
                    if entry == 301:
                        use_onset = True
                        onset_can_have_no_consonant = 0
            
            # Woohoo, the word meets the minimum constraints!
            if num_phonemes[0] <= len([phon for phon in word if phon < 300]) <= num_phonemes[1]:
                break
        
    
        # Use our transcription to find phonemes
        for phoneme in word:
            wordphon = wordphon + self.orthography.mapping[phoneme]
        
        return wordphon
        
                            
    def find_phoneme(self, qual, voicing, exclude_list):
        # This function should return a list of phonemes (consonants) that match the input criteria
        phon_list = []
        for consonant in self.consonants:
            # Check if consonant matches input qualities
            if (consonant.location == qual or consonant.method == qual) or consonant.num == qual:
                # If no voicing constraints, and not specifically excluded, append
                if voicing == None and consonant.num not in exclude_list:
                    phon_list.append((consonant.num, consonant.freq))
                # Else, append if matches voicing requirements and not specifically excluded
                elif voicing == consonant.voicing and consonant.num not in exclude_list:
                    phon_list.append((consonant.num, consonant.freq))
            
        return phon_list
            

def w_rand(_list):
    # Return a weighted randomization from the input list
    total_num = 0
    letter_values = {}
    
    for iteration in range(len(_list)):
        c_index, c_chance = _list[iteration-1]
        
        letter_values[c_index] = (total_num, total_num + c_chance)
        total_num += c_chance + 1 # add 1 so possibilities don't overlap?
    
    choice = random.randint(0, total_num - 1) # subtract 1 to counterract the "extra" 1 in the last iteration of the above step
    
    for c_index, c_chance in _list:
        (low, high) = letter_values[c_index]
        if low <= choice <= high:
            # Returning the index of the weighted choice in the list 
            return c_index
            break

    

if __name__ == '__main__':
    # create an instance of the Language class
    lang = Language()
    
    
    print ' -- MASCULINE -- '
    for eng_word, word in lang.vocab_m.iteritems():
        print eng_word, '-', word
    print ' -- FEMININE -- '
    for eng_word, word in lang.vocab_f.iteritems():
        print eng_word, '-', word
    print ' -- NEUTRAL -- '
    for eng_word, word in lang.vocab_n.iteritems():
        print eng_word, '-', word
    for eng_word, word in lang.vocab_function.iteritems():
        print eng_word, '-', word
