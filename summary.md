# Content Publishing System

This application scraps XML's sources for items containing links to news articles. The news articles are then fetched and  processed to extract images, titles, text and other metadata. The extracted text is then summarized to extract the essence. 

The raw information in then put together in a fixed json schema and sent over HTTP on the specified API endpoint. The application repeats the whole process once again after every *X* minutes provided as parameters.

## Key Points
- The parameters to the application can be configured inside `constants.py`. 
- New XML can be added, API endpoint can be modified and the wait time to rerun can be modified there. 
- Instructions to run this application can be found inside `README.md`.



