# Dynamic Resume Builder

A Python-based resume generator that compiles text files into a professionally formatted, ATS-optimized PDF resume.

## Features
- **Dynamic Content:** Edit text files in the `content/` folder to update your resume easily.
- **ATS Optimization:** Includes a hidden text layer (invisible to humans, visible to bots) to improve keyword matching.
- **Photo Integration:** Automatically embeds your profile photo if present.
- **Auto-Formatting:** Handles fonts (Arial), bullet points, and layout automatically.

## Prerequisites
- Python 3.x
- `fpdf2` library

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/tsbr007/Resume-Builder.git
   cd Resume-Builder
   ```
2. Install dependencies:
   ```bash
   pip install fpdf2
   ```

## How to Use

### 1. Update Content
Navigate to the `content/` directory and edit the text files with your own details:
- `header.txt`: Your Name.
- `role.txt` & `headline.txt`: Your Job Title / Target Role.
- `contact.txt`: Email, Phone, LinkedIn, GitHub links (pipe `|` separated).
- `summary.txt`, `education.txt`, `experience_*.txt`: Your professional details.
- `ats.txt`: Add keywords relevant to your industry (these will be hidden in the PDF).

### 2. Add Your Photo
1. Go to the folder: `content/photo/`
2. Place your passport-size photo there.
3. Supported formats: **JPG, PNG**.
   - *Note: Ensure there is only one image file in this folder. The script picks the first one it finds.*

### 3. Generate Resume
Run the Python script:
```bash
python generate_resume.py
```

### 4. Output
The generated PDF will be saved in the `resumes/` folder with a timestamped filename, e.g.:
`Your_Name_Role_YYYY-MM-DD_HH-MM-SS.pdf`

## Customization
- **Fonts:** The script uses the system's `Arial` font to support bullet points (`•`) and special characters.
- **Layout:** You can modify `generate_resume.py` to adjust margins, colors, or section ordering.
