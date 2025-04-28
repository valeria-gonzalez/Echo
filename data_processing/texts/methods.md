# LibriSpeechProcessor methods descriptions

## extract_chapter_directories

```text
Get all chapters from the root directory. 

Args:
    root_directory (str): Path to the root directory

Returns:
    list[str]: List of paths to chapters  
```

The `extract_chapter_directories` function takes the root directory of a dataset and returns all directories that do not have subdirectories (final chapter directories). Here's an example:

**Root directory structure:**
```text
datasets/
└── LibriSpeech/
    └── dev-clean/
        ├── 1272/
        │   ├── 128104/
        │   └── 128105/
        └── 1988/
            ├── 147956/
            └── 147957/
```
**Would return:**
```text
[
    'datasets/LibriSpeech/dev-clean/1272/128104',
    'datasets/LibriSpeech/dev-clean/1272/128105',
    'datasets/LibriSpeech/dev-clean/1988/147956',
    'datasets/LibriSpeech/dev-clean/1988/147957'
]
```

## group_chapters

```text
Splits the list of chapters into groups of a specified length.

Args:
    list_of_chapters (List[str]): List of chapters to be grouped
    length_group (int): Length of each group

Yields:
    Generator[List, None, None]: Generator yielding groups of chapters
```

The `group_chapters` function takes a list of chapters and splits it into groups of a specified length.

Assume you have the following list of chapter paths:

```text
[
    'datasets/LibriSpeech/dev-clean/1272/128104',
    'datasets/LibriSpeech/dev-clean/1272/128105',
    'datasets/LibriSpeech/dev-clean/1988/147956',
    'datasets/LibriSpeech/dev-clean/1988/147957',
    'datasets/LibriSpeech/dev-clean/2010/128202'
]
```
calling the `group_chapters(list_of_chapters, 2)` **would return:**

```text
[
    ['datasets/LibriSpeech/dev-clean/1272/128104', 'datasets/LibriSpeech/dev-clean/1272/128105'],
    ['datasets/LibriSpeech/dev-clean/1988/147956', 'datasets/LibriSpeech/dev-clean/1988/147957'],
    ['datasets/LibriSpeech/dev-clean/2010/128202']
]
```
## move_chapters

```text
Moves each chapter into a new directory structure under a destination path.

 Args:
    groups (list[str]): List of groups of chapters
    dest_directory (str): Path to the destination directory
    verbose (bool): Indicator for terminal messages. Defaults to False.
```

The `move_chapters` function takes a list of grouped chapter paths and moves 
each chapter into a new directory structure under a destination path.

Assume the following input:
```text
[
    ['datasets/LibriSpeech/dev-clean/1272/128104', 'datasets/LibriSpeech/dev-clean/1272/128105'],
    ['datasets/LibriSpeech/dev-clean/1988/147956', 'datasets/LibriSpeech/dev-clean/1988/147957'],
    ['datasets/LibriSpeech/dev-clean/2010/128202']
]
```
Calling `move_chapters(groups, dest_directory)` **would return:**
```text
datasets/
└── LibriSpeech/
    └── chapter-groups/
        ├── group_1/
        │   ├── 128104/
        │   └── 128105/
        └── group_2/
            ├── 147956/
            └── 147957/
```

## map_book_to_chapter

```text
A function to create a mapping between chapter IDs and book titles.

Returns:
    dict: A dictionary mapping chapter IDs to book titles.
    verbose (bool): Indicator for terminal messages. Defaults to False.
```

The `map_book_chapter` function reads two text files: one containing book information and another with chapter metadata. It creates a mapping between each chapter ID and its corresponding book title.

**Given:**
`books.txt`
```txt
1001 | The Adventures of Sherlock Holmes
1002 | Pride and Prejudice
```
`chapters.txt`
```text
128104 | 1272 | ... | ... | ... | 1001 | A Scandal in Bohemia
128105 | 1272 | ... | ... | ... | 1001 | The Red-Headed League
147956 | 1988 | ... | ... | ... | 1002 | Chapter 1
```

Calling `map_book_to_chapter("books.txt", "chapters.txt")` **would return:**

```text
{
    "128104": "The Adventures of Sherlock Holmes - (A Scandal in Bohemia)",
    "128105": "The Adventures of Sherlock Holmes - (The Red-Headed League)",
    "147956": "Pride and Prejudice - (Chapter 1)"
}
```

## map_audio_transcript

```text
This function converts a transcription file into a dictionary.

Args:
    transcript_filepath (str): Path to the transcription file

Returns:
    dict: Dictionary with audio IDs as keys and their corresponding text as values  
```

