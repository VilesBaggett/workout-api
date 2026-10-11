from flask import Flask, request, jsonify
from flasgger import Swagger  # add this

app = Flask(__name__)
swagger = Swagger(app)        # and this


def validate_workout(data):
    if not data:
        return {
            "is_valid": False,
            "error": "Request body must be JSON"
        }

    required_fields = ["name", "durationMinutes", "isCompleted"]
    for field in required_fields:
        if field not in data:
            return {
                "is_valid": False,
                "error": f"Missing required field: {field}"
            }

    # (Optional: type checks, positive duration, allowed intensity values, etc.)

    return {"is_valid": True}



workouts = []
next_id = 1


@app.route("/workouts", methods=["GET"])
def list_workouts():
    """
    List all workouts
    ---
    tags:
      - Workouts
    responses:
      200:
        description: A list of workouts
        content:
          application/json:
            schema:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                  name:
                    type: string
                  durationMinutes:
                    type: integer
                  intensity:
                    type: string
                    nullable: true
                  isCompleted:
                    type: boolean
    """
    return jsonify(workouts), 200


@app.route("/workouts", methods=["POST"])
def create_workout():
    """
    Create a new workout
    ---
    tags:
      - Workouts
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required:
              - name
              - durationMinutes
              - isCompleted
            properties:
              name:
                type: string
                example: Push Day
              durationMinutes:
                type: integer
                example: 60
              intensity:
                type: string
                nullable: true
                example: high
              isCompleted:
                type: boolean
                example: false
    responses:
      201:
        description: Workout created
        content:
          application/json:
            schema:
              type: object
              properties:
                id:
                  type: integer
                  example: 1
                name:
                  type: string
                durationMinutes:
                  type: integer
                intensity:
                  type: string
                  nullable: true
                isCompleted:
                  type: boolean
      400:
        description: Invalid input
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: "Missing required field: name"
    """
    global next_id
    data = request.get_json()
    validation = validate_workout(data)
    if not validation["is_valid"]:
        return jsonify({"error": validation["error"]}), 400
    ...

    new_workout = {
        "id": next_id,
        "name": data["name"],
        "durationMinutes": data["durationMinutes"],
        "intensity": data.get("intensity"),
        "isCompleted": data["isCompleted"],
    }
    workouts.append(new_workout)
    next_id += 1

    return jsonify(new_workout), 201

@app.route("/workouts/<int:workout_id>", methods=["GET"])
def get_workout(workout_id):
    """
    Get a workout by id
    ---
    tags:
      - Workouts
    parameters:
      - name: workout_id
        in: path
        required: true
        description: ID of the workout to retrieve
        schema:
          type: integer
    responses:
      200:
        description: Workout found
        content:
          application/json:
            schema:
              type: object
              properties:
                id:
                  type: integer
                name:
                  type: string
                durationMinutes:
                  type: integer
                intensity:
                  type: string
                  nullable: true
                isCompleted:
                  type: boolean
      404:
        description: Workout not found
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: "Workout not found"
    """
    for workout in workouts:
        if workout["id"] == workout_id:
            return jsonify(workout), 200

    return jsonify({"error": "Workout not found"}), 404



@app.route("/workouts/<int:workout_id>", methods=["DELETE"])
def delete_workout(workout_id):
    """
    Delete a workout
    ---
    tags:
      - Workouts
    parameters:
      - name: workout_id
        in: path
        required: true
        description: ID of the workout to delete
        schema:
          type: integer
    responses:
      204:
        description: Workout deleted successfully (no content)
      404:
        description: Workout not found
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: "Workout not found"
    """
    for index, workout in enumerate(workouts):
        if workout["id"] == workout_id:
            del workouts[index]
            return "", 204

    return jsonify({"error": "Workout not found"}), 404



@app.route("/workouts/<int:workout_id>", methods=["PUT"])
def update_workout(workout_id):
    """
    Replace an existing workout
    ---
    tags:
      - Workouts
    parameters:
      - name: workout_id
        in: path
        required: true
        description: ID of the workout to update
        schema:
          type: integer
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required:
              - name
              - durationMinutes
              - isCompleted
            properties:
              name:
                type: string
                example: Leg Day
              durationMinutes:
                type: integer
                example: 45
              intensity:
                type: string
                nullable: true
                example: medium
              isCompleted:
                type: boolean
                example: true
    responses:
      200:
        description: Workout updated
        content:
          application/json:
            schema:
              type: object
              properties:
                id:
                  type: integer
                name:
                  type: string
                durationMinutes:
                  type: integer
                intensity:
                  type: string
                  nullable: true
                isCompleted:
                  type: boolean
      400:
        description: Invalid input
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: "Missing required field: name"
      404:
        description: Workout not found
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: "Workout not found"
    """
    data = request.get_json()
    validation = validate_workout(data)
    if not validation["is_valid"]:
        return jsonify({"error": validation["error"]}), 400

    for workout in workouts:
        if workout["id"] == workout_id:
            workout["name"] = data["name"]
            workout["durationMinutes"] = data["durationMinutes"]
            workout["intensity"] = data.get("intensity")
            workout["isCompleted"] = data["isCompleted"]
            return jsonify(workout), 200

    return jsonify({"error": "Workout not found"}), 404



if __name__ == "__main__":
    app.run(debug=True)