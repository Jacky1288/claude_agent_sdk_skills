# MinerU Code Examples

Runnable code examples demonstrating MinerU usage patterns.

## Directory Structure

```
code-examples/
├── 01-hello-world/       # Getting started examples
├── 02-core-concepts/     # Understanding MinerU internals
└── 03-patterns/          # Real-world usage patterns
```

## Prerequisites

Before running these examples, ensure:

1. **MinerU is installed**:
   ```bash
   uv pip install -U "mineru[all]"
   ```

2. **Python 3.10+ is available**:
   ```bash
   python --version
   ```

3. **Test PDFs are available** (or use your own):
   ```bash
   # Download a sample PDF
   curl -o sample.pdf "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"
   ```

## 01-hello-world/

Basic examples for first-time users.

### verify_installation.py

Check if MinerU is properly installed and configured.

```bash
python 01-hello-world/verify_installation.py
```

**What it checks:**
- MinerU import
- Dependencies
- System RAM
- GPU availability
- Recommended backend for your system

### basic_parse.sh

Simplest way to parse a document with MinerU.

```bash
chmod +x 01-hello-world/basic_parse.sh
./01-hello-world/basic_parse.sh sample.pdf
```

**Output**: `output/` directory with Markdown and JSON

## 02-core-concepts/

Examples demonstrating MinerU's core architecture.

### backend_comparison.py

Compare all three backends on the same document.

```bash
python 02-core-concepts/backend_comparison.py sample.pdf
```

**What it does:**
- Parses with `pipeline`, `hybrid-auto-engine`, and `vlm-auto-engine`
- Measures execution time for each
- Compares output sizes
- Shows which backend is fastest

**Use this to:** Understand backend tradeoffs and choose the right one.

### async_processing.py

Asynchronous document processing for concurrent execution.

```bash
# Process multiple files concurrently
python 02-core-concepts/async_processing.py doc1.pdf doc2.pdf doc3.pdf

# With specific backend
python 02-core-concepts/async_processing.py *.pdf pipeline
```

**What it does:**
- Processes multiple documents concurrently using `asyncio`
- Compares concurrent vs sequential time
- Shows speed benefits of async processing

**Use this to:** Learn how to process documents in parallel efficiently.

## 03-patterns/

Real-world patterns for production use.

### rag_pipeline.py

Complete RAG pipeline: parse → chunk → prepare for indexing.

```bash
python 03-patterns/rag_pipeline.py document.pdf

# With custom chunk size
python 03-patterns/rag_pipeline.py document.pdf 1500 300
```

**What it does:**
1. Parses document with MinerU
2. Splits into chunks with overlap
3. Adds metadata for RAG
4. Saves to JSON for indexing

**Output**: `rag_output/rag_documents.json` ready for vector database

**Use this to:** Build a document Q&A system or RAG pipeline.

### batch_processor.py

Process hundreds/thousands of documents with progress tracking.

```bash
python 03-patterns/batch_processor.py documents/

# With specific backend and worker count
python 03-patterns/batch_processor.py documents/ pipeline 8
```

**Features:**
- Parallel processing with thread pool
- Progress bar (if tqdm installed)
- Resume capability (skips already processed files)
- Detailed JSON report
- Error handling and reporting

**Use this to:** Process large document collections efficiently.

## Running Examples

### Quick Start

1. **Verify installation**:
   ```bash
   python 01-hello-world/verify_installation.py
   ```

2. **Parse your first document**:
   ```bash
   ./01-hello-world/basic_parse.sh sample.pdf
   ```

3. **Compare backends**:
   ```bash
   python 02-core-concepts/backend_comparison.py sample.pdf
   ```

### Common Issues

**Issue: "ModuleNotFoundError: No module named 'mineru'"**
```bash
# Solution: Install MinerU
uv pip install -U "mineru[all]"
```

**Issue: "tqdm not installed" (batch_processor.py)**
```bash
# Solution: Install tqdm for progress bar
pip install tqdm
```

**Issue: "CUDA not available" (when using VLM backend)**
```bash
# Solution: Use pipeline or hybrid backend instead
python script.py document.pdf pipeline
```

**Issue: "Out of memory"**
```bash
# Solution: Use pipeline backend (CPU-only, less memory)
python script.py document.pdf pipeline
```

## Example Workflows

### Workflow 1: Single Document Analysis

```bash
# 1. Parse document
python 01-hello-world/basic_parse.sh research_paper.pdf

# 2. View output
cat output/research_paper/auto/research_paper.md
```

### Workflow 2: RAG Pipeline Setup

```bash
# 1. Parse and chunk document
python 03-patterns/rag_pipeline.py document.pdf

# 2. Review chunks
cat rag_output/rag_documents.json

# 3. Index in vector database (your code here)
```

### Workflow 3: Batch Processing

```bash
# 1. Organize PDFs in directory
mkdir documents
cp *.pdf documents/

# 2. Process all documents
python 03-patterns/batch_processor.py documents/ pipeline 4

# 3. Review report
cat output_batch/batch_report.json

# 4. If interrupted, resume
python 03-patterns/batch_processor.py documents/ pipeline 4
```

### Workflow 4: Backend Selection

```bash
# 1. Compare backends on sample
python 02-core-concepts/backend_comparison.py sample.pdf

# 2. Choose fastest for your use case
# - pipeline: CPU-only, fast
# - hybrid-auto-engine: balanced (default)
# - vlm-auto-engine: highest accuracy (GPU required)

# 3. Use chosen backend in production
python 03-patterns/batch_processor.py documents/ pipeline 8
```

## Customization

All examples can be modified for your needs:

### Change Backend

```python
# In any Python script, modify:
backend="pipeline"  # Change to: "hybrid-auto-engine" or "vlm-auto-engine"
```

### Adjust Chunk Size (RAG)

```python
# In rag_pipeline.py
chunk_size=1000   # Change to: 500, 1500, 2000, etc.
overlap=200       # Change to: 100, 300, 400, etc.
```

### Change Worker Count (Batch)

```python
# In batch_processor.py
max_workers=4  # Change to: 2, 8, 16, etc. (based on CPU cores)
```

## Next Steps

After running these examples:

1. **Integrate into your application**: Use patterns as templates
2. **Experiment with your documents**: Test on real PDFs
3. **Optimize performance**: Benchmark different backends and settings
4. **Build production systems**: Scale up with batch processing and APIs
5. **Contribute back**: Share your examples on GitHub Discussions

## Need Help?

- **Documentation**: https://opendatalab.github.io/MinerU/
- **GitHub Issues**: https://github.com/opendatalab/MinerU/issues
- **Discussions**: https://github.com/opendatalab/MinerU/discussions
- **Learning Path**: See `../learning-path.md`

## License

These examples are provided as-is for educational purposes. Use freely in your projects.

---

Happy coding! 🚀
