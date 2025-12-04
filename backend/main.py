#from init import create_app
import flask
from controllers.login import login_bp
from controllers.inference import inference_bp
from controllers.compiler import compiler_bp
from controllers.behavior import behavior_bp
from controllers.question_contoller import question_bp
app = flask.Flask(__name__)
app.register_blueprint(login_bp, url_prefix="/auth")
app.register_blueprint(inference_bp,url_prefix = "/inference")
app.register_blueprint(compiler_bp, url_prefix="/compiler")
app.register_blueprint(behavior_bp, url_prefix="/behavior")
app.register_blueprint(question_bp, url_prefix="/testmaking")
if __name__=="__main__":
    app.run(debug = True)
