import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///transactions.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False