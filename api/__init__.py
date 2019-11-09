from api import config
import api.Tables


Session = config.Session

config.Base.metadata.create_all(config.engine)

print(">> configuration de la base de donnees terminee")