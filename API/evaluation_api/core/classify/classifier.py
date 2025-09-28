import pickle
import numpy as np
import os
class SpeechClassifier:
    def __init__(self):
        # Get the path to this script's directory
        base_path = os.path.dirname(os.path.abspath(__file__))
        self.modelPath = "models/decision_tree_v1.pkl"
        # Build absolute path to file
        self.full_model_path = os.path.join(base_path, self.modelPath)
        self.tree = None
        self.label_map = {0: "Beginner", 1: "Intermediate", 2: "Advanced"}
        self._load_model()
        
    def _load_model(self):
        """ Load the classifier model. """
        
        print("Loading model...", end="")
        try:
            with open(self.full_model_path, "rb") as f:
                self.tree = pickle.load(f)
            print("Success!")
        except Exception as e:
            print("Failed.")
            print(f"Speech Classifier error: Could not load model. {e}")
        
    def _shape_data(self, difference_analysis:dict)->np.array:
        """Reshape the difference analysis for the model.

        Args:
            difference_analysis (dict): Difference array between user and reference analysis.

        Returns:
            np.array: Reshaped difference analysis.
        """
        print("Reshaping data...", end="")
        difference_data = [abs(x) for x in list(difference_analysis.values())]
        try:
            n_features = len(difference_analysis)
            difference_np = np.array(difference_data).reshape(1, n_features)
            print("Success!")
            return difference_np
        except Exception as e:
            print("Failed.")
            print(f"Error speech classifier: Could not reshape difference array. Check if the features are correct. {e}")
    
    def predict(self, difference_analysis:dict)->str:
        """Predict a label for the difference array as beginner, intermediate or advanced.

        Args:
            difference_analysis (dict): Difference array between user and reference analysis..

        Returns:
            str: Label for classification.
        """
        print("Predicting data...")
        difference_np = self._shape_data(difference_analysis)
        try:
            y_pred = self.tree.predict(difference_np)[-1]
            label = self.label_map[y_pred]
            return label
        except Exception as e:
            print(f"Error speech classifier: Could not predict. {e} ")
            return "Unclassified"