# ============================================================
# model_loader.py
# Load Trained Model and Scaler
# ============================================================

import joblib
from pathlib import Path


class ModelLoader:
    """
    Loads the trained machine learning model and scaler.
    """

    def __init__(self):
        base_dir = Path(__file__).resolve().parent.parent.parent

        self.model_path = base_dir / "models" / "model.pkl"
        self.scaler_path = base_dir / "models" / "scaler.pkl"

        self.model = None
        self.scaler = None

    def load_model(self):
        """
        Load trained model.
        """

        if self.model is None:
            self.model = joblib.load(self.model_path)

        return self.model

    def load_scaler(self):
        """
        Load feature scaler.
        """

        if self.scaler is None:
            self.scaler = joblib.load(self.scaler_path)

        return self.scaler

    def load(self):
        """
        Load both model and scaler.
        """

        return self.load_model(), self.load_scaler()


# Global instance
model_loader = ModelLoader()