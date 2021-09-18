# mapOverlay

## HOW TO RUN
Run `python mapOverlay.py`. This will host the server locally at `localhost:5000`.

## ENDPOINTS
1. `localhost:5000/getImage?<latitude>&<longitude>` here latitude and longitude are mandatory parameters. This endpoint retrieves the google map centered at the given coordinates. The application then prompts the user to upload an image to overlay on the map.
2. `localhost:5000/download` downloads the overlaid image on the server side.If needed the image can then further be stored in cloud and downloaded at the clients convinience. 

## TESTING
