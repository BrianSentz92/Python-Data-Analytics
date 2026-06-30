# Resume Narrator

## Overview

Resume Narrator is a Python application that converts PDF resumes into natural-sounding speech.

The application extracts text from PDF documents, reformats common resume elements for improved pronunciation, and reads the content aloud using a text-to-speech engine. This project demonstrates PDF processing, text preprocessing, regular expressions, and speech synthesis using Python.

---

## Features

- Select a PDF resume using a graphical file picker
- Extract text from PDF documents
- Improve pronunciation through text preprocessing
- Format phone numbers for natural speech
- Spell acronyms letter-by-letter (e.g., "CEO" → "C E O")
- Convert dates into spoken language
- Improve pronunciation of email addresses and URLs
- Read resumes aloud using text-to-speech

---

## Technologies

- Python
- PyPDF2
- pyttsx3
- Regular Expressions

---

## Installation

Clone the repository and install the required packages.

```bash
pip install -r requirements.txt
```

---

## Repository Structure

```text
Resume Narrator/
│
├── README.md
├── ResumeNarrator.py
├── Resume Narrator.ipynb
├── requirements.txt
└── images/
```

---

## Example Workflow

1. Launch the application.
2. Select a PDF resume.
3. Extract the document text.
4. Format the text for natural speech.
5. Listen to the narrated resume.

---

## Sample Output

> Add a screenshot of the application or terminal output after running the program.

```text
images/resume-narrator.png
```

After adding the screenshot, replace the placeholder above with:

```markdown
![Resume Narrator](images/resume-narrator.png)
```

---

## Jupyter Notebook

This repository includes a Jupyter Notebook that demonstrates the application's workflow, including:

- Importing required libraries
- Selecting a PDF document
- Extracting text from the PDF
- Applying text preprocessing
- Converting text to natural speech

---

## Future Enhancements

Potential improvements for future versions include:

- Microsoft Word (.docx) support
- Adjustable speaking speed
- Multiple voice selections
- Export narration to MP3
- Resume keyword analysis
- AI-powered resume feedback and optimization
- Batch processing for multiple resumes

---

## Author

**Brian Sentz**

Technical Project Manager | PMP | Data Analytics | Python | SQL | Tableau
