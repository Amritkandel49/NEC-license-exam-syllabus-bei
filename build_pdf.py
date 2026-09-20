"""
Build a PDF book from Chapter 1 markdown files.
Combines all sections into one styled HTML then converts to PDF.
"""
import markdown
import os
import re

# ── Configuration ──────────────────────────────────────────────
BASE_DIR = r"C:\Users\sunco\Desktop\lincense_exam"
OUTPUT_HTML = os.path.join(BASE_DIR, "NEC_Chapter1_Complete_Textbook.html")
OUTPUT_PDF = os.path.join(BASE_DIR, "NEC_Chapter1_Complete_Textbook.pdf")

# Order of files to combine
FILES = [
    "ch1_master_roadmap.md",
    "ch1_s1.1_part1.md",
    "ch1_s1.1_part2.md",
    "ch1_s1.2.md",
    "ch1_s1.3.md",
    "ch1_s1.4.md",
    "ch1_s1.5.md",
    "ch1_s1.6.md",
]

# ── CSS Styling ────────────────────────────────────────────────
CSS = """
@page {
    size: A4;
    margin: 2cm 2cm 2.5cm 2cm;
    @bottom-center {
        content: "NEC License Exam — Chapter 1 | Page " counter(page);
        font-size: 9pt;
        color: #666;
    }
    @top-center {
        content: "Concept of Basic Electrical and Electronics Engineering";
        font-size: 8pt;
        color: #999;
        border-bottom: 0.5pt solid #ccc;
        padding-bottom: 3mm;
    }
}

@page :first {
    @top-center { content: none; }
    @bottom-center { content: none; }
}

body {
    font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
    font-size: 11pt;
    line-height: 1.6;
    color: #1a1a1a;
    max-width: 100%;
}

/* ── Title Page ─────────────────────────────────────── */
.title-page {
    page-break-after: always;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    min-height: 90vh;
    text-align: center;
}
.title-page h1 {
    font-size: 28pt;
    color: #1a237e;
    margin-bottom: 10px;
    border: none;
}
.title-page h2 {
    font-size: 18pt;
    color: #333;
    font-weight: normal;
    margin-bottom: 30px;
    border: none;
}
.title-page .subtitle {
    font-size: 14pt;
    color: #555;
    margin-bottom: 40px;
}
.title-page .exam-info {
    font-size: 11pt;
    color: #666;
    border: 2px solid #1a237e;
    padding: 20px 40px;
    border-radius: 8px;
    margin-top: 30px;
}

/* ── Section Breaks ─────────────────────────────────── */
.section-break {
    page-break-before: always;
    border-top: 3px solid #1a237e;
    padding-top: 10px;
    margin-top: 0;
}

/* ── Headings ───────────────────────────────────────── */
h1 {
    font-size: 22pt;
    color: #1a237e;
    border-bottom: 3px solid #1a237e;
    padding-bottom: 8px;
    margin-top: 30px;
    page-break-after: avoid;
}
h2 {
    font-size: 16pt;
    color: #283593;
    border-bottom: 1.5px solid #c5cae9;
    padding-bottom: 5px;
    margin-top: 25px;
    page-break-after: avoid;
}
h3 {
    font-size: 13pt;
    color: #303f9f;
    margin-top: 20px;
    page-break-after: avoid;
}
h4 {
    font-size: 11.5pt;
    color: #3949ab;
    margin-top: 15px;
    page-break-after: avoid;
}

/* ── Tables ─────────────────────────────────────────── */
table {
    border-collapse: collapse;
    width: 100%;
    margin: 15px 0;
    font-size: 10pt;
    page-break-inside: avoid;
}
th {
    background-color: #1a237e;
    color: white;
    padding: 8px 12px;
    text-align: left;
    font-weight: 600;
}
td {
    padding: 6px 12px;
    border: 1px solid #ddd;
}
tr:nth-child(even) {
    background-color: #f5f5f5;
}
tr:hover {
    background-color: #e8eaf6;
}

/* ── Code / Diagrams ────────────────────────────────── */
pre {
    background-color: #f5f5f5;
    border: 1px solid #e0e0e0;
    border-left: 4px solid #1a237e;
    padding: 12px 15px;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 9.5pt;
    line-height: 1.4;
    overflow-x: auto;
    white-space: pre-wrap;
    word-wrap: break-word;
    page-break-inside: avoid;
    border-radius: 4px;
}
code {
    background-color: #f0f0f0;
    padding: 1px 4px;
    border-radius: 3px;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 10pt;
}
pre code {
    background: none;
    padding: 0;
}

/* ── Blockquotes (Alerts) ──────────────────────────── */
blockquote {
    border-left: 4px solid #1a237e;
    background-color: #e8eaf6;
    padding: 12px 15px;
    margin: 15px 0;
    font-style: normal;
    page-break-inside: avoid;
    border-radius: 0 4px 4px 0;
}

/* ── Alerts Styling ────────────────────────────────── */
.alert-note {
    border-left: 4px solid #2196f3;
    background-color: #e3f2fd;
}
.alert-tip {
    border-left: 4px solid #4caf50;
    background-color: #e8f5e9;
}
.alert-important {
    border-left: 4px solid #9c27b0;
    background-color: #f3e5f5;
}
.alert-warning {
    border-left: 4px solid #ff9800;
    background-color: #fff3e0;
}
.alert-caution {
    border-left: 4px solid #f44336;
    background-color: #ffebee;
}

/* ── Math-like formatting ──────────────────────────── */
.math-block {
    text-align: center;
    margin: 10px 0;
    font-style: italic;
}

/* ── Lists ──────────────────────────────────────────── */
ul, ol {
    margin: 8px 0;
    padding-left: 25px;
}
li {
    margin: 3px 0;
}

/* ── Horizontal Rule ────────────────────────────────── */
hr {
    border: none;
    border-top: 2px solid #c5cae9;
    margin: 25px 0;
}

/* ── Emphasis ───────────────────────────────────────── */
strong {
    color: #1a237e;
}

/* ── Page Break Utility ─────────────────────────────── */
.page-break {
    page-break-after: always;
}

/* ── Exam Focus Boxes ──────────────────────────────── */
.exam-trap {
    background-color: #fff3e0;
    border: 1px solid #ff9800;
    border-left: 4px solid #e65100;
    padding: 10px 15px;
    margin: 10px 0;
    border-radius: 4px;
}
.engineering-intuition {
    background-color: #e8f5e9;
    border: 1px solid #4caf50;
    border-left: 4px solid #2e7d32;
    padding: 10px 15px;
    margin: 10px 0;
    border-radius: 4px;
}
"""

