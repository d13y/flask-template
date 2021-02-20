from flaskapp import create_app

app = create_app()

# Run app only from within module (i.e. run.py)
if __name__ == "__main__":
    app.run(debug=True)
