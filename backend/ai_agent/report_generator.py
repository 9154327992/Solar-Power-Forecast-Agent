# ============================================================
# report_generator.py
# Solar Power Report Generator
# ============================================================

from datetime import datetime
import json
import os


class ReportGenerator:

    def __init__(self):

        self.report_directory = "reports"

        os.makedirs(

            self.report_directory,

            exist_ok=True

        )

    # ========================================================
    # Create Report Dictionary
    # ========================================================

    def create_report(

        self,

        weather,

        prediction,

        recommendation

    ):

        report = {

            "generated_at":

                datetime.now().strftime(

                    "%Y-%m-%d %H:%M:%S"

                ),

            "weather": weather,

            "prediction": prediction,

            "recommendation": recommendation

        }

        return report

    # ========================================================
    # Save JSON Report
    # ========================================================

    def save_json(

        self,

        report,

        filename=None

    ):

        if filename is None:

            filename = (

                datetime.now().strftime(

                    "solar_report_%Y%m%d_%H%M%S.json"

                )

            )

        path = os.path.join(

            self.report_directory,

            filename

        )

        with open(

            path,

            "w",

            encoding="utf-8"

        ) as file:

            json.dump(

                report,

                file,

                indent=4

            )

        return path

    # ========================================================
    # Save Text Report
    # ========================================================

    def save_text(

        self,

        report,

        filename=None

    ):

        if filename is None:

            filename = (

                datetime.now().strftime(

                    "solar_report_%Y%m%d_%H%M%S.txt"

                )

            )

        path = os.path.join(

            self.report_directory,

            filename

        )

        with open(

            path,

            "w",

            encoding="utf-8"

        ) as file:

            file.write("=" * 60 + "\n")
            file.write("SOLAR POWER FORECAST REPORT\n")
            file.write("=" * 60 + "\n\n")

            file.write(

                f"Generated : {report['generated_at']}\n\n"

            )

            file.write("Weather\n")
            file.write("-" * 30 + "\n")

            for key, value in report["weather"].items():

                file.write(

                    f"{key}: {value}\n"

                )

            file.write("\n")

            file.write("Prediction\n")
            file.write("-" * 30 + "\n")

            for key, value in report["prediction"].items():

                file.write(

                    f"{key}: {value}\n"

                )

            file.write("\n")

            file.write("Recommendations\n")
            file.write("-" * 30 + "\n")

            if isinstance(report["recommendation"], list):

                for item in report["recommendation"]:

                    file.write(

                        f"- {item}\n"

                    )

            else:

                file.write(

                    str(report["recommendation"])

                )

        return path

    # ========================================================
    # Generate Complete Report
    # ========================================================

    def generate(

        self,

        weather,

        prediction,

        recommendation

    ):

        report = self.create_report(

            weather,

            prediction,

            recommendation

        )

        json_path = self.save_json(

            report

        )

        text_path = self.save_text(

            report

        )

        return {

            "report": report,

            "json_file": json_path,

            "text_file": text_path

        }


# ============================================================
# Global Object
# ============================================================

generator = ReportGenerator()


# ============================================================
# Test Module
# ============================================================

if __name__ == "__main__":

    weather = {

        "temperature": 31,

        "humidity": 60,

        "pressure": 1012,

        "wind_speed": 4.2,

        "cloud_cover": 15

    }

    prediction = {

        "prediction": 5420,

        "level": "Excellent 🌞",

        "efficiency": 91.2

    }

    recommendation = [

        "Charge batteries.",

        "Export excess energy.",

        "Operate heavy appliances."

    ]

    result = generator.generate(

        weather,

        prediction,

        recommendation

    )

    print(result)