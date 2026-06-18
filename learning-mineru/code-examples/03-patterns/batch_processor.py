#!/usr/bin/env python3
"""
Batch document processor with progress tracking and error handling.

Features:
- Parallel processing with thread pool
- Progress bar with tqdm
- Detailed error reporting
- JSON report generation
- Resume capability
"""

import json
import sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from mineru.cli.common import do_parse

try:
    from tqdm import tqdm
    HAS_TQDM = True
except ImportError:
    HAS_TQDM = False
    print("⚠️  tqdm not installed - progress bar disabled")
    print("   Install with: pip install tqdm")

class BatchProcessor:
    """Process multiple documents in parallel with MinerU."""

    def __init__(self, input_dir, output_dir, backend="pipeline", max_workers=4):
        """
        Initialize batch processor.

        Args:
            input_dir: Directory containing PDF files
            output_dir: Directory for outputs
            backend: MinerU backend (pipeline/hybrid/vlm)
            max_workers: Number of parallel workers
        """
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.backend = backend
        self.max_workers = max_workers

        self.output_dir.mkdir(exist_ok=True)

        # Resume support
        self.status_file = self.output_dir / "batch_status.json"
        self.processed_files = self._load_status()

    def _load_status(self):
        """Load previously processed files."""
        if self.status_file.exists():
            with open(self.status_file, "r") as f:
                status = json.load(f)
                return set(status.get("processed", []))
        return set()

    def _save_status(self, filename):
        """Save processed file status."""
        self.processed_files.add(str(filename))
        with open(self.status_file, "w") as f:
            json.dump({"processed": list(self.processed_files)}, f)

    def process_single(self, pdf_path):
        """
        Process a single PDF file.

        Args:
            pdf_path: Path to PDF file

        Returns:
            Dictionary with processing results
        """
        try:
            output_path = self.output_dir / pdf_path.stem

            result = do_parse(
                pdf_path=str(pdf_path),
                output_dir=str(output_path),
                backend=self.backend
            )

            # Mark as processed
            self._save_status(pdf_path.name)

            if result == 0:
                # Get output size
                md_file = output_path / "auto" / f"{pdf_path.stem}.md"
                output_size = md_file.stat().st_size if md_file.exists() else 0

                return {
                    "file": pdf_path.name,
                    "status": "success",
                    "output": str(output_path),
                    "output_size_kb": output_size / 1024
                }
            else:
                return {
                    "file": pdf_path.name,
                    "status": "failed",
                    "error_code": result
                }

        except Exception as e:
            return {
                "file": pdf_path.name,
                "status": "error",
                "error": str(e)
            }

    def find_pdfs(self):
        """Find all PDF files in input directory."""
        pdf_files = list(self.input_dir.glob("*.pdf"))

        # Filter out already processed files
        new_files = [
            f for f in pdf_files
            if f.name not in self.processed_files
        ]

        if len(self.processed_files) > 0:
            print(f"⏭️  Skipping {len(self.processed_files)} already processed files")

        return new_files

    def process_batch(self):
        """Process all PDFs in input directory."""
        pdf_files = self.find_pdfs()

        if not pdf_files:
            if len(self.processed_files) > 0:
                print("✅ All files already processed!")
            else:
                print(f"❌ No PDF files found in {self.input_dir}")
            return []

        print(f"📚 Processing {len(pdf_files)} PDF files")
        print(f"⚙️  Backend: {self.backend}")
        print(f"🔧 Workers: {self.max_workers}")
        print()

        results = []

        # Process with thread pool
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all tasks
            future_to_pdf = {
                executor.submit(self.process_single, pdf): pdf
                for pdf in pdf_files
            }

            # Track progress
            if HAS_TQDM:
                progress_bar = tqdm(total=len(pdf_files), desc="Processing")

            for future in as_completed(future_to_pdf):
                result = future.result()
                results.append(result)

                if HAS_TQDM:
                    # Update progress bar
                    success_count = sum(1 for r in results if r["status"] == "success")
                    progress_bar.set_postfix({
                        "success": success_count,
                        "failed": len(results) - success_count
                    })
                    progress_bar.update(1)
                else:
                    # Simple text progress
                    print(f"[{len(results)}/{len(pdf_files)}] {result['file']}: {result['status']}")

            if HAS_TQDM:
                progress_bar.close()

        return results

    def save_report(self, results):
        """Save processing report."""
        report = {
            "total": len(results),
            "success": sum(1 for r in results if r["status"] == "success"),
            "failed": sum(1 for r in results if r["status"] == "failed"),
            "errors": sum(1 for r in results if r["status"] == "error"),
            "backend": self.backend,
            "max_workers": self.max_workers,
            "results": results
        }

        report_file = self.output_dir / "batch_report.json"
        with open(report_file, "w") as f:
            json.dump(report, f, indent=2)

        return report_file, report

def main():
    if len(sys.argv) < 2:
        print("Usage: python batch_processor.py <input_dir> [backend] [max_workers]")
        print("\nExample:")
        print("  python batch_processor.py documents/")
        print("  python batch_processor.py documents/ pipeline 8")
        sys.exit(1)

    input_dir = sys.argv[1]
    backend = sys.argv[2] if len(sys.argv) > 2 else "pipeline"
    max_workers = int(sys.argv[3]) if len(sys.argv) > 3 else 4

    if not Path(input_dir).exists():
        print(f"Error: Directory not found: {input_dir}")
        sys.exit(1)

    print("=" * 60)
    print("Batch Document Processor")
    print("=" * 60)
    print(f"Input directory: {input_dir}")
    print(f"Output directory: output_batch/")
    print(f"Backend: {backend}")
    print(f"Max workers: {max_workers}")
    print()

    # Create processor
    processor = BatchProcessor(
        input_dir=input_dir,
        output_dir="output_batch",
        backend=backend,
        max_workers=max_workers
    )

    # Process all documents
    results = processor.process_batch()

    if not results:
        sys.exit(0)

    # Save report
    report_file, report = processor.save_report(results)

    # Print summary
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"✅ Success: {report['success']}")
    print(f"❌ Failed: {report['failed']}")
    print(f"⚠️  Errors: {report['errors']}")
    print(f"📊 Total: {report['total']}")
    print(f"\n📄 Report saved to: {report_file}")

    # Show failed files
    failed = [r for r in results if r["status"] != "success"]
    if failed:
        print("\n❌ Failed files:")
        for r in failed:
            print(f"  - {r['file']}: {r.get('error', r.get('error_code', 'unknown'))}")

    print("\n💡 Tip: Re-run this script to resume from where it stopped")

if __name__ == "__main__":
    main()
