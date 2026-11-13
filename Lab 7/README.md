LAB 7 - FUZZ TESTING SUBMISSION KIT

Files:
- original_processor.py : exact buggy starter implementation
- processor.py          : hardened implementation
- test_processor.py     : 3 Hypothesis fuzz tests + 3 valid-input tests
- capture_lab7_evidence.py : runs both versions, creates 4 PNG command-output
  evidence images, and assembles Lab7_FuzzTesting_Report.pdf
- requirements.txt      : required Python packages

RUN ON WINDOWS (PowerShell) OR TERMINAL
1. Open this folder in the terminal.
2. Install dependencies:
   python -m pip install -r requirements.txt
3. Run evidence/report generation:
   python capture_lab7_evidence.py

The script intentionally runs the original version first and expects its fuzz
tests to fail. It then runs the fixed version and requires all tests to pass.
If either expectation is not met, it stops and tells you which stage failed.

Generated files:
- evidence/01_original_application.png
- evidence/02_original_fuzz_failures.png
- evidence/03_fixed_application.png
- evidence/04_fixed_tests_passed.png
- Lab7_FuzzTesting_Report.pdf

The PNG files are terminal-output evidence captured from actual subprocess
runs on the computer where the script is executed. They are not screenshots
of a physical monitor. If your instructor specifically requires desktop
screenshots, open each command/output in your terminal and use Win+Shift+S.

IMPORTANT:
The report must only be submitted after the evidence script completes
successfully on your machine. The script checks that original tests fail and
fixed tests pass; it does not silently invent test results.
