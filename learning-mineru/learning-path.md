# MinerU Learning Path

A progressive, hands-on guide to mastering MinerU document parsing.

---

## Level 1: Overview & Motivation

### What Problem Does MinerU Solve?

In the era of Large Language Models, **document parsing is the critical bottleneck** for AI systems. Research shows that **80% of production RAG failures trace back to document parsing gone wrong**.

Traditional PDF extraction tools face these challenges:

- **Lost Structure**: Multi-column layouts become garbled text
- **Formula Mangling**: Mathematical equations turn into gibberish or image descriptions
- **Table Destruction**: Complex tables lose their structure
- **Language Barriers**: Poor support for non-English languages
- **Artifacts**: Headers, footers, and page numbers pollute the content
- **Format Limitations**: Can't handle diverse document types (PDFs, images, Office files)

**MinerU solves these problems** by providing high-precision document parsing that:
- Preserves document structure (headings, lists, paragraphs)
- Converts formulas to compilable LaTeX (not descriptions)
- Extracts tables as structured HTML
- Supports 109 languages with built-in OCR
- Removes artifacts automatically
- Handles PDFs, images, Word, PowerPoint, and Excel

### What Existed Before? Why is MinerU Better?

**Before MinerU:**

1. **Basic PDF Libraries** (PyMuPDF, PDFMiner)
   - Simple text extraction only
   - No layout understanding
   - Can't handle formulas or complex tables

2. **Commercial APIs** (Adobe PDF Services, AWS Textract)
   - Expensive at scale
   - Privacy concerns (data leaves your infrastructure)
   - Limited customization

3. **Other Open-Source Tools** (Marker, MarkItDown)
   - Good for general documents
   - Weak formula recognition (<70% accuracy)
   - Limited multi-language support

**Why MinerU is Better:**

| Feature | MinerU | Marker | MarkItDown | Commercial APIs |
|---------|--------|--------|------------|-----------------|
| **Formula Recognition** | 90%+ BLEU | <70% BLEU | None | Varies |
| **Table Extraction** | HTML/OTSL | Markdown | Basic | Good |
| **Languages Supported** | 109 | ~10 | Limited | Varies |
| **Privacy** | ✅ Local | ✅ Local | ✅ Local | ❌ Cloud |
| **Cost** | Free | Free | Free | $$$ |
| **Structure Preservation** | Excellent | Good | Basic | Good |
| **Academic Papers** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐ | ⭐⭐⭐⭐ |

### Who Uses MinerU? For What?

**1. AI Engineers & Data Scientists**
- Building RAG (Retrieval Augmented Generation) pipelines
- Preparing training data for LLMs
- Processing millions of documents at scale
- Real-world result: "40% improvement in retrieval precision" (legal AI startup)

**2. Academic Researchers**
- Extracting information from scientific papers
- Processing literature with complex formulas
- Multi-language research document analysis
- Throughput: 1,200-1,500 pages/hour for equation-dense papers

**3. Enterprise Document Management**
- Digitizing document archives
- Legal contract analysis
- Financial document processing
- Multi-format document workflows

**4. Document Conversion Services**
- PDF to Markdown conversion
- Scanned document OCR
- Multi-language document processing
- Content reuse and search optimization

### When Should You NOT Use MinerU?

**MinerU is NOT ideal for:**

❌ **Real-time document viewing** (use PDF.js, browser viewers)
❌ **PDF editing** (use Adobe Acrobat, PDFtk)
❌ **Simple text extraction** from clean documents (use PyMuPDF - faster)
❌ **Comic books or art albums** (acknowledged limitation)
❌ **Vertical text documents** (not supported)
❌ **When you have <16GB RAM** (hardware requirement)

**Use MinerU when:**

✅ Document structure matters
✅ You need accurate formula extraction
✅ Processing academic/scientific papers
✅ Building AI/LLM pipelines (RAG, training data)
✅ Multi-language document processing
✅ Complex tables need preservation
✅ You want local, privacy-preserving processing

### Key Takeaway

MinerU is the **bridge between raw document pixels and structured, LLM-ready data**. If you're building AI systems that need to understand documents deeply - not just extract text - MinerU is your tool.

---

## Level 2: Installation & Hello World

### Prerequisites

Before installing MinerU, ensure you have:

**Operating System:**
- ✅ Linux (2019+ distributions)
- ✅ Windows (with Python 3.10-3.12; Python 3.13 not supported with Ray)
- ✅ macOS (version 14.0+; Python 3.10-3.13)

**Hardware:**
- **Minimum**: 16GB RAM, 20GB disk space
- **Recommended**: 32GB+ RAM, SSD, GPU with 8GB+ VRAM
- **CPU-only mode**: Works with 16GB RAM (pipeline backend)

**Software:**
- Python 3.10, 3.11, 3.12, or 3.13 (check: `python --version`)
- pip or uv package manager
- Git (for source installation)

### Installation Steps

#### Method 1: Using pip/uv (Recommended for Beginners)

```bash
# Step 1: Upgrade pip
pip install --upgrade pip

# Step 2: Install uv (modern, fast package installer)
pip install uv

# Step 3: Install MinerU with all dependencies
uv pip install -U "mineru[all]"
```

**What does `[all]` include?**
- Core parsing engine
- All backend options (Pipeline, VLM, Hybrid)
- OCR support (PaddleOCR)
- Formula recognition models
- API server dependencies

#### Method 2: From Source (For Contributors/Advanced Users)

```bash
# Clone the repository
git clone https://github.com/opendatalab/MinerU.git
cd MinerU

# Install in editable mode
uv pip install -e .[all]
```

#### Method 3: Docker (For Production/Isolation)

```bash
# Pull the official image
docker pull opendatalab/mineru:latest

# Run with volume mapping
docker run -v /path/to/input:/input -v /path/to/output:/output \
  opendatalab/mineru:latest \
  mineru -p /input/document.pdf -o /output
```

### Verify Installation

```bash
# Check if mineru command is available
mineru --version

# Expected output: mineru, version 2.7.6 (or later)
```

### Your First Document Parse - Hello World

Let's parse a simple PDF to verify everything works!

#### Step 1: Prepare a Test Document

Create a simple test PDF or download one:

```bash
# Create a test directory
mkdir ~/mineru-test
cd ~/mineru-test

# Download a sample PDF (or use your own)
curl -o sample.pdf "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"
```

