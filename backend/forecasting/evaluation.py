# ============================================================
# evaluation.py
# Model Evaluation
# ============================================================

import numpy as np
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)


class ModelEvaluator:
    """
    Evaluates regression models for solar power prediction.
    """

    def evaluate(self, y_true, y_pred):
        """
        Compute evaluation metrics.
        """

        mae = mean_absolute_error(y_true, y_pred)
        mse = mean_squared_error(y_true, y_pred)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_true, y_pred)

        return {
            "MAE": round(mae, 4),
            "MSE": round(mse, 4),
            "RMSE": round(rmse, 4),
            "R2 Score": round(r2, 4)
        }

    def print_report(self, metrics):
        """
        Print evaluation results.
        """

        print("\n========== Model Evaluation ==========")

        for metric, value in metrics.items():
            print(f"{metric}: {value}")

        print("======================================")

    def compare(self, train_score, test_score):
        """
        Compare training and testing scores.
        """

        difference = abs(train_score - test_score)

        if difference < 0.05:
            status = "Good Generalization"

        elif difference < 0.10:
            status = "Slight Overfitting"

        else:
            status = "Possible Overfitting"

        return {
            "Training R2": round(train_score, 4),
            "Testing R2": round(test_score, 4),
            "Difference": round(difference, 4),
            "Status": status
        }


# Global instance
evaluator = ModelEvaluator()