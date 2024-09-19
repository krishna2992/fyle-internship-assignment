from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment
from core.models.users import User
from core.models.principals import Principal
from werkzeug.exceptions import HTTPException

from .schema import AssignmentSchema, AssignmentGradeSchema, UserSchema
principal_assignments_resources = Blueprint('principal_assignments_resources', __name__)


@principal_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def grade_assignments_principal(p, incoming_payload):
    grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)

    graded_assignment = Assignment.mark_grade(
        _id=grade_assignment_payload.id,
        grade=grade_assignment_payload.grade,
        auth_principal=p,
        principle=True
    )
    db.session.commit()
    graded_assignment_dump = AssignmentSchema().dump(graded_assignment)
    return APIResponse.respond(data=graded_assignment_dump)


@principal_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_assignments(p):
    """Returns list of assignments"""
    
    principle  = Principal.get_by_id(p.principal_id)
    repr(principle)
    principle_assignments = Assignment.get_assignments_by_principle(p)
    teachers_assignments_dump = AssignmentSchema().dump(principle_assignments, many=True)
    return APIResponse.respond(data=teachers_assignments_dump)

@principal_assignments_resources.route('/user', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def get_user(p):
    
    principle_assignments = User.get_by_id(p.user_id)
    users_dump = UserSchema().dump(principle_assignments)
    return APIResponse.respond(data=users_dump)
