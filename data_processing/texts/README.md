# 📁 LibriSpeech Chapter Grouper and Segmenter

## Objective

In order to provide practice texts for the project, relevant information pertaining to english texts provided by the LibriSpeech corpus must be extracted and saved into a single file.

The needed information for a text is the following:

- English text
- Audio file (max 30s)
- Transcript
- Book origin

This module preprocesses audio data from the [LibriSpeech](http://www.openslr.org/12) dataset by segmenting each chapter’s audio files into 30-second chunks with their corresponding transcriptions.

## What is LibriSpeech?

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

This module organizes LibriSpeech chapter folders into groups of N elements (e.g., 100 chapters per group) and moves them into a target directory.

Its first callable method `create_chapters_directory`:

- Takes a list of chapter folders.
- Groups them into chunks of specified size.
- Moves them into `group_1`, `group_2`, etc., under a new parent folder.

### Folder Structure

```
LibriSpeech/
├── dev-clean/
│   ├── chapter1/
│   ├── chapter2/
│   └── ...
```

Its second callable method `process_all_chapters`:

- Loads a transcription `.txt` file where each line is in the format `<AUDIO_ID> <TRANSCRIPTION>`.
- Iterates through each audio file in a chapter.
- Concatenates audio files until reaching a 30-second segment (max).
- Saves each audio segment and its corresponding transcriptions into a new folder.

## 🧪 Requirements

- Python 3.7+
- [`pydub`](https://github.com/jiaaro/pydub) (used for manipulating audio)

### 🔧 Installation

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

## ▶️ Usage

### Step 1: Group Chapters

```python
from text_processing import LibriSpeechProcessor

def main():
    dest_directory = "datasets/chapters"
    
    processor = LibriSpeechProcessor(
        corpus_directory="datasets/LibriSpeech/dev-clean"
    )

    # Extract and group chapters
    processor.create_chapters_directory(
        group_length=100,
        dest_directory=dest_directory,
        verbose=False
    )

if __name__ == "__main__":
    main()
```

### Step 2: Segment Audio + Generate Transcriptions

```python
root_dir = "groups/group_1/"
dest_dir = "processed_segments/"

os.makedirs(dest_dir, exist_ok=True)
process_all_chapters(root_dir, dest_dir)
```

Each segment will contain up to 30 seconds of audio and a `.txt` file with aligned transcriptions and timestamps.

## ✨ Output Example (Transcription)

```
0: 84-121550-0000 [0.00s - 3.20s]: THE DOCTOR SEEMED DETERMINED TO MAKE HIMSELF DISAGREEABLE
1: 84-121550-0001 [3.20s - 6.45s]: HE SHOWED NO CONCERN FOR MY SUFFERINGS
...
```

## 📌 Notes

- The scripts expect that `.flac` audio files and one transcription `.txt` file are present in each chapter folder.
- Only audio files with matching transcription IDs will be included in the output.

