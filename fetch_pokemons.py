# Save this file as: fetch_pokemon_data.py
# You can run this script independently from your Django project.

import requests
import json
import os

# Base URL for the PokéAPI
POKEAPI_BASE_URL = "https://pokeapi.co/api/v2/pokemon/"
POKEAPI_SPECIES_URL = "https://pokeapi.co/api/v2/pokemon-species/"

# Number of Pokémon to fetch
NUM_POKEMON_TO_FETCH = 400

# Output file name
OUTPUT_JSON_FILE = "pokemon_raw_data.json"

def get_pokemon_data(pokemon_id):
    """Fetches data for a single Pokémon by ID."""
    pokemon_url = f"{POKEAPI_BASE_URL}{pokemon_id}/"
    species_url = f"{POKEAPI_SPECIES_URL}{pokemon_id}/"
    pokemon_data = {}

    try:
        # Fetch main Pokémon data
        response_pokemon = requests.get(pokemon_url)
        response_pokemon.raise_for_status() # Raise an exception for HTTP errors
        data = response_pokemon.json()

        # Fetch species data for descriptions
        response_species = requests.get(species_url)
        response_species.raise_for_status()
        species_data = response_species.json()

        # Extract relevant data
        pokemon_data['pokemon_id'] = data['id']
        pokemon_data['name'] = data['name'].capitalize()

        # Extract image URLs (official artwork and various sprites)
        pokemon_data['image_url'] = data['sprites']['other'].get('official-artwork', {}).get('front_default')
        # Fallback to a default sprite if official artwork is missing
        if not pokemon_data['image_url']:
            pokemon_data['image_url'] = data['sprites'].get('front_default')

        pokemon_data['sprite_front_default_url'] = data['sprites'].get('front_default')
        pokemon_data['sprite_back_default_url'] = data['sprites'].get('back_default')
        pokemon_data['sprite_front_shiny_url'] = data['sprites'].get('front_shiny')
        pokemon_data['sprite_back_shiny_url'] = data['sprites'].get('back_shiny')

        # Extract description (flavor text) in English
        flavor_text_entries = species_data.get('flavor_text_entries', [])
        description = next(
            (entry['flavor_text'].replace('\n', ' ').replace('\x0c', ' ')
             for entry in flavor_text_entries if entry['language']['name'] == 'en'),
            "No description available."
        )
        pokemon_data['description'] = description

        # Extract types
        pokemon_data['types'] = [t['type']['name'] for t in data['types']]

        # Extract stats
        pokemon_data['stats'] = {s['stat']['name']: s['base_stat'] for s in data['stats']}

        # Extract abilities
        pokemon_data['abilities'] = [a['ability']['name'] for a in data['abilities']]

        print(f"Fetched data for {pokemon_data['name']} (ID: {pokemon_data['pokemon_id']})")
        return pokemon_data

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for Pokémon ID {pokemon_id}: {e}")
        return None
    except KeyError as e:
        print(f"Missing key in data for Pokémon ID {pokemon_id}: {e}")
        return None

def main():
    all_pokemon_data = []
    print(f"Starting to fetch data for {NUM_POKEMON_TO_FETCH} Pokémon...")

    for i in range(1, NUM_POKEMON_TO_FETCH + 1):
        data = get_pokemon_data(i)
        if data:
            all_pokemon_data.append(data)

    # Save data to JSON file
    with open(OUTPUT_JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(all_pokemon_data, f, indent=4, ensure_ascii=False)

    print(f"\nSuccessfully fetched data for {len(all_pokemon_data)} Pokémon.")
    print(f"Data saved to {OUTPUT_JSON_FILE}")

if __name__ == "__main__":
    main()

