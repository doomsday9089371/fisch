import os
import subprocess
import sys

from flask import Flask, jsonify, request, send_from_directory

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, BASE_DIR)
app = Flask(__name__, template_folder=BASE_DIR)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/players")
def players():
    return jsonify({"players": ["Alice", "Bob", "Charlie"]})


def launch_test_script():
    script_path = os.path.join(BASE_DIR, "test.py")
    try:
        subprocess.Popen(
            [sys.executable, script_path],
            cwd=BASE_DIR,
            shell=False,
        )
        return jsonify({
            "status": "started",
            "detail": "test.py launched",
        })
    except Exception as exc:
        return jsonify({"status": "error", "detail": str(exc)}), 500

@app.route("/load_fish_data")
def load_fish_data():
    try:
        from test import load_fisch_data_from_db

        entries = load_fisch_data_from_db()
        return jsonify({
            "status": "ok",
            "fish_count": len(entries),
            "first_items": entries[:10],
        })
    except Exception as exc:
        return jsonify({"status": "error", "detail": str(exc)}), 500

@app.route("/island_letters")
def island_letters():
    try:
        from test import load_fisch_data_from_db, build_codex

        entries = load_fisch_data_from_db()
        codex = build_codex(entries)
        groups = [
            {
                "group_code": group_code,
                "letter": data["letter"],
                "count": len(data["islands"]),
            }
            for group_code, data in codex.items()
            if data["islands"]
        ]
        return jsonify({"status": "ok", "groups": groups})
    except Exception as exc:
        return jsonify({"status": "error", "detail": str(exc)}), 500

@app.route("/locations/<string:letter>")
def locations(letter):
    try:
        from test import load_fisch_data_from_db, build_codex

        entries = load_fisch_data_from_db()
        codex = build_codex(entries)
        letter = letter.upper()
        group = next((data for data in codex.values() if data["letter"] == letter), None)
        if not group:
            return jsonify({"status": "error", "detail": f"Unknown island letter: {letter}"}), 404

        locations = [
            {"code": code, "name": loc_data["name"]}
            for code, loc_data in group["islands"].items()
        ]
        return jsonify({"status": "ok", "letter": letter, "locations": locations})
    except Exception as exc:
        return jsonify({"status": "error", "detail": str(exc)}), 500

@app.route("/fish/<string:letter>/<string:island_code>")
def fish(letter, island_code):
    try:
        from test import load_fisch_data_from_db, build_codex

        entries = load_fisch_data_from_db()
        codex = build_codex(entries)
        letter = letter.upper()
        group = next((data for data in codex.values() if data["letter"] == letter), None)
        if not group:
            return jsonify({"status": "error", "detail": f"Unknown island letter: {letter}"}), 404
        island = group["islands"].get(island_code)
        if not island:
            return jsonify({"status": "error", "detail": f"Unknown island code: {island_code}"}), 404

        fish_list = [
            {"code": code, "name": fish_data["name"]}
            for code, fish_data in island["fish"].items()
        ]
        return jsonify({
            "status": "ok",
            "letter": letter,
            "island_code": island_code,
            "island_name": island["name"],
            "fish": fish_list,
        })
    except Exception as exc:
        return jsonify({"status": "error", "detail": str(exc)}), 500

@app.route("/select_prefix_count/<int:count>")
def select_prefix_count(count):
    try:
        if count not in (1, 2, 3):
            return jsonify({"status": "error", "detail": "Prefix count must be 1, 2, or 3."}), 400
        from test import MUTATION_LIST

        allowed_letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "R", "S", "T", "V", "W"]
        letters = []
        for letter in allowed_letters:
            count_by_letter = sum(1 for name, _ in MUTATION_LIST if name.upper().startswith(letter))
            if count_by_letter:
                letters.append({"letter": letter, "count": count_by_letter})
        return jsonify({"status": "ok", "count": count, "letters": letters})
    except Exception as exc:
        return jsonify({"status": "error", "detail": str(exc)}), 500

@app.route("/mutations/<string:letter>")
def mutations(letter):
    try:
        from test import MUTATION_LIST

        letter = letter.upper()
        entries = [
            {"code": f"{idx:03d}", "name": name, "mult": mult}
            for idx, (name, mult) in enumerate(MUTATION_LIST)
            if name.upper().startswith(letter)
        ]
        return jsonify({"status": "ok", "letter": letter, "mutations": entries})
    except Exception as exc:
        return jsonify({"status": "error", "detail": str(exc)}), 500

