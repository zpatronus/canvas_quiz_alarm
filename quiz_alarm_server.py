from flask import Flask, request, jsonify, render_template
import requests
import random

app = Flask(__name__)


@app.route("/quiz_alarm/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/quiz_alarm/get/", methods=["GET"])
def get_quizzes():
    course_id = request.args.get("course_id")
    access_token = request.args.get("access_token")

    if not course_id:
        return jsonify({"error": "Course ID is required"}), 400
    if not access_token:
        return jsonify({"error": "Access token is required"}), 400

    canvas_api_url = (
        f"https://umich.instructure.com/api/v1/courses/{course_id}/quizzes"
    )
    headers = {"Authorization": f"Bearer {access_token}"}

    try:
        response = requests.get(
            canvas_api_url, headers=headers, timeout=10
        )  # Set a 10-second timeout
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.Timeout:
        return jsonify({"error": "The request timed out"}), 504
    except requests.exceptions.HTTPError as e:
        # Check for 401 Unauthorized and 404 Not Found status codes
        if e.response.status_code == 401:
            return jsonify({"error": "Access token/course id invalid"}), 401
        elif e.response.status_code == 404:
            return (
                jsonify({"error": "The requested course was not found"}),
                404,
            )
        else:
            return (
                jsonify({"error": "HTTP error occurred"}),
                e.response.status_code,
            )
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "A request exception occurred"}), 500


if __name__ == "__main__":
    app.run(debug=True)