def process_github_alerts(html):
    """Convert GitHub-style alerts to styled divs."""
    alert_types = {
        '[!NOTE]': 'alert-note',
        '[!TIP]': 'alert-tip',
        '[!IMPORTANT]': 'alert-important',
        '[!WARNING]': 'alert-warning',
        '[!CAUTION]': 'alert-caution',
    }
    for marker, css_class in alert_types.items():
        pattern = f'<blockquote>\\s*<p>{re.escape(marker)}'
        replacement = f'<blockquote class="{css_class}"><p>'
        html = re.sub(pattern, replacement, html)
    return html

def add_section_breaks(html):
    """Add page breaks before major section headings."""
    # Add page break before each major section (h1 tags that indicate new sections)
    section_patterns = [
        r'(<h1[^>]*>(?:Section 1\.[2-6]|CHAPTER 1 —|1\.1\.[2-9]|1\.[2-6]))',
        r'(<h1[^>]*>(?:SECTION|Section) 1\.[2-6])',
    ]
    # Simple approach: add page break before every h1 except the very first
    parts = html.split('<h1')
    if len(parts) > 1:
        result = parts[0]
        for i, part in enumerate(parts[1:], 1):
            if i > 1:  # Skip first h1 (title page handles it)
                result += '<div class="section-break"></div><h1' + part
            else:
                result += '<h1' + part
        html = result
    return html

