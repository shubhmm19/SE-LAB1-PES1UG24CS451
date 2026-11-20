# Reflection

> Answers are written for the four reflection questions in the lab handout.
> If the handout's wording differs, adjust the question headings to match.

## 1. Which issue was the most serious, and why?

The most serious issue was the `os.system("send-sms " + " ".join(phoneList))`
call. It builds a shell command from data, so a "phone number" such as
`1234; rm -rf ~` would execute an attacker's commands with the program's
privileges. In a system that holds donor data this could expose or destroy
health records. The hard-coded password and the insecure `mktemp` call are also
real security risks, but command injection gives an attacker the most control.
I fixed it by validating every number with a regular expression and passing the
command as an argument list to `subprocess.run` with `shell=False`.

## 2. What did each tool find that the others did not?

- **Bandit** found the security problems: the hard-coded password, `mktemp`,
  `os.system` and the `assert` used for validation. Neither Pylint nor Flake8
  treats these as security issues.
- **Pylint** found design and quality problems: the mutable default argument,
  the broad `except Exception`, naming conventions, missing docstrings and the
  `or` comparison that should use `in`.
- **Flake8** found formatting problems such as the missing whitespace around
  `=` and the wrong number of blank lines.

None of the tools noticed that `COMPATIBLE` was missing `A-`, `B-` and `AB-`.
I only found that by reading the code, which shows static analysis is a helper
and not a replacement for review and testing.

## 3. Did your fixes change how the program behaves? How did you check?

The demonstration output is identical before and after the changes: the same
stock, the same 3 units for an A+ patient, 0 units for the unknown group `Z+`,
and the same eligible-donor list. I ran the original and the cleaned file and
compared the output. The intentional behaviour changes are all error cases:
an invalid blood group now raises `ValueError` (it used to raise
`AssertionError`), invalid `units` are rejected, and `AB-`, `A-` and `B-`
patients now get correct unit counts instead of 0. I also added a few unit
tests that exercise these paths.

## 4. How would you use static analysis in a real project?

I would run Flake8, Pylint and Bandit automatically in continuous integration
(for example a GitHub Actions workflow) and in a pre-commit hook, so problems
are caught before code is merged. I would fail the build on high-severity
Bandit findings and on a Pylint score below an agreed threshold. Because tools
produce some false positives, I would allow a justified `# nosec` or
`# pylint: disable` with a comment rather than ignoring the reports. Static
analysis would sit alongside code review and automated tests, since it cannot
check whether the logic is correct.
