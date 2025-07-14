# Translate Text

## Objective

Translate a given text from english to spanish.

## Overview

This class was made possible by the open source APIs of:

- [Libre Translate](https://libretranslate.com/)
- [Free Translate API](https://ftapi.pythonanywhere.com/)

The first one must be locally hosted (see instructions below), while the other 
isn't. 

Libre translate will be the API used by default because it yields better results.

### 1. Install needed libraries

For this section, the following modules were used:
```
pip install requests
pip install libretranslate
```

These modules can be installed individually or via the `requirements.txt` file
located in the root directory.

To install using the `requirements.txt` use:

```bash
pip install -r requirements.txt
```

###  3. Setting up 

> If the `ftapi` is used, there is no need for setting up.

If the `libre translate api` will be used to generate translations, after installation, make sure to run the following command:

Make sure you have Python 3.8, 3.9 or 3.10 installed, then from a terminal run:

```bash
pip install libretranslate
libretranslate --load-only en,es
```
This command loads only the english and spanish language packages, if other languages are desired, review the [documentation](https://docs.libretranslate.com/guides/installation/).

Once done, all the api requests will be directed to `http://127.0.0.1:5000`.

If for any reason the installation process for the language packages are interrupted, 
run the following commands for this [issue](https://community.libretranslate.com/t/cannot-download-models/631):
```bash
rm -rf ~/.local/share/argos-translate
rm -rf ~/.local/cache/argos-translate
```

###  4. Example usage

All that's necessary is to call the method `translate_text` with the text to translate.

```python
from text_translate import TextTranslator

def main():
    text = "A man said to the universe sir i exist sweat covered brion's body trickling into the tight loincloth that was the only garment he wore"

    # Declare translator object
    translator = TextTranslator()

    # Translate text with ftapi (web server)
    translation = translator.translate_text(text, "ftapi")

    # Translate text with libre (local server)
    translation = translator.translate_text(text)

    print(translation)

if __name__ == "__main__":
    main()
    
```
#### Method description

- `translate_text` receives as parameters the text to be translated and either the keywords `libre` or `ftapi` to indicate which translation api to use.




