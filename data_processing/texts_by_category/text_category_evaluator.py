import json
from transformers import pipeline

class TextCategoryEvaluator:
    """Zero-shot classification for categorizing text into predefined 
    categories.
    """    
    def __init__(self):
        self.classifier = pipeline("zero-shot-classification", 
        model="facebook/bart-large-mnli")
        
        self.category_labels = {
            "daily life": "Situations related to everyday routines like eating, "
            "sleeping, shopping, hygiene, and home activities.",
            "work": "Concepts involving employment, jobs, office tasks, careers, "
            "or professional environments.",
            "social life": "Scenarios involving friends, communication, entertainment,"
            "community, and social interaction.",
            "education": "Topics involving learning, studying, schools, teaching, "
            "or acquiring knowledge.",
            "travel": "Experiences involving transportation, visiting places, "
            "vacations, tourism, and moving between locations.",
            "health": "Concepts related to physical or mental well-being, medicine, "
            "fitness, nutrition, and medical care."
        }
        
    def classify_words(self, text_data:str) -> dict:
        """This function classifies the input text into predefined categories
        using a zero-shot classification model. It returns a dictionary with 
        the categories as keys and their corresponding scores as values.

        Args:
            text_data (str): The input text to be classified.

        Returns:
            dict: A dictionary where keys are category names and values are
        """        
        categories = {}
        text = text_data.lower()
        label_descriptions = list(self.category_labels.values())

        result = self.classifier(text, label_descriptions)

        description_to_category = {v: k for k, v in self.category_labels
        .items()}

        for label, score in zip(result["labels"], result["scores"]):
            category = description_to_category[label]
            categories[category] = score
        return categories
    
evaluator = TextCategoryEvaluator()
results = evaluator.classify_words("I visited Paris and enjoyed the food and "
"museums.")

for category, score in results.items():
    print(f"Category: [{category}], Score: [{score:.2%}]")

