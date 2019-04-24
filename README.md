# Backend for weird-brains web-site on aiohttp web-server

### Website
url

### About project:
Aim of the project is to show how i write code and to demonstrate some of my skills

### Start:
| Command                           | Description                        |
| --------------------------------- | :--------------------------------- |
| docker-compose up -d              | Run server as daemon               | 
| docker-compose up                 | Run server                         | 
| docker-compose down               | Stop server                        | 
| docker rm -vf $(docker ps -aq)    | Stop containers and remove volumes | 
  
### Start locally:
  python3 -m pip install -r requirements.txt 
  python3 src/tasks.py --config etc/config/development.yml server

### Features and technologies:
* asynchronius python web-server on aoihttp library (which is using asyncio)
* postgresql database (in docker container)
* sqlachemy orm with aiopg connector
* nginx proxies /api requests to backend server, returns static content (react application and it's resources and images)
* api tests on pytest library
* front-end is added by submodule
* travis auto deploy on push to master branch

### Front-end
Frontend functionality was implemented by my colleague here: https://github.com/EkaterinaSukhanova/weird_brains_frontend

