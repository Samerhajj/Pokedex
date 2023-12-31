from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    pokemon_query = request.args.get('pokemon_query')

    if pokemon_query:
        # Check if the input is numeric, indicating an ID
        if pokemon_query.isnumeric():
            api_url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_query}"
        else:
            api_url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_query.lower()}"
        
        response = requests.get(api_url)

        if response.status_code == 200:
            # Parse the API response to extract relevant data
            data = response.json()
            pokemon = {
                'name': data['name'],
                'image': data['sprites']['front_default'],
                'type': ', '.join([type['type']['name'] for type in data['types']]),
                'abilities': ', '.join([ability['ability']['name'] for ability in data['abilities']]),
                'height': data['height'],
                'weight': data['weight'],
                'base_experience': data['base_experience']
            }
            return render_template('index.html', pokemon=pokemon)
    
    return render_template('index.html', no_results=True)

if __name__ == '__main__':
    app.run()
