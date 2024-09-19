from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment
from core.models.users import User

from .schema import AssignmentSchema, AssignmentGradeSchema, UserSchema
teacher_assignments_resources = Blueprint('teacher_assignments_resources', __name__)


@teacher_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_assignments(p):
    """Returns list of assignments"""
    teachers_assignments = Assignment.get_assignments_by_teacher(p.teacher_id)
    teachers_assignments_dump = AssignmentSchema().dump(teachers_assignments, many=True)
    return APIResponse.respond(data=teachers_assignments_dump)


@teacher_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def grade_assignment(p, incoming_payload):
    """Grade an assignment"""
    grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)

    graded_assignment = Assignment.mark_grade(
        _id=grade_assignment_payload.id,
        grade=grade_assignment_payload.grade,
        auth_principal=p
    )
    db.session.commit()
    graded_assignment_dump = AssignmentSchema().dump(graded_assignment)
    return APIResponse.respond(data=graded_assignment_dump)


@teacher_assignments_resources.route('/user/email', methods=['GET'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def get_user_by_mail(p, incoming_payload):
    user_mail = incoming_payload['user_mail']
    user_data = User.get_by_email(user_mail)
    repr(user_data)
    user_ser_data = UserSchema().dump(user_data)
    return APIResponse.respond(data=user_ser_data)