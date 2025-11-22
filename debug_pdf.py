import sys
import pdfplumber
from pathlib import Path

# Add modules to path
sys.path.insert(0, str(Path("modules").absolute()))

from extrator import ExtratorPDF

pdf_path = "exemplos/22112025.PDF"
print(f"Testing extraction on {pdf_path}")

extrator = ExtratorPDF(pdf_path)

# Extract with a very low minimum to see negative stocks if they are parsed
# If regex works, we should see them.
produtos = extrator.extrair_produtos(estoque_minimo=-999999)

print(f"Total extracted: {len(produtos)}")

negative_stocks = [p for p in produtos if p['estoque'] < 0]
print(f"Negative stocks found: {len(negative_stocks)}")
for p in negative_stocks[:5]:
    print(f"  {p['descricao']}: {p['estoque']}")

positive_stocks = [p for p in produtos if p['estoque'] > 0]
print(f"Positive stocks found: {len(positive_stocks)}")

# Check if any parsing failed
print("\n--- Inspecting raw text for potential failures ---")
with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        for line in text.split('\n'):
            if "CX" in line or "UN" in line or "FD" in line:
                # Check if it matches regex
                if not extrator._extrair_produto(line):
                    print(f"FAILED MATCH: {line}")
                elif " -" in line or "- " in line: # Check for potential negative signs that might be weird
                     print(f"MATCHED BUT CHECK: {line}")