def convert_latex_to_html(text):
    """Simple LaTeX math conversion for display in HTML."""
    # Convert display math $$...$$ to styled divs
    text = re.sub(
        r'\$\$(.*?)\$\$',
        r'<div style="text-align:center;margin:10px 0;font-family:serif;font-style:italic;">\1</div>',
        text,
        flags=re.DOTALL
    )
    # Convert inline math $...$ (but not $$)
    text = re.sub(
        r'(?<!\$)\$(?!\$)(.*?)(?<!\$)\$(?!\$)',
        r'<span style="font-family:serif;font-style:italic;">\1</span>',
        text
    )
    return text

def build_title_page():
    """Generate the title page HTML."""
    return """
    <div class="title-page">
        <h1>CHAPTER 1</h1>
        <h2>Concept of Basic Electrical and Electronics Engineering</h2>
        <div class="subtitle">
            <p><strong>Complete Textbook for NEC License Examination Preparation</strong></p>
            <p>Electronics, Communication and Information Engineering (AEiE)</p>
        </div>
        <div class="exam-info">
            <p><strong>Nepal Engineering Council</strong></p>
            <p>Registration Examination</p>
            <p>Code: AExE01</p>
            <br/>
            <p><em>Sections: 1.1 Basic Concept &bull; 1.2 Network Theorems &bull; 1.3 AC Fundamentals</em></p>
            <p><em>1.4 Semiconductor Devices &bull; 1.5 Signal Generators &bull; 1.6 Amplifiers</em></p>
        </div>
    </div>
    """

def build_toc():
    """Generate table of contents."""
    return """
    <div style="page-break-after:always;">
    <h1 style="text-align:center;">TABLE OF CONTENTS</h1>
    <hr/>
    <h2>Master Roadmap</h2>
    <ul>
        <li>Complete Hierarchical Structure</li>
        <li>Dependency Relationships</li>
        <li>Recommended Learning Order</li>
        <li>Priority Classification</li>
        <li>Topic Characterization</li>
    </ul>
    <h2>Section 1.1 — Basic Concept (AExE0101)</h2>
    <ul>
        <li>Part 1: Electric Charge, Voltage, Current, Resistance, Ohm's Law, Power, Energy</li>
        <li>Part 2: Conductors &amp; Insulators, Series &amp; Parallel Circuits, Star-Delta Conversion, Kirchhoff's Laws, Circuit Classifications</li>
        <li>Practice Questions &amp; MCQs</li>
    </ul>
    <h2>Section 1.2 — Network Theorems (AExE0102)</h2>
    <ul>
        <li>Superposition Theorem</li>
        <li>Thevenin's Theorem</li>
        <li>Norton's Theorem</li>
        <li>Maximum Power Transfer Theorem</li>
        <li>R-L, R-C, R-L-C Circuits</li>
        <li>Series &amp; Parallel Resonance</li>
        <li>Active, Reactive &amp; Apparent Power</li>
        <li>Practice Questions &amp; MCQs</li>
    </ul>
    <h2>Section 1.3 — Alternating Current Fundamentals (AExE0103)</h2>
    <ul>
        <li>AC Generation, Equations &amp; Waveforms</li>
        <li>Peak, Average &amp; RMS Values</li>
        <li>Three-Phase System</li>
        <li>Practice Questions &amp; MCQs</li>
    </ul>
    <h2>Section 1.4 — Semiconductor Devices (AExE0104)</h2>
    <ul>
        <li>Semiconductor Fundamentals</li>
        <li>Diode Characteristics</li>
        <li>BJT Configuration &amp; Biasing</li>
        <li>Small &amp; Large Signal Models</li>
        <li>MOSFET Working Principle</li>
        <li>CMOS Technology</li>
        <li>Practice Questions &amp; MCQs</li>
    </ul>
    <h2>Section 1.5 — Signal Generator (AExE0105)</h2>
    <ul>
        <li>Oscillator Principles &amp; Barkhausen Criterion</li>
        <li>RC Oscillators (Wien Bridge, Phase-Shift)</li>
        <li>LC Oscillators (Hartley, Colpitts)</li>
        <li>Crystal Oscillators</li>
        <li>Waveform Generators</li>
        <li>Practice Questions &amp; MCQs</li>
    </ul>
    <h2>Section 1.6 — Amplifiers (AExE0106)</h2>
    <ul>
        <li>Classification of Output Stages</li>
        <li>Class A, B, AB Amplifiers</li>
        <li>Power BJTs &amp; Push-Pull Stages</li>
        <li>Tuned Amplifiers</li>
        <li>Operational Amplifiers (Op-Amps)</li>
        <li>Practice Questions &amp; MCQs</li>
    </ul>
    </div>
    """

