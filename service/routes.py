"""
Controller for routes
"""
from flask import jsonify, url_for, abort
from service import app
from service.common import status

# In-memory dictionary to store counters
COUNTER = {}


################
# Health Endpoint
################
@app.route("/health")
def health():
    """Returns the health status of the service"""
    return jsonify(dict(status="OK")), status.HTTP_200_OK


################
# Index page
################
@app.route("/")
def index():
    """Returns basic information about the service"""
    app.logger.info("Request for Base URL")
    return jsonify(
        status=status.HTTP_200_OK,
        message="Hit Counter Service",
        version="1.0.0",
        url=url_for("list_counters", _external=True),
    )


#################
# List counters
#################
@app.route("/counters", methods=["GET"])
def list_counters():
    """Lists all counters"""
    app.logger.info("Request to list all counters...")
    counters = [
        dict(name=name, counter=count)
        for name, count in COUNTER.items()
    ]
    return jsonify(counters), status.HTTP_200_OK


################
# Create counter
################
@app.route("/counters/<name>", methods=["POST"])
def create_counters(name):
    """Creates a new counter with initial value 0"""
    app.logger.info("Request to create counter: %s...", name)

    if name in COUNTER:
        abort(
            status.HTTP_409_CONFLICT,
            f"Counter '{name}' already exists"
        )

    COUNTER[name] = 0
    location_url = url_for(
        "read_counters",
        name=name,
        _external=True
    )

    return (
        jsonify(name=name, counter=0),
        status.HTTP_201_CREATED,
        {"Location": location_url},
    )


################
# Read counter
################
@app.route("/counters/<name>", methods=["GET"])
def read_counters(name):
    """Reads a single counter by name"""
    app.logger.info("Request to read counter: %s...", name)

    if name not in COUNTER:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Counter '{name}' does not exist"
        )

    return jsonify(
        name=name,
        counter=COUNTER[name]
    ), status.HTTP_200_OK


################
# Update counter
################
@app.route("/counters/<name>", methods=["PUT"])
def update_counters(name):
    """Increments the value of a counter"""
    app.logger.info("Request to update counter: %s...", name)

    if name not in COUNTER:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Counter '{name}' does not exist"
        )

    COUNTER[name] += 1
    return jsonify(
        name=name,
        counter=COUNTER[name]
    ), status.HTTP_200_OK


################
# Delete counter
################
@app.route("/counters/<name>", methods=["DELETE"])
def delete_counters(name):
    """Deletes a counter by name"""
    app.logger.info("Request to delete counter: %s...", name)

    if name in COUNTER:
        del COUNTER[name]

    return "", status.HTTP_204_NO_CONTENT


################
# Utility for testing
################
def reset_counters():
    """Resets all counters — used only in testing mode"""
    global COUNTER  # pylint: disable=global-statement
    if app.testing:
        COUNTER = {}