#### Step 2: Run Your First Parse

```bash
# Basic usage - MinerU will start a temporary API automatically
mineru -p sample.pdf -o output

# What happens:
# 1. MinerU downloads required models (first run only - takes 5-10 min)
# 2. Analyzes the document layout
# 3. Extracts text, images, tables, formulas
# 4. Outputs structured Markdown and JSON
```

**First-time model download:**
The first run downloads ~2-4GB of deep learning models:
- Layout detection model
- Formula recognition model
- OCR model (PaddleOCR)

This is **one-time only** and cached locally.

#### Step 3: Check the Output

```bash
# Navigate to output directory
cd output

# List generated files
ls -la

# Expected structure:
# ├── sample/
# │   ├── auto/
# │   │   ├── sample.md          # Markdown output
# │   │   ├── sample_content_list.json  # Metadata
# │   │   └── images/            # Extracted images
```

#### Step 4: View the Results

```bash
# Read the Markdown output
cat sample/auto/sample.md

# Or open in your editor
code sample/auto/sample.md  # VS Code
vim sample/auto/sample.md   # Vim
```

**Success!** You've just parsed your first document with MinerU! 🎉

### Understanding the Output

MinerU creates several files:

1. **`sample.md`**: Clean Markdown with:
   - Preserved structure (headings, paragraphs, lists)
   - Inline formulas as LaTeX: `$E = mc^2$`
   - Display formulas as LaTeX blocks
   - Table references: `[Table 1]`
   - Image references: `![Image](images/img_001.jpg)`

2. **`sample_content_list.json`**: Metadata including:
   - Page-by-page content breakdown
   - Element types (text, table, image, formula)
   - Bounding boxes and coordinates
   - Reading order information

3. **`images/`**: Extracted images at original resolution

### Common First-Run Issues

**Issue 1: Model Download Fails**
```bash
# Error: Connection timeout downloading models
# Solution: Set HuggingFace mirror or download manually
export HF_ENDPOINT=https://hf-mirror.com
mineru -p sample.pdf -o output
```

**Issue 2: Out of Memory**
```bash
# Error: Killed (OOM)
# Solution: Use pipeline backend (CPU-only, less memory)
mineru -p sample.pdf -o output -b pipeline
```

**Issue 3: CUDA Not Found** (GPU users)
```bash
# Error: CUDA not available
# Solution: Verify PyTorch CUDA installation
python -c "import torch; print(torch.cuda.is_available())"
# If False, reinstall PyTorch with CUDA support
```

### Next Steps

Now that you have MinerU working, let's understand **how** it works in Level 3!

---

## Level 3: Core Concepts

To use MinerU effectively, you need to understand its **5 core concepts**.

### Concept 1: Multi-Backend Architecture

MinerU isn't a single algorithm - it's a **flexible system with three distinct parsing engines**.

#### The Three Backends

**1. Pipeline Backend (`pipeline`)**
- **What**: Traditional computer vision + OCR pipeline
- **Hardware**: CPU-only (no GPU required)
- **Speed**: ⚡⚡⚡ Fastest (seconds per page)
- **Accuracy**: ✓✓✓ Good (85%+ on OmniDocBench)
- **Memory**: 16GB RAM minimum
- **Best for**: Batch processing, cost-conscious deployments, CPU-only servers

```bash
# Use pipeline backend explicitly
mineru -p document.pdf -o output -b pipeline
```

**2. VLM Backend (`vlm-auto-engine`)**
- **What**: Vision-Language Model (1.2B parameters)
- **Hardware**: GPU required (8GB+ VRAM)
- **Speed**: ⚡ Slower (more inference time)
- **Accuracy**: ✓✓✓✓✓ Highest (90%+ on OmniDocBench)
- **Memory**: 16GB RAM + 8GB VRAM minimum
- **Best for**: Complex documents, maximum accuracy, when GPU available

```bash
# Use VLM backend for maximum accuracy
mineru -p document.pdf -o output -b vlm-auto-engine
```

**3. Hybrid Backend (`hybrid-auto-engine`) - DEFAULT**
- **What**: Combines pipeline + VLM strengths
- **Hardware**: Works on CPU, better with GPU
- **Speed**: ⚡⚡ Balanced
- **Accuracy**: ✓✓✓✓ High (88-92%)
- **Memory**: 16GB RAM, optional GPU
- **Best for**: Most use cases, balanced performance

```bash
# Default - hybrid backend (no flag needed)
mineru -p document.pdf -o output

# Or explicitly:
mineru -p document.pdf -o output -b hybrid-auto-engine
```

#### How to Choose?

| Scenario | Backend | Why |
|----------|---------|-----|
| **Batch processing 1000s of docs** | `pipeline` | Fast, cost-effective |
| **Academic papers with complex formulas** | `vlm-auto-engine` | Best formula recognition |
| **General documents, mixed types** | `hybrid-auto-engine` | Balanced speed/accuracy |
| **No GPU available** | `pipeline` | Only CPU-compatible option |
| **High-accuracy requirement** | `vlm-auto-engine` | Maximum precision |

#### Common Mistake 1: Using Wrong Backend

❌ **Mistake**: Using VLM backend on CPU-only machine
```bash
# This will be EXTREMELY slow or fail
mineru -p doc.pdf -o output -b vlm-auto-engine  # No GPU!
```

✅ **Fix**: Use pipeline or hybrid (which falls back gracefully)
```bash
mineru -p doc.pdf -o output -b pipeline
```

---

### Concept 2: Two-Stage Inference Pipeline

MinerU processes documents in **two distinct stages**, not a single pass.

#### Stage 1: Layout Analysis
**Goal**: Understand the document structure

1. **Page Decomposition**: Break document into visual regions
2. **Element Classification**: Identify types (text, table, image, formula, title, list)
3. **Reading Order**: Determine correct sequence (critical for multi-column)
4. **Bounding Boxes**: Locate each element precisely

**Output**: Structured regions with metadata

#### Stage 2: Content Recognition
**Goal**: Extract the actual content

1. **Text Recognition**: OCR for scanned pages, native extraction for text PDFs
2. **Formula Recognition**: Convert math to LaTeX using MFD/MFR models
3. **Table Parsing**: Extract tables as HTML or OTSL format
4. **Image Extraction**: Save images at original resolution

**Output**: Markdown + JSON with all content

