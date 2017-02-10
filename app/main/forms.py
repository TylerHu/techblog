#-*_ coding:utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField, SelectMultipleField
from wtforms.validators import Required, Length, Email, Regexp
from wtforms import ValidationError
from ..models import Tag
from flask_pagedown.fields import PageDownField

class PostForm(FlaskForm):
    title = StringField(u'标题', validators=[Required()])
    body = PageDownField(u'正文', validators=[Required()])
    tag = SelectMultipleField(u'标签', coerce=int)
    submit = SubmitField(u'提交')

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.tag.choices = [(tag.id, tag.name) for tag in Tag.query.order_by(Tag.id).all()]


