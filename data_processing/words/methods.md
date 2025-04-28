# Wikiextract Processor methods descriptions

## extract_word_from_json
```text
Extract the relevant keys for a word from a JSON object. The keys are: word, pos (part of speech), definitions, ipa, mp3_url, and translation.  

Args:
    obj (dict): JSON object.

Returns:
    dict: Dicitonary with word information.
```

This function takes a json object extracted when reading a non-empty line from the JSONL file and creates a dictionary with all the relevant information for a word.

The final dictionary has the following structure:

```text
word_obj = {
        "word": word,
        "pos" : part_of_speech,
        "definitions" : unique_definitions,
        "ipa": ipa,
        "mp3_url" : mp3_url,
        "translation" : spanish_translation,
    }
```

## accumulate_word

```text
Add an extracted word to the accumulated words dictonary.

Args:
    word_obj (dict): Dictionary with the word information.

Returns:
    None
```

The JSONL dump provides multiple entries for the same word, distinguishing each by their role in the part of speech (noun, adjective, verb, etc).

To avoid having multiple entries of the same word, this function groups different entries for the same word. For every different part of speech, its corresponding definitions are saved under it.

The structure for the final dictionary is as follows:

```text
word_dict = {
    word: {
        "definitions": {
            part_of_speech: [list of definitions]
        },
        "ipa": ipa,
        "mp3_url": mp3_url,
        "translations": [list of translations],
    }
}
```

## save_words_to_JSONL
This functions writes the accumulated words without repetition to a JSONL file.

```text
Write the accumulated words dictionary to a JSONL file. 

Args:
    None

Returns:
    None
```

## remove_incomplete_words

This function takes the accumulated words dictionaries and eliminates all words that are missing any field.

```text
Eliminate words that have empty keys from the accumulated words dictionary.

Args:
    None

Returns:
    None
```

## get_words_JSONL

```text
Extracts up to `max_words` entries from the WikiExtract word dump. These words can be saved in multiple JSONL files with a specific amount of words_per_file. By default it will extract all words and save them in files with 10000 words each.

Args:
    max_words (int, optional): Amount of words to extract. Defaults to -1.
    words_per_file (int, optional): Amount of words per JSONL file. Defaults to 10000.

    Returns:
        int: Total number of words successfully saved.
```

This is the driver function for all the above functions.

This function:

- Reads the JSONL dump line by line until the specified amount of words has been reached.
- Extracts the pertinent word information.
- Adds the word to an accumulated words dictionary.
- Once the amount of words reaches the specified 'words per JSON' limit, it saves the dictionary to a JSON file.
- Returns the amount of words saved.

The call to the function should include the maximum number of words to read and the amount of words to save per JSON. If no max_words is specified, it'll read the whole file.