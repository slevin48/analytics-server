# Analytics server

A REST API to expose datasets with FastAPI
(previous version was with Flask & connexion)

This is the data manipulation performed by the server:
![analytics-server.png](analytics-server.png)

This command starts the server:
```
uvicorn fast:app --reload
```

By default it will run the fastAPI server on port 8000:
[http://localhost:8000](http://localhost:8000)

You will be prompted by the following home template:
![home-template.png](home-template.png)

You will see the automatic interactive API documentation (provided by Swagger UI):
[http://localhost:8000/docs](http://localhost:8000/docs)

![swaggerUI.png](swaggerUI.png)

## Inspiration
[https://realpython.com/flask-connexion-rest-api/#demonstration-single-page-application](https://realpython.com/flask-connexion-rest-api/#demonstration-single-page-application)
[https://medium.com/better-programming/migrate-from-flask-to-fastapi-smoothly-cc4c6c255397](Migrate From Flask to FastAPI Smoothly)
[https://fastapi.tiangolo.com/advanced/templates/](Jinja Templates for FastAPI)