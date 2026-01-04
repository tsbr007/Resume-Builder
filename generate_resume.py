from fpdf import FPDF
import os
import re
from datetime import datetime
import unicodedata

class PDF(FPDF):
    def footer(self):
        self.set_y(-15)
        # Check if font family is set, else fall back to standard
        if 'Arial' in self.fonts:
            self.set_font('Arial', 'I', 8)
        else:
            self.set_font('Helvetica', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')

def read_content(filename):
    path = os.path.join("content", filename)
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            
            # Normalize unicode
            content = unicodedata.normalize('NFKD', content)
            
            # Map special bullet to standard round bullet
            replacements = {
                '': '\u2022' 
            }
            for original, replacement in replacements.items():
                content = content.replace(original, replacement)
            
            # Replace start-of-line hyphens with bullets
            bullet_char = '\u2022'
            content = re.sub(r'(^|\n)-\s+', f'\\1{bullet_char} ', content)

            # Return unicode content directly for TTF font usage
            return content
    return ""

def create_resume():
    pdf = PDF()
    
    # Register Fonts (Arial)
    # Using raw strings for Windows paths
    font_family = "Helvetica" # Default fallback
    try:
        # Check if files exist before adding to avoid crash if system assumes different path
        # But standard Windows is C:\Windows\Fonts
        pdf.add_font("Arial", "", r"C:\Windows\Fonts\arial.ttf")
        pdf.add_font("Arial", "B", r"C:\Windows\Fonts\arialbd.ttf")
        pdf.add_font("Arial", "I", r"C:\Windows\Fonts\ariali.ttf")
        font_family = "Arial"
    except Exception as e:
        print(f"Warning: Could not load Arial font ({e}). Falling back to Helvetica (Unicode chars will fail).")

    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Colors
    PRIMARY_COLOR = (0, 51, 102) # Dark Blue
    
    # 1. Header
    name = read_content("header.txt")
    role = read_content("role.txt")
    headline = read_content("headline.txt")
    top_skills = read_content("top_skills.txt")
    contact = read_content("contact.txt")
    
    print(f"DEBUG: top_skills content: {repr(top_skills)}", flush=True)

    # Photo placement (Top Right)
    photo_path = None
    photo_dir = os.path.join("content", "photo")
    if os.path.exists(photo_dir):
        files = os.listdir(photo_dir)
        for f in files:
            if f.lower().endswith(('.png', '.jpg', '.jpeg')):
                photo_path = os.path.join(photo_dir, f)
                break
    
    print(f"DEBUG: Photo path found: {photo_path}", flush=True)

    print("Generating header...")
    if photo_path:
        # Place photo
        pdf.image(photo_path, x=160, y=10, w=35)
        header_w = 140
    else:
        header_w = 190 # Explicit width instead of 0

    # Name
    print("Printing Name...", flush=True)
    pdf.set_font(font_family, 'B', 24)
    pdf.set_text_color(*PRIMARY_COLOR)
    pdf.cell(0, 10, name, new_x="LMARGIN", new_y="NEXT") # Updated for fpdf2 warning
    pdf.set_x(10)

    # Role
    print("Printing Role...", flush=True)
    pdf.set_font(font_family, 'B', 12)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 10, role, new_x="LMARGIN", new_y="NEXT")
    pdf.set_x(10)
    
    # Headline
    if headline:
        print("Printing Headline...", flush=True)
        pdf.set_font(font_family, 'B', 12)
        pdf.set_text_color(0, 51, 102)
        pdf.cell(0, 8, headline, new_x="LMARGIN", new_y="NEXT")
        pdf.set_x(10)

    # Top Skills
    print("Printing Top Skills...", flush=True)
    pdf.set_font(font_family, 'B', 10)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 5, top_skills, new_x="LMARGIN", new_y="NEXT")
    pdf.set_x(10)
    pdf.ln(2)

    # Contact
    print("Printing Contact...", flush=True)
    pdf.set_font(font_family, '', 9)
    # Split contact by newlines to ensure clean printing with cell
    if contact:
        contact_lines = contact.split('\n')
        for line in contact_lines:
            line = line.strip()
            if line:
                pdf.cell(0, 5, line, new_x="LMARGIN", new_y="NEXT")
                pdf.set_x(10)
    pdf.ln(5)

    print("Header done. Drawing line...", flush=True)
    # Draw line
    pdf.set_draw_color(200, 200, 200)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)

    def add_section_header(title):
        print(f"Adding header: {title}")
        pdf.set_font(font_family, 'B', 12)
        pdf.set_text_color(*PRIMARY_COLOR)
        pdf.cell(0, 8, title.upper(), new_x="LMARGIN", new_y="NEXT")
        pdf.set_x(10)
        pdf.ln(1)

    def add_section_content(content):
        if not content: return
        print(f"Adding content length: {len(content)}", flush=True)
        pdf.set_font(font_family, '', 10)
        pdf.set_text_color(0, 0, 0)
        pdf.set_x(10)
        pdf.multi_cell(0, 5, content)
        pdf.ln(3)

    # Sections
    sections = [
        ("Summary", "summary.txt"),
        ("Career Highlights", "career_highlights.txt"),
        ("Core Skills", "core_skills.txt")
    ]

    for title, filename in sections:
        content = read_content(filename)
        if content:
            add_section_header(title)
            add_section_content(content)
            pdf.ln(2)

    # Experience
    print("Adding Experience section...")
    add_section_header("Professional Experience")
    exp_files = ["experience_1.txt", "experience_2.txt", "experience_3.txt", "experience_4.txt"]
    for f in exp_files:
        content = read_content(f)
        if content:
            print(f"Processing experience file: {f}")
            lines = content.split('\n')
            if lines:
                # Bold the first line (Title/Company)
                pdf.set_font(font_family, 'B', 10)
                pdf.set_text_color(0, 0, 0)
                pdf.multi_cell(0, 5, lines[0]) # Use multi_cell for wrapping
                
                # Rest
                if len(lines) > 1:
                    pdf.set_font(font_family, '', 10)
                    rest = '\n'.join(lines[1:])
                    pdf.set_x(10)
                    pdf.multi_cell(0, 5, rest)
            pdf.ln(3)
    pdf.ln(2)

    # Other Sections
    print("Adding other sections...")
    other_sections = [
        ("Selected Projects & Impact", "projects.txt"),
        ("Certifications & Recognition", "certifications.txt"),
        ("Education", "education.txt"),
        ("Role Alignment", "role_alignment.txt")
    ]

    for title, filename in other_sections:
        content = read_content(filename)
        if content:
            add_section_header(title)
            add_section_content(content)
            pdf.ln(2)
            
    # ATS Optimization (Hidden Keywords)
    ats_content = read_content("ats.txt")
    if ats_content:
        print("Adding ATS optimized content...", flush=True)
        # Removed add_page() to compact into remaining space
        pdf.set_text_color(255, 255, 255) # White
        pdf.set_font(font_family, '', 1) # Tiny
        pdf.multi_cell(0, 1, ats_content)
        # Reset color just in case
        pdf.set_text_color(0, 0, 0)

    # Filename
    if not role:
        role_str = "Resume"
    else:
        role_str = re.sub(r'[^a-zA-Z0-9]', '_', role)
    
    # Sanitize name for filename
    sanitized_name = re.sub(r'[^a-zA-Z0-9]', '_', name)
    
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_filename = f"{sanitized_name}_{role_str}_{timestamp}.pdf"
    
    # Ensure resumes dir exists
    if not os.path.exists("resumes"):
        os.makedirs("resumes")

    output_path = os.path.join("resumes", output_filename)
    pdf.output(output_path)
    print(f"Successfully generated resume: {output_path}")

if __name__ == "__main__":
    create_resume()
