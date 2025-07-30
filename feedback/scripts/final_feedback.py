import os
import json
import matplotlib.pyplot as plt
from collections import Counter
import textwrap

# ---------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------
DATA_FILE = "feedback/data/final_feedback.json"
OUT_DIR = "feedback/figures"
os.makedirs(OUT_DIR, exist_ok=True)

# ---------------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------------
def _bar(values, title, img_name):
    """Create bar chart for multiple choice responses"""
    cnt = Counter(values)
    plt.figure(figsize=(12, 8))
    bars = plt.bar(cnt.keys(), cnt.values(), color='#4682B4', alpha=0.7)
    plt.title(title, fontsize=16, fontweight='bold', pad=20)
    plt.ylabel("Number of responses", fontsize=12)
    plt.xticks(rotation=45, ha="right", fontsize=11)
    plt.yticks(fontsize=11)
    plt.grid(axis='y', alpha=0.3)

    total = sum(cnt.values())
    for bar in bars:
        h = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, h + 0.1,
                f"{h} ({100*h/total:.1f}%)", ha="center", va="bottom",
                fontsize=10, fontweight='bold')

    plt.tight_layout()
    plt.savefig(f"{OUT_DIR}/{img_name}", dpi=300, bbox_inches='tight')
    plt.close()


def _list_chart(responses, title, img_name):
    """
    Optimized list chart with proper spacing between responses
    """
    # Filter empty responses, keep original numbering
    processed_responses = []
    for i, text in enumerate(responses):
        cleaned = text.strip() if text else ""
        if cleaned:
            processed_responses.append((i + 1, cleaned))

    if not processed_responses:
        print(f"No valid responses for {title}")
        return

    n_responses = len(processed_responses)
    print(f"Creating chart for '{title}' with {n_responses} responses")

    # Text wrapping based on content length
    avg_length = sum(len(resp[1]) for resp in processed_responses) / n_responses
    wrap_width = 75 if avg_length < 60 else 85 if avg_length < 120 else 95

    # Pre-wrap responses to calculate space needed
    wrapped_responses = []
    total_text_lines = 0

    for idx, text in processed_responses:
        wrapped = textwrap.wrap(text, width=wrap_width) or [text]
        wrapped_responses.append((idx, wrapped))
        total_text_lines += len(wrapped)

    # Font sizing based on response count
    if n_responses <= 15:
        font_size, title_size = 9, 12
    elif n_responses <= 30:
        font_size, title_size = 8, 11
    elif n_responses <= 50:
        font_size, title_size = 7, 10
    else:
        font_size, title_size = 6, 9

    # Calculate figure height - KEY CHANGE: More space between responses
    response_gaps = n_responses * 0.5  # INCREASED from 0.25 to 0.5 for more space
    title_space = 0.7
    margin_space = 0.4

    content_lines = total_text_lines + response_gaps
    line_height = font_size / 72 * 1.1
    fig_height = max(4, (content_lines * line_height) + title_space + margin_space)
    fig_width = 5.5

    print(f"Dimensions: {fig_width}x{fig_height:.1f}in, Wrap: {wrap_width} chars")

    # Create figure
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    ax.axis('off')

    # Title
    ax.text(0.5, 0.98, title, fontsize=title_size, fontweight='bold', 
            ha='center', va='top', transform=ax.transAxes)

    # Layout parameters
    content_start_y = 0.94
    content_height = 0.92
    line_step = content_height / content_lines if content_lines > 0 else 0.01

    # Positioning - clear separation between numbers and text
    number_x_pos = 0.02
    text_x_pos = 0.08

    current_y = content_start_y

    for idx, wrapped_lines in wrapped_responses:
        # Response number
        ax.text(number_x_pos, current_y, f"{idx}.", 
               fontsize=font_size, fontweight='bold', color='#2E8B57',
               transform=ax.transAxes, va='top', ha='left')

        # Response text
        for i, line in enumerate(wrapped_lines):
            ax.text(text_x_pos, current_y - (i * line_step), line,
                   fontsize=font_size, transform=ax.transAxes, va='top', ha='left')

        # Move to next response - INCREASED spacing here
        current_y -= (len(wrapped_lines) + 0.5) * line_step  # +0.5 creates more space

        # Handle space overflow
        if current_y < 0.01:
            remaining = len(wrapped_responses) - (wrapped_responses.index((idx, wrapped_lines)) + 1)
            if remaining > 0:
                ax.text(text_x_pos, current_y, f"... and {remaining} more responses",
                       fontsize=max(5, font_size-1), style='italic', color='#666666',
                       transform=ax.transAxes, va='top', ha='left')
            break

    plt.subplots_adjust(left=0.01, right=0.99, top=0.995, bottom=0.005)
    plt.savefig(f"{OUT_DIR}/{img_name}", dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none', pad_inches=0.02)
    plt.close()

    print(f"✓ Generated {img_name} (height: {fig_height:.1f}in)")


# ---------------------------------------------------------------------
# MAIN - Only the essential charts
# ---------------------------------------------------------------------
if __name__ == "__main__":
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    print("Generating bar charts...")
    # Multiple choice questions - bar charts
    _bar([r[0][1] for r in data], "Overall impressions", "overall_impressions.png")
    _bar([r[1][1] for r in data], "Now I …", "now_i.png")
    _bar([r[2][1] for r in data], "Confidence (1-10)", "confidence.png")
    _bar([r[4][1] for r in data], "Feeling after talking with classmates", "feel_after_talk.png")
    _bar([r[5][1] for r in data], "Elective vs other courses", "course_compare.png")
    _bar([r[6][1] for r in data], "Received help when needed?", "help_received.png")
    _bar([r[7][1] for r in data], "If known in advance I would …", "if_known.png")
    _bar([r[8][1] for r in data], "At the end of the course I …", "at_end.png")
    _bar([r[20][1] for r in data], "I think that Timur …", "timur_knowledge.png")
    _bar([r[21][1] for r in data], "Timur's English level", "timur_english.png")
    _bar([r[22][1] for r in data], "Timur's approach vs other courses", "timur_approach.png")

    print("\nGenerating list charts...")
    # Open-ended questions - list charts
    _list_chart([r[3][1] for r in data], "Code Examples Clarity", "code_examples_clarity.png")
    _list_chart([r[9][1] for r in data], "Recommend to peers? Why?", "recommendations.png")
    _list_chart([r[10][1] for r in data], "Not seen elsewhere & liked", "liked_unique.png")
    _list_chart([r[11][1] for r in data], "Not seen elsewhere & glad absent", "glad_absent.png")
    _list_chart([r[12][1] for r in data], "Seen elsewhere & not enough here", "not_enough.png")
    _list_chart([r[13][1] for r in data], "Seen elsewhere & glad absent here", "glad_not_here.png")
    _list_chart([r[14][1] for r in data], "Demotivated by …", "demotivators.png")
    _list_chart([r[15][1] for r in data], "I've learned …", "learned.png")
    _list_chart([r[16][1] for r in data], "Seemed useless to me …", "useless.png")
    _list_chart([r[17][1] for r in data], "Course can be improved by …", "improve_by.png")
    _list_chart([r[18][1] for r in data], "Irrelevant topics", "irrelevant_topics.png")
    _list_chart([r[19][1] for r in data], "Add / remove suggestions", "add_remove.png")
    _list_chart([r[23][1] for r in data], "I want after finishing the course …", "goals.png")
    _list_chart([r[24][1] for r in data], "I promise over the summer …", "promises.png")

    print(f"\n✓ All feedback figures generated to {OUT_DIR}")