from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

from cojo_app import application

if __name__ == "__main__":
    application.run()