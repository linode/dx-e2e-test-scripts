import datetime
import logging
import os
import xml.etree.ElementTree as ET

timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M")
current_time = datetime.datetime.now()
output_xml_file = current_time.strftime("%Y%m%d%H%M") + "_terraform_merged_report.xml"


def log_and_print(message, level=logging.INFO):
    logging.log(level, message)
    print(message)


def merge_xml_files(input_dir):
    # Create the root element for the new XML
    new_testsuites = ET.Element("testsuites")

    # Create a new <testsuite> element under <testsuites>
    new_testsuite = ET.SubElement(new_testsuites, "testsuite")

    total_failures = 0
    total_skipped = 0
    total_errors = 0
    total_tests = 0

    # Iterate through each XML file in the input directory
    for filename in os.listdir(input_dir):
        if filename.endswith(".xml"):
            filepath = os.path.join(input_dir, filename)
            tree = ET.parse(filepath)
            root = tree.getroot()

            testsuites_element = root

            total_tests += (
                int(testsuites_element.get("tests"))
                if testsuites_element.get("tests") is not None
                else 0
            )
            total_failures += (
                int(testsuites_element.get("failures"))
                if testsuites_element.get("failures") is not None
                else 0
            )
            total_errors += (
                int(testsuites_element.get("errors"))
                if testsuites_element.get("errors") is not None
                else 0
            )
            total_skipped += (
                int(testsuites_element.get("skipped"))
                if testsuites_element.get("skipped") is not None
                else 0
            )

            # Create a new <testsuites> element with aggregated values
            new_testsuite.set("tests", str(total_tests))
            new_testsuite.set("failures", str(total_failures))
            new_testsuite.set("errors", str(total_errors))
            new_testsuite.set("skipped", str(total_skipped))

            for testcase in root.findall(".//testcase"):
                new_testcase = ET.SubElement(
                    new_testsuite, "testcase", attrib=testcase.attrib
                )
                for child in testcase:
                    new_testcase.append(child)

    # Save the new XML to a file
    try:
        new_tree = ET.ElementTree(new_testsuites)
        new_tree.write(output_xml_file, encoding="UTF-8", xml_declaration=True)

        log_and_print(
            f"{timestamp}:XML content successfully over-written to " + output_xml_file
        )
    except Exception as e:
        log_and_print(f"{timestamp}:Error writing XML content:", str(e))


# Example usage specific to ansible repository
input_directory = os.getcwd()

merge_xml_files(input_directory)
