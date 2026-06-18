#!/usr/bin/env python3
"""
Complete RAG (Retrieval Augmented Generation) pipeline using MinerU.

This example demonstrates:
1. Document parsing with MinerU
2. Text chunking for RAG
3. Metadata extraction
4. Preparation for vector database indexing
"""

import json
import sys
from pathlib import Path
from mineru.cli.common import do_parse

class MinerURAGPipeline:
    """RAG pipeline built on MinerU document parsing."""

    def __init__(self, output_dir="rag_output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def parse_document(self, pdf_path, backend="hybrid-auto-engine"):
        """
        Parse a document with MinerU.

        Args:
            pdf_path: Path to PDF file
            backend: MinerU backend to use

        Returns:
            Dictionary with parsed content and metadata
        """
        pdf_path = Path(pdf_path)
        output_path = self.output_dir / pdf_path.stem

        print(f"📄 Parsing: {pdf_path.name}")

        result = do_parse(
            pdf_path=str(pdf_path),
            output_dir=str(output_path),
            backend=backend
        )

        if result != 0:
            raise Exception(f"Parsing failed for {pdf_path}")

        return self._load_parsed_content(output_path, pdf_path)

    def _load_parsed_content(self, output_path, original_file):
        """Load parsed content from MinerU output."""
        stem = output_path.name
        md_file = output_path / "auto" / f"{stem}.md"
        json_file = output_path / "auto" / f"{stem}_content_list.json"
        images_dir = output_path / "auto" / "images"

        # Load markdown
        with open(md_file, "r", encoding="utf-8") as f:
            markdown = f.read()

        # Load metadata
        with open(json_file, "r", encoding="utf-8") as f:
            metadata = json.load(f)

        # Count images
        image_count = len(list(images_dir.glob("*"))) if images_dir.exists() else 0

        return {
            "markdown": markdown,
            "metadata": metadata,
            "images_dir": str(images_dir),
            "image_count": image_count,
            "source_file": str(original_file),
            "page_count": len(metadata) if isinstance(metadata, list) else 0
        }

    def chunk_for_rag(self, content, chunk_size=1000, overlap=200):
        """
        Split document into chunks suitable for RAG.

        Args:
            content: Parsed content from parse_document()
            chunk_size: Target size in characters
            overlap: Overlap between chunks in characters

        Returns:
            List of text chunks
        """
        markdown = content["markdown"]
        chunks = []

        # Split by double newlines (paragraphs)
        paragraphs = markdown.split("\n\n")

        current_chunk = ""
        current_size = 0

        for para in paragraphs:
            para_size = len(para)

            # If adding this paragraph would exceed chunk_size
            if current_size + para_size > chunk_size and current_chunk:
                chunks.append(current_chunk.strip())

                # Start new chunk with overlap
                # Take last 'overlap' characters from current chunk
                if len(current_chunk) > overlap:
                    current_chunk = current_chunk[-overlap:] + "\n\n" + para
                    current_size = len(current_chunk)
                else:
                    current_chunk = para
                    current_size = para_size
            else:
                # Add paragraph to current chunk
                if current_chunk:
                    current_chunk += "\n\n" + para
                else:
                    current_chunk = para
                current_size += para_size

        # Add final chunk
        if current_chunk:
            chunks.append(current_chunk.strip())

        return chunks

    def create_rag_documents(self, pdf_path, chunk_size=1000, overlap=200):
        """
        End-to-end: parse document and create RAG-ready chunks.

        Args:
            pdf_path: Path to PDF
            chunk_size: Target chunk size
            overlap: Overlap between chunks

        Returns:
            List of RAG documents with chunks and metadata
        """
        # Step 1: Parse with MinerU
        print(f"\n{'='*60}")
        print("Step 1: Parsing Document")
        print(f"{'='*60}")
        content = self.parse_document(pdf_path)
        print(f"✅ Parsed {content['page_count']} pages")
        print(f"✅ Found {content['image_count']} images")

        # Step 2: Chunk for RAG
        print(f"\n{'='*60}")
        print("Step 2: Chunking for RAG")
        print(f"{'='*60}")
        print(f"Chunk size: {chunk_size} characters")
        print(f"Overlap: {overlap} characters")

        chunks = self.chunk_for_rag(content, chunk_size, overlap)
        print(f"✅ Created {len(chunks)} chunks")

        # Step 3: Create RAG documents
        print(f"\n{'='*60}")
        print("Step 3: Creating RAG Documents")
        print(f"{'='*60}")

        rag_docs = []
        for i, chunk in enumerate(chunks):
            doc = {
                "chunk_id": i,
                "content": chunk,
                "metadata": {
                    "source": content["source_file"],
                    "chunk_index": i,
                    "total_chunks": len(chunks),
                    "page_count": content["page_count"],
                    "has_images": content["image_count"] > 0,
                    "image_count": content["image_count"],
                    "images_dir": content["images_dir"]
                }
            }
            rag_docs.append(doc)

        print(f"✅ Created {len(rag_docs)} RAG documents")

        return rag_docs

    def save_rag_documents(self, rag_docs, output_file="rag_documents.json"):
        """Save RAG documents to JSON file."""
        output_path = self.output_dir / output_file

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(rag_docs, f, indent=2, ensure_ascii=False)

        print(f"\n💾 Saved to: {output_path}")

        return output_path

def main():
    if len(sys.argv) < 2:
        print("Usage: python rag_pipeline.py <input.pdf> [chunk_size] [overlap]")
        print("\nExample:")
        print("  python rag_pipeline.py document.pdf")
        print("  python rag_pipeline.py document.pdf 1500 300")
        sys.exit(1)

    pdf_path = sys.argv[1]
    chunk_size = int(sys.argv[2]) if len(sys.argv) > 2 else 1000
    overlap = int(sys.argv[3]) if len(sys.argv) > 3 else 200

    if not Path(pdf_path).exists():
        print(f"Error: File not found: {pdf_path}")
        sys.exit(1)

    print("=" * 60)
    print("MinerU RAG Pipeline")
    print("=" * 60)
    print(f"Input: {pdf_path}")
    print(f"Chunk size: {chunk_size}")
    print(f"Overlap: {overlap}")

    # Create pipeline
    pipeline = MinerURAGPipeline()

    # Process document
    rag_docs = pipeline.create_rag_documents(pdf_path, chunk_size, overlap)

    # Save to JSON
    output_file = pipeline.save_rag_documents(rag_docs)

    # Show sample chunks
    print("\n" + "=" * 60)
    print("Sample Chunks (first 3)")
    print("=" * 60)

    for doc in rag_docs[:3]:
        print(f"\n--- Chunk {doc['chunk_id']} ---")
        print(f"Length: {len(doc['content'])} characters")
        print(f"Preview: {doc['content'][:200]}...")

    print("\n" + "=" * 60)
    print("Next Steps")
    print("=" * 60)
    print("1. Load RAG documents from:", output_file)
    print("2. Generate embeddings using sentence-transformers")
    print("3. Index in vector database (ChromaDB, Pinecone, etc.)")
    print("4. Implement semantic search")
    print("5. Connect to LLM for question answering")
    print("\nExample:")
    print("  from sentence_transformers import SentenceTransformer")
    print("  model = SentenceTransformer('all-MiniLM-L6-v2')")
    print("  embeddings = model.encode([doc['content'] for doc in rag_docs])")

if __name__ == "__main__":
    main()
