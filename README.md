# UFTAB rekyl portal 

rekyl_portal is a tool that allows users to download all errands in a web portal into a MySQL database.  


## How to run

`docker compose up --abort-on-container-exit --build scraper`  

Run with `--abort-on-container-exit` to close all containers if one container exits, used to 
close selenium container when the scraper exits.  
Use `--build scraper` to rebuild scraper with latest changes.  

## Run a specific .py-file for development
- Start the `selenium/standalone-chrome` container by running 
`docker run -d -p 4444:4444 --name chrome selenium/standalone-chrome`
  
- Make sure that the browser object created in `setup_browser()` is pointed to `"http://0.0.0.0:4444/wd/hub"`  
- Install all packages in `requirements.txt`  
- Run the .py-file
  