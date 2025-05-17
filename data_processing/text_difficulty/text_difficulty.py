import textstat
from big_phoney import BigPhoney
from wordfreq import zipf_frequency

class TextDifficultyEvaluator:
    def __init__(self):
        """ Initialize the TextDifficultyEvaluator with predefined thresholds,
        weights, and tools for evaluating word and text complexity."""
        # Threshold constants per word 
        self.MAX_FREQ = 8
        self.MAX_PHONEMES = 15
        self.MAX_SYLL_WORD = 6  
        
        # Threshold constants per sentence 
        self.MAX_WORDS = 15
        self.MAX_GRADE = 9
        self.MAX_SYLL_SEN = 17 

        # Evaluation weights for words
        self.FREQ_WEIGHT = 0.2
        self.PHONEME_WEIGHT = 0.3
        self.SYLL_WORD_WEIGHT = 0.5
        
        # Evaluation weights for words
        self.GRADE_WEIGHT = 0.25
        self.WORD_WEIGHT = 0.5
        self.SYLL_SEN_WEIGHT = 0.25
        
        # Scale for difficulty
        self.DIFFICULTY_SCALE = 2
        
        # Object to extract phonemes
        self.phoney = BigPhoney()
        
    def _count_words(self, str:str)->int:
        """Count words in a string using texstat module.

        Args:
            str (str): A string containing one or more words.

        Returns:
            int: Number of words in a string.
        """
        return textstat.lexicon_count(str, removepunct=True)
    
    def _count_syllables(self, str:str)->int:
        """Count syllables in a string using Big Phoney module.

        Args:
            str (str): A string containing one or more words.

        Returns:
            int: Number of syllables in a string.
        """
        return self.phoney.count_syllables(str)
    
    def _difficulty_threshold(self, thresholds:dict, value:int)->int:
        """Return the class according to the difficulty threshold.

        Args:
            thresholds (dict): Dictionary of {threshold : class} key-values.
            value (int): Value to evaluate against threshold.

        Returns:
            int: Class corresponding to threshold.
        """
        for threshold in thresholds.keys():
            if value < threshold:
                return thresholds[threshold]
        
    def word_difficulty(self, word:str)->int:
        """Classify english words by difficulty based on frequency, syllable 
        count and phoneme count on a cateogrical scale from 0 to 2 
        (0 - Easy, 1 - Medium, 2 - Hard).

        Args:
            word (str): Word to classify.

        Returns:
            int: Difficulty of the word.
        """
        phonemes = self.phoney.phonize(word)
        phoneme_count = self._count_words(phonemes)
        syllable_count = self._count_syllables(word)
        frequency = zipf_frequency(word, lang="en")
        
        # Normalize values between [0,1]
        freq_score = 1 - (frequency / self.MAX_FREQ) 
        phoneme_score = min(phoneme_count / self.MAX_PHONEMES, 1)
        syllable_score = min(syllable_count / self.MAX_SYLL_WORD, 1)

        # Calculate difficulty with weighted sum
        difficulty = (
            self.FREQ_WEIGHT * freq_score +
            self.PHONEME_WEIGHT * phoneme_score +
            self.SYLL_WORD_WEIGHT * syllable_score
        )

        difficulty = min(difficulty, 1.0)
        
        # Obtain final difficulty
        thresholds = { 0.45 : 0, 0.64: 1, 1:2 }
        return self._difficulty_threshold(thresholds, difficulty)
        
    def sentence_difficulty(self, sentence:str)->int:
        """Classify english sentences by difficulty based on grade level 
        comprehension, word count and syllable count on a cateogrical scale 
        from 0 to 2 (0 - Easy, 1 - Medium, 2 - Hard).

        Args:
            sentence (str): Sentence to classify.

        Returns:
            int: Difficulty of the sentence.
        """
        grade_level = max(textstat.text_standard(sentence, float_output=True),1.0)
        word_count = self._count_words(sentence)
        syllable_count = self._count_syllables(sentence)
        
        # Normalize values between [0,1]
        grade_score = min(grade_level / self.MAX_GRADE, 1) 
        word_score = min(word_count / self.MAX_WORDS, 1)
        syllable_score = min(syllable_count / self.MAX_SYLL_SEN, 1)
        
        # Calculate difficulty with weighted sum
        difficulty = (
            self.GRADE_WEIGHT * grade_score +
            self.WORD_WEIGHT * word_score +
            self.SYLL_SEN_WEIGHT * syllable_score
        )
        
        difficulty = min(difficulty, 1.0)
        
        # Obtain final difficulty
        thresholds = { 0.4 : 0, 0.6: 1, 1:2 }
        return self._difficulty_threshold(thresholds, difficulty)