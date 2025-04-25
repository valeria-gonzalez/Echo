import pandas as pd
from typing import List
import json

class TatoebaProcessor:
    def __init__(self, eng_sentences:str, sentences_with_audio:str, 
                 eng_spa_pairs:str):
        """Initialize Tatoeba Processor for sentences with filepaths with needed
        sentences downloadable from Tatoeba. These are the needed files from Tatoeba:
        - English sentences : `eng_sentences_CC0.tsv`
        - Sentences with audio : `sentences_with_audio.csv`
        - English spanish sentence pairs : `Sentence pairs in English-Spanish -{YYYY-MM-DD}.tsv`

        Args:
            eng_sentences (str): Filepath for english sentences file.
            sentences_with_audio (str): Filepath for sentences with audio file.
            eng_spa_pairs (str): Filepath for english spanish sentence pairs file.
        """
        self.eng_sen_filepath = eng_sentences
        self.audio_sen_filepath = sentences_with_audio
        self.eng_spa_pairs_filepath = eng_spa_pairs
        self.json_filepath = None
    
    def load_datasets(self)->List[pd.DataFrame]:
        """Load the datasets for english sentences, senteces with audio and
        english spanish pairs (respectively) as pandas Dataframes.  

        Returns:
            List[pd.DataFrame]: List of sentences dataframes.
        """
        # Sentences in english
        eng_sen = pd.read_csv(self.eng_sen_filepath, 
                              sep='\t',
                              names=["id", "lang", "text", "date_last_modified"])
        
        # Sentences in all languages with audio
        audio_sen = pd.read_csv(self.audio_sen_filepath, 
                                sep='\t',
                                names = ['id', 'audio_id', 'username', 
                                         'license', 'attribution_url'])
        
        # English sentences with spanish translations
        engspa_trans = pd.read_csv(self.eng_spa_pairs_filepath,
                                   sep='\t',
                                   usecols=range(4),
                                   names=['eng_id', 'eng_text', 'spa_id', 
                                          'spa_text'])
        
        return [eng_sen, audio_sen, engspa_trans]
    
    def sentences_with_audio(self, eng_sen:pd.DataFrame, 
                             audio_sen:pd.DataFrame)->pd.DataFrame:
        """Extract sentences in english that also have audio.

        Args:
            eng_sen (pd.DataFrame): English sentences.
            audio_sen (pd.DataFrame): Sentences with audio.

        Returns:
            pd.DataFrame: English sentences with audio.
        """
        # Remove entries for sentences with audio that don't have a license
        audio_sen = audio_sen[audio_sen['license'].notna()]
        
        # Extract id of english sentences as a list
        id_english = eng_sen['id'].values.tolist()
        
        # Extract sentences with audio that are in english
        eng_audio_sen = audio_sen[audio_sen['id'].isin(id_english)]
        
        return eng_audio_sen
    
    def english_spanish_pairs_with_audio(self, engspa_pairs:pd.DataFrame, 
                                         eng_audio_sen:pd.DataFrame)->pd.DataFrame:
        """Extract english - spanish sentence pairs that also have audio.

        Args:
            engspa_pairs (pd.DataFrame): English - spanish sentence pairs.
            eng_audio_sen (pd.DataFrame): English sentences with audio.

        Returns:
            pd.DataFrame: English - spanish sentence pairs with audio.
        """
        # Extract english sentences with audio ids
        eng_audio_ids = eng_audio_sen['id'].values.tolist()
        
        # Select only those translated sentences that also have audio
        engspa_pairs = engspa_pairs[engspa_pairs['eng_id'].isin(eng_audio_ids)]
        
        # Drop entries with duplicated english id 
        engspa_pairs = engspa_pairs[engspa_pairs.duplicated('eng_id', keep='first') != True]
        
        # Sort the data entries by english sentence id 
        engspa_pairs = engspa_pairs.sort_values(by='eng_id')
        
        return engspa_pairs
    
    def unite_datasets(self, engspa_pairs:pd.DataFrame, 
                       eng_audio_sen:pd.DataFrame)->pd.DataFrame:
        """Create a final dataframe with sentences in english, their spanish
        translation and audio id.

        Args:
            engspa_pairs (pd.DataFrame): English - spanish sentence pairs.
            eng_audio_sen (pd.DataFrame): English sentences with audio.

        Returns:
            pd.DataFrame: English spanish sentence pairs with audio.
        """
        # Extract ids of valid translated sentences
        engspa_ids = engspa_pairs['eng_id'].values.tolist()
        
        # Retrieve the audio links of the english sentences with translation
        engspa_audios = eng_audio_sen[eng_audio_sen['id'].isin(engspa_ids)]
        
        # Drop entries with duplicated english id 
        engspa_audios = engspa_audios[engspa_audios.duplicated('id', keep='first') != True]
        
        # Sort the entries by english id
        engspa_audios = engspa_audios.sort_values(by='id')
        
        # Create a new dataframe with sentence, translation and audio link
        data = {
            'eng_id': engspa_pairs['eng_id'].values,
            'eng_sen': engspa_pairs['eng_text'].values,
            'spa_id': engspa_pairs['spa_id'].values,
            'spa_sen': engspa_pairs['spa_text'].values,
            'audio_id': engspa_audios['audio_id'].values
        }
        
        return pd.DataFrame(data=data)
    
    def get_sentences_df(self)->pd.DataFrame:
        """Retrieve english sentences with spanish translation and audio. The
        datframe has the following data (in this order):
        - `eng_id`: English sentence Tatoeba id.
        - `eng_sen`: English sentence text.
        - `spa_id`: Spanish sentence Tatoeba id.
        - `spa_sen`: Spanish sentence translation text.
        - `audio_id`: English sentence audio file Tatoeba id.

        Returns:
            pd.DataFrame
        """
        eng_sen, audio_sen, engspa_pairs = self.load_datasets()
        eng_audio_sen = self.sentences_with_audio(eng_sen, audio_sen)
        engspa_audio = self.english_spanish_pairs_with_audio(engspa_pairs, 
                                                             eng_audio_sen)
        united_dataset = self.unite_datasets(engspa_audio, eng_audio_sen)
        return united_dataset
    
    def get_sentences_csv(self, filepath:str="tatoeba_sentences.csv")->None:
        """Get a comma separated csv file of the english sentences with 
        spanish translation and audio.

        Args:
            filepath (str, optional): Filepath to save file to. Defaults to 
            "`tatoeba_sentences.csv`".
        """
        
        clean_sentences = self.get_sentences_df()
        clean_sentences.to_csv(filepath, index=False)
        
    def df_to_jsonl(self, df:pd.DataFrame)->None:
        """Write every row in a dataframe as its own json object to a JSONL file.

        Args:
            df (pd.DataFrame): Dataframe to turn into JSONL
        """
        # Dictionary for all instances
        instances = list()
        columns = df.columns.tolist()
        
        for instance in df.values.tolist():
            # Dictionary for individual instance
            instance_dict = dict()
            
            for key, value in zip(columns, instance):
                instance_dict[key] = value
                
            instances.append(instance_dict)
            
        # Create json object of all instances
        json_object = json.dumps(instances)
 
        # Writing to jsonl file
        with open(self.json_filepath, "w") as outfile:
            outfile.write(json_object + "\n")
        
        
    def get_sentences_jsonl(self, filepath:str="tatoeba_sentences.jsonl")->None:
        """Get a jsonl file of the english sentences with spanish translation 
        and audio.

        Args:
            filepath (str, optional): Filepath to save file to. Defaults to 
            "`tatoeba_sentences.jsonl`".
        """
        self.json_filepath = filepath
        clean_sentences = self.get_sentences_df()
        self.df_to_jsonl(clean_sentences)
        
        
        