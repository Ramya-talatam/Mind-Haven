from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import re
# from textblob.classifiers import NaiveBayesClassifier as nb
import string
from textblob import TextBlob
def custom_tokenize(text):
    words = [word.strip(string.punctuation) for word in text.split() if word.strip(string.punctuation).isalnum()]
    return words

# Initialize sentiment analysis
def fun(journal_entry):
    journal_entries = journal_entry.split(".")
    positive_words = []
    negative_words = []
    focused_words=[]
    for entry in journal_entries:
        analysis = TextBlob(entry)

        for word in custom_tokenize(entry):
            word_polarity = TextBlob(word).sentiment.polarity

            if analysis.sentiment.polarity >= 0.05 and word_polarity > 0:
                positive_words.append([word, word_polarity])
            elif analysis.sentiment.polarity <= -0.05 and word_polarity < 0:
                negative_words.append([word, word_polarity])

        # focused_words+=(analysis.words[:5])  # Get the first 5 words
        for word, pos_tag in analysis.tags:
            word_polarity = TextBlob(word).sentiment.polarity
            if pos_tag.startswith(('NN')):
                focused_words.append([word, word_polarity])
        # focused_words=[i for i,j in sorted(focused_words, key= lambda x:abs(x[1]),reverse=True)][:10]
        # focused_words=[word for word, _ in sorted(focused_words, key=lambda x: x[1], reverse=True)][:10]
    fcw=[i for i,j in sorted(focused_words, key= lambda x:abs(x[1]),reverse=True)][:10]
    # print(fcw)
        

    return [positive_words, negative_words, fcw, TextBlob(journal_entry).sentiment.polarity]

train_data = [
    ("yes","yes"),
    ("no","no"),
    ("yup","yes"),
    ("nope","no"),
    ("yes, tell me more", "yes"),
    ("not needed.", "no"),
    ("no thanks","no"),
    ("yes, please.", "yes"),
    ("no way!", "no")
]

# classifier = nb(train_data)

message=""
q=""
intents = {
    'hi' : ['hello','hey','hi!','hi'],
    'bye' : ['goodbye','buhbye','bye'],
    'depression' : ['depressed','sad','worried','despair','misery','bad'],
    'anxiety' : ['anxiety','anxious','nervous','stress','strain','tension','discomfort','tensed'],
    'paranoia' :['disbelieve', 'distrustful', 'doubting', 'incredulous','mistrustful', 'negativistic','questioning','show-me','skeptical','suspecting','suspicious','unbelieving'],
    'sleeping_disorder' :['restlessness','indisposition','sleeplessness','stress','tension','vigil','vigilance','wakefulness'],
    'substance_abuse' :['alcohol abuse','drug abuse','drug use','addiction','alcoholic addiction','alcoholism','chemical abuse','dipsomania','drug dependence','drug habit','narcotics abuse','solvent abuse'],
    'personality_disorder':['insanity','mental disorder','schizophrenia','craziness','delusions','depression','derangement','disturbed mind','emotional disorder','emotional instability',
                            'loss of mind','lunacy','madness','maladjustment','mania','mental disease','mental sickness','nervous breakdown','nervous disorder',
                            'neurosis','neurotic disorder','paranoia','phobia','psychopathy','psychosis','sick mind','troubled mind','unbalanced mind','unsoundness of mind'],
    'happy':['good','great','relieved','happy','okay']
}

responses = {
    'hi' : 'Hello, i am a medical healthcare chatbot!',
    'bye' : 'Thank you for your time!'
}

dictionary = {
    'a':0,
    'b' : 0,
    'c' : 0,
    'd' : 0
}

s = {
    'a':0,
    'b' : 1,
    'c' : 2,
    'd' : 3
}

question = ["Do you have little interest or pleasure in doing things?","Feeling down, depressed, or hopeless","Trouble falling or staying asleep, or sleeping too much","Feeling tired or having little energy","Feeling bad about yourself - or that you are a failure or have let yourself or your family down"]

negative = 0
positive = 0

def intent(message):
    for words in intents.keys():
        pattern = re.compile('|'.join([syn for syn in intents[words]]))
        match = pattern.search(message)
        if match:
            return words
    return 'default'

def respond(message):
    word = intent(message)
    return responses[word]


def score():
    sc = 0
    for k in dictionary.keys():
        sc += dictionary[k]*s[k]
    return sc


def predict_(x):
    # tfidf = vectorizer.transform([x])
    # preds = model.predict(tfidf)
    #probab = model.predict_proba(tfidf)[0][preds]
    probab=TextBlob(x).sentiment.polarity
    #print(preds,probab)
    feeling(probab)
    return probab

