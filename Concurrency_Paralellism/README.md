# Download Info from PokeAPI

Script that do multiple request from POKEAPI and save image in local folder

- Set global variable NUMBER_POKEMONS that you want to download
- Get JSON response from POKEAPI with Threading ( IO TASK ) ( CONCURRENCY )
- Iterate over json reponse and get name of pokemon and url image from web
- Get Binary response from request from image url ( IO TASK ) ( CONCURRENCY)
- Save image in local folder ( images ) ( CPU TASK ) ( Paralellism )

## Installation

You need to create .env file inside env folder and set the enviroment variables MAPBOX_TOKEN and SECRET_KEY:

```env
pip install requests
```