#### Why Two Stages Matter

**Example: Multi-Column Document**

```
┌─────────────────────────┐
│  Title: Research Paper  │
├───────────┬─────────────┤
│ Column 1  │  Column 2   │
│ Text A    │  Text C     │
│ Text B    │  Text D     │
│           │  [Table 1]  │
└───────────┴─────────────┘
```

**Without layout analysis** (single-pass):
```markdown
Title: Research Paper Text A Text C Text B Text D [Table 1]
# WRONG! Reading order broken
```

**With two-stage pipeline**:
```markdown
# Title: Research Paper

Text A
Text B

Text C
Text D

[Table 1]
# CORRECT! Proper reading order
```

#### Common Mistake 2: Ignoring Reading Order

❌ **Mistake**: Assuming PDF text order = reading order
- PDFs store text in rendering order, NOT reading order
- Multi-column documents often have garbled order

✅ **Understanding**: MinerU's two-stage approach fixes this automatically

---

### Concept 3: Modular Model Design

MinerU uses a **single multi-task model** instead of multiple specialized models.

#### Traditional Approach (Multiple Models)

```
OCR Model (500MB) → Language Detection Model (200MB)
  ↓
Layout Analysis Model (800MB) → Table Parser (600MB)
  ↓
Formula Recognition Model (1GB) → Handwriting Model (700MB)

Total: ~3.8GB, 6 separate models, complex coordination
```

#### MinerU Approach (Unified Model)

```
MinerU2.5-Pro Model (1.2B parameters, ~2.4GB)
  ├── Multilingual recognition (109 languages)
  ├── Handwriting recognition
  ├── Layout analysis
  ├── Table parsing
  ├── Formula recognition
  └── Reading order sorting

Total: ~2.4GB, single model, simple deployment
```

#### Benefits of Modular Design

1. **Simpler Deployment**: One model download, not six
2. **Shared Representations**: Model learns cross-task patterns
3. **Consistent Quality**: Same architecture across all tasks
4. **Lower Memory**: No duplication of base layers
5. **Faster Updates**: Update one model, all tasks improve

#### How It Works Internally

```python
# Conceptual (simplified)
class MinerUModel:
    def __init__(self):
        self.shared_encoder = VisionEncoder()  # Shared across tasks
        self.layout_head = LayoutHead()
        self.ocr_head = OCRHead()
        self.formula_head = FormulaHead()
        self.table_head = TableHead()

    def forward(self, image):
        features = self.shared_encoder(image)  # Once!
        layout = self.layout_head(features)
        text = self.ocr_head(features)
        formulas = self.formula_head(features)
        tables = self.table_head(features)
        return layout, text, formulas, tables
```

#### Common Mistake 3: Trying to Use Individual Models

❌ **Mistake**: Looking for separate formula/OCR models to optimize
```bash
# No separate model for "just formulas"
mineru --only-formulas document.pdf  # Doesn't exist!
```

✅ **Understanding**: MinerU's modular design means you get all capabilities, always. Optimize by choosing the right backend instead.

---

### Concept 4: Format Preservation & Conversion

MinerU doesn't just extract text - it **understands and converts document elements** intelligently.

#### Element Type Conversions

| Document Element | Input Format | MinerU Output | Why It Matters |
|------------------|--------------|---------------|----------------|
| **Text** | PDF glyphs | Plain text | Native extraction (fast) |
| **Formulas** | Images/glyphs | LaTeX code | `$E=mc^2$` is compilable |
| **Tables** | Visual layout | HTML structure | `<table><tr><td>` preserves structure |
| **Lists** | Bullets/numbers | Markdown lists | `- item` or `1. item` |
| **Headings** | Font size/style | Markdown headers | `#`, `##`, `###` |
| **Images** | Embedded | PNG/JPEG files | Original resolution |

#### Formula Conversion Deep Dive

**Input**: Mathematical formula in PDF (as image or font glyphs)

**MinerU Output**:
```latex
Inline: The equation $E = mc^2$ relates energy and mass.

Display:
$$
\int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}
$$
```

**Why LaTeX?**
- ✅ Machine-readable (LLMs can process)
- ✅ Re-renderable (can typeset again)
- ✅ Searchable (find equations)
- ✅ Editable (modify formulas)

**Competing Tools** often output:
```
"An equation showing E equals m times c squared"
# Description, not formula! ❌
```

#### Table Conversion Deep Dive

**Input**: Complex table in PDF

**MinerU Output** (HTML):
```html
<table>
  <thead>
    <tr>
      <th>Model</th>
      <th>Accuracy</th>
      <th>Speed</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>MinerU</td>
      <td>95.69%</td>
      <td>1800 pages/hr</td>
    </tr>
  </tbody>
</table>
```

**Alternative**: OTSL (Table Structure Language)
```
<otsl>
  <row><cell>Model</cell><cell>Accuracy</cell><cell>Speed</cell></row>
  <row><cell>MinerU</cell><cell>95.69%</cell><cell>1800 pages/hr</cell></row>
</otsl>
```

**Why Structured Output?**
- ✅ Preserves cell relationships
- ✅ Can be converted to any format (Markdown, CSV, JSON)
- ✅ Maintains merged cells and complex layouts

#### Markdown Structure Preservation

```markdown
# Document Title

## Section 1

This is a paragraph with **bold** and *italic* text.

- Bulleted list item 1
- Bulleted list item 2
  - Nested item

1. Numbered list
2. Second item

### Subsection

[Table 1 is shown here]

![Figure 1: Extracted image](images/img_001.jpg)

The formula $\alpha + \beta = \gamma$ appears inline.
```

**Reading order is preserved** - critical for comprehension!

#### Common Mistake 4: Expecting Perfect OCR Without Understanding

❌ **Mistake**: Assuming scanned PDFs work perfectly without OCR configuration
```bash
# Scanned PDF with poor quality
mineru -p scanned_doc.pdf -o output
# Result: Garbled text, missing characters
```

✅ **Fix**: Understand that format preservation depends on input quality
- Native text PDFs: Near-perfect extraction
- High-quality scans: 95%+ accuracy
- Low-quality scans: May need pre-processing (denoising, deskewing)
- Handwritten text: Lower accuracy (but MinerU still tries!)

---

### Concept 5: Artifact Cleaning & Extraction

