from marshmallow import Schema, fields, validates, ValidationError, validate, post_load


class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(dump_only=True)
    exercise_id = fields.Int(required=True)
    sets = fields.Int(load_default=None)
    reps = fields.Int(load_default=None)
    duration_seconds = fields.Int(load_default=None)
    exercise = fields.Nested(lambda: ExerciseSchema(only=("id", "name", "muscle_group")), dump_only=True)

    @validates("sets")
    def validate_sets(self, value):
        if value is not None and value <= 0:
            raise ValidationError("sets must be a positive integer")

    @validates("reps")
    def validate_reps(self, value):
        if value is not None and value <= 0:
            raise ValidationError("reps must be a positive integer")

    @validates("duration_seconds")
    def validate_duration(self, value):
        if value is not None and value <= 0:
            raise ValidationError("duration_seconds must be a positive integer")

    @post_load
    def check_sets_reps_or_duration(self, data, **kwargs):
        has_sets_reps = data.get("sets") is not None and data.get("reps") is not None
        has_duration = data.get("duration_seconds") is not None
        if not has_sets_reps and not has_duration:
            raise ValidationError(
                "Provide either both 'sets' and 'reps', or 'duration_seconds'"
            )
        return data


class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    notes = fields.Str(load_default=None, validate=validate.Length(max=500))
    workout_exercises = fields.List(
        fields.Nested(WorkoutExerciseSchema), dump_only=True
    )


class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    muscle_group = fields.Str(required=True)

    VALID_MUSCLE_GROUPS = {
        "chest", "back", "legs", "shoulders", "arms", "core", "cardio", "full body"
    }

    @validates("muscle_group")
    def validate_muscle_group(self, value):
        if value.lower() not in self.VALID_MUSCLE_GROUPS:
            raise ValidationError(
                f"muscle_group must be one of: {', '.join(sorted(self.VALID_MUSCLE_GROUPS))}"
            )


workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)
exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)
workout_exercise_schema = WorkoutExerciseSchema()
