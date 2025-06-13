from flask import Flask, jsonify, request
import scraper

app = Flask(__name__)

@app.route("/run-scrape", methods=["POST"])
def scrape_endpoint():
    try:
        data = request.get_json()
        userid = data.get("userid")
        password = data.get("password")
        formname = data.get("formname", "default")

        if not userid or not password:
            return jsonify({"status": "error", "message": "Missing userid or password"}), 400

        scraper.run_scrape(userid, password, formname)
        return jsonify({"status": "success"}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    # for local testing
    app.run(host="0.0.0.0", port=5009)