@app.route("/prefix_mutations")
def prefix_mutations():
    try:
        from test import PREFIX_MUTATIONS

        mutations = [
            {"code": code, "name": value["name"], "mult": value["mult"]}
            for code, value in PREFIX_MUTATIONS.items()
        ]
        return jsonify({"status": "ok", "mutations": mutations})
    except Exception as exc:
        return jsonify({"status": "error", "detail": str(exc)}), 500

@app.route("/tournament")
def tournament():
    try:
        from tournament import get_tournament_page
        page = get_tournament_page()
        return jsonify({"status": "ok", "page": page})
    except Exception as exc:
        return jsonify({"status": "error", "detail": str(exc)}), 500

@app.route("/tournament/join", methods=["POST"])
def tournament_join():
    try:
        from tournament import join_tournament
        result = join_tournament()
        return jsonify({"status": "ok", "result": result})
    except Exception as exc:
        return jsonify({"status": "error", "detail": str(exc)}), 500

@app.route("/submit_entry", methods=["POST"])
def submit_entry():
    try:
        from test import (
            load_fisch_data_from_db,
            build_codex,
            PREFIX_MUTATIONS,
            insert_tracked_item,
        )

        payload = request.get_json(force=True)
        letter = payload.get("letter", "").upper()
        island_code = payload.get("island_code", "")
        fish_code = payload.get("fish_code", "")
        weight = payload.get("weight", "")
        prefix_codes = payload.get("prefix_codes", [])
        core_code = payload.get("core_code", "000")

        entries = load_fisch_data_from_db()
        codex = build_codex(entries)
        group = next((data for data in codex.values() if data["letter"] == letter), None)
        if not group:
            return jsonify({"status": "error", "detail": f"Unknown island letter: {letter}"}), 400
        island = group["islands"].get(island_code)
        if not island:
            return jsonify({"status": "error", "detail": f"Unknown island code: {island_code}"}), 400
        fish = island["fish"].get(fish_code)
        if not fish:
            return jsonify({"status": "error", "detail": f"Unknown fish code: {fish_code}"}), 400

        try:
            weight_val = float(weight)
        except (TypeError, ValueError):
            return jsonify({"status": "error", "detail": f"Invalid weight: {weight}"}), 400

        fish_price = float(fish.get("sell", 0.0))
        base_price = fish_price * weight_val

        prefix_mult = 1.0
        prefix_names = []
        for code in prefix_codes:
            info = PREFIX_MUTATIONS.get(code, {"name": "None", "mult": 1.0})
            prefix_mult *= info["mult"]
            if info["name"] != "None":
                prefix_names.append(info["name"])
        prefix_summary = ", ".join(prefix_names) if prefix_names else "None"

        core_info = PREFIX_MUTATIONS.get(core_code, {"name": "None", "mult": 1.0})
        core_name = core_info["name"]
        core_mult = core_info["mult"]
        final_price = base_price * prefix_mult * core_mult

        display_island_code = f"{letter}-{island_code}" if letter and island_code else island_code

        item_id = insert_tracked_item(
            {
                "island_code": display_island_code,
                "island_name": island["name"],
                "fish_code": fish_code,
                "fish_name": fish["name"],
                "weight": weight_val,
                "base_price": base_price,
                "prefix_summary": prefix_summary,
                "core_name": core_name,
                "prefix_mult": prefix_mult,
                "core_mult": core_mult,
                "final_price": final_price,
            }
        )

        return jsonify({
            "status": "ok",
            "item_id": item_id,
            "display_island_code": display_island_code,
            "island_name": island["name"],
            "fish_name": fish["name"],
            "weight": weight_val,
            "base_price": base_price,
            "prefix_summary": prefix_summary,
            "core_name": core_name,
            "prefix_mult": prefix_mult,
            "core_mult": core_mult,
            "final_price": final_price,
        })
    except Exception as exc:
        return jsonify({"status": "error", "detail": str(exc)}), 500

@app.route("/tracked_items")
def tracked_items():
    try:
        from test import load_tracked_items_from_db

        items = load_tracked_items_from_db()
        return jsonify({"status": "ok", "tracked_items": items})
    except Exception as exc:
        return jsonify({"status": "error", "detail": str(exc)}), 500

@app.route("/run_islands")
def run_islands():
    return launch_test_script()

@app.route("/settings")
def settings():
    return jsonify({"settings": {"volume": 80, "difficulty": "normal"}})

@app.route("/mobile.html")
def mobile_html():
    file_path = os.path.join(BASE_DIR, "mobile.html")
    if not os.path.exists(file_path):
        return jsonify({"status": "error", "detail": "mobile.html not found"}), 404
    with open(file_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    return html_content, 200, {"Content-Type": "text/html; charset=utf-8"}

@app.route("/")
def mobile_ui():
    return mobile_html()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
