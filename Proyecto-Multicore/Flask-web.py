from flask import Flask, render_template
#This file is used to create the web page that will have the content of the prices,scores,playtime,titles
app = Flask(__name__)


@app.route('/')

def home():
    with open('Proyecto-Multicore\\templates\game_data.txt','r',encoding="utf-8") as file:     #It opens the file with all the information received by the generate info function in main.py or parallel-main.py
        l_games = file.readlines()
        l = len(l_games)

        return render_template('home.html',data=l_games, len=l)         #It returns the information that is content in home.html 
                                                                        #and also 2 variables to make a native for loop of python in the html file

if __name__ == '__main__':
    app.run(debug=True)
