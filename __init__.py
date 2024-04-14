import os

from flask import Flask, render_template, request, redirect, url_for


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.instance_path = ""
    from . import db
    db.init_app(app)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'todolist.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    @app.route('/')
    def index():
        cur = db.get_db().cursor()
        sql = '''SELECT * from TASKS_TABLE'''
        cur.execute(sql)
        tasks = cur.fetchall()
           
        return render_template("index.html", tasks=tasks)
    
    @app.route('/failure', methods=['GET'])
    def failure():
        return render_template("failure.html")

    @app.route('/tasks/new', methods=['GET', 'POST'])
    def new_task():
        if request.method == 'POST':
            title = request.form['task_title']
            status = request.form['status']
            priority = request.form['priority']
            deadline = request.form['deadline']

            db_connection = db.get_db()
            cur = db_connection.cursor()

            cur.execute(
                '''INSERT INTO tasks_table (task_title, status, priority, deadline) VALUES (?, ?, ?, ?)''',
                (title, status, priority, deadline)
            )
            db_connection.commit()  # This line commits the transaction
            return redirect(url_for('index'))
        else:
            return render_template('new_task.html')
        
    @app.route('/tasks/update', methods=['GET', 'POST'])
    def update_task():
        if request.form.get("_method") == 'PUT':
            id = request.form['id']

            db_connection = db.get_db()
            cur = db_connection.cursor()

            cur = db.get_db().cursor()
            sql = '''SELECT * from TASKS_TABLE WHERE id = ?'''
            cur.execute(sql, (id,))
            task = cur.fetchone()

            if task is not None:
                title = request.form['task_title']
                status = request.form['status']
                priority = request.form['priority']
                deadline = request.form['deadline']

                cur.execute(
                    '''UPDATE tasks_table SET task_title = ?, status = ?, priority = ?, deadline = ? WHERE id = ?''',
                    (title, status, priority, deadline, id)
                )
                db_connection.commit()
                return redirect(url_for('index'))
            else:
                return render_template('failure.html')
        else:
            return render_template('new_task.html')


    @app.route('/tasks/delete', methods=['GET', 'POST'])
    def delete_task():
        if request.form.get("_method") == 'DELETE':
            id = request.form['id']

            db_connection = db.get_db()
            cur = db_connection.cursor()

            sql = '''SELECT * from TASKS_TABLE WHERE id = ?'''
            cur.execute(sql, (id,))
            task = cur.fetchone()

            if task is not None:

                cur.execute(
                    '''DELETE FROM tasks_table WHERE id = ?''',
                    (id,)
                )
                db_connection.commit()
                return redirect(url_for('index'))
            else:
                return render_template('failure.html')
        else:
            return render_template('new_task.html')

    return app