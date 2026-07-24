from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from app.extensions import db
from app.models import Workout, Exercise, WorkoutExercise
from app.schemas import (
    workout_schema, workouts_schema,
    exercise_schema, exercises_schema,
    workout_exercise_schema,
)

bp = Blueprint("api", __name__)


def error(message, status=400):
    return jsonify({"error": message}), status


# ── Workouts ──────────────────────────────────────────────────────────────────

@bp.get("/workouts")
def get_workouts():
    return workouts_schema.dump(Workout.query.all()), 200


@bp.get("/workouts/<int:id>")
def get_workout(id):
    workout = db.get_or_404(Workout, id)
    return workout_schema.dump(workout), 200


@bp.post("/workouts")
def create_workout():
    try:
        data = workout_schema.load(request.get_json())
    except ValidationError as e:
        return error(e.messages)
    try:
        workout = Workout(**data)
        db.session.add(workout)
        db.session.commit()
    except ValueError as e:
        db.session.rollback()
        return error(str(e))
    return workout_schema.dump(workout), 201


@bp.delete("/workouts/<int:id>")
def delete_workout(id):
    workout = db.get_or_404(Workout, id)
    db.session.delete(workout)
    db.session.commit()
    return {}, 204


# ── Exercises ─────────────────────────────────────────────────────────────────

@bp.get("/exercises")
def get_exercises():
    return exercises_schema.dump(Exercise.query.all()), 200


@bp.get("/exercises/<int:id>")
def get_exercise(id):
    exercise = db.get_or_404(Exercise, id)
    return exercise_schema.dump(exercise), 200


@bp.post("/exercises")
def create_exercise():
    try:
        data = exercise_schema.load(request.get_json())
    except ValidationError as e:
        return error(e.messages)
    try:
        exercise = Exercise(**data)
        db.session.add(exercise)
        db.session.commit()
    except ValueError as e:
        db.session.rollback()
        return error(str(e))
    return exercise_schema.dump(exercise), 201


@bp.delete("/exercises/<int:id>")
def delete_exercise(id):
    exercise = db.get_or_404(Exercise, id)
    db.session.delete(exercise)
    db.session.commit()
    return {}, 204


# ── Workout Exercises ─────────────────────────────────────────────────────────

@bp.post("/workouts/<int:workout_id>/exercises")
def add_exercise_to_workout(workout_id):
    db.get_or_404(Workout, workout_id)
    try:
        data = workout_exercise_schema.load(request.get_json())
    except ValidationError as e:
        return error(e.messages)

    exercise_id = data.pop("exercise_id")
    if not db.session.get(Exercise, exercise_id):
        return error(f"Exercise {exercise_id} not found", 404)

    existing = WorkoutExercise.query.filter_by(
        workout_id=workout_id, exercise_id=exercise_id
    ).first()
    if existing:
        return error("Exercise already added to this workout")

    try:
        we = WorkoutExercise(workout_id=workout_id, exercise_id=exercise_id, **data)
        db.session.add(we)
        db.session.commit()
    except ValueError as e:
        db.session.rollback()
        return error(str(e))

    return workout_exercise_schema.dump(we), 201