def feeling(polar):
    global negative,positive,q
    q=""
    if polar >= 0.05:
        positive +=1
        q=("That's great to hear!")
    elif polar <= -0.05:
        negative +=1
        q=("Oh, sorry to hear that!")
    else:    
        q=("Okay, thanks for sharing.")

def classification(pred):
    if pred>=0.05:
        return 1
    else:
        return 0


# app = Flask(__name__)
name=""
questions = ["hi",
"Hi! I'm a medical healthcare chatbot! Before we proceed, may I know your first name?",
"That's a nice name! Before we get started, I want to know about your current mood.",
"I'm a CBT coach that can consult with you during difficult times, and also not-so-difficult times. Do you wanna know a little more?",
"Mood tracking and thinking hygiene - among other useful concepts - are skills you'll learn as you practice CBT. Skills that can help you make positive changes to your thoughts, feelings and behaviour. Can you walk me through how did your last week go?",
"Can you walk me through how did your last week go?",
"I know that question can be tough and sometime painful to answer so I really appreciate you doing it... Can you tell me a bit about what's going on in your life that has brought you here today?",
"Can you tell me a bit about what's going on in your life that has brought you here today?",
"That's okay! I've listened everything you said",
"I have got great tools for people dealing with stress,wanna give it a go,Yes/No?",
"Great! Thanks for trusting me. Let's start with a small mental assessment test,so buckle up!",
"Please ask me for help whenever you feel like it! I'm always online.",
"Now we're starting with a small assessment and hopefully at the end of the assessment,we'll be able to evaluate your mental health",
"To respond please type the following answer depending upon your choice",
"A. not at all, B. several days, C. more than half a day, D. all the days. Now we'll be starting with the quiz,type okay if you're ready!",
"Do you have little interest or pleasure in doing things?",
"Feeling down, depressed, or hopeless",
"Trouble falling or staying asleep, or sleeping too much",
"Feeling tired or having little energy",
"Feeling bad about yourself - or that you are a failure or have let yourself or your family down",
"Thank you for taking the assessment!",
"Please make sure that you keep checking in with me. What's your mood now after opening up?",
"Please ask me for help whenever you feel like it! I'm always online.",
"Gosh, that is tough... I am sorry to hear that. Here is a thought that might motivate you! There you go...let it all slide out.Unhappiness cannot stick in a person's soul when it's slick with tear.",
"Gosh, that is tough... I am sorry to hear that. Here is a thought that might motivate you! Take a deep breath, listen to your thoughts, try to figure them out. Then take things one day at a time.",
"Gosh, that is tough... I am sorry to hear that. Here is a thought that might motivate you! If you want someone, you have to be willing to wait for them and trust that what you have is real and strong enough for them to wait for you. If somebody jumps ship for you, that fact will always haunt you because you'll know they're light on their feet. Spare yourself the paranoia and the pain and walk away until the coast is clear.",
"Gosh, that is tough... I am sorry to hear that. Here is a thought that might motivate you! Overhead, the glass envelope of the Insomnia Balloon is malfunctioning. It blinks on and off at arrhythmic intervals, making the world go gray:black, gray:black. In the distance, a knot of twisted trees flashes like cerebral circuitry.",
"Gosh, that is tough... I am sorry to hear that. Here is a thought that might motivate you! ...repeated trauma in childhood forms and deforms the personality. The child trapped in an abusive environment is faced with formidable tasks of adaptation. She must find a way to preserve a sense of trust in people who are untrustworthy, safety in a situation that is unsafe, control in a situation that is terrifyingly unpredictable, power in a situation of helplessness. Unable to care for or protect herself, she must compensate for the failures of adult care and protection with the only means at her disposal, an immature system of psychological defenses.",
"Gosh, that is tough... I am sorry to hear that. Here is a thought that might motivate you! My Recovery Must Come First So That Everything I Love In Life Doesn't Have To Come Last.",
"We're really sorry to know that and for further assistance we would try to connect you with our local assistance who is available 24/7. Here are the details -- Contact Jeevan Suicide Prevention Hotline. Address:171, Ambiga Street Golden George Nagar, Nerkundram, Chennai, Tamil Nadu 600107. Number : 044 2656 4444"
]
ans=[]
# current_question = 1

# @app.route('/')
# def index():
#     return render_template('botindex.html')


def getquestion(current_question):
    # global current_question
    if current_question < len(questions):
        question = q+" "+questions[current_question]
        return jsonify({'question': question})
    else:
        return jsonify({'question': 'stop'})

