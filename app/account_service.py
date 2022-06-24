from flask import *
from Login import check_username_availability, verify_user, add_user, get_expiry_date, change_password

# 初始化蓝图
accountService = Blueprint("accountService", __name__)


### Sign-up, login, logout ###
@accountService.route("/signup", methods=['GET', 'POST'])
def signup():
    '''
    注册
    :return: 根据注册是否成功返回不同界面
    '''
    if request.method == 'GET':
        # GET方法直接返回注册页面
        return render_template('signup.html')
    elif request.method == 'POST':
        # POST方法需判断是否注册成功，再根据结果返回不同的内容
        username = escape(request.form['username'])
        password = escape(request.form['password'])

        available = check_username_availability(username)
        if not available: # 用户名不可用
            flash('用户名 %s 已经被注册。' % (username))
            return render_template('signup.html')
        elif len(password.strip()) < 4: # 密码过短
            return '密码过于简单。'
        else: # 添加账户信息
            add_user(username, password)
            verified = verify_user(username, password)
            if verified:
                # 写入session
                session['logged_in'] = True
                session[username] = username
                session['username'] = username
                session['expiry_date'] = get_expiry_date(username)
                session['articleID'] = None
                return '<p>恭喜，你已成功注册， 你的用户名是 <a href="%s">%s</a>。</p>\
                <p><a href="/%s">开始使用</a> <a href="/">返回首页</a><p/>' % (username, username, username)
            else:
                return '用户名密码验证失败。'


@accountService.route("/login", methods=['GET', 'POST'])
def login():
    '''
    登录
    :return: 根据登录是否成功返回不同页面
    '''
    if request.method == 'GET':
        # GET请求
        if not session.get('logged_in'):
            # 未登录，返回登录页面
            return render_template('login.html')
        else:
            # 已登录，提示信息并显示登出按钮
            return '你已登录 <a href="/%s">%s</a>。 登出点击<a href="/logout">这里</a>。' % (
                session['username'], session['username'])
    elif request.method == 'POST':
        # POST方法用于判断登录是否成功
        # check database and verify user
        username = escape(request.form['username'])
        password = escape(request.form['password'])
        verified = verify_user(username, password)
        if verified:
            # 登录成功，写入session
            session['logged_in'] = True
            session[username] = username
            session['username'] = username
            user_expiry_date = get_expiry_date(username)
            session['expiry_date'] = user_expiry_date
            session['articleID'] = None
            return redirect(url_for('user_bp.userpage', username=username))
        else:
            return '无法通过验证。'


@accountService.route("/logout", methods=['GET', 'POST'])
def logout():
    '''
    登出
    :return: 重定位到主界面
    '''
    # 将session标记为登出状态
    session['logged_in'] = False
    return redirect(url_for('mainpage'))


@accountService.route("/reset", methods=['GET', 'POST'])
def reset():
    '''
    重设密码
    :return: 返回适当的页面
    '''
    # 下列方法用于防止未登录状态下的修改密码
    if not session.get('logged_in'):
        return render_template('login.html')
    username = session['username']
    if username == '':
        return redirect('/login')
    if request.method == 'GET':
        # GET请求返回修改密码页面
        return render_template('reset.html', username=session['username'], state='wait')
    else:
        # POST请求用于提交修改后信息
        old_password = escape(request.form['old-password'])
        new_password = escape(request.form['new-password'])
        flag = change_password(username, old_password, new_password) # flag表示是否修改成功
        if flag:
            session['logged_in'] = False
            return \
'''
<script>
alert('密码修改成功，请重新登录。');
window.location.href="/login";
</script>

'''

        else:
            return \
'''
<script>
alert('密码修改失败');
window.location.href="/reset";
</script>

'''