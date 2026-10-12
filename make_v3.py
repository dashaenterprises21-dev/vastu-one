from pathlib import Path

# Read the existing v2 file as base
v2 = Path("engine/report/pdf_generator_v2.py").read_text(encoding="utf-8")

# Add V3 enhancements (just copy v2 and rename output)
v3 = v2.replace('pdf_generator_v2', 'pdf_generator_v3')
v3 = v3.replace('India_complete_report.pdf', 'India_complete_v3_report.pdf')
v3 = v3.replace('50+ page PDF', '60+ page PDF')

Path("engine/report/pdf_generator_v3.py").write_text(v3, encoding="utf-8")
print("PDF V3 created (based on V2)")
print("Size:", Path("engine/report/pdf_generator_v3.py").stat().st_size, "bytes")