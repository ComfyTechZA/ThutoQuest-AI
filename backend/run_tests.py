#!/usr/bin/env python
"""
Test Runner & Coverage Report Generator
Runs all professional-grade tests and generates detailed coverage reports
"""

import subprocess
import sys
import json
from pathlib import Path
from datetime import datetime


def run_tests():
    """Run all tests with coverage and reporting"""
    print("=" * 80)
    print("ThutoQuest AI Backend - Professional Test Suite")
    print("MICT SETA Code Quality Verification")
    print("=" * 80)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Define test suites
    test_suites = [
        {
            "name": "Career Prediction Logic Tests (Tests 1-11)",
            "file": "tests/test_api_quality.py::TestCareerPredictionLogic",
            "markers": "not performance",
        },
        {
            "name": "Database Connection Tests (Tests 12-18)",
            "file": "tests/test_api_quality.py::TestDatabaseConnection",
            "markers": "not performance",
        },
        {
            "name": "Offline-Sync Delta Handler (Tests 19-31)",
            "file": "tests/test_api_quality.py::TestOfflineDeltaSync",
            "markers": "not performance",
        },
        {
            "name": "Integration Tests (Tests 30-31)",
            "file": "tests/test_api_quality.py::TestIntegration",
            "markers": "not performance",
        },
        {
            "name": "Error Handling & Edge Cases (Tests 32-34)",
            "file": "tests/test_api_quality.py::TestErrorHandling",
            "markers": "not performance",
        },
        {
            "name": "Performance & Load Tests (Tests 35-36)",
            "file": "tests/test_api_quality.py::TestPerformance",
            "markers": "performance",
        },
    ]
    
    # Run all tests with coverage
    cmd = [
        "pytest",
        "tests/test_api_quality.py",
        "-v",
        "--tb=short",
        "--cov=src",
        "--cov-report=html",
        "--cov-report=term-missing",
        "-m", "not performance",  # Skip performance tests by default
        "--durations=10",  # Show 10 slowest tests
    ]
    
    print("Command:", " ".join(cmd))
    print()
    
    result = subprocess.run(cmd, cwd=str(Path(__file__).parent.parent))
    
    print("\n" + "=" * 80)
    print("Test Summary Report")
    print("=" * 80)
    print(f"Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    if result.returncode == 0:
        print("✅ ALL TESTS PASSED")
    else:
        print("❌ SOME TESTS FAILED")
    
    print("\nGenerated Reports:")
    print("  - HTML Coverage: htmlcov/index.html")
    print("  - Terminal Coverage: See above")
    print()
    
    return result.returncode


if __name__ == "__main__":
    exit_code = run_tests()
    sys.exit(exit_code)
