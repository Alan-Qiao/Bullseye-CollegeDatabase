import re
from tempfile import mkdtemp
from pathlib import Path
from functions import load_obj
from flask import Flask, render_template, request, url_for, redirect, flash

# Configure application
app = Flask(__name__)

app.secret_key = 'bullseye_team'

# Templates auto-reload
app.config['TEMPLATES_AUTO_RELOAD'] = True


# Clear cache after
@app.after_request
def after_request(response):
    response.headers['Cache-Control'] = "no-cache, no-store, must-revalidate"
    response.headers['Expires'] = 0
    response.headers['Pragma'] = 'no-cache'
    return response


# Use filesystem instead of signed cookies
app.config['SESSION_FILE_DIR'] = mkdtemp()
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'

# Load Pickled Data
db = load_obj(Path('college/college_list.pickle'))
college_groups = load_obj(Path('college/college_groups.pickle'))
common_names = load_obj(Path('college/common_names.pickle'))
s_queue = ','.join(common_names.keys())


# HOMEPAGE
@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        college_list = []
        cur_select = request.form['group']
        for college in college_groups[cur_select]:
            college_list.append(db[college])
        return render_template('home.html', cur_select=cur_select, college_list=college_list)
    return render_template('home.html', cur_select='All', college_list=db.values())


# SCHOOL PAGE
@app.route('/college/<college_name>')
def college_info(college_name):
    college = db[college_name]
    return render_template('school_page.html', college=college)


# SEARCH PROCESS
@app.route('/search', methods=['POST', 'GET'])
def search():
    if request.method == 'POST':
        name = request.form['find'].replace(' ', '')
        rgx = r'<[^,]*{name}[^,]*>'.format(name=name)
        results = re.findall(rgx, s_queue, re.IGNORECASE)
        if not results:
            flash('School Not Found! Check your spelling and try again.')
            return redirect(url_for('home'))
        results = {common_names[x] for x in results}
        if len(results) == 1:
            return redirect(url_for('college_info', college_name=results.pop()))
        return render_template('search.html', results=results)
    return redirect(url_for('home'))

