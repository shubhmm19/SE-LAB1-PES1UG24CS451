"""Create explicitly labeled Jira-style training mockups and project PDFs."""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import textwrap

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


ROOT = Path(__file__).parent
W, H = 1440, 900
NAVY, BLUE, BG, PANEL, BORDER = "#101827", "#1868db", "#f7f8f9", "#ffffff", "#dfe1e6"
INK, MUTED, PURPLE, GREEN, RED, YELLOW = "#172b4d", "#626f86", "#6554c0", "#216e4e", "#c9372c", "#946f00"

try:
    FONT = ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", 18)
    SMALL = ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", 14)
    BOLD = ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", 20)
    TITLE = ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", 28)
except OSError:
    FONT = SMALL = BOLD = TITLE = ImageFont.load_default()


def base(section="Board"):
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, W, 58), fill="#ffffff")
    d.text((24, 17), "◆ Jira", fill=BLUE, font=BOLD)
    d.rounded_rectangle((220, 12, 700, 46), radius=6, fill="#f1f2f4")
    d.text((238, 20), "Search", fill=MUTED, font=SMALL)
    d.text((1320, 18), "⋯   ?   ●", fill=INK, font=BOLD)
    d.rectangle((0, 58, 260, H-52), fill="#f1f2f4")
    d.text((24, 88), "My projects", fill=MUTED, font=SMALL)
    d.text((24, 126), "HCDE  Courier Dispatch", fill=INK, font=BOLD)
    for i, item in enumerate(["Summary", "Backlog", "Board", "Reports", "Issues", "Project settings"]):
        y = 182 + i*46
        if item == section:
            d.rounded_rectangle((12, y-7, 244, y+30), radius=5, fill="#e9f2ff")
        d.text((32, y), item, fill=BLUE if item == section else INK, font=FONT)
    d.rectangle((260, 58, W, H-52), fill=BG)
    d.rectangle((0, H-52, W, H), fill="#fff3cd")
    d.text((18, H-37), "TRAINING MOCKUP  •  SIMULATED JIRA-STYLE UI  •  NOT CAPTURED FROM A LIVE JIRA WORKSPACE", fill="#614700", font=SMALL)
    return im


def pill(d, xy, label, color):
    x, y = xy
    d.rounded_rectangle((x, y, x+116, y+27), radius=12, fill=color)
    d.text((x+11, y+5), label, fill="#ffffff", font=SMALL)


def board_image(cards=None, highlight=None):
    cards = cards or {
        "TO DO": [("HCDE-1", "Offline rider appears in dispatch results", "Highest", RED),
                  ("HCDE-4", "Availability toggle is not reflected in time", "Medium", YELLOW)],
        "IN PROGRESS": [("HCDE-2", "Expired OTP can complete delivery", "Highest", RED)],
        "DONE": [("HCDE-3", "Sender notification exceeds 5 seconds", "High", PURPLE),
                 ("HCDE-5", "Optimized route exceeds naive distance", "Medium", YELLOW)],
    }
    im = base("Board")
    d = ImageDraw.Draw(im)
    d.text((300, 90), "HCDE  /  Board", fill=MUTED, font=SMALL)
    d.text((300, 122), "Courier Dispatch — Bug Tracking", fill=INK, font=TITLE)
    d.text((300, 171), "Board  ·  Backlog  ·  Reports", fill=MUTED, font=SMALL)
    d.rounded_rectangle((1190, 112, 1398, 154), radius=6, fill=BLUE)
    d.text((1215, 123), "+ Create issue", fill="#ffffff", font=SMALL)
    colx = [300, 670, 1040]
    names = list(cards.keys())
    colors = ["#dfe1e6", "#fff0b3", "#dcfff1"]
    for j, name in enumerate(names):
        x = colx[j]
        d.rounded_rectangle((x, 222, x+340, 814), radius=8, fill="#f1f2f4", outline=BORDER)
        d.text((x+18, 242), f"{name}  ·  {len(cards[name])}", fill=INK, font=BOLD)
        for i, (key, summary, priority, color) in enumerate(cards[name]):
            y = 292 + i*192
            active = key == highlight
            d.rounded_rectangle((x+12, y, x+328, y+172), radius=7,
                                fill="#eef4ff" if active else PANEL,
                                outline=BLUE if active else BORDER, width=2 if active else 1)
            d.text((x+26, y+15), key, fill=BLUE, font=SMALL)
            for line_i, line in enumerate(textwrap.wrap(summary, 30)[:3]):
                d.text((x+26, y+43+line_i*23), line, fill=INK, font=FONT)
            d.text((x+26, y+125), "Bug", fill=PURPLE, font=SMALL)
            pill(d, (x+175, y+119), priority, color)
    return im


