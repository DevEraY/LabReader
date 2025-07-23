# LabReader

**LabReader** is a Windows Application where the user can upload their pdf results and get easy medical advice from them. Like High LDL -> Increased risk of Cardio Vascular Disease.
## Features

- **PDF Upload**: Users can upload their lab results in PDF format.
- **Automatic Table Extraction**: The app uses PDF parsing techniques to extract tables from lab reports.
- **Parameter Matching**: Custom similarity algorithms (Jaccard, substring matching) are used to match test names with known parameters.
- **Reference-Based Evaluation**: Lab results are evaluated against gender-specific reference ranges.
- **Personalized Feedback**: When a result is too low or too high, the app provides user-friendly explanations and possible health implications.
- **Consent System**: A disclaimer popup is shown on first use, asking users to confirm that the app is not intended for diagnosis or treatment.

## Technologies Used

- **Python 3.10+**
- **Kivy & KivyMD** (for the Android interface)
- **pandas** (for data handling)
- **tabula-py** (for PDF table extraction)
- **JPype1 + Java** (required for Tabula backend)
- **JSON** (for user agreement state)
- **CSV** (for managing database)

## Folder Structure
-lab_reader_screens: Shows the screen for the app you can customize your buttons and stuff from here.
-main.py
-parametrelerr.csv: Where the parameters and low and high messages are shown. You can just translate it through there.


