from app import create_app

# This is the entry point for running the application
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)