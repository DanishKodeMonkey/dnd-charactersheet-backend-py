# A backend rest API using Python and Prisma-py

An effort to see how well Prisma holds up in a python rest API using flask.

I tried to maintain best practising, leveraging flask blueprints to keep route definitions modular, and maintaining seperations of concerns of the different moving parts. 

Furthermore, seperating database logic from API logic. 

Lastly, I use docker to compartemenentalise the different services and run them in isolation for testing.

The process starts in `main.py` where the app is created by callign `create_app()` from `app/__init__.py`

`create_app()` in turn creates the Flask app, and calls the `register_blueprint(app)` function from `app/routes/__init__.py` to register all blueprints from the any routes created, allowing easy scaling of the project API routes as needed. Furthermore, it sets up database connections using Prisma.

Finally the Flask app starts listening on localhost:5000