Documents contain **noise** (artifacts) that pollute the content. MinerU intelligently removes these.

#### Common Document Artifacts

**Headers & Footers**
```
┌──────────────────────────────┐
│ Document Title        Page 1 │  ← Header (artifact)
├──────────────────────────────┤
│                              │
│  Actual content here...      │  ← Keep this!
│                              │
├──────────────────────────────┤
│ © 2024 Company   Confidential│  ← Footer (artifact)
└──────────────────────────────┘
```

**Page Numbers**: `1`, `2`, `3`... (usually redundant)

**Footnote Markers**: `[1]`, `*`, `†` (can break reading flow)

**Watermarks**: "DRAFT", "CONFIDENTIAL" overlays

**Decorative Elements**: Borders, lines, background images

#### How MinerU Handles Artifacts

**1. Spatial Analysis**
- Identifies repeating elements across pages
- Detects edge-positioned elements (typical headers/footers)
- Recognizes isolation from main content

**2. Semantic Analysis**
- Distinguishes navigation elements from content
- Identifies boilerplate patterns
- Preserves meaningful footnotes while removing markers

**3. Cleaning Strategy**
```python
# Conceptual flow
def clean_artifacts(page):
    # Detect artifacts
    headers = detect_repeating_top_elements(page)
    footers = detect_repeating_bottom_elements(page)
    page_numbers = detect_isolated_numbers(page)

    # Remove them
    content = page.elements
    content = remove_elements(content, headers)
    content = remove_elements(content, footers)
    content = remove_elements(content, page_numbers)

    # Maintain semantic coherence
    content = merge_split_paragraphs(content)
    content = maintain_reading_order(content)

    return content
```

#### Before vs After Example

**Before Cleaning** (Raw extraction):
```markdown
Company Confidential                                    Page 5

Introduction

The quick brown fox jumps over the lazy dog.

© 2024 Acme Corp                              Document ID: 12345

Company Confidential                                    Page 6

This is a continuation of the previous paragraph
but it was split across pages.

© 2024 Acme Corp                              Document ID: 12345
```

**After Cleaning** (MinerU output):
```markdown
# Introduction

The quick brown fox jumps over the lazy dog. This is a continuation of the previous paragraph but it was split across pages.
```

**What was removed:**
- ❌ Headers: "Company Confidential"
- ❌ Footers: "© 2024 Acme Corp" + Document ID
- ❌ Page numbers: "Page 5", "Page 6"
- ❌ Page breaks: Merged split paragraph

**What was preserved:**
- ✅ Section heading
- ✅ Content text
- ✅ Semantic coherence

#### Intelligent Footnote Handling

**Challenge**: Some footnotes are meaningful, others are artifacts.

**MinerU's Approach**:
```markdown
# Original PDF Content
"Recent studies[1] show significant improvements."

[1] Smith et al., 2024, Journal of AI Research

# MinerU Output (preserves meaningful footnotes)
"Recent studies[^1] show significant improvements."

[^1]: Smith et al., 2024, Journal of AI Research
```

**But removes inline citation artifacts** when appropriate:
```markdown
# Input: "As demonstrated [see page 45] previously..."
# Output: "As demonstrated previously..."
```

#### Common Mistake 5: Expecting Manual Control Over Artifact Removal

❌ **Mistake**: Looking for flags to customize artifact removal
```bash
# No such flags exist
mineru -p doc.pdf -o output --keep-headers --remove-footers
```

✅ **Understanding**: MinerU's artifact removal is **automatic and intelligent**. It's designed to "just work" without configuration.

**If you need artifacts preserved**:
- Use `--debug` mode to see what was removed
- Post-process the JSON output (contains all elements)
- Report edge cases on GitHub Issues for model improvement

---

### Core Concepts Summary

| Concept | Key Insight | Why It Matters |
|---------|-------------|----------------|
| **1. Multi-Backend** | Choose speed vs accuracy | Match backend to use case |
| **2. Two-Stage Pipeline** | Layout → Content | Preserves reading order |
| **3. Modular Model** | Single model, many tasks | Simple deployment |
| **4. Format Conversion** | Tables→HTML, Formulas→LaTeX | Machine-readable output |
| **5. Artifact Cleaning** | Automatic noise removal | Clean, usable content |

### Mental Model: How MinerU Works

```
Input Document (PDF/Image/DOCX)
         ↓
   [Stage 1: Layout Analysis]
   - Identify regions
   - Classify elements
   - Determine reading order
         ↓
   [Stage 2: Content Recognition]
   - Extract text (OCR/native)
   - Parse tables → HTML
   - Convert formulas → LaTeX
   - Extract images
         ↓
   [Artifact Cleaning]
   - Remove headers/footers
   - Clean page numbers
   - Merge split paragraphs
         ↓
   Output: Clean Markdown + JSON + Images
```

**Key Takeaway**: MinerU is a **pipeline**, not a simple function. Understanding the stages helps you debug issues and optimize usage.

---

## Level 4: Practical Patterns

Now that you understand the concepts, let's build real solutions!

### Pattern 1: Simple Document Parsing (CLI)

**Use Case**: Quick one-off document conversion

#### Basic Usage

```bash
# Single file
mineru -p document.pdf -o output

# Directory of files
mineru -p /path/to/pdfs/ -o output

# Specific backend
mineru -p document.pdf -o output -b pipeline
```

#### Output Structure

```
output/
└── document/
    └── auto/
        ├── document.md              # Main Markdown output
        ├── document_content_list.json  # Detailed metadata
        └── images/                  # Extracted images
            ├── img_001.jpg
            └── img_002.png
```

#### Accessing Results

```bash
# Read Markdown
cat output/document/auto/document.md

# Parse JSON for programmatic access
python -c "import json; print(json.load(open('output/document/auto/document_content_list.json')))"
```

---

### Pattern 2: Python API Integration

**Use Case**: Integrate MinerU into Python applications

#### Example 1: Synchronous Parsing

```python
from mineru.cli.common import do_parse

# Parse a single document
result = do_parse(
    pdf_path="input.pdf",
    output_dir="output",
    backend="hybrid-auto-engine"  # or "pipeline", "vlm-auto-engine"
)

print(f"Parsing complete: {result}")

# Result contains:
# - Exit code (0 = success)
# - Output paths
# - Metadata
```

#### Example 2: Asynchronous Parsing (Recommended for Multiple Files)

