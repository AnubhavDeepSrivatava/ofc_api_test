from app.models.user import User
from app.models.student import Student
from app.models.advisor import Advisor
from app.models.jury import Jury
from app.models.school import School
from app.models.program import Program
from app.models.course import Course
from app.models.activity import Activity

# Simple registry mapping entity names to model and id_field
REGISTRY = {
    "user": {
        "model": User,
        "id_field": "user_id"
    },
    "student": {
        "model": Student,
        "id_field": "student_id"
    },
    "advisor": {
        "model": Advisor,
        "id_field": "advisor_id"
    },
    "jury": {
        "model": Jury,
        "id_field": "jury_id"
    },
    "school": {
        "model": School,
        "id_field": "school_id"
    },
    "program": {
        "model": Program,
        "id_field": "program_id"
    },
    "course": {
        "model": Course,
        "id_field": "course_id"
    },
    "activity": {
        "model": Activity,
        "id_field": "activity_id"
    }
}


def get_model(name: str):
    """Get model class for an entity name."""
    if name not in REGISTRY:
        raise ValueError(f"Entity '{name}' not found in registry")
    return REGISTRY[name]["model"]


def get_id_field(name: str) -> str:
    """Get id field name for an entity."""
    if name not in REGISTRY:
        raise ValueError(f"Entity '{name}' not found in registry")
    return REGISTRY[name]["id_field"]
