import os
import shutil
from typing import Generator, List
from pydub import AudioSegment

class LibriSpeechProcessor:
    def __init__(self, corpus_directory:str, books_txt_filepath:str,
                 chapters_txt_filepath:str):
        self.corpus_directory = corpus_directory
        self.books_txt_filepath = books_txt_filepath
        self.chapters_txt_filepath = chapters_txt_filepath
        self.dest_directory = None
        self.chapter_to_book = None
        
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
        self.dest_directory = dest_directory
        chapters = self.extract_chapter_directories()
        chapter_groups = list(self.group_chapters(chapters, amount_of_chapters))
        self.move_chapters(chapter_groups, dest_directory, verbose)
        
    def map_book_chapter(self, verbose:bool=False)->dict:
        """ A function to create a mapping between chapter IDs and book titles.

        Returns:
            dict: A dictionary mapping chapter IDs to book titles.
            verbose (bool): Indicator for terminal messages. Defaults to False.
        """    
        
        book_id_to_title = {}
        chapter_to_book = {}
        
        with open(self.books_txt_filepath, 'r', encoding='utf-8') as file:
            for line in file:
                if "|" in line:
                    parts = line.strip().split("|")
                    if len(parts) >= 2:
                        book_id = parts[0].strip()
                        title = parts[1].strip()
                        book_id_to_title[book_id] = title
                        
        with open(self.chapters_txt_filepath, 'r', encoding='utf-8') as file:
            for line in file:
                if "|" in line:
                    parts = [part.strip() for part in line.strip().split("|")]
                    if len(parts) >= 7:
                        chapter_id = parts[0]
                        book_id = parts[5]
                        chapter_title = parts[6]
                        book_title = book_id_to_title.get(book_id, "Unknown Book")
                        chapter_to_book[chapter_id] = f"{book_title} - ({chapter_title})"
                        if verbose: 
                            print(
                                f"Chapter ID: {chapter_id}, "
                                f"Book ID: {book_id}, " 
                                f"Book Title: {book_title}, "
                                f"Chapter Title: {chapter_title}"
                            )
                        
        return chapter_to_book
    
    def map_audio_transcript(self, transcript_filepath:str)->dict:
        """ This function converts a transcription file into a dictionary.

        Args:
            transcript_filepath (str): Path to the transcription file

        Returns:
            dict: Dictionary with audio IDs as keys and their corresponding text 
            as values
        """    
        trans = {}
        with open(transcript_filepath, 'r', encoding='utf-8') as file:
            for line in file:
                if line.strip():
                    # Separating the ID and the text
                    parts = line.strip().split(" ", 1) 
                    if len(parts) == 2:
                        id_audio, text = parts
                        trans[id_audio] = text
                        
        return trans
    
    def combine_chapter_audios(self, chapter_filepath:str, transcript_filepath:str, 
                               dest_dir:str, audio_length:float=30)->None:
        """ Combine all audio files in a chapter into 30 second audio files 
        and creating their corresponding transcription files.

        Args:
            chapter_filepath (str): path to the chapter directory
            transcript_filepath (str): path to the transcription file
            dest_dir (str): path to the destination directory for the segments
            audio_length (float): Duration in seconds of combined audio segments. 
            Defaults to 30s.
        """    
        trans = self.map_audio_transcript(transcript_filepath)
        # sorting the audio files to ensure they are processed in order
        audios = sorted([f for f in os.listdir(chapter_filepath) if f.endswith(".flac")])
        
        # Segment audio initialization
        act_segment = AudioSegment.empty()
        # List to store transcriptions for the current segment
        act_trans = []
        max_duration = audio_length * 1000
        # Duration accumulated in the current segment
        act_duration = 0
        count = 0
        
        # Create the directory for the chapter
        chapter_name = os.path.basename(chapter_filepath)
        dir_chapter = os.path.join(dest_dir, chapter_name)
        os.makedirs(dir_chapter, exist_ok=True)
        
        book_title = self.chapter_to_book.get(chapter_name, "Unknown Book")
        
        for audio in audios:
            # Delete the extension in the file
            id_audio = os.path.splitext(audio)[0]
            audio_route = os.path.join(chapter_filepath, audio)
            # Load the audio file
            actual_audio = AudioSegment.from_file(audio_route)
            duration = len(actual_audio)
            
            if len(act_segment) + len(actual_audio) > max_duration:
                name = f"segment_{count}"
                new_file_route = os.path.join(dir_chapter, name + ".flac")
                new_txt_route = os.path.join(dir_chapter, name + ".txt")
                # Export the new audio file
                act_segment.export(new_file_route, format="flac")
                
                # Write the new transcription file
                with open(new_txt_route, "w", encoding="utf-8") as file:
                    file.write(f"Book title: {book_title}\n\n")
                    for i, line in enumerate(act_trans):
                        file.write(f"{i}: {line}\n")
                
                # Reset the initialization for the next segment
                count += 1
                act_segment = AudioSegment.empty()
                act_trans = []
                act_duration = 0
                
            # Calculate the start and end time for the transcription
            start = act_duration
            end = act_duration + duration
            
            # Look for the transcription in the dictionary
            trans_line = trans.get(id_audio," ")
            act_trans.append(   f"{id_audio} "
                                f"[{start/1000:.2f}s - {end/1000:.2f}s]: "
                                f"{trans_line}"
                            )
            
            act_segment += actual_audio
            act_duration += duration
            
        # Export the last segment if it has any audio
        if len(act_segment) > 0:
            name = f"segment_{count}"
            new_file_route = os.path.join(dir_chapter, name + ".flac")
            new_txt_route = os.path.join(dir_chapter, name + ".txt")
            act_segment.export(new_file_route, format="flac")
                
            with open(new_txt_route, "w", encoding="utf-8") as file:
                file.write(f"Book title: {book_title}\n\n")
                for i, line in enumerate(act_trans):
                        file.write(f"{i}: {line}\n")
    
    def combine_chapter_group_audios(self, chapter_group_dir:str, dest_dir:str,
                                     audio_length:float=30, 
                                     verbose:bool=False)->None:
        """For every chapter in a chapter group, combine all audio files in a 
        chapter into 30 second audio files and create their corresponding 
        transcription files. Returns every processed chapter in a new directory.

        Args:
            chapter_group_dir (str): path to the directory containing chapter 
            subdirectories
            dest_dir (str): path to the destination directory to store the 
            processed chapters
            audio_length (float): Duration in seconds of combined audio segments. 
            Defaults to 30s.
            verbose (bool): Indicator for terminal messages. Defaults to False.
        """   
        os.makedirs(dest_dir, exist_ok=True) 
        self.chapter_to_book = self.map_book_chapter(verbose)
        
        for chapter in os.listdir(chapter_group_dir):
            chapter_path = os.path.join(chapter_group_dir, chapter)
            if os.path.isdir(chapter_path):
                file_txt = [f for f in os.listdir(chapter_path)
                            if f.endswith(".txt")]
                if file_txt:
                    transcript_txt = os.path.join(chapter_path, file_txt[0])
                    
                    self.combine_chapter_audios(chapter_path, 
                                                transcript_txt, 
                                                dest_dir,
                                                audio_length)
                    
                    if verbose: print(f"Processed chapter: {chapter}")