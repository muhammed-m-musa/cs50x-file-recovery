# CS50x File Recovery & Organization System

## Overview
This project is a hybrid software system developed as part of the CS50x curriculum, designed to recover deleted files from raw memory/flash data streams, systematically organize them, and manage them through a web interface. The architecture combines low-level byte manipulation in C with a robust Python and Flask backend integrated with an SQLite database.

---

## Core Architecture & Technical Workflow

### 1. Low-Level Recovery & Organization Engine (`recover.c` & `organizer.c`)
The system scans raw memory cards or disk images block-by-block to extract deleted assets and structure them:
* **Supported Formats:** Successfully detects and recovers standard file types including **JPEGs**, **PNGs**, **GIFs**, and **ZIP archives**.
* **Contiguous Memory Logic:** The algorithm successfully reconstructs files when data blocks are stored contiguously (sequential bytes in memory). 
* **Design Constraint & Engineering Reality:** If data blocks are fragmented (scattered across memory—such as a first byte here and a second byte on the opposite side), simple sequential block recovery cannot reconstruct the file without advanced spatial mapping and file-system carving algorithms. Recognizing these hardware and structural boundaries is a fundamental part of low-level systems engineering.
* **Systematic Organization (`organizer.c`):** Once extracted, the organization module processes, validates, and arranges the recovered files into structured directories, preparing their metadata for seamless pipeline transfer.

### 2. Backend Pipeline & Database Integration (`app.py`)
Once the C programs extract, structure, and organize the files, the pipeline transitions the data upward:
* The parsed metadata and recovered files are securely passed to a **Python/Flask** application layer.
* The application processes these entries and commits them into an **SQLite database**, ensuring persistent storage, indexing, and organized retrieval.
* Users can interact with the system via the web interface to view, manage, and verify the successfully recovered assets.

---

## Technologies Used
* **C:** Low-level file parsing, byte-signature recognition, and file organization routines.
* **Python & Flask:** Web framework, data processing pipeline, and application logic.
* **SQLite:** Relational database for storing and managing file records.
* **HTML/Templates:** Clean front-end interface for user interaction.

---
  
## How to Run

1. **Compile the C programs:**

```bash
make project
```

2. **Install Python dependencies (first time only):**

```bash
pip install flask cs50
```

3. **Run the Flask web application:**

```bash
python app.py
```

4. **Open your browser and go to:**
http://127.0.0.1:5000


5. **Upload a raw disk/flash image (`.raw`) through the web interface.**
   The C programs (`recover` and `organizer`) run automatically in the background for each session — no manual execution needed.
