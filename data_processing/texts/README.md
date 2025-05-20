# 📁 LibriSpeech Chapter Grouper and Audio Combiner

## 📚 Objective

In order to provide practice texts for the project, relevant information pertaining to english texts provided by the LibriSpeech corpus must be extracted and saved into a single file.

The needed information for a text is the following:

- English text
- Audio file (max 30s)
- Transcript
- Book origin

This module preprocesses audio data from the [LibriSpeech](http://www.openslr.org/12) dataset by segmenting each chapter’s audio files into 30-second chunks with their corresponding transcriptions.

## 🌐 What is LibriSpeech?

LibriSpeech is a corpus of approximately 1000 hours of 16kHz read English speech, prepared by Vassil Panayotov with the assistance of Daniel Povey. The data is derived from read audiobooks from the LibriVox project, and has been carefully segmented and aligned.

Special thanks and acknowledgments to LibriSpeech.

[Click here for more information](https://www.openslr.org/12).

## 📂 Dataset description
The purpose of this corpus is to enable the training and testing of automatic speech recognition(ASR) systems. It's split into different parts, for this project, the information in the directory `dev-clean`is used.

When extracted, the corpus re-creates LibriSpeech's root directory, containing some metadata, and a dedicated subdirectory for the subset itself. The audio for each individual speaker is stored under a dedicated subdirectory in the subset's directory, and each audio chapter read by this speaker is stored in separate subsubdirectory. The following ASCII diagram depicts the directory structure:

```
<corpus root>
    |
    .- README.TXT
    |
    .- READERS.TXT
    |
    .- CHAPTERS.TXT
    |
    .- BOOKS.TXT
    |
    .- train-clean-100/
                   |
                   .- 19/
                       |
                       .- 198/
                       |    |
                       |    .- 19-198.trans.txt
                       |    |    
                       |    .- 19-198-0001.flac
                       |    |
                       |    .- 14-208-0002.flac
                       |    |
                       |    ...
                       |
                       .- 227/
                            | ...
```
, where 19 is the ID of the reader, and 198 and 227 are the IDs of the chapters
read by this speaker. The *.trans.txt files contain the transcripts for each
of the utterances, derived from the respective chapter and the FLAC files contain
the audio itself.

The main metainfo about the speech is listed in the READERS and the CHAPTERS:

- READERS.TXT contains information about speaker's gender and total amount of audio in the corpus.

- CHAPTERS.TXT has information about the per-chapter audio durations.

- BOOKS.TXT contains the title for each book, whose text is used in the corpus, and its Project Gutenberg ID.

## 📜 Overview

This module:
- Organizes LibriSpeech chapter folders into groups of N elements (e.g., 100 chapters per group) and moves them into a target directory. 

- Processes each chapter by combining all the audio files into larger audios of specific length and generating their transcription files.

- Creates structured JSON and JSONL files with the information of the collected chapters in the form of dictionaries with the chapter id, english text, transcript, audio file name and book name.

## ⚙️⚙️ Requirements

### 🔧 Installation

- Python 3.7+

Install the required dependencies:

```bash
pip install pydub
pip install shutil
pip install os
```

Also make sure you have `ffmpeg` installed and accessible via system path. You can install it via:

**On Ubuntu/Debian:**

```bash
sudo apt install ffmpeg
```

**On macOS (with Homebrew):**

```bash
brew install ffmpeg
```

**On Windows:**

- Download from: https://ffmpeg.org/download.html
- Add the `bin/` folder to your system PATH.


### 🗄️ Required files

In order to use this module, please download LibriSpeech corpus from the page link mentioned above.

Needed file:

 - `dev-clean.tar.gz`

## 🚀 Usage

```python
from text_processing import LibriSpeechProcessor

def main():
    
    processor = LibriSpeechProcessor(
        corpus_directory="datasets/LibriSpeech/dev-clean",
        books_txt_filepath="datasets/LibriSpeech/BOOKS.TXT",
        chapters_txt_filepath="datasets/LibriSpeech/CHAPTERS.TXT"
    )
    
    # Extract chapters in groups
    chapters_dest_directory = "datasets/chapters"
    processor.create_chapters_directory(amount_of_chapters=100, 
                                        dest_directory=chapters_dest_directory,
                                        verbose=True)
    
    # Create 30s audios for each chapter and json file for all chapters
    chapters_directory = "datasets/chapters/group_1"
    audio_dest_directory = "datasets/audio_segments"
    processor.combine_chapter_group_audios(chapters_directory, 
                                           audio_dest_directory,
                                           audio_length=30,
                                           verbose=True)
    
    # Create JSONL file for specified chapter directory
    json_filepath = "datasets/chapters/group_1_audios/texts.json"
    jsonl_filepath = "datasets/chapters/group_1_texts.jsonl"
    processor.get_texts_jsonl(json_filepath, jsonl_filepath, verbose=True)
    
if __name__ == "__main__":
    main()
```

### Step 1: Group Chapters
```python
chapters_dest_directory = "datasets/chapters"
    processor.create_chapters_directory(amount_of_chapters=100, 
                                        dest_directory=chapters_dest_directory,
                                        verbose=True)
```

### Step 2: Segment Audio + Generate Transcriptions + JSON

```python
chapters_directory = "datasets/chapters/group_1"
audio_dest_directory = "datasets/audio_segments"
processor.combine_chapter_group_audios(chapters_directory, 
                                        audio_dest_directory,
                                        audio_length=30,
                                        verbose=True)
```

Each segment will contain up to `audio_length` seconds of audio and a `.txt` file with aligned transcriptions and timestamps.

### Step 3: Create JSONL file with specific amount of chapters

```python
# Create JSONL file for specified chapter directory
json_filepath = "datasets/chapters/group_1_audios/texts.json"
jsonl_filepath = "datasets/chapters/group_1_texts.jsonl"
processor.get_texts_jsonl(json_filepath, jsonl_filepath, verbose=True)
```

## ✨ Results

### create_chapters_directory

The first callable method `create_chapters_directory`:

- Takes a list of chapter folders.
- Groups them into chunks of specified size.
- Moves them into `group_1`, `group_2`, etc., under a new parent folder.

This is the resulting file structure: 

```
chapters/
├── group_1/
│   ├── chapterid/
│   ├── chapterid/
│   └── ...
├── group_2/
│   ├── chapterid/
│   ├── chapterid/
│   └── ...
```
### combine_chapter_group_audios

The second callable method `combine_chapter_group_audios`:

- Reads a `.txt` transcription file in the format `<AUDIO_ID> <TRANSCRIPTION>`.
- Iterates through all audio files in each chapter directory.
- Concatenates short audio files into 30 seconds chunks (max).
- Saves each audio segment and generates matching `.txt` transcription files with timestamps.

This is the resulting file structure: 

```
audio_segments/
├── chapterid/
│   ├── segment_0.flac
│   ├── segment_0.txt
│   ├── segment_1.flac
│   ├── segment_1.txt
│   └── ...
├── chapterid/
│   ├── segment_0.flac
│   ├── segment_0.txt
│   └── ...
```

Example of a generated transcript.

```
0: 84-121550-0000 [0.00s - 3.20s]: THE DOCTOR SEEMED DETERMINED TO MAKE HIMSELF DISAGREEABLE
1: 84-121550-0001 [3.20s - 6.45s]: HE SHOWED NO CONCERN FOR MY SUFFERINGS
...
```

This function also generates the following files:

- A `all_segments.json` file with full chapter data
- A `hundred_segments.jsonl` file for sampling one transcription per chapter

### Final JSONL file description

The following examples are for 20 second audios.

- **all_segments.json**:
  A full JSON file containing all chapter IDs, book titles, chapter names, and
  their corresponding transcriptions.

```json
[
    {
        "chapter_id": "141231",
        "book_name": "Planet of the Damned - (Chapter 01)",
        "transcript": [
            {
                "audio_file": "segment_0.flac",
                "duration": 11.19,
                "text_lines": [
                    "1272-141231-0000 [0.00s - 4.65s]: A MAN SAID TO THE UNIVERSE SIR I EXIST",
                    "1272-141231-0001 [4.65s - 11.19s]: SWEAT COVERED BRION'S BODY TRICKLING INTO THE TIGHT LOINCLOTH THAT WAS THE ONLY GARMENT HE WORE"
                ],
                "full_text": "A MAN SAID TO THE UNIVERSE SIR I EXIST SWEAT COVERED BRION'S BODY TRICKLING INTO THE TIGHT LOINCLOTH THAT WAS THE ONLY GARMENT HE WORE"
            },
            {
                "audio_file": "segment_1.flac",
                "duration": 18.75,
                "text_lines": [
                    "1272-141231-0002 [0.00s - 13.34s]: THE CUT ON HIS CHEST STILL DRIPPING BLOOD THE ACHE OF HIS OVERSTRAINED EYES EVEN THE SOARING ARENA AROUND HIM WITH THE THOUSANDS OF SPECTATORS WERE TRIVIALITIES NOT WORTH THINKING ABOUT",
                    "1272-141231-0003 [13.34s - 18.75s]: HIS INSTANT OF PANIC WAS FOLLOWED BY A SMALL SHARP BLOW HIGH ON HIS CHEST"
                ],
                "full_text": "THE CUT ON HIS CHEST STILL DRIPPING BLOOD THE ACHE OF HIS OVERSTRAINED EYES EVEN THE SOARING ARENA AROUND HIM WITH THE THOUSANDS OF SPECTATORS WERE TRIVIALITIES NOT WORTH THINKING ABOUT HIS INSTANT OF PANIC WAS FOLLOWED BY A SMALL SHARP BLOW HIGH ON HIS CHEST"
            },
            ...
        ]
    }
]
```

- **data.jsonl**:
  A JSON Lines file, that is a list of dictionaries where each dicitonary contains the information for an audio extracted from a chapter. The script collects one audio per chapter, repeating across chapters until reaching 100 entries.

The json file is an array of json objects with the following keys.

- `chapter_id`: (int) Id of the chapter being read in the LibriSpeech database.
- `book_title`: (str) Title of the chapter being read corresponding to the text.
- `transcript`: (dict) Dictionary that contains the transcript information for the text. It has the following sub keys:
  - `audio_file`: (str) Name of the `.flac` file containing the audio reading of the text.
  - `duration`: (float) Duration in seconds of the audio.
  - `text_lines`: (array of str) Contains an array of strings corresponding to the transcript by time for the audio. It contains the audio file id, the seconds timestamp and the text line.
  - `full_text`: (str) Contains the full text being read.

This is an example of the JSON object:

```json
{
    "chapter_id": "141231", 
    "book_title": "Planet of the Damned - (Chapter 01)", 
    "transcript": {
        "audio_file": "segment_0.flac", 
        "duration": 11.19, 
        "text_lines": [
            "1272-141231-0000 [0.00s - 4.65s]: A MAN SAID TO THE UNIVERSE SIR I EXIST", 
            "1272-141231-0001 [4.65s - 11.19s]: SWEAT COVERED BRION'S BODY TRICKLING INTO THE TIGHT LOINCLOTH THAT WAS THE ONLY GARMENT HE WORE"
        ], 
        "full_text": "A MAN SAID TO THE UNIVERSE SIR I EXIST SWEAT COVERED BRION'S BODY TRICKLING INTO THE TIGHT LOINCLOTH THAT WAS THE ONLY GARMENT HE WORE"
    }
}
```

Example of the file as a `JSONL`:

```jsonl
[{"chapter_id": "141231", "book_title": "Planet of the Damned - (Chapter 01)", "transcript": {"audio_file": "segment_0.flac", "duration": 11.19, "text_lines": ["1272-141231-0000 [0.00s - 4.65s]: A MAN SAID TO THE UNIVERSE SIR I EXIST", "1272-141231-0001 [4.65s - 11.19s]: SWEAT COVERED BRION'S BODY TRICKLING INTO THE TIGHT LOINCLOTH THAT WAS THE ONLY GARMENT HE WORE"], "full_text": "A MAN SAID TO THE UNIVERSE SIR I EXIST SWEAT COVERED BRION'S BODY TRICKLING INTO THE TIGHT LOINCLOTH THAT WAS THE ONLY GARMENT HE WORE"}}]
```

## 📌 Notes

- The scripts expect that `.flac` audio files and one transcription `.txt` file are present in each chapter folder.
- Only audio files with matching transcription IDs will be included in the output.

