from sqlalchemy.orm import validates
from app.extensions import db


class WorkoutExercise(db.Model):
    __tablename__ = "workout_exercises"

    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey("workouts.id"), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey("exercises.id"), nullable=False)
    sets = db.Column(db.Integer)
    reps = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)

    __table_args__ = (
        db.UniqueConstraint("workout_id", "exercise_id", name="uq_workout_exercise"),
        db.CheckConstraint(
            "(sets IS NOT NULL AND reps IS NOT NULL) OR duration_seconds IS NOT NULL",
            name="ck_sets_reps_or_duration",
        ),
    )

    @validates("sets", "reps")
    def validate_positive_int(self, key, value):
        if value is not None and value <= 0:
            raise ValueError(f"{key} must be a positive integer")
        return value

    @validates("duration_seconds")
    def validate_duration(self, key, value):
        if value is not None and value <= 0:
            raise ValueError("duration_seconds must be a positive integer")
        return value


class Workout(db.Model):
    __tablename__ = "workouts"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    notes = db.Column(db.String(500))

    workout_exercises = db.relationship(
        "WorkoutExercise", backref="workout", cascade="all, delete-orphan"
    )

    @validates("name")
    def validate_name(self, key, value):
        if not value or not value.strip():
            raise ValueError("Workout name cannot be blank")
        return value.strip()


class Exercise(db.Model):
    __tablename__ = "exercises"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    muscle_group = db.Column(db.String(50), nullable=False)

    VALID_MUSCLE_GROUPS = {
        "chest", "back", "legs", "shoulders", "arms", "core", "cardio", "full body"
    }

    workout_exercises = db.relationship("WorkoutExercise", backref="exercise")

    @validates("name")
    def validate_name(self, key, value):
        if not value or not value.strip():
            raise ValueError("Exercise name cannot be blank")
        return value.strip()

    @validates("muscle_group")
    def validate_muscle_group(self, key, value):
        if not value or value.lower() not in self.VALID_MUSCLE_GROUPS:
            raise ValueError(
                f"muscle_group must be one of: {', '.join(sorted(self.VALID_MUSCLE_GROUPS))}"
            )
        return value.lower()