def recordanswer(answer,current_question):
    global name, ans, negative, positive,q, dictionary
    q=""
    answer = request.form.get('answer')
    answer= answer.lower()
    if answer=='restart':
        current_question=0
    print("prev ", current_question)
    if current_question==1:
        name=answer
    elif current_question==2:
        sentiment = predict_(answer)
    elif current_question==3 :
        sentiment=predict_(answer)
        # yorn= classifier.classify(answer)
        # print(yorn ,answer)
        if "no" in answer or ("not" in answer):
            current_question+=1
    elif current_question in [4,5]:
        sentiment=predict_(answer)
        pos=classification(sentiment)
        if pos==1:
            current_question=6
        else:
            current_question=5
    elif current_question in [6,7]:
        sentiment = predict_(message)
        if negative != 0:
            current_question+=1
    elif current_question== 9:
        # if answer.lower()=='yes':
        if "no" in answer or ("not" in answer):
            current_question=10
        else:
            current_question=9
    elif current_question == 10:
        current_question+=1
    elif current_question ==11:
        current_question = 29
    elif current_question == 14:
        l=['yes','yeah','ok','okay']
        flag=0
        for i in l:
            if i in answer.lower():
                flag=1
        if flag==0:
            current_question=0
    elif current_question in [15,16,17,18,19]:
        dictionary[answer]+=1
    elif current_question==21:
        sc=score()
        print(sc)
        if sc>=0 and sc<=18:
            m_intent=intent(answer)
            l=['happy','depression','anxiety','sleeping disorder','paranoia','personality_disorder','substance_abuse']
            if m_intent in l:
                current_question+= l.index(m_intent)
            else:
                current_question=28
        else:
            current_question=28
        
    elif current_question >=22:
        current_question=29
    current_question+=1
    print("now ", current_question )
    return jsonify({'status': 'success','qno':current_question})

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'bluehawkhunting'

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://default:1hQ6btoOVMcT@ep-wandering-snow-82640766.ap-southeast-1.postgres.vercel-storage.com:5432/verceldb"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    sleep_data = db.relationship('SleepData', backref='user', lazy=True)
    affirmations = db.relationship('Affirmations', backref='user', lazy=True)
    goals = db.relationship('Goals', backref='user', lazy=True)

class SleepData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    hours = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Affirmations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Goals(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

def get_past_days_data(username, days):
    today = datetime.utcnow().date()
    start_date = today - timedelta(7)
    print(start_date)
    data = SleepData.query.filter_by(user_id=username).all()
    print(data)

    return data

def insert_sleep_data(username, date, hours):
    existing_entry = SleepData.query.filter_by(user_id=username, date=date).first()

    if existing_entry:
        # If an entry exists, update the hours
        existing_entry.hours = hours
    else:
        # If no entry exists, insert a new one
        new_entry = SleepData(user_id=username, date=date, hours=hours)
        db.session.add(new_entry)

    db.session.commit()
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.', 'danger')
        else:
            hashed_password = generate_password_hash(password, method='sha256')
            new_user = User(username=username, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful. You can now log in.', 'success')
            return redirect(url_for('login'))

    return render_template('register.html')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            # Successful login
            session['logged_in'] = True
            session['user_id'] = user.id  # Store user ID in the session for future use
            return redirect(url_for('chatbot'))
        else:
            session['message'] = 'Login failed. Please check your username and password.'
    message = session.pop('message', None)
    return render_template('login.html', message=message)

@app.route('/chatbot')
def chatbot():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('chatindex.html')
@app.route('/record_answer', methods=['POST'])
def record_answer():
    answer = request.form.get('answer')
    qno= request.form.get('qno')
    return recordanswer(answer,int(qno))
@app.route('/get_question', methods=['POST'])
def get_question():
    qno= request.form.get('qno')
    ques= getquestion(int(qno))
    print(ques)
    return ques
@app.route('/logout')
def logout():
    session['logged_in'] = False
    return redirect(url_for('login'))
@app.route('/analyze', methods=['POST'])
def analyze():
    journal_text = request.form.get('journalText')
    positive_words, negative_words, focused_words,op= fun(journal_text)
    response = {
        'positive_words': positive_words,
        'negative_words': negative_words,
        'focused_words': focused_words,
        'overall_polarity': op
    }
    return jsonify(response)

@app.route('/sleep_hours', methods=['GET', 'POST'])
def sleep_hours():
    if request.method == 'POST':
        username = session['user_id'] 
        sleep_hours = int(request.json.get('hours'))
        current_date = datetime.utcnow().date()

        # Insert sleep data into the database
        insert_sleep_data(username, current_date, sleep_hours)

    # Retrieve and display past 7 days sleep data
    username = session['user_id']  
    past_7_days_data = get_past_days_data(username, 7)
    return render_template('sleep_tracker.html', past_7_days_data=past_7_days_data)

@app.route("/goals")
def goals():
    return render_template("goal_setting.html")
@app.route('/guided_med')
def guided_med():
    return render_template("guided_meditation.html")
@app.route('/affirmations')
def affirmations():
    return render_template("daily_affirmations.html")
if __name__ == '__main__':
    # Create the database tables
    with app.app_context():
        db.create_all()
    # app.run()


