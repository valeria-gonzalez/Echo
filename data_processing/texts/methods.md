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