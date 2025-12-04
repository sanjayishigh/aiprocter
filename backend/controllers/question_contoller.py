from flask import Blueprint
from services.question_service import QuestionService

question_bp = Blueprint("question", __name__)

@question_bp.route("/test", methods=["POST"])
def create_test():
    return QuestionService.create_test()

@question_bp.route("/question", methods=["POST"])
def create_question():
    return QuestionService.create_question()

@question_bp.route("/test/<testname>", methods=["GET"])
def get_questions(testname):
    return QuestionService.get_test_questions(testname)

@question_bp.route("/add-marks", methods=["POST"])
def add_student_marks():
    return QuestionService.add_student_marks()

