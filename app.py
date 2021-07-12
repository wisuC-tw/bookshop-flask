from project import create_app

# Call the application factory function to construct a Flask application
# instance using the development configuration
app = create_app()

@app.route('/')
def index():
    return 'Index Page'

@app.route('/hello')
def hello():
    return 'Hello, World'

if __name__=='__main__':
    app.run(host = '0.0.0.0', debug = True)