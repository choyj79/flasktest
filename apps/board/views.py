# from apps.app import db
from app import db
from apps.crud.models import User
from flask import Blueprint, render_template, redirect, url_for, request, flash
from apps.board.forms import BoardForm
from flask_login import login_required, current_user
from apps.board.models import Board

# Blueprint로 crud 앱을 생성한다
board = Blueprint(
    "board",
    __name__,
    template_folder="templates",
    static_folder="static", 
)

# index 엔드포인트를 작성하고 index.html을 반환한다
@board.route("/")
def index():
    return render_template("board/index.html") 

@board.route('/boards')
def boards():
    posts = Board.query.order_by(Board.created_at.desc()).all()  # 최신 글부터 조회
    return render_template('board/board.html', posts=posts)

@board.route('/board/write', methods=['GET', 'POST'])
@login_required  # 로그인한 사용자만 접근 가능
def write():
    # BoardForm을 인스턴스화한다
    form = BoardForm()

    # 폼의 값을 벨리데이트한다
    if form.validate_on_submit():
        # 게시글을 작성한다
        new_post = Board(
            title=form.title.data,
            content=form.content.data,
            author_id=current_user.id
        )

        # 게시글을 추가하고 커밋한다
        db.session.add(new_post)
        db.session.commit()

        # 게시글 목록 화면으로 리다이렉트한다
        flash('글이 성공적으로 작성되었습니다!', 'success')
        return redirect(url_for('board.boards'))
    
    # GET 요청 시 작성 폼을 렌더링한다
    return render_template('board/write.html', form=form)

@board.route('/board/<int:post_id>', methods=['GET'])
def view(post_id):
    post = Board.query.get_or_404(post_id)  # 게시글 ID로 게시글을 조회
    return render_template('board/view.html', post=post)

@board.route('/board/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    # 게시글 조회
    post = Board.query.get_or_404(post_id)  # 게시글 조회
    form = BoardForm(obj=post)  # 기존 데이터로 폼 초기화

    # POST 요청 처리
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('게시글이 수정되었습니다!', 'success')
        return redirect(url_for('board.view', post_id=post.id))

    # GET 요청 시 수정 화면 렌더링
    return render_template('board/edit.html', form=form, post=post)