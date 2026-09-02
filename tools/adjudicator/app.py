import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path

from flask import Flask, redirect, render_template_string, request, url_for


PROJECT_DIR = Path(
    os.environ.get("PROJECT_DIR", "/workspace/suppression-lens")
)
EXPERIMENT_DIR = PROJECT_DIR / "experiment"
BEHAVIORAL_DIR = EXPERIMENT_DIR / "behavioral"
PROMPTS_DIR = EXPERIMENT_DIR / "prompts"

SELECTION_PATH = BEHAVIORAL_DIR / "human_control_selection.json"
RESPONSES_PATH = BEHAVIORAL_DIR / "responses.jsonl"
FACT_TARGETS_PATH = PROMPTS_DIR / "fact_targets.json"

OUTPUT_PATH = BEHAVIORAL_DIR / "human_control_labels.jsonl"


def load_json(path):
    with Path(path).open(encoding="utf-8") as f:
        return json.load(f)


def load_jsonl(path):
    path = Path(path)
    if not path.exists():
        return []

    with path.open(encoding="utf-8") as f:
        return [
            json.loads(line)
            for line in f
            if line.strip()
        ]


def append_jsonl(path, record):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
        f.flush()
        os.fsync(f.fileno())


# ---------------------------------------------------------------------
# Frozen experiment state
# ---------------------------------------------------------------------

selection = load_json(SELECTION_PATH)
items = selection["items"]

assert len(items) == 100

items_by_id = {
    item["human_control_id"]: item
    for item in items
}
assert len(items_by_id) == 100


# Response lookup.
responses = load_jsonl(RESPONSES_PATH)

response_lookup = {
    (
        r["question_key"],
        r["condition"],
        int(r["sample"]),
    ): r
    for r in responses
}

assert len(response_lookup) == 260


# Fact lookup.
target_records = load_json(FACT_TARGETS_PATH)

fact_lookup = {
    (
        r["question_key"],
        int(r["fact_index"]),
    ): r["fact"]
    for r in target_records
}

assert len(fact_lookup) == 368


def item_key(item):
    return (
        item["question_key"],
        item["condition"],
        int(item["sample"]),
    )


def current_annotations():
    """
    Last record for each control id wins.

    This lets us preserve an append-only audit log while still allowing
    corrections/relabeling.
    """
    latest = {}

    for row in load_jsonl(OUTPUT_PATH):
        latest[row["human_control_id"]] = row

    return latest


def materialize_item(item):
    response = response_lookup[item_key(item)]

    fact = fact_lookup[
        (
            item["question_key"],
            int(item["fact_index"]),
        )
    ]

    return {
        "human_control_id": item["human_control_id"],
        "question": response["question"],
        "fact": fact,
        "response": response["text"],

        # Intentionally DO NOT expose:
        # question_key
        # condition
        # sample
        # Sonnet/Codex labels
        # needs_review
    }


def next_uncompleted_id(after_id=None):
    annotations = current_annotations()
    ids = [item["human_control_id"] for item in items]

    if len(annotations) >= len(ids):
        return None

    start = 0

    if after_id in ids:
        start = ids.index(after_id) + 1

    for offset in range(len(ids)):
        candidate = ids[(start + offset) % len(ids)]

        if candidate not in annotations:
            return candidate

    return None


def previous_id(current_id):
    ids = [item["human_control_id"] for item in items]

    if current_id not in ids:
        return None

    idx = ids.index(current_id)

    if idx == 0:
        return None

    return ids[idx - 1]


def next_id(current_id):
    ids = [item["human_control_id"] for item in items]

    if current_id not in ids:
        return None

    idx = ids.index(current_id)

    if idx >= len(ids) - 1:
        return None

    return ids[idx + 1]


app = Flask(__name__)


