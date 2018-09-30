from flask import Flask, render_template, request, redirect, url_for, flash
from flaskext.mysql import MySQL

app = Flask(__name__)

app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'contacts_python'

mysql = MySQL(app)

app.secret_key = 'mysecretkey'

@app.route('/')
def Index():
    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute('SELECT * FROM contacts')
    data = cur.fetchall()
    return render_template('index.html', contacts = data)

@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute('INSERT INTO contacts (fullname, phone, email) VALUES (%s, %s, %s)', (fullname, phone, email) )
    conn.commit() 
    flash('Contact added successfully')
    return redirect(url_for('Index'))

@app.route('/edit/<id>')
def get_contact(id):
    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute('SELECT * FROM contacts WHERE id = %s', (id))
    data = cur.fetchall()
    return render_template('edit-contact.html', contact = data[0])

@app.route('/update/<id>', methods=['POST'])
def update_contact(id):
    if request.method == 'POST':
        fullname = request.form['fullname']
        email = request.form['email']
        phone = request.form['phone']
        conn = mysql.connect()
        cur = conn.cursor()
        cur.execute(""" 
            UPDATE contacts
            SET fullname = %s,
                email = %s,
                phone = %s
            WHERE ID = %s
        """, (fullname, phone, email, id))
        conn.commit()
        flash('Contact updated successfully')

    return redirect(url_for('Index'))


@app.route('/delete/<string:id>')
def delete_contact(id):
    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute('DELETE FROM contacts WHERE id = {0}'.format(id))
    conn.commit()
    flash('Contact removed successfully')
    return redirect(url_for('Index'))
    
    
if __name__ == '__main__':
    app.run(port = 3000, debug = True)