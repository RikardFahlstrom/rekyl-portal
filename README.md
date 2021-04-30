# UFTAB rekyl portal 

rekyl_portal is a tool that allows users to download all errands in a web portal into a MySQL database.  


## How to run

`docker compose up --abort-on-container-exit --build scraper`  

Run with `--abort-on-container-exit` to close all containers if one container exits, used to 
close selenium container when the scraper exits.  
Use `--build scraper` to rebuild scraper with latest changes.  