```python
import asyncio
from mineru.cli.common import aio_do_parse

async def parse_documents(file_list):
    tasks = []
    for pdf_file in file_list:
        task = aio_do_parse(
            pdf_path=pdf_file,
            output_dir=f"output/{pdf_file.stem}",
            backend="hybrid-auto-engine"
        )
        tasks.append(task)

    # Parse all documents concurrently
    results = await asyncio.gather(*tasks)
    return results

# Run the async function
file_list = [Path("doc1.pdf"), Path("doc2.pdf"), Path("doc3.pdf")]
results = asyncio.run(parse_documents(file_list))

print(f"Parsed {len(results)} documents")
```

#### Example 3: Processing with Configuration

```python
from pathlib import Path
from mineru.cli.common import do_parse

def process_research_papers(input_dir, output_dir):
    """Process academic papers with VLM backend for best formula recognition."""
    input_path = Path(input_dir)
    output_path = Path(output_dir)

    # Find all PDFs
    pdf_files = list(input_path.glob("*.pdf"))

    results = []
    for pdf_file in pdf_files:
        print(f"Processing: {pdf_file.name}")

        result = do_parse(
            pdf_path=str(pdf_file),
            output_dir=str(output_path / pdf_file.stem),
            backend="vlm-auto-engine"  # Best for formulas
        )

        results.append({
            "file": pdf_file.name,
            "status": "success" if result == 0 else "failed",
            "output": output_path / pdf_file.stem
        })

    return results

# Usage
results = process_research_papers("papers/", "output/")
for r in results:
    print(f"{r['file']}: {r['status']}")
```

---

### Pattern 3: REST API Server

**Use Case**: Deploy MinerU as a service for multiple clients

#### Step 1: Start the API Server

```bash
# Start FastAPI server
mineru-api --host 0.0.0.0 --port 8000

# Server starts at http://localhost:8000
# API docs available at http://localhost:8000/docs
```

#### Step 2: Submit Documents via API

**Synchronous Endpoint** (`/file_parse` - wait for result):

```python
import requests

# Upload and parse immediately
with open("document.pdf", "rb") as f:
    response = requests.post(
        "http://localhost:8000/file_parse",
        files={"file": f},
        data={"backend": "hybrid-auto-engine"}
    )

result = response.json()
print(f"Markdown output:\n{result['markdown']}")
print(f"Metadata:\n{result['metadata']}")
```

**Asynchronous Endpoint** (`/tasks` - submit and check later):

```python
import requests
import time

# Step 1: Submit task
with open("large_document.pdf", "rb") as f:
    response = requests.post(
        "http://localhost:8000/tasks",
        files={"file": f},
        data={"backend": "vlm-auto-engine"}
    )

task_id = response.json()["task_id"]
print(f"Task submitted: {task_id}")

# Step 2: Poll for completion
while True:
    status_response = requests.get(f"http://localhost:8000/tasks/{task_id}")
    status_data = status_response.json()

    if status_data["status"] == "completed":
        print("Parsing complete!")
        result = status_data["result"]
        break
    elif status_data["status"] == "failed":
        print(f"Parsing failed: {status_data['error']}")
        break
    else:
        print("Processing...")
        time.sleep(5)  # Wait 5 seconds before checking again

# Step 3: Retrieve results
print(f"Output:\n{result['markdown']}")
```

#### Step 3: Using Existing API Server (Client Mode)

```bash
# Start local parsing with external API
mineru -p document.pdf -o output --api-url http://your-server:8000

# This sends the document to the specified API instead of processing locally
```

---

### Pattern 4: Building a RAG Pipeline

**Use Case**: Extract and index documents for Retrieval Augmented Generation

#### Complete RAG Pipeline Example

```python
from pathlib import Path
from mineru.cli.common import do_parse
import json

class DocumentRAGPipeline:
    def __init__(self, output_dir="rag_output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def parse_document(self, pdf_path, split_pages=True):
        """
        Parse document for RAG.

        Args:
            pdf_path: Path to PDF
            split_pages: If True, maintain page-level granularity for RAG
        """
        pdf_path = Path(pdf_path)
        output_path = self.output_dir / pdf_path.stem

        # Parse with MinerU
        result = do_parse(
            pdf_path=str(pdf_path),
            output_dir=str(output_path),
            backend="hybrid-auto-engine"
        )

        if result != 0:
            raise Exception(f"Parsing failed for {pdf_path}")

        return self._load_parsed_content(output_path)

    def _load_parsed_content(self, output_path):
        """Load parsed content from MinerU output."""
        md_file = output_path / "auto" / f"{output_path.name}.md"
        json_file = output_path / "auto" / f"{output_path.name}_content_list.json"

        with open(md_file, "r", encoding="utf-8") as f:
            markdown = f.read()

        with open(json_file, "r", encoding="utf-8") as f:
            metadata = json.load(f)

        return {
            "markdown": markdown,
            "metadata": metadata,
            "images_dir": output_path / "auto" / "images"
        }

    def chunk_for_rag(self, content, chunk_size=1000, overlap=200):
        """
        Split content into chunks for RAG indexing.

        Args:
            content: Parsed content from parse_document()
            chunk_size: Target chunk size in characters
            overlap: Overlap between chunks
        """
        markdown = content["markdown"]
        chunks = []

        # Simple chunking by paragraph and size
        paragraphs = markdown.split("\n\n")
        current_chunk = ""

        for para in paragraphs:
            if len(current_chunk) + len(para) < chunk_size:
                current_chunk += para + "\n\n"
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = para + "\n\n"

        if current_chunk:
            chunks.append(current_chunk.strip())

        return chunks

    def process_for_rag(self, pdf_path):
        """End-to-end: parse and chunk for RAG."""
        # Step 1: Parse
        print(f"Parsing {pdf_path}...")
        content = self.parse_document(pdf_path)

        # Step 2: Chunk
        print("Chunking for RAG...")
        chunks = self.chunk_for_rag(content)

        # Step 3: Add metadata
        rag_docs = []
        for i, chunk in enumerate(chunks):
            rag_docs.append({
                "chunk_id": i,
                "content": chunk,
                "source": str(pdf_path),
                "metadata": {
                    "total_chunks": len(chunks),
                    "images_available": len(list(content["images_dir"].glob("*"))) if content["images_dir"].exists() else 0
                }
            })

        print(f"Created {len(rag_docs)} chunks for indexing")
        return rag_docs

# Usage
pipeline = DocumentRAGPipeline()
rag_documents = pipeline.process_for_rag("research_paper.pdf")

# Now index these chunks in your vector database (e.g., Pinecone, Weaviate, ChromaDB)
for doc in rag_documents:
    print(f"Chunk {doc['chunk_id']}: {doc['content'][:100]}...")
    # vector_db.add(doc['content'], metadata=doc['metadata'])
```

