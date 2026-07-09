# Example Inputs

Sample requests you can feed into the agent (via `apps/cli_app.py` or `apps/streamlit_app.py`) to see how it handles each task type.

---

## 1. Code Explanation

**Request:**
> Can you explain what this function does?

**Code/context:**
```python
def flatten(nested_list):
    result = []
    for item in nested_list:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result
```

**Expected `task_type`:** `code_explanation`

---

## 2. Debugging (with a real syntax error)

**Request:**
> This function is throwing an error when I run it, can you check what's wrong?

**Code/context:**
```python
def hello(
    print("hi")
```

**Expected `task_type`:** `debugging`
**Note:** This is the exact snippet already used as a suggested test in `apps/streamlit_app.py`'s sidebar. It has a missing closing parenthesis, so `check_python_syntax` should catch it directly.

---

## 3. Debugging (logical bug, not a syntax error)

**Request:**
> I'm getting the wrong average back from this function, can you spot the issue?

**Code/context:**
```python
def average(numbers):
    total = 0
    for n in numbers:
        total += n
    return total / len(numbers) - 1
```

**Expected `task_type`:** `debugging`
**Note:** Syntactically valid, so `check_python_syntax` won't flag anything — this tests whether the model can reason about logic errors on its own.

---

## 4. Feature Planning

**Request:**
> I want to add a "save report to file" option to the CLI app. How should I approach this?

**Code/context:** *(none — general planning question)*

**Expected `task_type`:** `feature_planning`

---

## 5. General Question

**Request:**
> What's the difference between a list and a tuple in Python, and when should I use each?

**Code/context:** *(none)*

**Expected `task_type`:** `general_question`

---

## 6. Empty/edge case

**Request:**
> Check this code for issues.

**Code/context:** *(left blank)*

**Expected behavior:** `build_developer_user_message` falls back to `"No code/context provided."`, and the agent should ask for code or note that none was given rather than inventing an answer.
