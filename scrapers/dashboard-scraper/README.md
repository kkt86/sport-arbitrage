# README file for dashboard-scraper

In this project, we write a docker application, which reads information 
from the following page: http://184.73.28.182/

#### Build docker image
`docker build -t kosta/flask-selenium .`

#### Start image with containerized flask application
`docker run --name dashboard-scraper -d -p 5001:5001 kosta/flask-selenium`

games information can be found in `localhost:5001`

 
 