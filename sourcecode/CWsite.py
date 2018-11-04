from flask import Flask, render_template, redirect, request, url_for
app = Flask(__name__)
app. secret_key = 'supersecret'

@app.route('/')
def home():
   return render_template ('home.html ')

@app . route ('/ login /')
@app . route ('/ login /< message >')
def login ( message = None ):
   if ( message != None ):
      flash ( message )
   else :
      flash (u'A default message ')
   return redirect ( url_for ('home '))

if __name__ == "__main__":
   app.run(host='0.0.0.0', debug=True)
