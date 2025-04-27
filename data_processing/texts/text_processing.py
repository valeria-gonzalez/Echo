import os
import shutil
from typing import Generator, List
from pydub import AudioSegment

class LibriSpeechProcessor:
    def __init__(self, corpus_directory):
        self.corpus_directory = corpus_directory
        
    def extract_chapter_directories(self)->list[str]:
        """ Get all chapters from the root directory. 

        Args:
            root_directory (str): Path to the root directory

        Returns:
            list[str]: List of paths to chapters
        """   
        chapters = []
        
        for act_root, sub_dirs, files in os.walk(self.corpus_directory):
            if not sub_dirs:
                chapters.append(act_root)
                
        return chapters
    
    def group_chapters(self, list_of_chapters:List[str], 
                       length_group:int)->Generator[List, None, None]:
        
        """Splits the list of chapters into groups of a specified length.

        Args:
            list_of_chapters (List[str]): List of chapters to be grouped
            length_group (int): Length of each group

        Yields:
            Generator[List, None, None]: Generator yielding groups of chapters
        """    
        for i in range(0, len(list_of_chapters), length_group):
            yield list_of_chapters[i:i + length_group]
            
    def move_chapters(self, groups:list[str], dest_directory:str,
                      verbose:bool=False)->None:
        """ Moves each chapter into a new directory structure under a
        destination path.

        Args:
            groups (list[str]): List of groups of chapters
            dest_directory (str): Path to the destination directory
            verbose (bool): Indicator for terminal messages. Defaults to False.
        """    
        os.makedirs(dest_directory, exist_ok=True)
        
        # Move each group of chapters to a new directory
        for i, group in enumerate(groups):
            group_name = f"group_{i+1}"
            dest_group = os.path.join(dest_directory, group_name)
            os.makedirs(dest_group, exist_ok=True)
            
            # Move each chapter in the group to the new directory
            for chapter in group:
                name_chapter = os.path.basename(chapter)
                new_directory = os.path.join(dest_group, name_chapter) 
                shutil.copytree(chapter, new_directory)
                if verbose: print(f"Moved {chapter} to {new_directory}")
                
            if verbose: print(f"\nGroup {i + 1} completed ({len(group)} chapters) in {dest_group}.\n")
    
    def create_chapters_directory(self, amount_of_chapters:int, dest_directory:str,
                                  verbose:bool=False)->None:
        """Create a directory at `dest_directory` that contains a certain 
        `amount_of_chapters` subdirectories. 

        Args:
            amount_of_chapters (int): Amount of chapters to extract.
            dest_directory (str): Destination directory for chapters subdirectories.
            verbose (bool): Indicator for terminal messages. Defaults to False.
        """
        chapters = self.extract_chapter_directories()
        chapter_groups = list(self.group_chapters(chapters, amount_of_chapters))
        self.move_chapters(chapter_groups, dest_directory, verbose)
    
         