---

### Pattern 5: Batch Processing with Progress Tracking

**Use Case**: Process hundreds/thousands of documents efficiently

```python
from pathlib import Path
from mineru.cli.common import do_parse
import json
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

class BatchProcessor:
    def __init__(self, input_dir, output_dir, backend="pipeline", max_workers=4):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.backend = backend
        self.max_workers = max_workers
        self.output_dir.mkdir(exist_ok=True)

    def process_single(self, pdf_path):
        """Process a single PDF."""
        try:
            output_path = self.output_dir / pdf_path.stem
            result = do_parse(
                pdf_path=str(pdf_path),
                output_dir=str(output_path),
                backend=self.backend
            )

            return {
                "file": pdf_path.name,
                "status": "success" if result == 0 else "failed",
                "output": str(output_path)
            }
        except Exception as e:
            return {
                "file": pdf_path.name,
                "status": "error",
                "error": str(e)
            }

    def process_batch(self):
        """Process all PDFs in input directory."""
        pdf_files = list(self.input_dir.glob("*.pdf"))

        if not pdf_files:
            print(f"No PDF files found in {self.input_dir}")
            return []

        print(f"Found {len(pdf_files)} PDF files to process")
        print(f"Using backend: {self.backend}")
        print(f"Max workers: {self.max_workers}")

        results = []

        # Process with progress bar
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all tasks
            future_to_pdf = {
                executor.submit(self.process_single, pdf): pdf
                for pdf in pdf_files
            }

            # Track progress
            with tqdm(total=len(pdf_files), desc="Processing PDFs") as pbar:
                for future in as_completed(future_to_pdf):
                    result = future.result()
                    results.append(result)
                    pbar.update(1)

                    # Update description with status
                    success_count = sum(1 for r in results if r["status"] == "success")
                    pbar.set_postfix({"success": success_count, "failed": len(results) - success_count})

        return results

    def save_report(self, results, report_path="batch_report.json"):
        """Save processing report."""
        report = {
            "total": len(results),
            "success": sum(1 for r in results if r["status"] == "success"),
            "failed": sum(1 for r in results if r["status"] != "success"),
            "details": results
        }

        with open(self.output_dir / report_path, "w") as f:
            json.dump(report, indent=2, fp=f)

        print(f"\nReport saved to {self.output_dir / report_path}")
        print(f"Success: {report['success']}/{report['total']}")
        print(f"Failed: {report['failed']}/{report['total']}")

# Usage
processor = BatchProcessor(
    input_dir="documents/",
    output_dir="output/",
    backend="pipeline",  # Fast CPU-only processing
    max_workers=4  # Adjust based on your CPU cores
)

results = processor.process_batch()
processor.save_report(results)
```

---

### Pattern 6: Multi-Format Processing

**Use Case**: Handle PDFs, images, Word docs, PowerPoint, Excel

```python
from pathlib import Path
from mineru.cli.common import do_parse

class MultiFormatProcessor:
    SUPPORTED_FORMATS = {
        ".pdf": "PDF Document",
        ".jpg": "Image",
        ".jpeg": "Image",
        ".png": "Image",
        ".docx": "Word Document",
        ".pptx": "PowerPoint Presentation",
        ".xlsx": "Excel Spreadsheet"
    }

    def __init__(self, output_dir="output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def process_file(self, file_path, backend="hybrid-auto-engine"):
        """Process any supported file format."""
        file_path = Path(file_path)

        if file_path.suffix.lower() not in self.SUPPORTED_FORMATS:
            raise ValueError(f"Unsupported format: {file_path.suffix}")

        print(f"Processing {self.SUPPORTED_FORMATS[file_path.suffix.lower()]}: {file_path.name}")

        output_path = self.output_dir / file_path.stem

        result = do_parse(
            pdf_path=str(file_path),  # Works for all formats!
            output_dir=str(output_path),
            backend=backend
        )

        return result == 0

    def process_directory(self, input_dir):
        """Process all supported files in a directory."""
        input_path = Path(input_dir)

        # Find all supported files
        files = []
        for ext in self.SUPPORTED_FORMATS.keys():
            files.extend(input_path.glob(f"*{ext}"))

        print(f"Found {len(files)} supported files")

        results = {}
        for file in files:
            try:
                success = self.process_file(file)
                results[file.name] = "success" if success else "failed"
            except Exception as e:
                results[file.name] = f"error: {str(e)}"

        return results

# Usage
processor = MultiFormatProcessor()

# Process a single file
processor.process_file("document.pdf")
processor.process_file("presentation.pptx")
processor.process_file("spreadsheet.xlsx")
processor.process_file("scanned_doc.jpg")

# Or process entire directory
results = processor.process_directory("mixed_documents/")
print(results)
```

---

### Pattern 7: WebUI for Non-Technical Users

**Use Case**: Provide a browser-based interface

```bash
# Start Gradio WebUI
mineru-gradio --server-name 0.0.0.0 --server-port 7860

# Access at http://localhost:7860
```

**Features of WebUI:**
- Drag-and-drop file upload
- Backend selection (Pipeline/VLM/Hybrid)
- Real-time processing status
- Download results (Markdown + JSON)
- Preview extracted content

**Use Cases:**
- ✅ Internal tool for team members
- ✅ Demo for stakeholders
- ✅ Testing documents before scripting

---

### Common Patterns Summary

| Pattern | Use Case | Key Tool |
|---------|----------|----------|
| **CLI** | Quick one-off conversions | `mineru -p <file> -o <dir>` |
| **Python API** | Application integration | `do_parse()`, `aio_do_parse()` |
| **REST API** | Service deployment | `mineru-api` server |
| **RAG Pipeline** | LLM data preparation | Parse + chunk + index |
| **Batch Processing** | Large-scale conversion | ThreadPoolExecutor |
| **Multi-Format** | Mixed document types | Same API for all formats |
| **WebUI** | Non-technical users | `mineru-gradio` |

