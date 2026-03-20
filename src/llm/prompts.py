def make_rule_prompt(bug: dict, retry_hint: str = "") -> str:
    """
    Строит промпт для генерации cppcheck XML-правила.

    bug — словарь с полями: id, name, description, bad_code, good_code
    retry_hint — дополнительная подсказка при повторной попытке
    """

    rule_id = bug["id"].lower().replace("-", "_")
    bug_id = bug["id"]
    bug_name = bug["name"]
    bug_desc = bug["description"]
    bad_code = bug["bad_code"]
    good_code = bug["good_code"]

    # rf"..." = raw f-string: фигурные скобки для интерполяции работают,
    # но обратные слеши НЕ интерпретируются как escape-последовательности.
    # Это нужно чтобы \( \w+ \b и т.д. в тексте промпта не вызывали SyntaxWarning.
    prompt = rf"""You are an expert in C/C++ static analysis tools, specifically cppcheck.

Your task: generate a cppcheck custom rule in XML format that detects the following bug.

Bug ID: {bug_id}
Bug name: {bug_name}
Description: {bug_desc}

Example of BAD code (the rule MUST detect this):
```c
{bad_code}
```

Example of GOOD code (the rule MUST NOT trigger on this):
```c
{good_code}
```

═══════════════════════════════════════════════════════
CRITICAL: HOW CPPCHECK PATTERN MATCHING WORKS
═══════════════════════════════════════════════════════

Cppcheck does NOT match patterns against raw source text.
It tokenizes the source code first, then matches your regex
against the TOKEN STREAM — a single string where every token
is separated by exactly ONE SPACE.

Examples of how source code becomes a token stream:

  Source:       free(ptr);
  Token stream: free ( ptr ) ;

  Source:       if (ptr == NULL) return;
  Token stream: if ( ptr == NULL ) return ;

  Source:       int *p = NULL;
  Token stream: int * p = NULL ;

  Source:       strcpy(buffer, input);
  Token stream: strcpy ( buffer , input ) ;

  Source:       malloc(n * sizeof(int))
  Token stream: malloc ( n * sizeof ( int ) )

  Source:       *ptr = 42; free(ptr); printf("%d", *ptr);
  Token stream: * ptr = 42 ; free ( ptr ) ; printf ( "%d" , * ptr ) ;

RULES FOR WRITING PATTERNS:
  CORRECT — space between tokens:    strcpy \(
  CORRECT — \w+ for identifier:      free \( \w+ \)
  CORRECT — .* to skip tokens:       free \( \w+ \) .* \* \w+
  CORRECT — backreferences work:     free \( (\w+) \) .* \* \1
  WRONG   — \s+ between tokens:      free\s*\(   <- never matches
  WRONG   — no spaces:               free\([^)]+\)  <- never matches
  WRONG   — \n or multiline:         not supported, stream is one line
  WRONG   — \b word boundaries:      unreliable in token stream

GOOD PATTERN EXAMPLES:
  Detect strcpy:           strcpy \(
  Detect free then deref:  free \( (\w+) \) .* \* \1
  Detect double free:      free \( (\w+) \) .* free \( \1 \)
  Detect NULL assign:      = NULL
  Detect uninitialized:    int \w+ ; if \(
═══════════════════════════════════════════════════════

Rules for your answer:
- Return ONLY the XML block, nothing else
- No explanations, no markdown, no extra text
- The <pattern> must be a valid PCRE regex for the TOKEN STREAM
- The XML must be well-formed

Required format:
<rule>
  <pattern>YOUR_TOKEN_STREAM_REGEX_HERE</pattern>
  <message>Clear description of the problem for the developer</message>
  <severity>warning</severity>
  <id>{rule_id}</id>
</rule>
"""

    if retry_hint:
        prompt += f"\nNote: {retry_hint}\n"

    return prompt


def make_retry_hint(attempt: int, reason: str) -> str:
    """
    Формирует подсказку для следующей попытки.

    attempt — номер провалившейся попытки (0, 1, 2...)
    reason  — причина провала ('no_xml', 'bad_xml', 'no_pattern')
    """

    hints = {
        "no_xml": (
            "Your previous response did not contain a <rule>...</rule> block. "
            "Return ONLY the XML, starting with <rule> and ending with </rule>."
        ),
        "bad_xml": (
            "Your previous response contained malformed XML. "
            "Make sure all tags are properly opened and closed."
        ),
        "no_pattern": (
            "Your previous response had an empty <pattern> tag. "
            "Provide a valid PCRE regex for the cppcheck TOKEN STREAM. "
            r"Remember: tokens are separated by spaces, write 'strcpy \(' not 'strcpy\('."
        ),
    }

    base = hints.get(reason, "Previous attempt failed. Try again carefully.")
    return f"Attempt {attempt + 1} failed. {base}"
