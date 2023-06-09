from flask import Flask, redirect, url_for, session, request, jsonify, render_template, flash, Markup
from flask_apscheduler import APScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from flask_oauthlib.client import OAuth
from bson.objectid import ObjectId

import pprint
import os
import time
import pymongo
import sys
 
app = Flask(__name__)

#initialize scheduler with your preferred timezone
scheduler = BackgroundScheduler({'apscheduler.timezone': 'America/Los_Angeles'})
scheduler.start()
 
app.secret_key = os.environ['SECRET_KEY'] #used to sign session cookies
oauth = OAuth(app)
oauth.init_app(app) #initialize the app to be able to make requests for user information

#Set up GitHub as OAuth provider
github = oauth.remote_app(
    'github',
    consumer_key=os.environ['GITHUB_CLIENT_ID'], #your web app's "username" for github's OAuth
    consumer_secret=os.environ['GITHUB_CLIENT_SECRET'],#your web app's "password" for github's OAuth
    request_token_params={'scope': 'user:email'}, #request read-only access to the user's email.  For a list of possible scopes, see developer.github.com/apps/building-oauth-apps/scopes-for-oauth-apps
    base_url='https://api.github.com/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://github.com/login/oauth/access_token',  
    authorize_url='https://github.com/login/oauth/authorize' #URL for github's OAuth login
)

#Connect to database
url = os.environ["MONGO_CONNECTION_STRING"]
client = pymongo.MongoClient(url)
db = client[os.environ["MONGO_DBNAME"]]
collection = db['Cart'] 
db2 = client[os.environ["MONGO_DBNAME2"]]
collection2 = db2['item']#TODO: put the name of the collection here




print("connected to db")

#context processors run before templates are rendered and add variable(s) to the template's context
#context processors must return a dictionary 
#this context processor adds the variable logged_in to the conext for all templates
@app.context_processor
def inject_logged_in():
    if 'user_data' in session:
        cart=collection.find_one({'User': session['user_data']['id']})
        return {"logged_in":('github_token' in session), "item": (str(len(cart['Item-Name'])))}
    else:
        return {"logged_in":('github_token' in session)}

@app.route('/')
def home():
    return render_template('home.html')
    
@app.route('/info1', methods=['POST'])
def info1():
    #Need to check how many and if greater than 0
    return render_template('info1.html')
    
@app.route('/info2', methods=['POST'])
def info2():
    #Need to check how many and if greater than 0
    return render_template('info2.html')
    
@app.route('/about')
def about():
    return render_template('about.html')
    
@app.route('/Fusion')
def Fusion():
    if collection.find_one({'User': session['user_data']["id"]})['AF'] == True:
        return render_template('alreadyFusion.html')
    return render_template('Fusion.html')
    
@app.route('/fusiondone', methods=['POST'])
def fusiondone():
    cpage = ''
    collection.update_one({'User': session['user_data']['id']}, {'$set':{"AF":True}})
    if 'current page' in session:
        cpage = session['current page']
    return render_template('fusiondone.html', page=cpage)
    
@app.route('/alreadyFusion', methods=['POST'])
def alreadyFusion():
    return render_template('alreadyFusion.html')

@app.route('/whyCancel', methods=['POST'])
def whyCancel():
    return render_template('whyCancel.html')

@app.route('/fusionCancel', methods=['POST'])
def fusionCancel():
    collection.update_one({'User': session['user_data']['id']}, {'$set':{"AF":False}})
    return render_template('fusionCancel.html')
    
@app.route('/complete', methods=['POST'])
def complete():
    if collection.find_one({'User': session['user_data']["id"]})['AF'] == True:
        ship= "Order complete! Your items will arive in approximately 2 days!"
    else:
        ship="Order complete! Your items will arive in approximately 39 years."
    return render_template('complete.html', shipping = ship)

@app.route('/Cart')
def Cart():
    if collection.find_one({'User': session['user_data']["id"]})['AF'] == True:
        fus= ""
    else:
        fus=". A $5 shipping fee will be automatically added to your order. Sign up for Amazone Fusion to get free shipping!"
    return render_template('cart.html', cart=finalCart(), fus=fus)
#redirect to GitHub's OAuth page and confirm callback URL
@app.route('/login')
def login():   
    return github.authorize(callback=url_for('authorized', _external=True, _scheme='http')) #callback URL must match the pre-configured callback URL

@app.route('/logout')
def logout():
    session.clear()
    flash('You were logged out.')
    return redirect('/')

