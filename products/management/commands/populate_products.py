# Save this file as: backend/products/management/commands/populate_products.py
# Create the directories: backend/products/management/commands/ if they don't exist.

import json
import os
from django.core.management.base import BaseCommand, CommandError
from products.models import Product # Import your Product model
import random # For assigning random prices

class Command(BaseCommand):
    help = 'Populates the Product model with Pokémon data from a JSON file.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            default='pokemon_raw_data.json', # Default to the file created by fetch_pokemon_data.py
            help='Path to the JSON file containing Pokémon data.',
        )
        parser.add_argument(
            '--default_price',
            type=float,
            default=5.99,
            help='Default price to assign to each digital Pokémon image.',
        )
        parser.add_argument(
            '--min_price',
            type=float,
            default=4.00,
            help='Minimum random price to assign to each digital Pokémon image (if random pricing is enabled).',
        )
        parser.add_argument(
            '--max_price',
            type=float,
            default=15.00,
            help='Maximum random price to assign to each digital Pokémon image (if random pricing is enabled).',
        )
        parser.add_argument(
            '--random_price',
            action='store_true',
            help='Assign a random price between min_price and max_price instead of a default price.',
        )


    def handle(self, *args, **options):
        file_path = options['file']
        default_price = options['default_price']
        min_price = options['min_price']
        max_price = options['max_price']
        random_price_enabled = options['random_price']

        if not os.path.exists(file_path):
            raise CommandError(f'File "{file_path}" does not exist.')

        self.stdout.write(f"Loading data from {file_path}...")
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                pokemon_data_list = json.load(f)
        except json.JSONDecodeError:
            raise CommandError(f'Could not decode JSON from "{file_path}".')

        self.stdout.write(f"Found {len(pokemon_data_list)} Pokémon entries.")

        created_count = 0
        updated_count = 0

        for entry in pokemon_data_list:
            pokemon_id = entry.get('pokemon_id')
            name = entry.get('name')
            image_url = entry.get('image_url')
            description = entry.get('description', '')
            types = entry.get('types', [])
            stats = entry.get('stats', {})
            abilities = entry.get('abilities', [])

            if not all([pokemon_id, name, image_url]):
                self.stderr.write(self.style.WARNING(
                    f"Skipping entry due to missing required data: {entry.get('name', 'N/A')} (ID: {entry.get('pokemon_id', 'N/A')})"
                ))
                continue

            # Determine price
            if random_price_enabled:
                price = round(random.uniform(min_price, max_price), 2)
            else:
                price = default_price

            try:
                product, created = Product.objects.update_or_create(
                    pokemon_id=pokemon_id, # Use pokemon_id as the unique identifier for update_or_create
                    defaults={
                        'name': name,
                        'image_url': image_url,
                        'sprite_front_default_url': entry.get('sprite_front_default_url'),
                        'sprite_back_default_url': entry.get('sprite_back_default_url'),
                        'sprite_front_shiny_url': entry.get('sprite_front_shiny_url'),
                        'sprite_back_shiny_url': entry.get('sprite_back_shiny_url'),
                        'description': description,
                        'price': price,
                        'is_active': True,
                        'types': types,
                        'stats': stats,
                        'abilities': abilities,
                    }
                )
                if created:
                    created_count += 1
                    self.stdout.write(self.style.SUCCESS(f'Created product: {product.name}'))
                else:
                    updated_count += 1
                    self.stdout.write(self.style.SUCCESS(f'Updated product: {product.name}'))

            except Exception as e:
                self.stderr.write(self.style.ERROR(f'Error processing {name} (ID: {pokemon_id}): {e}'))

        self.stdout.write(self.style.SUCCESS(
            f'\nDatabase population complete. Created {created_count} products, updated {updated_count} products.'
        ))

