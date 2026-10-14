# Submission guide (what to record and submit)

The assignment asks for exactly three things: a **before** video, an **after**
video (each ~10 seconds), and the **chat/LLM link with full history**.

## 1. BEFORE video (~10 s) — original starter code

Use a clean copy of the original starter:

```
git clone https://github.com/SETAPESU26/23_dots_and_boxes.git starter
cd starter
python main.py
```

Type these, quickly:

```
H 0 0
V 0 0
H ² 1        <- crashes with a ValueError traceback
```

What the video shows: the board where the `.` dots and `|` walls don't line up,
and the crash on a character that looks like a number. For extra clarity you can
instead press `Ctrl-D` at the prompt to show the second crash (EOFError).

## 2. AFTER video (~10 s) — the finished project

```
python main.py --rows 1 --cols 2
```

Type:

```
H ² 1        <- friendly error instead of a crash
H 0 0
H 0 0        <- "That line has already been drawn."
H 1 0
V 0 0
V 0 1        <- Player 2 completes a box: it shows "2", score updates, plays again
```

Then (optional, 2-3 s) show the computer opponent:

```
python main.py --rows 2 --cols 2 --vs-computer
```

and/or run the tests:

```
python -m unittest discover
```

(expected: `Ran 34 tests ... OK`)

## 3. Chat / LLM link

Use the **Share** option on the conversation where this was built to get a
public link that includes the complete chat history, and submit that link.

## Before you submit — checklist

- [ ] `python -m unittest discover -v` → all 34 tests pass on your machine
- [ ] Before video shows the broken behaviour (misaligned board + crash)
- [ ] After video shows the fixes and at least one new feature
- [ ] Chat link opens without login and shows the whole conversation