def wizard_frame(step, project_name, subtitle):
    im = base("Summary")
    d = ImageDraw.Draw(im)
    d.text((300, 100), "Projects  /  Create project", fill=MUTED, font=SMALL)
    d.text((300, 138), "Create a project", fill=INK, font=TITLE)
    steps = ["Template", "Type", "Details", "Create"]
    for i, s in enumerate(steps):
        x = 330+i*230
        d.ellipse((x, 208, x+34, 242), fill=BLUE if i <= step else "#dfe1e6")
        d.text((x+50, 213), s, fill=BLUE if i <= step else MUTED, font=FONT)
        if i < len(steps)-1: d.line((x+125, 225, x+205, 225), fill=BORDER, width=3)
    d.rounded_rectangle((320, 290, 1270, 720), radius=12, fill=PANEL, outline=BORDER)
    d.text((365, 330), "Project details", fill=INK, font=BOLD)
    d.text((365, 387), "Name", fill=MUTED, font=SMALL)
    d.rounded_rectangle((365, 412, 1215, 460), radius=5, fill="#ffffff", outline=BLUE if step == 2 else BORDER, width=2)
    d.text((382, 426), project_name, fill=INK, font=FONT)
    d.text((365, 492), "Key", fill=MUTED, font=SMALL)
    d.rounded_rectangle((365, 516, 770, 562), radius=5, fill="#ffffff", outline=BORDER)
    d.text((382, 529), "HCDE", fill=INK, font=FONT)
    d.text((365, 596), "Template", fill=MUTED, font=SMALL)
    d.rounded_rectangle((365, 620, 1215, 670), radius=5, fill="#e9f2ff", outline=BLUE if step == 0 else BORDER)
    d.text((382, 635), subtitle, fill=INK, font=FONT)
    d.rounded_rectangle((1120, 735, 1270, 780), radius=6, fill=BLUE)
    d.text((1164, 748), "Continue", fill="#ffffff", font=SMALL)
    return im


def create_issue_frame(stage):
    im = board_image()
    d = ImageDraw.Draw(im)
    d.rectangle((260, 58, W, H-52), fill="#00000088")
    d.rounded_rectangle((390, 100, 1240, 810), radius=12, fill="#ffffff", outline=BORDER, width=2)
    d.text((425, 128), "Create issue", fill=INK, font=TITLE)
    fields = [("Project", "HCDE — Courier Dispatch"), ("Issue type", "Bug"),
              ("Summary", "Offline rider appears in dispatch results"),
              ("Priority", "Highest"), ("Description", "Expected: offline riders are excluded from matching.\nActual: closest offline rider may be selected.")]
    for i, (label, value) in enumerate(fields):
        y = 194 + i*94
        d.text((425, y), label, fill=MUTED, font=SMALL)
        d.rounded_rectangle((425, y+24, 1195, y+72), radius=5, fill="#ffffff", outline=BLUE if stage >= i else BORDER, width=2 if stage >= i else 1)
        d.multiline_text((440, y+35), value, fill=INK, font=SMALL, spacing=4)
    d.rounded_rectangle((1040, 742, 1195, 785), radius=6, fill=BLUE)
    d.text((1082, 755), "Create", fill="#ffffff", font=SMALL)
    return im


def issue_detail_frame(stage):
    im = board_image()
    d = ImageDraw.Draw(im)
    d.rectangle((260, 58, W, H-52), fill="#00000066")
    d.rounded_rectangle((330, 90, 1300, 820), radius=10, fill="#ffffff", outline=BORDER, width=2)
    d.text((368, 118), "HCDE-2  /  Bug", fill=BLUE, font=SMALL)
    d.text((368, 152), "Expired OTP can complete delivery", fill=INK, font=TITLE)
    pill(d, (368, 210), "Highest", RED)
    status = ["To Do", "In Progress", "Resolved"][stage]
    d.rounded_rectangle((1110, 204, 1260, 246), radius=6, fill=GREEN if stage == 2 else BLUE)
    d.text((1135, 216), status, fill="#ffffff", font=SMALL)
    d.text((368, 292), "Description", fill=INK, font=BOLD)
    d.multiline_text((368, 330), "Expired one-time passwords are accepted, potentially allowing\nunverified delivery completion.", fill=INK, font=FONT, spacing=8)
    d.text((368, 420), "Assignee", fill=MUTED, font=SMALL)
    d.rounded_rectangle((368, 444, 760, 490), radius=5, fill="#ffffff", outline=BLUE if stage >= 1 else BORDER)
    d.text((385, 457), "Rider Platform Team", fill=INK, font=SMALL)
    d.text((368, 530), "Activity", fill=INK, font=BOLD)
    d.rounded_rectangle((368, 570, 1238, 642), radius=6, fill="#f7f8f9", outline=BORDER)
    comment = ["", "Assigned to Rider Platform Team.", "Fixed expiry validation and added an integration test."][stage]
    if comment: d.text((390, 596), comment, fill=INK, font=SMALL)
    d.rounded_rectangle((368, 670, 1238, 735), radius=6, fill="#ffffff", outline=BLUE if stage == 2 else BORDER)
    d.text((390, 690), "Add a comment…", fill=MUTED, font=SMALL)
    return im


def save_gif(frames, filename, duration=900):
    out = ROOT / filename
    frames[0].save(out, save_all=True, append_images=frames[1:], duration=duration, loop=0, optimize=True)


