from flask import Flask, request, jsonify
from flask_cors import CORS

from parser import parse_input
from encoder import encode_to_rbn
from solver import check_safety

import traceback

# =========================================
# APP
# =========================================

app = Flask(__name__)

CORS(app)

# =========================================
# HOME
# =========================================

@app.route("/", methods=["GET"])
def home():

    return jsonify({
        "message": "OMAS Safety Checker Running"
    })


# =========================================
# CHECK
# =========================================

@app.route("/check", methods=["POST"])
def check():

    logs = []

    # -------------------------------------
    # LOGGER
    # -------------------------------------

    def logger(msg):

        print(msg)

        logs.append(str(msg))

    try:

        logger("\n===================================")
        logger("🚀 /check endpoint called")
        logger("===================================\n")

        # ---------------------------------
        # INPUT
        # ---------------------------------

        data = request.get_json()

        if not data:

            return jsonify({
                "error": "No JSON received"
            })

        input_text = data.get("input", "")

        if not input_text.strip():

            return jsonify({
                "error": "Empty input"
            })

        logger("📥 INPUT:\n")
        logger(input_text)

        # =================================
        # PARSER
        # =================================

        logger("\n📦 STARTING PARSER...\n")

        omas = parse_input(
            input_text,
            logger=logger
        )

        logger("\n✅ PARSING FINISHED\n")
        logger(str(omas))

        # =================================
        # ENCODER
        # =================================

        logger("\n🔄 STARTING RBN ENCODING...\n")

        rbn = encode_to_rbn(
            omas,
            logger=logger
        )

        logger("\n✅ RBN ENCODING FINISHED\n")
        logger(str(rbn))

        # =================================
        # BFS SAFETY CHECK
        # =================================

        logger("\n🧠 STARTING BFS SAFETY CHECK...\n")

        result = check_safety(
            rbn,
            logger=logger
        )

        logger("\n✅ SAFETY CHECK FINISHED\n")
        logger(str(result))

        # =================================
        # RESPONSE
        # =================================

        return jsonify({

            "safe": result["safe"],

            "reachable_states":
                result["reachable_states"],

            "unsafe_reached":
                result["unsafe_reached"],

            "rbn": {

                "RC": rbn["RC"],

                "RL": rbn["RL"],

                "Sigma": rbn["Sigma"],

                "unsafe_states":
                    rbn["unsafe_states"],

                "safety_formula":
                    rbn["safety_formula"]
            },

            "logs": logs
        })

    except Exception as e:

        traceback.print_exc()

        logger("\n🔥 ERROR OCCURRED\n")

        logger(str(e))

        return jsonify({

            "error": str(e),

            "logs": logs
        })


# =========================================
# RUN
# =========================================

if __name__ == "__main__":

    app.run(
        port=5001,
        debug=True
    )