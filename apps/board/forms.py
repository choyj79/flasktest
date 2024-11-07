from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class BoardForm(FlaskForm):
    # 게시글 제목 필드
    title = StringField(
        "제목",
        validators=[
            DataRequired(message="제목은 필수입니다."),
            Length(max=100, message="제목은 100자 이내로 입력해 주세요."),
        ],
    )
    
    # 게시글 내용 필드
    content = TextAreaField(
        "내용",
        validators=[DataRequired(message="내용은 필수입니다.")],
    )

    # 제출 버튼
    submit = SubmitField("글 작성")