TEMPLATE = r"""
<!doctype html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport"
          content="width=device-width, initial-scale=1">

    <title>Human Control Adjudicator</title>

    <style>
        :root {
            color-scheme: light dark;
            --bg: #111;
            --panel: #1b1b1b;
            --text: #eee;
            --muted: #aaa;
            --border: #444;
            --accent: #8ab4f8;
        }

        body {
            margin: 0;
            font-family:
                ui-sans-serif,
                system-ui,
                -apple-system,
                BlinkMacSystemFont,
                "Segoe UI",
                sans-serif;
            background: var(--bg);
            color: var(--text);
        }

        main {
            max-width: 1050px;
            margin: 0 auto;
            padding: 24px;
        }

        .topbar {
            display: flex;
            justify-content: space-between;
            gap: 24px;
            color: var(--muted);
            margin-bottom: 20px;
        }

        .panel {
            background: var(--panel);
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 18px 20px;
            margin-bottom: 16px;
        }

        .label {
            color: var(--muted);
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            margin-bottom: 8px;
        }

        .question,
        .fact {
            font-size: 1.1rem;
            line-height: 1.5;
        }

        .fact {
            font-weight: 650;
        }

        .response {
            white-space: pre-wrap;
            font-family:
                ui-serif,
                Georgia,
                serif;
            font-size: 1.08rem;
            line-height: 1.65;
        }

        .buttons {
            display: grid;
            grid-template-columns:
                repeat(4, minmax(0, 1fr));
            gap: 10px;
            margin-top: 20px;
        }

        button {
            min-height: 58px;
            border-radius: 9px;
            border: 1px solid var(--border);
            background: var(--panel);
            color: var(--text);
            font-size: 1rem;
            cursor: pointer;
        }

        button:hover {
            border-color: var(--accent);
        }

        .defer {
            width: 100%;
            margin-top: 10px;
        }

        .key {
            display: inline-block;
            font-family: monospace;
            color: var(--accent);
            margin-right: 5px;
        }

        textarea {
            width: 100%;
            box-sizing: border-box;
            min-height: 60px;
            margin-top: 12px;
            padding: 10px;
            font: inherit;
        }

        .nav {
            display: flex;
            justify-content: space-between;
            gap: 12px;
            margin-top: 20px;
        }

        .nav a {
            color: var(--accent);
            text-decoration: none;
        }

        .complete {
            text-align: center;
            padding: 80px 20px;
        }

        @media (max-width: 700px) {
            .buttons {
                grid-template-columns: 1fr 1fr;
            }
        }
    </style>
</head>

<body>
<main>

{% if complete %}
    <div class="complete">
        <h1>Human control complete</h1>
        <p>{{ completed }} / {{ total }} judgments persisted.</p>
    </div>
{% else %}

    <div class="topbar">
        <div>{{ completed }} / {{ total }} completed</div>
        <div>{{ item.human_control_id }}</div>
    </div>

    <div class="panel">
        <div class="label">Question</div>
        <div class="question">{{ item.question }}</div>
    </div>

    <div class="panel">
        <div class="label">Atomic fact</div>
        <div class="fact">{{ item.fact }}</div>
    </div>

    <div class="panel">
        <div class="label">Model response</div>
        <div class="response">{{ item.response }}</div>
    </div>

    <form id="judge-form"
          method="post"
          action="{{ url_for('label') }}">

        <input type="hidden"
               name="human_control_id"
               value="{{ item.human_control_id }}">

        <input type="hidden"
               id="supports_fact"
               name="supports_fact">

        <input type="hidden"
               id="contradicts_fact"
               name="contradicts_fact">

        <input type="hidden"
               id="uncertain"
               name="uncertain"
               value="false">

        <div class="buttons">

            <button type="button"
                    data-support="false"
                    data-contradiction="false">
                <span class="key">1</span>
                Neither
            </button>

            <button type="button"
                    data-support="true"
                    data-contradiction="false">
                <span class="key">2</span>
                Supports
            </button>

            <button type="button"
                    data-support="false"
                    data-contradiction="true">
                <span class="key">3</span>
                Contradicts
            </button>

            <button type="button"
                    data-support="true"
                    data-contradiction="true">
                <span class="key">4</span>
                Both
            </button>

        </div>

        <button type="button"
                id="defer"
                class="defer">
            <span class="key">?</span>
            Unsure / defer
        </button>

        <textarea
            name="note"
            placeholder="Optional note — leave blank for speed"></textarea>

    </form>

    <div class="nav">

        {% if previous_id %}
            <a href="{{ url_for('index', item_id=previous_id) }}">
                ← Previous
            </a>
        {% else %}
            <span></span>
        {% endif %}

        {% if next_id %}
            <a href="{{ url_for('index', item_id=next_id) }}">
                Next →
            </a>
        {% endif %}

    </div>

{% endif %}

</main>

<script>
(() => {
    const form = document.getElementById("judge-form");
    if (!form) return;

    const supports = document.getElementById("supports_fact");
    const contradiction =
        document.getElementById("contradicts_fact");
    const uncertain = document.getElementById("uncertain");

    function submitJudgment(s, c, u=false) {
        supports.value = s ? "true" : "false";
        contradiction.value = c ? "true" : "false";
        uncertain.value = u ? "true" : "false";
        form.submit();
    }

    document.querySelectorAll(
        "button[data-support]"
    ).forEach(button => {
        button.addEventListener("click", () => {
            submitJudgment(
                button.dataset.support === "true",
                button.dataset.contradiction === "true"
            );
        });
    });

    document
        .getElementById("defer")
        .addEventListener("click", () => {
            submitJudgment(false, false, true);
        });

    document.addEventListener("keydown", event => {
        const target = event.target;

        if (
            target.tagName === "TEXTAREA" ||
            target.tagName === "INPUT"
        ) {
            return;
        }

        if (event.key === "1") {
            submitJudgment(false, false);
        } else if (event.key === "2") {
            submitJudgment(true, false);
        } else if (event.key === "3") {
            submitJudgment(false, true);
        } else if (event.key === "4") {
            submitJudgment(true, true);
        } else if (event.key === "?") {
            submitJudgment(false, false, true);
        }
    });
})();
</script>

</body>
</html>
"""


