#!/usr/bin/env python3
"""
Demonstrate asynchronous document processing with MinerU.

This example shows how to process multiple documents concurrently
using Python's asyncio and MinerU's async API.
"""

import asyncio
import sys
import time
from pathlib import Path
from mineru.cli.common import aio_do_parse

async def parse_document(pdf_path, output_dir, backend="hybrid-auto-engine"):
    """Asynchronously parse a single document."""
    pdf_path = Path(pdf_path)
    output_path = Path(output_dir) / pdf_path.stem

    print(f"🚀 Starting: {pdf_path.name}")
    start_time = time.time()

    try:
        result = await aio_do_parse(
            pdf_path=str(pdf_path),
            output_dir=str(output_path),
            backend=backend
        )

        elapsed = time.time() - start_time

        if result == 0:
            print(f"✅ Completed: {pdf_path.name} ({elapsed:.1f}s)")
            return {
                "file": pdf_path.name,
                "status": "success",
                "time": elapsed,
                "output": str(output_path)
            }
        else:
            print(f"❌ Failed: {pdf_path.name}")
            return {
                "file": pdf_path.name,
                "status": "failed",
                "time": elapsed,
                "error_code": result
            }

    except Exception as e:
        elapsed = time.time() - start_time
        print(f"❌ Error in {pdf_path.name}: {str(e)}")
        return {
            "file": pdf_path.name,
            "status": "error",
            "time": elapsed,
            "error": str(e)
        }

async def process_batch(pdf_files, output_dir, backend="hybrid-auto-engine"):
    """Process multiple PDFs concurrently."""
    print(f"\n📚 Processing {len(pdf_files)} documents concurrently...")
    print(f"Backend: {backend}")
    print(f"Output directory: {output_dir}\n")

    # Create tasks for all files
    tasks = [
        parse_document(pdf_file, output_dir, backend)
        for pdf_file in pdf_files
    ]

    # Execute all tasks concurrently
    start_time = time.time()
    results = await asyncio.gather(*tasks)
    total_time = time.time() - start_time

    return results, total_time

def main():
    if len(sys.argv) < 2:
        print("Usage: python async_processing.py <pdf1> <pdf2> ... [backend]")
        print("\nExample:")
        print("  python async_processing.py doc1.pdf doc2.pdf doc3.pdf")
        print("  python async_processing.py *.pdf pipeline")
        sys.exit(1)

    # Parse arguments
    files = [arg for arg in sys.argv[1:] if arg.endswith('.pdf')]
    backend = sys.argv[-1] if not sys.argv[-1].endswith('.pdf') else "hybrid-auto-engine"

    if not files:
        print("Error: No PDF files provided")
        sys.exit(1)

    # Verify files exist
    pdf_files = []
    for file in files:
        path = Path(file)
        if path.exists():
            pdf_files.append(path)
        else:
            print(f"⚠️  File not found: {file}")

    if not pdf_files:
        print("Error: No valid PDF files found")
        sys.exit(1)

    print("=" * 60)
    print("Asynchronous Document Processing")
    print("=" * 60)

    # Run async processing
    output_dir = "output_async"
    results, total_time = asyncio.run(process_batch(pdf_files, output_dir, backend))

    # Summary
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)

    success_count = sum(1 for r in results if r["status"] == "success")
    failed_count = len(results) - success_count

    print(f"\n📊 Results:")
    print(f"  Total files: {len(results)}")
    print(f"  ✅ Success: {success_count}")
    print(f"  ❌ Failed: {failed_count}")
    print(f"  ⏱️  Total time: {total_time:.1f}s")

    if success_count > 0:
        avg_time = sum(r["time"] for r in results if r["status"] == "success") / success_count
        print(f"  ⏱️  Average per document: {avg_time:.1f}s")

    print(f"\n💡 Concurrent processing completed in {total_time:.1f}s")
    print(f"   Sequential would take ~{sum(r['time'] for r in results):.1f}s")

    print("\n📁 Outputs saved to:")
    for r in results:
        if r["status"] == "success":
            print(f"  {r['file']:30} → {r['output']}/")

if __name__ == "__main__":
    main()