@app.route('/login/authorized')
def authorized():
    resp = github.authorized_response()
    if resp is None:
        session.clear()
        flash('Access denied: reason=' + request.args['error'] + ' error=' + request.args['error_description'] + ' full=' + pprint.pformat(request.args), 'error') 
    else:
        try:
            session['github_token'] = (resp['access_token'], '') #save the token to prove that the user logged in
            session['user_data']=github.get('user').data
            #pprint.pprint(vars(github['/email']))
            #pprint.pprint(vars(github['api/2/accounts/profile/']))
            cart = collection.find_one({'User': session['user_data']['id']})
            if cart is None:
                collection.insert_one({'User':session['user_data']['id'], 'Item-Name':[], 'AF': False})
            flash('You were successfully logged in as ' + session['user_data']['login'] + '.')
        except Exception as inst:
            session.clear()
            print(inst)
            flash('Unable to login, please try again.', 'error')
    return redirect('/')
  
@github.tokengetter
def get_github_oauth_token():
    return session['github_token']
''''
Items
'''  
@app.route('/glue', methods=["GET", "POST"])
def glue():
    session['current page']= '/glue'
    return render_template('glue.html')

@app.route('/fork', methods=["GET", "POST"])
def fork():
    session['current page']= '/fork'
    return render_template('fork.html')


@app.route('/wine', methods=["GET", "POST"])
def wine():
    session['current page']= '/wine'
    return render_template('wine.html')


@app.route('/toaster', methods=["GET", "POST"])
def toaster():
    session['current page']= '/toaster'
    return render_template('toaster.html')


@app.route('/rock', methods=["GET", "POST"])
def rock():
    session['current page']= '/rock'
    return render_template('rock.html')

@app.route('/air', methods=["GET", "POST"])
def air():
    session['current page']= '/air'
    return render_template('air.html')


@app.route('/excuse', methods=["GET", "POST"])
def excuse():
    session['current page']= '/excuse'
    return render_template('excuse.html')

@app.route('/slippers', methods=["GET", "POST"])
def slippers():
    session['current page']= '/slippers'
    return render_template('slippers.html')

@app.route('/fish', methods=["GET", "POST"])
def fish():
    session['current page']= '/fish'
    return render_template('fish.html')


@app.route('/eyes', methods=["GET", "POST"])
def eyes():
    session['current page']= '/eyes'
    return render_template('eyes.html')

@app.route('/mug')
def mug():
    session['current page']= '/mug'
    return render_template('mug.html')
    
@app.route('/clock')
def clock():
    session['current page']= '/clock'
    return render_template('clock.html')
    
@app.route('/clear')
def clear():
    session['current page']= '/clear'
    return render_template('clear.html')

'''
End of Items
'''
    
@app.route('/addtoCart', methods=["GET", "POST"])
def addtoCart():
    collection.update_one({'User': session['user_data']['id']}, {'$push':{"Item-Name":ObjectId(request.form['Cart'])}})
    cart=collection.find_one({'User': session['user_data']['id']})
    return str(len(cart['Item-Name']))
    
def finalCart(): 
    x = collection.find_one({'User': session['user_data']['id']})
    y = x['Item-Name']
    
    if len(y) == 0:
        return('Your Amazone Cart is Empty')
    else:
        finalCart=Markup('<table> <tr> <th> Item </th> <th> Price </th> </tr>')
        total=0
        ship=5
        for element in y:
            item = collection2.find_one({'_id': ObjectId(str(element))})
            finalCart= finalCart + Markup('<tr> <td>' + item['Item-Name'] + '</td>')
            finalCart= finalCart + Markup('<td>' + str(item['Price']) + '</td> </tr>')
            total= total + item['Price']
            ship = ship + item['Price']
        finalCart= finalCart + Markup('<tr><td><b>Total</b></td>')
        if x['AF'] == False:
            finalCart= finalCart + Markup('<td><b>Plus Shipping</b></td></tr>')
        else:
            finalCart= finalCart + Markup('<td></td>')
            ship = ''
        finalCart= finalCart + Markup('<tr><td>'  + str(total) + '</td>')
        finalCart= finalCart + Markup('<td>' + str(ship) + '</td></tr>')
        finalCart= finalCart + Markup('</table>')
        return finalCart
  
@app.route ('/emptyCart', methods=["GET", "POST"])
def emptyCart():
    one = ({'User': session['user_data']['id']})
    newCart = {"$set": {"Item-Name": [] } }
    collection.update_one(one, newCart)
    return redirect('/')

if __name__ == '__main__':
    app.run()
