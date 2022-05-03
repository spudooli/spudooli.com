from spudoolicom import app
from flask_wtf import FlaskForm  
from wtforms import validators, ValidationError  
from wtforms import StringField, TextAreaField, SubmitField
from flask_wtf.csrf import CSRFProtect
from flask_wtf.recaptcha import RecaptchaField



  
class photoblogComment(FlaskForm):  
    csrf = CSRFProtect()
    csrf.init_app(app)

    commentmessage = TextAreaField("Message",[validators.DataRequired("We really need your comment")])  
    commentname = StringField("Name",[validators.DataRequired("Please enter your name.")])  
    commenturl = StringField("Your website URL (optional)")    
    commentemail =  StringField("Your email address (optional and never visible to anyone else)")
    recaptcha = RecaptchaField()  
    commentsubmit = SubmitField("Submit")


class search(FlaskForm):
    csrf = CSRFProtect()  
    csrf.init_app(app)

    searchblog = TextAreaField("Search")  
    searchsubmit = SubmitField("Submit")