#!/usr/bin/env python3
"""
Compare different MinerU backends on the same document.

This script parses the same PDF with all three backends and
compares execution time and output quality.
"""

import sys
import time
from pathlib import Path
from mineru.cli.common import do_parse

def parse_with_backend(pdf_path, backend, output_dir):
    """Parse a document with a specific backend and measure time."""
    print(f"\n{'='*60}")
    print(f"Backend: {backend}")
    print(f"{'='*60}")

    start_time = time.time()

    try:
        result = do_parse(
            pdf_path=pdf_path,
            output_dir=output_dir,
            backend=backend
        )

        elapsed_time = time.time() - start_time

        if result == 0:
            print(f"✅ Success in {elapsed_time:.2f} seconds")

            # Get output file size
            md_file = Path(output_dir) / Path(pdf_path).stem / "auto" / f"{Path(pdf_path).stem}.md"
            if md_file.exists():
                file_size = md_file.stat().st_size / 1024  # KB
                print(f"📄 Output size: {file_size:.1f} KB")
            else:
                print("⚠️  Output file not found")

            return {
                "backend": backend,
                "status": "success",
                "time": elapsed_time,
                "output": output_dir
            }
        else:
            print(f"❌ Failed (exit code: {result})")
            return {
                "backend": backend,
                "status": "failed",
                "time": elapsed_time,
                "error_code": result
            }

    except Exception as e:
        elapsed_time = time.time() - start_time
        print(f"❌ Error: {str(e)}")
        return {
            "backend": backend,
            "status": "error",
            "time": elapsed_time,
            "error": str(e)
        }

def main():
    if len(sys.argv) < 2:
        print("Usage: python backend_comparison.py <input.pdf>")
        sys.exit(1)

    pdf_path = sys.argv[1]

    if not Path(pdf_path).exists():
        print(f"Error: File not found: {pdf_path}")
        sys.exit(1)

    print("=" * 60)
    print("MinerU Backend Comparison")
    print("=" * 60)
    print(f"Input: {pdf_path}")
    print()

    backends = [
        ("pipeline", "output_pipeline"),
        ("hybrid-auto-engine", "output_hybrid"),
        ("vlm-auto-engine", "output_vlm")
    ]

    results = []

    for backend, output_dir in backends:
        result = parse_with_backend(pdf_path, backend, output_dir)
        results.append(result)

    # Summary
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)

    success_results = [r for r in results if r["status"] == "success"]

    if success_results:
        print("\n⏱️  Execution Times:")
        for r in success_results:
            print(f"  {r['backend']:25} {r['time']:8.2f}s")

        fastest = min(success_results, key=lambda x: x["time"])
        print(f"\n⚡ Fastest: {fastest['backend']} ({fastest['time']:.2f}s)")

    print("\n📊 Status Summary:")
    for r in results:
        status_icon = "✅" if r["status"] == "success" else "❌"
        print(f"  {status_icon} {r['backend']:25} {r['status']}")

    print("\n💡 Recommendations:")
    print("  - pipeline: Best for batch processing (CPU-only)")
    print("  - hybrid-auto-engine: Balanced speed and accuracy (default)")
    print("  - vlm-auto-engine: Highest accuracy (requires GPU)")

    print("\nOutputs saved to:")
    for r in results:
        if r["status"] == "success":
            print(f"  {r['backend']:25} → {r['output']}/")

if __name__ == "__main__":
    main()