---

## Level 5: Next Steps

Congratulations! You now have a solid foundation in MinerU. Here's how to go deeper.

### Advanced Topics to Explore

#### 1. Performance Optimization

**Topic**: Scale to thousands of documents efficiently

**Resources:**
- **Flash-MinerU**: Ray-based distributed processing
  - GitHub: https://github.com/opendatalab/MinerU (see docs on distributed mode)
  - Use case: Process 10,000+ documents across multiple GPUs

- **mineru-router**: Load balancing for multiple instances
  - Deploy multiple `mineru-api` servers
  - Route requests via `mineru-router` or nginx
  - Pattern: N instances with `MAX_CONCURRENT_REQUESTS=1` each

**Key Insights:**
- Single instance: ~1,800 pages/hour
- With 4 GPUs + mineru-router: ~7,200 pages/hour
- CPU-only cluster: ~85% accuracy, high throughput

**Hands-on Project:**
- Set up a 4-worker mineru-api cluster
- Implement load balancing
- Benchmark throughput

---

#### 2. Advanced Configuration

**Topic**: Fine-tune MinerU behavior via `mineru.json`

**Configuration File Location:**
- Linux/macOS: `~/.config/mineru/mineru.json`
- Windows: `%USERPROFILE%\.config\mineru\mineru.json`

**Key Settings:**
```json
{
  "latex_delimiters": {
    "inline": ["$", "$"],
    "display": ["$$", "$$"]
  },
  "llm_assisted_title_hierarchy": true,
  "model_dirs": {
    "layout": "/path/to/models/layout",
    "ocr": "/path/to/models/ocr"
  },
  "effort_parsing_strength": "high"
}
```

**Resources:**
- Configuration docs: https://opendatalab.github.io/MinerU/usage/configuration/
- Model management: https://opendatalab.github.io/MinerU/usage/models/

**Experiment:**
- Try `effort_parsing_strength: "medium"` vs `"high"`
- Measure accuracy vs speed tradeoff
- Test different LaTeX delimiter styles

---

#### 3. Custom Model Deployment

**Topic**: Host your own MinerU models for air-gapped environments

**Steps:**
1. Download models from HuggingFace:
   ```bash
   huggingface-cli download opendatalab/MinerU2.5-Pro-2604-1.2B
   ```

2. Configure local model paths in `mineru.json`

3. Deploy without internet access

**Resources:**
- Model Hub: https://huggingface.co/opendatalab
- Air-gapped deployment guide: https://opendatalab.github.io/MinerU/deployment/airgapped/

**Use Case:**
- Corporate environments with security restrictions
- Government/defense applications
- HIPAA/GDPR compliance requirements

---

#### 4. Integration with AI Frameworks

**Topic**: Connect MinerU to LangChain, LlamaIndex, Dify, etc.

**LangChain Integration Example:**
```python
from langchain.document_loaders import UnstructuredMarkdownLoader
from mineru.cli.common import do_parse
import tempfile

def load_pdf_with_mineru(pdf_path):
    """Custom LangChain loader using MinerU."""
    # Parse with MinerU
    with tempfile.TemporaryDirectory() as tmpdir:
        do_parse(pdf_path=pdf_path, output_dir=tmpdir, backend="hybrid-auto-engine")

        # Find output markdown
        md_file = Path(tmpdir) / Path(pdf_path).stem / "auto" / f"{Path(pdf_path).stem}.md"

        # Load with LangChain
        loader = UnstructuredMarkdownLoader(str(md_file))
        documents = loader.load()

    return documents

# Use in LangChain pipeline
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma

docs = load_pdf_with_mineru("research_paper.pdf")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = text_splitter.split_documents(docs)

# Index in vector DB
vectorstore = Chroma.from_documents(chunks, embedding_function)
```

**Resources:**
- LangChain docs: https://python.langchain.com/docs/integrations/document_loaders/
- Dify integration: Mentioned in MinerU docs
- FastGPT integration: https://github.com/labring/FastGPT

---

#### 5. Handling Edge Cases

**Topic**: Troubleshoot challenging documents

**Common Issues & Solutions:**

| Issue | Solution |
|-------|----------|
| **Vertical text** | Not supported - rotate PDF first with `pdftk` |
| **Complex nested tables** | May need manual post-processing |
| **Handwritten text** | Lower accuracy - consider pre-training on your handwriting |
| **Non-Latin scripts** | Ensure proper font support (especially Linux) |
| **Scanned low-quality docs** | Pre-process with ImageMagick (denoise, deskew) |

**Pre-processing Example:**
```bash
# Improve scanned PDF quality
convert input.pdf -density 300 -depth 8 -quality 90 output.pdf

# Then parse with MinerU
mineru -p output.pdf -o results
```

**Resources:**
- FAQ: https://opendatalab.github.io/MinerU/faq/
- GitHub Issues: https://github.com/opendatalab/MinerU/issues (search for similar problems)

---

#### 6. Contributing to MinerU

**Topic**: Improve MinerU and give back to the community

**Ways to Contribute:**

1. **Report Bugs**: Submit detailed issues with example PDFs
   - Include: MinerU version, backend used, expected vs actual output
   - Template: https://github.com/opendatalab/MinerU/issues/new

2. **Submit Examples**: Share challenging documents for testing
   - Helps improve model training
   - Especially valuable: edge cases (vertical text, rare languages)

3. **Code Contributions**: Fix bugs, add features
   - Fork repository: https://github.com/opendatalab/MinerU
   - Follow contribution guidelines
   - Submit pull request

4. **Documentation**: Improve tutorials, fix typos
   - Docs source: https://github.com/opendatalab/MinerU/tree/main/docs

5. **Community Support**: Answer questions in GitHub Discussions
   - Help newcomers
   - Share your use cases

**Getting Started:**
- Read: https://github.com/opendatalab/MinerU/blob/main/CONTRIBUTING.md
- Join: GitHub Discussions for coordination

---

### Best Resources for Continued Learning

#### Official Documentation (Essential)
- **Main Docs**: https://opendatalab.github.io/MinerU/
- **API Reference**: https://mineru.net/apiManage/docs
- **Changelog**: https://opendatalab.github.io/MinerU/reference/changelog/ (stay updated!)

