from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

#Endereço do arquivo do banco de dados
DATABASE_URL = "sqlite:///./library.db"

#Motor de conexão com o SQlite
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

#Fábrica de sessões, assim cada requisição abre e fecha su própria sessão
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Classe base que todas as tabelas vão herdar para se tornarem parte do banco
Base = declarative_base()


def get_db():
    #Abre a sessão com o banco, entrega para a requisição usar e garante que ela seja fechada ao final — mesmo que ocorra um erro
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
