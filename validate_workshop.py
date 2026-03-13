#!/usr/bin/env python3
"""
Complete Workshop Validation Script
Tests all components across both Python versions
"""

import subprocess
import sys
import os

def run_test(python_path, script_path, test_name):
    """Run a single test and report results"""
    try:
        result = subprocess.run(
            [python_path, script_path],
            capture_output=True,
            text=True,
            timeout=30
        )
        success = result.returncode == 0
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} | {test_name}")
        if not success and result.stderr:
            print(f"     Error: {result.stderr[:100]}...")
        return success
    except Exception as e:
        print(f"❌ ERROR | {test_name}: {str(e)[:50]}")
        return False

def main():
    # Use the script's directory as the base path to avoid hard-coded absolute paths
    base_path = os.path.dirname(os.path.abspath(__file__))
    
    print("\n" + "=" * 80)
    print("🚀 COMPLETE WORKSHOP VALIDATION")
    print("=" * 80 + "\n")
    
    # Python 3.14 tests
    py314_venv = f"{base_path}/.venv/bin/python"
    
    print("PYTHON 3.14 ENVIRONMENT (.venv)")
    print("-" * 80)
    
    test_results_314 = {
        "Day-1: Text Cleaner": run_test(py314_venv, f"{base_path}/Day-1/text_cleaner.py", "text_cleaner.py"),
        "Day-1: Semantic Similarity": run_test(py314_venv, f"{base_path}/Day-1/semantic_similarity.py", "semantic_similarity.py"),
        "Day-1: FAQ Finder": run_test(py314_venv, f"{base_path}/Day-1/faq_finder.py", "faq_finder.py"),
        "Day-3: Gemini Wrapper": run_test(py314_venv, f"{base_path}/Day-3/gemini_wrapper.py", "gemini_wrapper.py"),
    }
    
    py311_venv = f"{base_path}/.venv311/bin/python"
    
    print("\nPYTHON 3.11 ENVIRONMENT (.venv311)")
    print("-" * 80)
    
    test_results_311 = {
        "Day-2: Chunking Utility": run_test(py311_venv, f"{base_path}/Day-2/chunking_utility.py", "chunking_utility.py"),
        "Day-2: Knowledge Base": run_test(py311_venv, f"{base_path}/Day-2/knowledge_base.py", "knowledge_base.py"),
    }
    
    # Summary
    print("\n" + "=" * 80)
    print("📊 TEST SUMMARY")
    print("=" * 80 + "\n")
    
    all_results = {**test_results_314, **test_results_311}
    passed = sum(1 for v in all_results.values() if v)
    total = len(all_results)
    
    print(f"Python 3.14 Tests: {sum(1 for v in test_results_314.values() if v)}/{len(test_results_314)}")
    print(f"Python 3.11 Tests: {sum(1 for v in test_results_311.values() if v)}/{len(test_results_311)}")
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! Workshop is fully functional!")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. See above for details.")
    
    print("\n" + "=" * 80)
    print("✨ AVAILABLE COMMANDS")
    print("=" * 80 + "\n")
    print("Python 3.14 Components:")
    print(f'  "{py314_venv}" "Day-1/text_cleaner.py"')
    print(f'  "{py314_venv}" "Day-1/semantic_similarity.py"')
    print(f'  "{py314_venv}" "Day-1/faq_finder.py"')
    print(f'  "{py314_venv}" "Day-3/gemini_wrapper.py"')
    print(f'  "{py314_venv}" "Day-3/rag_agent.py"')
    print(f'  "{py314_venv}" "Day-3/streamlit_app.py"')
    
    print("\nPython 3.11 Components:")
    print(f'  "{py311_venv}" "Day-2/chunking_utility.py"')
    print(f'  "{py311_venv}" "Day-2/knowledge_base.py"')
    
    return 0 if passed == total else 1

if __name__ == "__main__":
    sys.exit(main())