def main():
    print("=" * 60)
    print("NEC Chapter 1 Textbook — PDF Builder")
    print("=" * 60)

    # Read and combine all markdown files
    combined_md = ""
    for fname in FILES:
        fpath = os.path.join(BASE_DIR, fname)
        print(f"Reading: {fname} ({os.path.getsize(fpath)/1024:.1f} KB)")
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        combined_md += content + "\n\n---\n\n"

    print(f"\nTotal markdown content: {len(combined_md)/1024:.1f} KB")

    # Pre-process LaTeX math before markdown conversion
    combined_md = convert_latex_to_html(combined_md)

    # Convert markdown to HTML
    print("Converting markdown to HTML...")
    md = markdown.Markdown(
        extensions=[
            'tables',
            'fenced_code',
            'toc',
            'nl2br',
            'sane_lists',
        ]
    )
    body_html = md.convert(combined_md)

    # Post-process
    body_html = process_github_alerts(body_html)
    body_html = add_section_breaks(body_html)

    # Build complete HTML document
    title_page = build_title_page()
    toc = build_toc()

    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>NEC Chapter 1 — Concept of Basic Electrical and Electronics Engineering</title>
    <style>
{CSS}
    </style>
</head>
<body>
    {title_page}
    {toc}
    {body_html}
</body>
</html>"""

    # Save HTML
    print(f"Saving HTML: {OUTPUT_HTML}")
    with open(OUTPUT_HTML, 'w', encoding='utf-8') as f:
        f.write(full_html)
    print(f"HTML saved ({os.path.getsize(OUTPUT_HTML)/1024:.1f} KB)")

    # Convert to PDF using WeasyPrint
    print("\nConverting HTML to PDF using WeasyPrint...")
    try:
        from weasyprint import HTML
        HTML(filename=OUTPUT_HTML).write_pdf(OUTPUT_PDF)
        size_mb = os.path.getsize(OUTPUT_PDF) / (1024 * 1024)
        print(f"\n{'=' * 60}")
        print(f"SUCCESS! PDF created: {OUTPUT_PDF}")
        print(f"PDF size: {size_mb:.2f} MB")
        print(f"{'=' * 60}")
    except Exception as e:
        print(f"WeasyPrint failed: {e}")
        print("Trying pdfkit as fallback...")
        try:
            import pdfkit
            options = {
                'page-size': 'A4',
                'margin-top': '20mm',
                'margin-bottom': '25mm',
                'margin-left': '20mm',
                'margin-right': '20mm',
                'encoding': 'UTF-8',
                'footer-center': 'Page [page] of [topage]',
                'footer-font-size': '8',
            }
            pdfkit.from_file(OUTPUT_HTML, OUTPUT_PDF, options=options)
            size_mb = os.path.getsize(OUTPUT_PDF) / (1024 * 1024)
            print(f"\nSUCCESS! PDF created: {OUTPUT_PDF}")
            print(f"PDF size: {size_mb:.2f} MB")
        except Exception as e2:
            print(f"pdfkit also failed: {e2}")
            print(f"\nHTML file saved at: {OUTPUT_HTML}")
            print("You can open it in a browser and print to PDF (Ctrl+P).")

if __name__ == "__main__":
    main()
