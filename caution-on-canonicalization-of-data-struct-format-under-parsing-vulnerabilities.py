import json
import xml.etree.ElementTree as ET

# Simulate a canonicalization issue where an XML input is misparsed due to comments in the data.
def parse_xml_to_json_with_bug(xml_data):
    # Parse the XML and remove comments (simulating canonicalization behavior)
    root = ET.fromstring(xml_data)
    
    # Convert XML data to JSON
    data = {}
    for elem in root.iter():
        if elem.tag == "NameId":
            # Simulate misinterpretation due to comment being included in the XML data
            data['NameId'] = elem.text  # This could result in an incorrect value due to bug
    return json.dumps(data)

# Example of correctly formatted XML
correct_xml = """<Assertion>
                    <NameId>trump@org.com</NameId>
                  </Assertion>"""

# Maliciously crafted XML with a comment inserted in the NameId value
malicious_xml = """<Assertion>
                      <NameId>trump@org.com<!---->.evil.com</NameId>
                    </Assertion>"""

# Parse both the correct and rigged XML into JSON
correct_json = parse_xml_to_json_with_bug(correct_xml)
malicious_json = parse_xml_to_json_with_bug(malicious_xml)

# Print both outputs to show the discrepancy
print("Correct XML -> JSON Conversion:")
print(correct_json)

print("\nMalicious XML -> JSON Conversion:")
print(malicious_json)


"""
Correct XML -> JSON Conversion:
{"NameId": "trump@org.com"}

Malicious XML -> JSON Conversion:
{"NameId": "trump@org.com.evil.com"}

"""