from flask import Flask, render_template, request
from ultralytics import YOLO
import os
import uuid
import json
import shutil
from datetime import datetime

app = Flask(__name__)


# ==================================================
# YOLO MODEL
# ==================================================

model = YOLO("runs/detect/train-2/weights/best.pt")


# ==================================================
# REPORT FILE
# ==================================================

REPORT_FILE = "reports.json"


# ==================================================
# FOLDERS
# ==================================================

UPLOAD_FOLDER = "static/uploads"
RESULT_FOLDER = "static/results"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)


# ==================================================
# DAMAGE INFORMATION
# ==================================================

damage_info = {

    "longitudinal crack": {
        "severity": "Moderate",
        "priority": "Medium",
        "recommendation":
        "Schedule road inspection and repair the crack before it expands."
    },

    "longitudinal crack wide": {
        "severity": "High",
        "priority": "High",
        "recommendation":
        "Repair the damaged section as soon as possible to prevent further deterioration."
    },

    "transverse crack": {
        "severity": "Moderate",
        "priority": "Medium",
        "recommendation":
        "Inspect the affected area and seal the crack to prevent water penetration."
    },

    "transverse crack wide": {
        "severity": "High",
        "priority": "High",
        "recommendation":
        "Immediate maintenance is recommended because the crack has significant width."
    },

    "alligator crack": {
        "severity": "High",
        "priority": "High",
        "recommendation":
        "Carry out pavement rehabilitation because interconnected cracks indicate structural damage."
    },

    "alligator crack sunken": {
        "severity": "Critical",
        "priority": "Critical",
        "recommendation":
        "Immediate road repair is required because the pavement shows severe structural failure."
    },

    "pothole": {
        "severity": "High",
        "priority": "High",
        "recommendation":
        "Repair the pothole quickly to reduce accident risk and prevent further pavement damage."
    },

    "pothole deep": {
        "severity": "Critical",
        "priority": "Critical",
        "recommendation":
        "Immediate emergency repair is recommended because the deep pothole can create serious safety hazards."
    }
}


# ==================================================
# LOAD REPORTS
# ==================================================

def load_reports():

    if not os.path.exists(REPORT_FILE):

        return []


    try:

        with open(
            REPORT_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)


    except Exception:

        return []


# ==================================================
# SAVE REPORTS
# ==================================================

def save_reports(reports):

    with open(
        REPORT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            reports,
            file,
            indent=4
        )


# ==================================================
# HOME PAGE
# ==================================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# ==================================================
# AI DETECTION PAGE
# ==================================================

