# Workout Tracker API

A RESTful backend API for a personal trainer workout tracking application. Built with Flask, SQLAlchemy, and Marshmallow.

## Description

This API allows personal trainers to manage workouts and reusable exercises. Trainers can create workouts, define exercises, and attach exercises to workouts with sets/reps or duration. The API enforces data integrity through database constraints, model validations, and schema validations.

## Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd workout-tracker

# Install dependencies
pipenv install

# Activate the virtual environment
pipenv shell

# Initialize the database
flask db init
flask db migrate -m "initial migration"
flask db upgrade

# Seed the database with sample data
python seed.py
```

## Running the Application

```bash
flask run
```

The API will be available at `http://127.0.0.1:5000`.

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/workouts` | List all workouts with their exercises |
| GET | `/workouts/<id>` | Get a single workout by ID |
| POST | `/workouts` | Create a new workout |
| DELETE | `/workouts/<id>` | Delete a workout and its exercise links |
| GET | `/exercises` | List all exercises |
| GET | `/exercises/<id>` | Get a single exercise by ID |
| POST | `/exercises` | Create a new exercise |
| DELETE | `/exercises/<id>` | Delete an exercise |
| POST | `/workouts/<workout_id>/exercises` | Add an exercise to a workout |

### Request Body Examples

**POST /workouts**
```json
{
  "name": "Push Day",
  "notes": "Chest and shoulders"
}
```

**POST /exercises**
```json
{
  "name": "Bench Press",
  "muscle_group": "chest"
}
```
Valid `muscle_group` values: `arms`, `back`, `cardio`, `chest`, `core`, `full body`, `legs`, `shoulders`

**POST /workouts/:id/exercises** — with sets/reps:
```json
{
  "exercise_id": 1,
  "sets": 4,
  "reps": 8
}
```

**POST /workouts/:id/exercises** — with duration:
```json
{
  "exercise_id": 3,
  "duration_seconds": 60
}
```

## Validations

- Workout and Exercise names must be non-blank and unique (table constraint + model + schema)
- `muscle_group` must be one of the valid values (model + schema)
- Each `WorkoutExercise` must have either `sets` + `reps` or `duration_seconds` (table constraint + schema)
- An exercise can only be added to a workout once (unique constraint)
- `sets`, `reps`, and `duration_seconds` must be positive integers
# home