def make_assets():
    board_image().save(ROOT / "Bug_Board.png")
    save_gif([wizard_frame(0, "", "Scrum — Software development"),
              wizard_frame(1, "", "Company-managed Scrum"),
              wizard_frame(2, "Hyperlocal Courier Dispatch & Tracking Engine", "Company-managed Scrum"),
              wizard_frame(3, "Hyperlocal Courier Dispatch & Tracking Engine", "Project created — HCDE")],
             "Bug_Tracking_1_Create_Project.gif")
    save_gif([create_issue_frame(i) for i in range(5)], "Bug_Tracking_2_Log_Bug.gif", 800)
    save_gif([issue_detail_frame(i) for i in range(3)], "Bug_Tracking_3_Assign_Comment_Resolve.gif", 1000)
    start = board_image()
    moving = board_image(highlight="HCDE-1")
    to_progress = board_image({"TO DO": [("HCDE-4", "Availability toggle is not reflected in time", "Medium", YELLOW)],
                               "IN PROGRESS": [("HCDE-1", "Offline rider appears in dispatch results", "Highest", RED), ("HCDE-2", "Expired OTP can complete delivery", "Highest", RED)],
                               "DONE": [("HCDE-3", "Sender notification exceeds 5 seconds", "High", PURPLE), ("HCDE-5", "Optimized route exceeds naive distance", "Medium", YELLOW)]}, highlight="HCDE-1")
    done = board_image({"TO DO": [("HCDE-4", "Availability toggle is not reflected in time", "Medium", YELLOW)],
                        "IN PROGRESS": [("HCDE-2", "Expired OTP can complete delivery", "Highest", RED)],
                        "DONE": [("HCDE-1", "Offline rider appears in dispatch results", "Highest", RED), ("HCDE-3", "Sender notification exceeds 5 seconds", "High", PURPLE), ("HCDE-5", "Optimized route exceeds naive distance", "Medium", YELLOW)]}, highlight="HCDE-1")
    save_gif([start, moving, to_progress, done], "Bug_Tracking_4_Board_Workflow.gif", 1000)


def pdf_page(pdf, title, lines, image=None):
    fig = plt.figure(figsize=(8.27, 11.69), facecolor="white")
    fig.text(.08, .95, title, fontsize=21, weight="bold", color="#172b4d", va="top")
    y = .89
    for text in lines:
        fig.text(.08, y, text, fontsize=10, color="#253858", va="top", wrap=True)
        y -= .052 if len(text) < 110 else .075
    if image:
        ax = fig.add_axes([.08, .08, .84, .48])
        ax.imshow(Image.open(image))
        ax.axis("off")
    fig.text(.08, .035, "Lab 2 • training mockup/report • not a live Jira export", fontsize=8, color="#626f86")
    pdf.savefig(fig, bbox_inches="tight")
    plt.close(fig)


def make_pdfs():
    with PdfPages(ROOT / "Kanban_proj.pdf") as pdf:
        pdf_page(pdf, "Kanban Project — Bug Tracking", [
            "Project: Hyperlocal Courier Dispatch & Tracking Engine (suggested key HCDE).",
            "Workflow: To Do → In Progress → Done. The cards model five sample defects derived from the Lab 1 requirements; they are not verified defects in a running application.",
            "Triage snapshot: two items To Do, one In Progress, and two Done. Highest-priority work is offline-rider exclusion and expired-OTP validation.",
        ], ROOT / "Bug_Board.png")
        pdf_page(pdf, "Bug Record Template and Triage", [
            "Each Jira Bug should include a concise summary, component, requirement link, preconditions, reproduction steps, expected result, actual result, severity/priority, assignee, and resolution note.",
            "HCDE-1 Offline rider appears in dispatch results — Highest / Critical — To Do.",
            "HCDE-2 Expired OTP can complete delivery — Highest / Critical — In Progress.",
            "HCDE-3 Sender status notification arrives after target — High / Major — Done.",
            "HCDE-4 Availability toggle takes too long to affect matching — Medium / Major — To Do.",
            "HCDE-5 Multi-stop route is longer than assignment order — Medium / Major — Done.",
        ])
    with PdfPages(ROOT / "Scrum_proj.pdf") as pdf:
        pdf_page(pdf, "Scrum Project — Bug Fix Sprints", [
            "Project: Hyperlocal Courier Dispatch & Tracking Engine (suggested key HCDE).",
            "Sprint 1 (one week): HCDE-1, HCDE-2, and HCDE-4. Goal: prevent invalid dispatch and delivery completion; make rider availability reliable.",
            "Sprint 2 (one week): HCDE-3 and HCDE-5. Goal: verify timely notifications and route optimization after fixes.",
            "Demo workflow: create each Bug, assign it, comment with investigation progress, move it across the board, and resolve only after recording a fix and verification note.",
            "The assignments and statuses are simulated examples. They do not represent changes made in a live Jira workspace.",
        ])
        pdf_page(pdf, "Scrum Board Workflow Preview", [
            "The GIF demonstrates one sample issue moving through the workflow. The board image and GIF are labeled simulations, not Jira screenshots or screen recordings.",
        ], ROOT / "Bug_Tracking_4_Board_Workflow.gif")


if __name__ == "__main__":
    make_assets()
    make_pdfs()
