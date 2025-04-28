# LibriSpeechProcessor methods descriptions

## extract_chapter_directories

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

The `combine_chapter_audios` function takes a chapter directory containing .flac audio 
files and a transcription file, and splits the audio into segments of up to 30 
seconds. For each segment, it creates a .flac file and a corresponding .txt 
file with timestamped transcriptions. It also includes the book title 
(retrieved using the chapter_to_book dictionary) at the top of the 
transcription.

Suppose that you have:
**A folder chap_001** with audio files like:
```text
1272-128104-0000.flac
1272-128104-0001.flac
1272-128104-0002.flac
```
A transcription file **chap_001.txt** like:
```text
1272-128104-0000 THE QUICK BROWN FOX
1272-128104-0001 JUMPS OVER THE LAZY DOG
1272-128104-0002 HELLO WORLD
```

A mapping dictionary:
```text
chapter_to_book = {
    "chap_001": "English Stories - (Chapter One)"
}
```
Calling `Segment_chapter_audios("chap_001", "chap_001.txt", "processed_chapters" chapter_to_book)` **would return:**

* A new folder `audio_segments/chap_001` containing:
- * segment_0.flac
- * segment_0.txt

Where the `.txt` might look like:
```text
Book title: English Stories - (Chapter One)

0: 1272-128104-0000 [0.00s - 4.23s]: THE QUICK BROWN FOX
1: 1272-128104-0001 [4.23s - 7.89s]: JUMPS OVER THE LAZY DOG
2: 1272-128104-0002 [7.89s - 10.52s]: HELLO WORLD
```
## combine_chapter_group_audios

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
