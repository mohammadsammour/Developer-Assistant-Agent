# Example Outputs

Sample `DeveloperTaskReport` objects the agent could return for the inputs in `example_inputs.md`. These are illustrative (hand-written to match the schema in `src/schemas.py`), not live model output — swap in real captures once you've run the agent yourself, e.g. via `report.model_dump()` in the Streamlit app's "Raw Structured Output" expander.

---

## Output for Example 2 (Debugging — syntax error)

```json
{
  "task_type": "debugging",
  "difficulty": "easy",
  "risk_level": "low",
  "summary": "The function definition is missing a closing parenthesis, causing a SyntaxError before the code can even run.",
  "key_points": [
    "The 'def hello(' line opens a parenthesis that is never closed.",
    "check_python_syntax confirmed a SyntaxError at line 2.",
    "No logic in the function body can be evaluated until the syntax is fixed."
  ],
  "potential_bugs": [
    {
      "bug": "Unclosed parenthesis in function signature",
      "explanation": "The parameter list for 'hello' is opened with '(' but never closed with ')', so Python cannot parse the function definition."
    }
  ],
  "next_steps": [
    "Close the parenthesis: def hello():",
    "Re-run check_python_syntax or the interpreter to confirm the fix.",
    "Add a docstring or parameters if the function is meant to take input."
  ],
  "needs_human_review": false
}
```

---

## Output for Example 3 (Debugging — logical bug)

```json
{
  "task_type": "debugging",
  "difficulty": "medium",
  "risk_level": "medium",
  "summary": "The function is syntactically valid but subtracts 1 from the final average, which is almost certainly unintended.",
  "key_points": [
    "The loop correctly sums all values in 'numbers'.",
    "The division 'total / len(numbers)' correctly computes the mean.",
    "The trailing '- 1' after the division changes the result and has no clear justification from the function name or context."
  ],
  "potential_bugs": [
    {
      "bug": "Unexplained '- 1' after computing the average",
      "explanation": "This shifts every returned average down by 1, which doesn't match a function named 'average'. Likely a leftover from earlier edits or a copy-paste error."
    }
  ],
  "next_steps": [
    "Confirm whether the '- 1' is intentional (e.g. some domain-specific adjustment).",
    "If not intentional, remove it so the function returns a true arithmetic mean.",
    "Add a unit test asserting average([1, 2, 3]) == 2 to catch regressions."
  ],
  "needs_human_review": true
}
```

---

## Output for Example 4 (Feature Planning)

```json
{
  "task_type": "feature_planning",
  "difficulty": "easy",
  "risk_level": "low",
  "summary": "Adding a save-to-file option to the CLI app is a small, additive change that doesn't affect existing behavior.",
  "key_points": [
    "The CLI already builds a full DeveloperTaskReport object after calling run_agent.",
    "Saving can reuse report.model_dump() to serialize the report as JSON.",
    "No changes are needed to src/agent.py or src/schemas.py for this feature."
  ],
  "potential_bugs": [],
  "next_steps": [
    "Add a prompt after printing the report asking if the user wants to save it.",
    "If yes, write report.model_dump() to a timestamped .json file in an output/ folder.",
    "Consider adding a --save flag for non-interactive use later."
  ],
  "needs_human_review": false
}
```

---

## Notes on reading these

- `potential_bugs` is an empty list when no issues are found (see Example 4) — the UI (`render_potential_bugs` in `streamlit_app.py`) shows a success message in that case.
- `needs_human_review: true` shows up when the fix depends on intent the agent can't verify on its own (see Example 3) — this is the schema's way of flagging "don't act on this blindly."
- `risk_level` tracks how safe it'd be to act on the report without a second look, which is a different axis from `difficulty` (how hard the task itself is).