The `map_audio_transcript` function reads a transcription text file 
where each line starts with an audio ID followed by its corresponding 
transcription. It returns a dictionary that maps each audio ID to its 
transcription text.

**Given:**
`transcriptions.txt`
```text
1272-128104-0000 THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG
1272-128104-0001 HELLO WORLD
1272-128104-0002 THIS IS A TEST
```

Calling `map_audio_transcript("transcript.txt")` **would return:**
```text
{
    "1272-128104-0000": "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG",
    "1272-128104-0001": "HELLO WORLD",
    "1272-128104-0002": "THIS IS A TEST"
}
```

## combine_chapter_audios

```text
Combine all audio files in a chapter into 30 second audio files and creating their corresponding transcription files.

Args:
    chapter_filepath (str): path to the chapter directory
    transcript_filepath (str): path to the transcription file
    dest_dir (str): path to the destination directory for the segments
    audio_length (float): Duration in seconds of combined audio segments. Defaults to 30s.   
```

The `combine_chapter_audios` function takes a chapter directory containing .flac audio files and a transcription file, and splits the audio into segments of up to 30 seconds. For each segment, it creates a .flac file and a corresponding .txt file with timestamped transcriptions. It also includes the book title (retrieved using the chapter_to_book dictionary) at the top of the transcription.

Suppose that you have: A folder chap_001 with audio files like:

```text
1272-128104-0000.flac
1272-128104-0001.flac
1272-128104-0002.flac
```

A transcription file chap_001.txt like:

```text
1272-128104-0000 THE QUICK BROWN FOX
1272-128104-0001 JUMPS OVER THE LAZY DOG
1272-128104-0002 HELLO WORLD
```

A mapping dictionary:

```python
chapter_to_book = {
    "chap_001": "English Stories - (Chapter One)"
}
```

Calling `process_chapter("chap_001", "chap_001.txt", "processed_chapters" chapter_to_book)` would return:

A new folder audio_segments/chap_001 containing:
- segment_0.flac
- segment_0.txt
Where the .txt might look like:

Book title: English Stories - (Chapter One)

```text
0: 1272-128104-0000 [0.00s - 4.23s]: THE QUICK BROWN FOX
1: 1272-128104-0001 [4.23s - 7.89s]: JUMPS OVER THE LAZY DOG
2: 1272-128104-0002 [7.89s - 10.52s]: HELLO WORLD
```

## combine_chapter_group_audios

```text
For every chapter in a chapter group, combine all audio files in a chapter into 30 second audio files and create their corresponding transcription files. Returns every processed chapter in a new directory.

Args:
    chapter_group_dir (str): path to the directory containing chapter subdirectories
    dest_dir (str): path to the destination directory to store the  processed chapters
    audio_length (float): Duration in seconds of combined audio segments. Defaults to 30s.
    verbose (bool): Indicator for terminal messages. Defaults to False.
```

The `combine_chapter_group_audios` function iterates over a root directory containing 
multiple chapter folders. For each chapter, it identifies the corresponding transcription file and processes the audio and transcription using 
the process_chapter function.

Given:

```text
root_dir/
├── 1272_128104/
│   ├── 0000.flac
│   ├── 0001.flac
│   └── 1272_128104.txt
├── 1272_128105/
│   ├── 0000.flac
│   └── 1272_128105.txt
```

Calling `combine_chapter_group_audios("root_dir", "processed")` **would result in:**

- The function going through each chapter folder inside root_dir
- It will find the .txt transcription file
- Then it will call process_chapter to generate audio segments and 
transcription .txt files
- The resulting files will be stored in a new folder audio_segments/chap_001, audio_segments/chap_002, etc.

## get_texts_jsonl

The `get_texts_jsonl` function reads a JSON file containing multiple chapters, each with several transcripts. It iterates over all the chapters, selecting one transcript per chapter at a time. until it collects a total of 100 transcripts.

Given a data.json file like this:
```json
[
    {
        "chapter_id": "chap_001",
        "book_title": "Book One",
        "transcript": ["line 1", "line 2", "line 3"]
    },
    {
        "chapter_id": "chap_002",
        "book_title": "Book Two",
        "transcript": ["line 1", "line 2"]
    }
]
```
Calling `get_texts_jsonl("data.json", "output_dir")` will:

- Read all chapters from data.json
- Pick the first transcript from each chapter
- Then the second one, and so on, looping through chapters
- Stop once 100 total transcript have been added to the new JSON file
- Save the output to new dir and new JSON file.