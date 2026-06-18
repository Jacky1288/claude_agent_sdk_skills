#!/usr/bin/env python3
"""
Verify MinerU installation and check system capabilities.

Run this after installing MinerU to ensure everything is working correctly.
"""

import sys

def check_mineru_import():
    """Check if MinerU can be imported."""
    try:
        import mineru
        print("✅ MinerU is installed")
        return True
    except ImportError:
        print("❌ MinerU is not installed")
        print("   Install with: uv pip install -U 'mineru[all]'")
        return False

def check_gpu_availability():
    """Check if GPU is available for VLM backend."""
    try:
        import torch
        if torch.cuda.is_available():
            print(f"✅ GPU available: {torch.cuda.get_device_name(0)}")
            print(f"   VRAM: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
            return True
        else:
            print("⚠️  GPU not available (VLM backend will not work)")
            print("   Pipeline backend (CPU-only) is still available")
            return False
    except ImportError:
        print("⚠️  PyTorch not installed (GPU check skipped)")
        return False

def check_dependencies():
    """Check for key dependencies."""
    deps = {
        'PIL': 'Pillow',
        'cv2': 'opencv-python',
        'numpy': 'numpy',
        'requests': 'requests'
    }

    all_installed = True
    for module, package in deps.items():
        try:
            __import__(module)
            print(f"✅ {package} is installed")
        except ImportError:
            print(f"❌ {package} is not installed")
            all_installed = False

    return all_installed

def check_system_resources():
    """Check system RAM."""
    try:
        import psutil
        total_ram = psutil.virtual_memory().total / (1024**3)
        available_ram = psutil.virtual_memory().available / (1024**3)

        print(f"💾 Total RAM: {total_ram:.1f} GB")
        print(f"💾 Available RAM: {available_ram:.1f} GB")

        if total_ram < 16:
            print("⚠️  Warning: Less than 16GB RAM (minimum requirement)")
            print("   You may encounter out-of-memory errors")
            return False
        else:
            print("✅ Sufficient RAM available")
            return True
    except ImportError:
        print("⚠️  psutil not installed (RAM check skipped)")
        return True

def main():
    print("=" * 60)
    print("MinerU Installation Verification")
    print("=" * 60)
    print()

    checks = {
        "MinerU Import": check_mineru_import(),
        "Dependencies": check_dependencies(),
        "System Resources": check_system_resources(),
        "GPU Availability": check_gpu_availability()
    }

    print()
    print("=" * 60)
    print("Summary")
    print("=" * 60)

    all_passed = all(checks.values())

    if all_passed:
        print("✅ All checks passed! MinerU is ready to use.")
    else:
        print("⚠️  Some checks failed. Review the output above.")
        print()
        print("Recommended backends based on your system:")
        if checks["GPU Availability"]:
            print("  - hybrid-auto-engine (default, recommended)")
            print("  - vlm-auto-engine (maximum accuracy)")
            print("  - pipeline (fastest)")
        else:
            print("  - pipeline (CPU-only, recommended for your system)")
            print("  - hybrid-auto-engine (will work but slower without GPU)")

    print()
    print("Next steps:")
    print("  1. Try parsing a document: mineru -p sample.pdf -o output")
    print("  2. Check the documentation: https://opendatalab.github.io/MinerU/")
    print("=" * 60)

    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