@app.route(
    "/detect",
    methods=["GET", "POST"]
)
def detect():

    # ==================================================
    # OPEN DETECTION PAGE
    # ==================================================

    if request.method == "GET":

        return render_template(
            "detect.html"
        )


    # ==================================================
    # CHECK IMAGE FILE
    # ==================================================

    if "image" not in request.files:

        return render_template(
            "detect.html",
            error="Please select a road image."
        )


    file = request.files["image"]


    if file.filename == "":

        return render_template(
            "detect.html",
            error="No image selected."
        )


    # ==================================================
    # CREATE UNIQUE IMAGE NAME
    # ==================================================

    unique_id = str(
        uuid.uuid4()
    )


    original_filename = (

        unique_id
        + "_"
        + file.filename

    )


    image_path = os.path.join(

        UPLOAD_FOLDER,

        original_filename

    )


    # ==================================================
    # SAVE ORIGINAL IMAGE
    # ==================================================

    file.save(
        image_path
    )


    # ==================================================
    # YOLO PREDICTION
    # ==================================================

    results = model.predict(

        source=image_path,

        save=True,

        conf=0.25,

        device="cpu"

    )


    # ==================================================
    # GET FIRST RESULT
    # ==================================================

    result = results[0]


    # ==================================================
    # YOLO RESULT IMAGE
    # ==================================================

    yolo_result_path = os.path.join(

        result.save_dir,

        os.path.basename(
            image_path
        )

    )


    # ==================================================
    # FINAL RESULT IMAGE NAME
    # ==================================================

    result_filename = (

        "result_"
        + unique_id
        + ".jpg"

    )


    final_result_path = os.path.join(

        RESULT_FOLDER,

        result_filename

    )


    # ==================================================
    # COPY YOLO RESULT TO STATIC FOLDER
    # ==================================================

    if os.path.exists(
        yolo_result_path
    ):

        shutil.copy2(

            yolo_result_path,

            final_result_path

        )

    else:

        # Fallback
        result.save(

            filename=final_result_path

        )


    # ==================================================
    # DETECTIONS
    # ==================================================

    detections = []


    for box in result.boxes:


        # ----------------------------------------------
        # CLASS ID
        # ----------------------------------------------

        class_id = int(
            box.cls[0]
        )


        # ----------------------------------------------
        # CONFIDENCE
        # ----------------------------------------------

        confidence = (

            float(
                box.conf[0]
            )
            * 100

        )


        # ----------------------------------------------
        # CLASS NAME
        # ----------------------------------------------

        class_name = model.names[
            class_id
        ]


        key = class_name.lower()


        # ----------------------------------------------
        # DAMAGE INFORMATION
        # ----------------------------------------------

        info = damage_info.get(

            key,

            {

                "severity":
                "Unknown",

                "priority":
                "Unknown",

                "recommendation":
                "Further inspection is recommended."

            }

        )


        # ----------------------------------------------
        # CREATE DETECTION
        # ----------------------------------------------

        detection = {

            "class":
            class_name,

            "confidence":
            round(
                confidence,
                2
            ),

            "severity":
            info["severity"],

            "priority":
            info["priority"],

            "recommendation":
            info["recommendation"]

        }


        detections.append(
            detection
        )


    # ==================================================
    # LOAD EXISTING REPORTS
    # ==================================================

    reports = load_reports()


    # ==================================================
    # CREATE INSPECTION ID
    # ==================================================

    inspection_id = (

        "RG-"
        + str(
            len(reports) + 1
        ).zfill(3)

    )


    # ==================================================
    # CURRENT DATE AND TIME
    # ==================================================

    current_time = datetime.now().strftime(

        "%d %b %Y, %I:%M %p"

    )


    # ==================================================
    # IMAGE URLS
    # ==================================================

    uploaded_image = (

        "/static/uploads/"
        + original_filename

    )


    result_image = (

        "/static/results/"
        + result_filename

    )


    # ==================================================
    # SAVE REPORTS
    # ==================================================

    for detection in detections:


        report = {

            "id":
            inspection_id,

            "date":
            current_time,

            "damage":
            detection["class"],

            "confidence":
            detection["confidence"],

            "severity":
            detection["severity"],

            "priority":
            detection["priority"],

            "recommendation":
            detection["recommendation"],

            # ------------------------------------------
            # IMAGE INFORMATION
            # ------------------------------------------

            "original_image":
            uploaded_image,

            "result_image":
            result_image

        }


        reports.insert(

            0,

            report

        )


    # ==================================================
    # SAVE JSON
    # ==================================================

    save_reports(
        reports
    )


    # ==================================================
    # SEND DATA TO DETECTION PAGE
    # ==================================================

    return render_template(

        "detect.html",

        uploaded_image=
        uploaded_image,

        result_image=
        result_image,

        detections=
        detections

    )


# ==================================================
# REPORTS PAGE
# ==================================================

@app.route("/reports")
def reports():

    reports_data = load_reports()


    # ==================================================
    # TOTAL INSPECTIONS
    # ==================================================

    total_inspections = len(

        set(

            report["id"]

            for report in reports_data

        )

    )


    # ==================================================
    # TOTAL DAMAGES
    # ==================================================

    total_damages = len(
        reports_data
    )


    # ==================================================
    # MODERATE
    # ==================================================

    moderate_count = sum(

        1

        for report in reports_data

        if report["severity"]
        == "Moderate"

    )


    # ==================================================
    # HIGH
    # ==================================================

    high_count = sum(

        1

        for report in reports_data

        if report["severity"]
        == "High"

    )


    # ==================================================
    # CRITICAL
    # ==================================================

    critical_count = sum(

        1

        for report in reports_data

        if report["severity"]
        == "Critical"

    )


    # ==================================================
    # RENDER REPORT PAGE
    # ==================================================

    return render_template(

        "reports.html",

        reports=
        reports_data,

        total_inspections=
        total_inspections,

        total_damages=
        total_damages,

        moderate_count=
        moderate_count,

        high_count=
        high_count,

        critical_count=
        critical_count

    )


# ==================================================
# RUN APPLICATION
# ==================================================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)