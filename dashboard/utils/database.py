from sqlalchemy import create_engine

def get_engine():
    return create_engine("postgresql://postgres:YOUR_PASSWORD@localhost:5432/hhkg_jobs")