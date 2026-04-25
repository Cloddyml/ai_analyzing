def make_rule_prompt(
    bug: dict,
    bad_stream: str = "",
    good_stream: str = "",
    retry_hint: str = "",
) -> str:
    rule_id = bug["id"].lower().replace("-", "_")

    lines = []
    lines.append("You are a cppcheck static analysis expert.")
    lines.append(
        "Generate a cppcheck custom rule in XML format to detect a specific C bug."
    )
    lines.append("")
    lines.append(f"BUG: {bug['id']} — {bug['name']}")
    lines.append(bug["description"])
    lines.append("")

    if bad_stream:
        lines.append("=" * 55)
        lines.append("STEP 1: Study these token streams carefully")
        lines.append("=" * 55)
        lines.append("")
        lines.append("cppcheck converts C source to a TOKEN STREAM before matching.")
        lines.append("Tokens are separated by EXACTLY ONE SPACE. No newlines ever.")
        lines.append("")
        lines.append("YOUR PATTERN MUST MATCH a substring of this BAD stream:")
        lines.append(f"  {bad_stream}")
        lines.append("")
        if good_stream:
            lines.append("YOUR PATTERN MUST NOT MATCH anything in this GOOD stream:")
            lines.append(f"  {good_stream}")
            lines.append("")
        lines.append("Look at the difference between the two streams above.")
        lines.append("Find a token sequence that appears in BAD but NOT in GOOD.")
        lines.append("")
    else:
        lines.append("BAD code (rule MUST trigger):")
        lines.append(bug["bad_code"])
        lines.append("")
        lines.append("GOOD code (rule MUST NOT trigger):")
        lines.append(bug["good_code"])
        lines.append("")

    lines.append("=" * 55)
    lines.append("STEP 2: Write the pattern — strict rules")
    lines.append("=" * 55)
    lines.append("")
    lines.append("Token stream examples (memorize these transformations):")
    lines.append("  free(ptr);        ->  free ( ptr ) ;")
    lines.append("  int *p = NULL;    ->  int * p = NULL ;")
    lines.append("  if (!data)        ->  if ( ! data )")
    lines.append("  return a + b;     ->  return a + b ;")
    lines.append("  arr[idx]          ->  arr [ idx ]")
    lines.append("")
    lines.append("CORRECT — always add spaces around brackets and operators:")
    lines.append(r"  free \( \w+ \)                    good")
    lines.append(r"  strcpy \( \w+ , \w+ \)            good")
    lines.append(r"  return \w+ \+ \w+ ;               good  (space before ;)")
    lines.append(r"  free \( (\w+) \) .* \* \1         good  (backreference)")
    lines.append(r"  [^=]= NULL                        good  (avoids == NULL)")
    lines.append(r"  malloc \( .* \) (?!.* free \()    good  (lookahead)")
    lines.append("")
    lines.append("WRONG — common mistakes that break matching:")
    lines.append(r"  free\(        WRONG — missing space before (")
    lines.append(r"  return \w+;   WRONG — semicolon needs space: \w+ ;")
    lines.append(r"  arr\[\w+\]    WRONG — brackets need spaces: arr \[ \w+ \]")
    lines.append(r"  \s+           WRONG — use single literal space")
    lines.append(r"  [^)]+         WRONG — ) has spaces around it in token stream")
    lines.append(r"  \* \w+        WRONG — too broad, matches all pointer use")
    lines.append("")
    lines.append("=" * 55)
    lines.append("STEP 3: Output this EXACT XML structure")
    lines.append("=" * 55)
    lines.append("")
    lines.append("IMPORTANT: id, severity, summary MUST be nested INSIDE <message>.")
    lines.append("")
    lines.append('<rule version="1">')
    lines.append("  <pattern>YOUR_REGEX_HERE</pattern>")
    lines.append("  <message>")
    lines.append(f"    <id>{rule_id}</id>")
    lines.append("    <severity>warning</severity>")
    lines.append("    <summary>Short description of the bug</summary>")
    lines.append("  </message>")
    lines.append("</rule>")
    lines.append("")
    lines.append("Output ONLY the XML. No markdown. No explanation.")
    lines.append('Start with: <rule version="1">')

    if retry_hint:
        lines.append("")
        lines.append(f"PREVIOUS ATTEMPT FAILED: {retry_hint}")

    return "\n".join(lines)


def make_retry_hint(attempt: int, reason: str) -> str:
    hints = {
        "no_xml": (
            "Output ONLY the XML block. "
            'Start with <rule version="1"> and end with </rule>. '
            "No markdown (```), no explanation text."
        ),
        "bad_xml": (
            "The XML was malformed. Check that every opening tag has a closing tag. "
            "Do not escape backslashes in <pattern> — write them as-is."
        ),
        "no_pattern": (
            "The <pattern> tag was empty. Look at the BAD token stream and write a regex "
            "that matches part of it. Remember: space before every bracket. "
            r"Example: 'free \( (\w+) \) .* \* \1'"
        ),
    }
    base = hints.get(reason, "Previous attempt failed. Try again carefully.")
    return f"Attempt {attempt + 1} failed. {base}"