#### Research Papers (Deep Understanding)
1. **MinerU Core**: https://arxiv.org/abs/2409.18839
2. **MinerU2.5**: https://arxiv.org/pdf/2509.22186
3. **MinerU2.5-Pro**: https://arxiv.org/pdf/2604.04771

#### Community (Ask Questions)
- **GitHub Discussions**: https://github.com/opendatalab/MinerU/discussions
- **GitHub Issues**: https://github.com/opendatalab/MinerU/issues

#### Tutorials (Hands-On)
- **StableLearn Beginner's Guide**: https://stable-learn.com/en/mineru-tutorial/
- **Sonu Sahani Blog**: https://sonusahani.com/blogs/mineru
- **YouTube Tutorial**: https://www.youtube.com/watch?v=xjC2_61ULe4

#### Benchmarks & Comparisons (Context)
- **Tool Comparison**: https://jimmysong.io/blog/pdf-to-markdown-open-source-deep-dive/
- **12 OCR Tools Analysis**: https://liduos.com/en/posts/ai-develope-tools-series-2-open-source-doucment-parsing

---

### Community Channels

**Where to Get Help:**

1. **GitHub Discussions** (Primary): https://github.com/opendatalab/MinerU/discussions
   - General questions
   - Feature requests
   - Use case sharing

2. **GitHub Issues** (Bugs): https://github.com/opendatalab/MinerU/issues
   - Bug reports
   - Technical problems

3. **HuggingFace Demo** (Try Online): https://huggingface.co/spaces/opendatalab/MinerU
   - Test before installing
   - Quick experiments

**When Asking for Help:**
- ✅ Provide MinerU version: `mineru --version`
- ✅ Include backend used: `pipeline`, `vlm-auto-engine`, etc.
- ✅ Share error messages (full traceback)
- ✅ Describe expected vs actual behavior
- ✅ Provide sample PDF if possible (or similar example)

---

### Hands-On Mini-Project: Build a Document Knowledge Base

**Goal**: Create an end-to-end system that parses documents and enables semantic search.

**Requirements:**
- Python 3.10+
- MinerU installed
- A collection of PDFs (10-50 documents)

**Steps:**

1. **Parse Documents**
   ```python
   # Use Pattern 5 (Batch Processing) from Level 4
   # Process all PDFs into Markdown
   ```

2. **Chunk for RAG**
   ```python
   # Use Pattern 4 (RAG Pipeline) from Level 4
   # Split into chunks with metadata
   ```

3. **Generate Embeddings**
   ```python
   from sentence_transformers import SentenceTransformer

   model = SentenceTransformer('all-MiniLM-L6-v2')
   embeddings = model.encode(chunks)
   ```

4. **Index in Vector Database**
   ```python
   import chromadb

   client = chromadb.Client()
   collection = client.create_collection("documents")
   collection.add(embeddings=embeddings, documents=chunks, ids=ids)
   ```

5. **Implement Search**
   ```python
   def search(query, top_k=5):
       query_embedding = model.encode([query])
       results = collection.query(query_embeddings=query_embedding, n_results=top_k)
       return results

   # Test
   results = search("What is the main conclusion of the research?")
   print(results)
   ```

6. **Add LLM Generation** (Optional)
   ```python
   from openai import OpenAI

   client = OpenAI()

   def answer_question(query):
       # Retrieve relevant chunks
       results = search(query, top_k=3)
       context = "\n\n".join(results['documents'])

       # Generate answer
       response = client.chat.completions.create(
           model="gpt-4",
           messages=[
               {"role": "system", "content": "Answer based on provided context."},
               {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {query}"}
           ]
       )
       return response.choices[0].message.content

   # Test
   answer = answer_question("What methodology was used in the study?")
   print(answer)
   ```

**Expected Outcome:**
- Fully functional document QA system
- Hands-on experience with MinerU + RAG
- Understanding of end-to-end pipeline

**Extensions:**
- Add WebUI with Gradio/Streamlit
- Support multiple languages
- Implement re-ranking
- Add document update/deletion

---

### Certification & Validation

**How to Know You've Mastered MinerU:**

✅ **Beginner Level**
- [ ] Can install MinerU on your system
- [ ] Parse a PDF using CLI
- [ ] Understand three backend types
- [ ] Read and interpret Markdown output

✅ **Intermediate Level**
- [ ] Use Python API for parsing
- [ ] Process multiple documents in batch
- [ ] Choose appropriate backend for use case
- [ ] Integrate MinerU into a Python application

✅ **Advanced Level**
- [ ] Deploy mineru-api REST service
- [ ] Build a complete RAG pipeline
- [ ] Optimize performance for large-scale processing
- [ ] Troubleshoot edge cases
- [ ] Contribute to MinerU project (bug reports, PRs)

**Validation Project:**
Build a "Document Intelligence System" that:
1. Accepts PDF uploads
2. Parses with MinerU
3. Extracts entities (tables, formulas, images)
4. Enables semantic search
5. Provides summary generation

---

### Final Thoughts

You've now completed the MinerU learning path! Here's what you've achieved:

- ✅ **Level 1**: Understood the "why" behind MinerU
- ✅ **Level 2**: Got hands-on with installation and first parse
- ✅ **Level 3**: Mastered core concepts and architecture
- ✅ **Level 4**: Built real-world patterns and integrations
- ✅ **Level 5**: Know where to go for advanced topics

**What's Next?**

1. **Apply to Your Work**: Use MinerU in your projects
2. **Experiment**: Try challenging documents, test limits
3. **Share**: Write blog posts, create tutorials
4. **Contribute**: Help improve MinerU for everyone
5. **Stay Updated**: Watch the GitHub repo for new releases

**Keep Learning Resources Handy:**
- 📚 Bookmark: https://opendatalab.github.io/MinerU/
- 💬 Join: https://github.com/opendatalab/MinerU/discussions
- 🔔 Watch: https://github.com/opendatalab/MinerU (get notified of updates)

**Remember**: Document parsing is complex, and MinerU is actively improving. Not every document will be perfect on the first try. Use the community, report issues, and iterate!

---

**Happy Parsing! 🚀**

If you found this guide helpful, consider:
- ⭐ Starring the MinerU repository
- 📝 Sharing your use cases in GitHub Discussions
- 🐛 Reporting bugs to help improve the tool
- 📚 Contributing to documentation

**You're now ready to transform documents into knowledge!**
