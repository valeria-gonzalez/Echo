from Echo.data_processing.texts_by_category.text_category_evaluator import TextCategoryEvaluator

def main():
    evaluator = TextCategoryEvaluator()
    results = evaluator.classify_words("I visited Paris and enjoyed the food and "
    "museums.")

    for category, score in results.items():
        print(f"Category: [{category}], Score: [{score:.2%}]")
        
if __name__ == "__main__":
    main()