# Caution On Canonicalization Of Data Struct Format Under Parsing Vulnerabilities

This memo serves as a cautionary note regarding the challenges and vulnerabilities associated with canonicalization processes in various data formats, specifically XML and JSON. While these processes may seem simple in concept, their implementations can often lead to severe security vulnerabilities if not handled with precision. One of the most notable issues is the misalignment between canonicalization strategies and parsing expectations, leading to unexpected or malicious behavior in systems that rely on these standards.

<hr>

## Canonicalization Challenges:

The term "canonicalization" refers to the process of converting data into a standard, well-defined format. Mismatched formats in canonicalization can create a vulnerability. 

The bug utilized a specially crafted <NameId> element in the SAML assertion, which contained a comment that would be processed differently depending on the canonicalization and parsing strategies used. This discrepancy caused one system to interpret the NameId as a valid address, while the other incorrectly parsed the NameId, allowing attackers to bypass validation mechanisms.

## Key Example – SAML Vulnerability:

This bug broke basically every SAML implementation. One notable example of a critical canonicalization bug occurred in the SAML (Security Assertion Markup Language) ecosystem, which broke numerous SAML implementations. This vulnerability was exploited through NameId manipulation.

It used NameIds (SAML-speak for “the entity this assertion is about”) that look like this:

<NameId>trump@org.com<!---->.evil.com</NameId>

The common canonicalization strategy ("exc-c14n") removes comments, interpreting the NameId as "trump@org.com.evil.com". The common parsing strategy sees this as a sequence of text nodes and comments, and interprets only the first node: "trump@org.com", which is not what the IdP (Identity Provider, messed up by the interprter lib, e.g. XML-DSIG library) signed.
This leads to a mismatch between what is expected by the system and what is validated, potentially allowing attackers to bypass security checks.

Specs also contradicts and/disambuates to create confusion and bugs, e.g.: Canonical JSON (from OLPC) and an RFC. 

<pre>
Expected Output:
Correct XML to JSON Conversion:

Correct XML -> JSON Conversion:
{"NameId": "barney@latacora.com"}
Malicious XML to JSON Conversion:

Malicious XML -> JSON Conversion:
{"NameId": "barney@latacora.com.evil.com"}
</pre>

## JSON and Canonicalization:

While transitioning from XML to JSON might appear simpler, it comes with its own set of canonicalization issues. There are at least two specifications to consider: Canonical JSON from OLPC and the RFC governing JSON. Both have their own nuances, and the process of canonicalizing and validating JSON is not always straightforward or foolproof. Like XML, canonicalization issues can lead to inconsistent or unintended behaviors, especially in security-sensitive operations.

## Recommendation:

Strict Validation: Always ensure that the canonicalization and parsing strategies are consistent across all components of a system. The validation process should match the expectations of all parties involved (e.g., IdPs, Service Providers, etc.). 

Strict Formats and Templates: Ensure start, length, end (termination), hashed, etc. 

Comprehensive Testing: Conduct thorough testing to ensure that canonicalization processes do not introduce security holes. Implement automated tests that validate data integrity across various formats (XML, JSON, etc.).

Review Standards and Libraries: When using canonicalization libraries or protocols, ensure they are up to date with security patches and follow well-defined standards. Rely on widely accepted and actively maintained libraries to handle canonicalization.

Monitor and Audit: Regularly audit security implementations that involve canonicalization processes. Be proactive in addressing any deviations or inconsistencies in parsing behaviors.

