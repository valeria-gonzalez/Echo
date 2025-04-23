# 📁 LibriSpeech Chapter Grouper and Segmenter

This project contains two Python scripts designed to help preprocess audio data from the [LibriSpeech](http://www.openslr.org/12) dataset. The scripts organize the dataset into manageable groups and segment each chapter’s audio files into 30-second chunks with their corresponding transcriptions.

---

## 📜 Overview

### 1. `get_group_chapters.ipynb`

This script organizes LibriSpeech chapter folders into groups of N elements (e.g., 100 chapters per group) and moves them into a target directory.

#### What it does:

- Takes a list of chapter folders.
- Groups them into chunks of specified size.
- Moves them into `group_1`, `group_2`, etc., under a new parent folder.

### 2. `get_new_audios.ipynb`

This script:

- Loads a transcription `.txt` file where each line is in the format `<AUDIO_ID> <TRANSCRIPTION>`.
- Iterates through each audio file in a chapter.
- Concatenates audio files until reaching a 30-second segment (max).
- Saves each audio segment and its corresponding transcriptions into a new folder.

---

## 🧪 Requirements

- Python 3.7+
- [`pydub`](https://github.com/jiaaro/pydub) (used for manipulating audio)

### 🔧 Installation

Install the required dependencies:

```bash
pip install pydub
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

---

## 📂 Folder Structure

```
LibriSpeech/
├── dev-clean/
│   ├── chapter1/
│   ├── chapter2/
│   └── ...
```

---

## ▶️ Usage

### Step 1: Group Chapters

```python
rootDirectory = "LibriSpeech/dev-clean/"
destDirectory = "groups/"

chapters = getChapters(rootDirectory)
groups = list(getGroups(chapters, 100))  # Group size
moveChaptersInGroups(groups, destDirectory)
```

### Step 2: Segment Audio + Generate Transcriptions

```python
root_dir = "groups/group_1/"
dest_dir = "processed_segments/"

os.makedirs(dest_dir, exist_ok=True)
process_all_chapters(root_dir, dest_dir)
```

Each segment will contain up to 30 seconds of audio and a `.txt` file with aligned transcriptions and timestamps.

---

## ✨ Output Example (Transcription)

```
0: 84-121550-0000 [0.00s - 3.20s]: THE DOCTOR SEEMED DETERMINED TO MAKE HIMSELF DISAGREEABLE
1: 84-121550-0001 [3.20s - 6.45s]: HE SHOWED NO CONCERN FOR MY SUFFERINGS
...
```

---

## 📌 Notes

- The scripts expect that `.flac` audio files and one transcription `.txt` file are present in each chapter folder.
- Only audio files with matching transcription IDs will be included in the output.

---

## 📬 License

MIT License. Feel free to modify or reuse!
