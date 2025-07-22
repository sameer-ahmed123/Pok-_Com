from django.db import models


class Product(models.Model):
    """
    Represents a digital Pokémon image product available for purchase.
    Images are linked via URL from an external API (PokéAPI).
    Includes additional Pokémon data for richer product information.
    """
    pokemon_id = models.IntegerField(
        unique=True, help_text="The official Pokémon ID from PokéAPI.")
    name = models.CharField(max_length=100, unique=True,
                            help_text="The name of the Pokémon.")

    image_url = models.URLField(
        max_length=500,
        help_text="URL to the Pokémon's primary digital image (e.g., official artwork from PokéAPI)."
    )

    sprite_front_default_url = models.URLField(max_length=500, blank=True, null=True,
                                               help_text="URL to the default front sprite.")
    sprite_back_default_url = models.URLField(max_length=500, blank=True, null=True,
                                              help_text="URL to the default back sprite.")
    sprite_front_shiny_url = models.URLField(max_length=500, blank=True, null=True,
                                             help_text="URL to the shiny front sprite.")
    sprite_back_shiny_url = models.URLField(max_length=500, blank=True, null=True,
                                            help_text="URL to the shiny back sprite.")

    description = models.TextField(
        blank=True,
        help_text="A brief description or Pokedex entry for the Pokémon."
    )
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        help_text="The price of the digital image."
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Whether the product is currently available for sale."
    )

    types = models.JSONField(
        default=list, help_text="List of Pokémon types (e.g., ['fire', 'water']).")
    stats = models.JSONField(
        default=dict, help_text="Dictionary of base stats (e.g., {'hp': 45, 'attack': 49}).")
    abilities = models.JSONField(
        default=list, help_text="List of Pokémon abilities.")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['pokemon_id']
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return f"{self.name} (ID: {self.pokemon_id})"
