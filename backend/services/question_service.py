import uuid
from flask import request, jsonify
from utils.mongo_util import mongo_util as mongo
from services.tokenizer_service import tokenizer_service
class QuestionService:

    @staticmethod
    def create_test():
        data = request.get_json()

        testname = data.get("testname", "").strip()
        test_time = int(data.get("testtime", "").strip())
        test_desc = data.get("testdesc", "").strip()
        hiring_email = data.get("hiring_email", "").strip()

        if not testname:
            return jsonify({"error": "testname is required"}), 400
        if not hiring_email:
            return jsonify({"error": "hiring_email is required"}), 400

        test_id = f"test_{uuid.uuid4().hex[:8]}"

        mongo.insert_one("assessments", {
            "_id": test_id,
            "testname": testname,
            "test_time": test_time,
            "description": test_desc,
            "hiring_email": hiring_email,
            "questions": [],
            "student_marks": []
        })

        mongo.update_one(
            "hr",
            {"email": hiring_email},
            {
                "$push": {
                    "tests": {
                        "test_id": test_id,
                        "testname": testname
                    }
                }
            },
            upsert=True  # creates HR doc if it doesn't exist
        )

        return jsonify({
            "message": "Test created",
            "test_id": test_id,
            "testname": testname
        }), 201


    @staticmethod
    def create_question():
        data = request.get_json()

        testname = data.get("testname", "").strip()
        question_text = data.get("question", "")
        testcases = data.get("testcases", [])
        output = data.get("output", "")

        if not testname or not question_text:
            return jsonify({"error": "testname and question are required"}), 400
        
        inference = tokenizer_service.add_inference(question_text)
        question_obj = {
            "text": question_text,
            "testcases": testcases,
            "output": output,
            "inference" : inference
        }
        

        # Push question into the array
        mongo.update_one(
            "assessments",
            {"_id": testname},
            {"$push": {"questions": question_obj}}
        )

        return jsonify({"message": "Question added", "testname": testname,"inference" : inference}), 201

    @staticmethod
    def get_test_questions(testname):
        data = mongo.find_one("assessments", {"_id": testname})
        if data:
            return jsonify(data)
        return jsonify({"error": "Test not found"}), 404
    @staticmethod
    def add_student_marks():
        data = request.json
        test_id = data.get("test_id")
        email = data.get("email")
        marks = data.get("marks")

        if not test_id or not email or marks is None:
            return jsonify({"error": "test_id, email, and marks required"}), 400

        # Step 1: Try updating existing student marks
        updated = mongo.update_one(
            "assessments",
            {"_id": test_id, "student_marks.email": email},
            {"$set": {"student_marks.$.marks": marks}}
        )

        # Step 2: If student not found → push into existing test
        if updated.matched_count == 0:
            mongo.update_one(
                "assessments",
                {"_id": test_id},
                {"$push": {"student_marks": {"email": email, "marks": marks}}}
            )

        return jsonify({"message": "marks added/updated successfully"}), 200
