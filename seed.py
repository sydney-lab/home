from app import create_app
from app.extensions import db
from app.models import Workout, Exercise, WorkoutExercise

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    # Exercises
    squat = Exercise(name="Barbell Squat", muscle_group="legs")
    bench = Exercise(name="Bench Press", muscle_group="chest")
    deadlift = Exercise(name="Deadlift", muscle_group="back")
    plank = Exercise(name="Plank", muscle_group="core")
    run = Exercise(name="Treadmill Run", muscle_group="cardio")
    ohp = Exercise(name="Overhead Press", muscle_group="shoulders")

    db.session.add_all([squat, bench, deadlift, plank, run, ohp])
    db.session.commit()

    # Workouts
    push_day = Workout(name="Push Day", notes="Chest and shoulders focus")
    leg_day = Workout(name="Leg Day", notes="Lower body strength")
    full_body = Workout(name="Full Body Circuit", notes="High intensity full body")

    db.session.add_all([push_day, leg_day, full_body])
    db.session.commit()

    # WorkoutExercises
    db.session.add_all([
        WorkoutExercise(workout_id=push_day.id, exercise_id=bench.id, sets=4, reps=8),
        WorkoutExercise(workout_id=push_day.id, exercise_id=ohp.id, sets=3, reps=10),
        WorkoutExercise(workout_id=leg_day.id, exercise_id=squat.id, sets=5, reps=5),
        WorkoutExercise(workout_id=leg_day.id, exercise_id=deadlift.id, sets=3, reps=6),
        WorkoutExercise(workout_id=full_body.id, exercise_id=plank.id, duration_seconds=60),
        WorkoutExercise(workout_id=full_body.id, exercise_id=run.id, duration_seconds=1200),
        WorkoutExercise(workout_id=full_body.id, exercise_id=squat.id, sets=3, reps=12),
    ])
    db.session.commit()

    print("Database seeded successfully!")
    print(f"  {Exercise.query.count()} exercises")
    print(f"  {Workout.query.count()} workouts")
    print(f"  {WorkoutExercise.query.count()} workout-exercise links")
