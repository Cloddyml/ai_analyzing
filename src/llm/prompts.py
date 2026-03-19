def make_rule_prompt(bug: dict, retry_hint: str = "") -> str:
    """
    Строит промпт для генерации cppcheck XML-правила.

    bug — словарь с полями: id, name, description, bad_code, good_code
    retry_hint — дополнительная подсказка при повторной попытке
    """

    rule_id = bug["id"].lower().replace("-", "_")

    prompt = f"""You are an expert in C/C++ static analysis tools.

Your task: generate a cppcheck rule in XML format that detects the following bug.

Bug ID: {bug["id"]}
Bug name: {bug["name"]}
Description: {bug["description"]}

Example of BAD code (the rule MUST detect this):
```c
{bug["bad_code"]}
```

Example of GOOD code (the rule MUST NOT trigger on this):
```c
{bug["good_code"]}
```

Rules for your answer:
- Return ONLY the XML block, nothing else
- No explanations, no markdown, no extra text
- The pattern field must be a valid PCRE regular expression
- The XML must be well-formed

Required format:
<rule>
  <pattern>YOUR_REGEX_HERE</pattern>
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
            "Provide a valid PCRE regular expression inside <pattern>.</pattern>."
        ),
    }

    base = hints.get(reason, "Previous attempt failed. Try again carefully.")
    return f"Attempt {attempt + 1} failed. {base}"
