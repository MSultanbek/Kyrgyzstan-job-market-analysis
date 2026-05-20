from sqlalchemy import create_engine

def get_engine():
    return create_engine("postgresql://postgres:g1k8tc@localhost:5432/hhkg_jobs")