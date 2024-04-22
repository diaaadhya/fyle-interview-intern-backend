from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.assignments.schema import AssignmentGradeSchema, AssignmentSchema
from core.apis.responses import APIResponse
from core.models.assignments import Assignment, AssignmentStateEnum

principal_assignements_resources = Blueprint('principal_assignments_resources', __name__)

@principal_assignements_resources.route("/assignments", methods=['GET'], strict_slashes= False)
@decorators.authenticate_principal
def list_assignments(p):
    """Returns list of assignments submitted and/or graded by teachers."""
    assignments = Assignment.filter(Assignment.state.in_([AssignmentStateEnum.SUBMITTED,AssignmentStateEnum.GRADED]))
    assignments_dump = AssignmentSchema().dump(assignments,many=True)
    return APIResponse.respond(data=assignments_dump)

@principal_assignements_resources.route("/assignments/grade", methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def grade_assignment(p, incoming_payload):
    """Regrade an assignment"""
    grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)
    
    graded_assignment = Assignment.re_grade(
        _id=grade_assignment_payload.id,
        grade=grade_assignment_payload.grade,
    )
    db.session.commit()
    graded_assignment_dump = AssignmentSchema().dump(graded_assignment)
    return APIResponse.respond(data=graded_assignment_dump)