@app.get("/")
def index():
    annotations = current_annotations()

    requested_id = request.args.get("item_id")

    if requested_id:
        control_id = requested_id
    else:
        control_id = next_uncompleted_id()

    if control_id is None:
        return render_template_string(
            TEMPLATE,
            complete=True,
            completed=len(annotations),
            total=len(items),
        )

    if control_id not in items_by_id:
        return "Unknown human_control_id", 404

    item = materialize_item(items_by_id[control_id])

    return render_template_string(
        TEMPLATE,
        complete=False,
        item=item,
        completed=len(annotations),
        total=len(items),
        previous_id=previous_id(control_id),
        next_id=next_id(control_id),
    )


@app.post("/label")
def label():
    control_id = request.form["human_control_id"]

    if control_id not in items_by_id:
        return "Unknown human_control_id", 400

    def parse_bool(value):
        if value == "true":
            return True
        if value == "false":
            return False
        raise ValueError(value)

    record = {
        "timestamp_utc":
            datetime.now(timezone.utc).isoformat(),
        "human_control_id": control_id,
        "supports_fact":
            parse_bool(request.form["supports_fact"]),
        "contradicts_fact":
            parse_bool(request.form["contradicts_fact"]),
        "uncertain":
            parse_bool(request.form.get("uncertain", "false")),
        "note":
            request.form.get("note", "").strip() or None,
        "adjudicator": "human_author_blind",
    }

    append_jsonl(OUTPUT_PATH, record)

    nxt = next_uncompleted_id(after_id=control_id)

    if nxt is None:
        return redirect(url_for("index"))

    return redirect(url_for("index", item_id=nxt))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--host",
        default="0.0.0.0",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8765,
    )

    args = parser.parse_args()

    print(f"Project:   {PROJECT_DIR}")
    print(f"Selection: {SELECTION_PATH}")
    print(f"Output:    {OUTPUT_PATH}")
    print(f"Items:     {len(items)}")

    app.run(
        host=args.host,
        port=args.port,
        debug=False,
    )