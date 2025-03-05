import xml.etree.ElementTree as ET
import sys
import os


def parse_junit_xml(xml_file):
    """Parse JUnit XML and generate a summary of test results."""
    if not os.path.exists(xml_file):
        print(f"Error: File '{xml_file}' not found.")
        sys.exit(1)

    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Extract statistics from <testsuite> attributes
    testsuite = root.find(".//testsuite")
    total_tests = int(testsuite.get("tests", 0))
    total_failures = int(testsuite.get("failures", 0))
    total_errors = int(testsuite.get("errors", 0))
    total_skipped = int(testsuite.get("skipped", 0))

    passed_tests = total_tests - (total_failures + total_errors + total_skipped)

    failures = []
    errors = []

    for testcase in root.findall(".//testcase"):
        name = testcase.get("name", "Unknown Test")

        failure = testcase.find("failure")
        error = testcase.find("error")
        system_out = testcase.find("system-out")  # Fallback log output

        # Extract failure details
        if failure is not None and failure.text:
            failures.append(f"• `{name}`")

        # Extract error details (fallback to system-out if error is missing)
        error_text = None
        if error is not None and error.text:
            error_text = error.text.strip()
        elif system_out is not None and system_out.text:
            error_text = system_out.text.strip()

        if error_text:
            errors.append(f"• `{name}`")

    # Summary
    summary = f"""
*Test Summary*\\n:white_check_mark: Passed: {passed_tests} :x: Failed: {total_failures} :warning: Errors: {total_errors} :fast_forward: Skipped: {total_skipped} :scroll: Total: {total_tests}\\n
"""

    # Detailed Failures & Errors
    if failures:
        summary += "\\n:x: *Test Failures:*\\n" + "\\n".join(failures) + "\\n"

    if errors:
        summary += "\\n:warning: *Test Errors:*\\n" + "\\n".join(errors) + "\\n"

    return summary.strip()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python parse_junit_report.py <junit_report.xml>")
        sys.exit(1)

    xml_file = sys.argv[1]
    result_summary = parse_junit_xml(xml_file)

    print(result_summary)
