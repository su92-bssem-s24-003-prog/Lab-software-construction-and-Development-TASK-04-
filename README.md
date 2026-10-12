# Student Marks Application – From a Monolith to Cohesive Python Modules

Software Construction and Development – Week 4 Laboratory Assignment.

The application reads a student's name and three marks, validates the marks (0–100),
calculates total and average, determines a grade and displays the result.
The original single-function program is kept in `docs/original_monolith.py`.

## Project structure
```
student_marks/
├── main.py           # coordinates the application (+ console input helpers)
├── validation.py     # validate_mark(mark), INVALID_MARK_MESSAGE
├── calculations.py   # calculate_total, calculate_average, calculate_grade
├── display.py        # display_result(name, total, average, grade)
├── tests/test_student_marks.py
└── docs/original_monolith.py
```

## Run
```
python main.py
python -m unittest discover -s tests -v
```

## Part A – Code archaeology
| Code | Responsibility |
|---|---|
| `input("Enter student name: ")`, `float(input(...))` (incl. re-prompt) | INPUT |
| `while mark < 0 or mark > 100` and the "Invalid marks" message | VALIDATION |
| `sum(marks)`, `total / len(marks)` | CALCULATION |
| `if average >= 80 ... else "F"` | GRADING / BUSINESS RULE |
| all `print(...)` of the result | DISPLAY |

## Part B – Responsibility map
| Responsibility | What it does | Where it lives |
|---|---|---|
| Input | Reads name and marks, converts marks to float | `main.py` (`read_mark`, `read_marks`) |
| Validation | Decides if a mark is 0–100; owns the error message | `validation.py` |
| Calculation | Total and average of marks | `calculations.py` |
| Grading rule | Maps average to A/B/C/D/F | `calculations.py` (`calculate_grade`) |
| Display | Formats and prints the result, no decisions | `display.py` |

## Part C – Module design
1. **Why each module exists:** `main.py` coordinates the steps; `validation.py` holds the rules for acceptable data; `calculations.py` holds pure logic (no I/O, easy to test); `display.py` holds presentation so it can change independently.
2. **In `calculations.py`:** `calculate_total`, `calculate_average`, `calculate_grade`.
3. **Should `display.py` calculate the grade?** No. It is a business rule; presentation should only show values it is given. Otherwise a grading change would touch display code and a GUI would duplicate the rule.
4. **`main.py` coordinates:** read name → read and validate marks → calculate total, average, grade → pass the results to `display_result`. No formulas, thresholds or formatting.
5. **Hidden details:** display does not know how the grade is derived; calculations do not know how results are printed or that input is a console; `main.py` does not know the formulas or output format; the range limits and message text are hidden behind `validation.py`.

*Design note:* input stays in `main.py` as two tiny helpers instead of an `input.py` – a separate module would be too small. If input grows (files/GUI), split it out.

## Part E – Dependency mapping
```
                 main.py
               /    |     \
              v     v      v
      validation calculations display
```
`validation`, `calculations` and `display` depend on nothing and not on each other.

1. `main.py` depends on `validation`, `calculations`, `display`.
2. No – `display.py` receives the grade as a finished value.
3. No – `calculations.py` only returns values; it has no print/input.
4. Only `display.py` is replaced (same inputs: name, total, average, grade); calculations and grading are untouched.
5. **Necessary:** `main.py` → the three modules. **Unnecessary (avoided):** display → calculations, calculations → display, validation → display/calculations, since they would make changes ripple.

## Part F – Change request test
1. Grading thresholds change → **`calculations.py`** (`calculate_grade`) only.
2. Result format changes → **`display.py`** only.
3. Validation message changes → **`validation.py`** (`INVALID_MARK_MESSAGE`) only.
4. GUI later → the **display layer** (`display.py`, and the input helpers in `main.py` if the GUI collects input) is replaceable without touching calculation logic.

## Part G – Verification
| Case | Input | Total | Average | Grade |
|---|---|---|---|---|
| Normal | 75, 82, 68 | 225.0 | 75.0 | B |
| Boundary | 50, 50, 50 | 150.0 | 50.0 | D |
| Boundary | 60, 60, 60 | 180.0 | 60.0 | C |
| Boundary | 70, 70, 70 | 210.0 | 70.0 | B |
| Boundary | 80, 80, 80 | 240.0 | 80.0 | A |
| Invalid | -5, 105 (re-prompted), then 90, 80, 70 | 240.0 | 80.0 | A |
| Second student | 40, 45, 30 | 115.0 | 38.333333333333336 | F |

Output was compared with the original monolithic program and is identical; the same cases are automated in `tests/`.

## Reflection
1. **Functions vs modules:** a function groups statements for one task; a module is a file grouping related functions around one responsibility, with its own namespace and public interface.
2. **Strongest cohesion:** `calculations.py` – only pure computation (total, average, grade), no I/O.
3. **Coupling example:** `main.py` is coupled to `display.py` through the signature `display_result(name, total, average, grade)`; also `calculate_average` calls `calculate_total`.
4. **Modularity and change:** each change is isolated to the module that owns the responsibility, so less code is touched, risk is lower, and parts (e.g. display) can be swapped.
5. **Too broad/small?** `main.py` is slightly broad (input + coordination), kept for simplicity; `validation.py` is small but justified as a distinct, likely-to-change concern.

## Semester project connection
Responsibilities → modules: UI/input → `ui.py`; business rules → `logic.py`; storage → `storage.py`; validation → `validation.py`; coordination → `main.py`. Dependencies point from `main.py` to the others; `logic.py` must not depend on UI or storage. *(Adapt to your own project.)*
