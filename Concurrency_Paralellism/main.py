import concurrent.futures
import multiprocessing
import time
import os 
import requests

from http.client import responses

"""
    SET the numbers of pokemon you want to download images from POKE API
    NUMBER_POKEMONS
"""
NUMBER_POKEMONS = 20
LIST_NUMBER_POKE = list( range(1, NUMBER_POKEMONS+1)) # list beetwen 1 to NUMBER_POKEMONS
NUMBER_CPU = multiprocessing.cpu_count() # Number of cpu avaliable in this machine
POKE_API = "https://pokeapi.co/api/v2/pokemon/%s"
# Define the application directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))  
IMAGE_DIR = os.path.join(BASE_DIR, 'images')

def request_get(number_pokemon):
    """
        Do simple request (Concurrency)
    """
    url = POKE_API % number_pokemon # example "https://pokeapi.co/api/v2/pokemon/1"
    return requests.get(url)

def getPokemons():
    """
        Concurrency
        MultiThreading with IO Task (Request API)
    """
    with concurrent.futures.ThreadPoolExecutor() as executor:
        responses = [ executor.submit(request_get, number_pokemon) for number_pokemon in LIST_NUMBER_POKE ]
        concurrent.futures.wait(responses) # wait to finish the 50 request
        responses = [ response.result().json() for response in responses] # list of dictionary with  respones
        return responses

def download_image( url, name_pokemon ):
    """
        Concurrency
        download_image 
    """
    response = requests.get(url)
    bytes_image = response.content # reponse is Image PNG
    return ( name_pokemon, bytes_image ) # return tuple with name pokemon and bytes image

def getImages( list_url_images ):
    """
        Concurrency
        MultiThreading with IO Task (Request API)
    """
    with concurrent.futures.ThreadPoolExecutor() as executor:
        responses = [ executor.submit(download_image, image_url, name_pokemon) for name_pokemon, image_url in list_url_images.items() ]
        concurrent.futures.wait(responses) # wait to finish the 5 request
        responses = [ response.result() for response in responses] # list of dictionary with respones
        return responses

def task_save_image( data ):
    """
        CPU TASK ( Paralellism )
        Save binary into file in folder images
        (this task is CPU BOUND)
    """
    # save image in folder
    name_pokemon, bytes_image = data
    path_image = os.path.join(IMAGE_DIR, f'{name_pokemon}.png')

    with open(path_image, 'wb') as f: # Save image in static files 
        f.write(bytes_image)

    if os.path.exists( path_image ): return path_image
    else: return False

def save_images( responses_binary ):
    """
        CPU TASK ( Paralellism )
    """
    pool = multiprocessing.Pool(NUMBER_CPU)
    pool.map( task_save_image, responses_binary)

if __name__ == "__main__":
    start_time = time.time()

    print(f"Total pokemons {len(LIST_NUMBER_POKE)}")

    # get pokemons json
    responses_json = getPokemons()
    duration = time.time() - start_time
    print(f"Downloaded json info from POKEAPI in {duration} seconds")

    # get image binary
    list_url_images = { pokemon.get('name') : pokemon['sprites']['back_default'] for pokemon in responses_json } # create dictionary with name and image url
    responses_binary = getImages( list_url_images )
    print(f"Downloaded images in {duration} seconds")

    save_images( responses_binary )
    print(f"Saved images in {duration} seconds")

    print(f"watch images in {IMAGE_DIR} ")
