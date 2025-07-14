from text_translate import TextTranslator

def main():
    translator = TextTranslator()
    text = "A man said to the universe sir i exist sweat covered brion's body trickling into the tight loincloth that was the only garment he wore"
    translation = translator.translate_text(text)
    print(translation)

if __name__ == "__main__":
    main()