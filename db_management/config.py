import firebase_admin
from firebase_admin import credentials
from firebase_admin import db



firekey = {
"type": "service_account",
  "project_id": "cojo-74668",
  "private_key_id": "95de1357ff4f17ba0ed076be997212c2673a5f3b",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDF4DjGXrQfzuor\nks6hS3nltnkmuMzrpOW/0I/hPOhw62OVr4UPdpH2vUQ2c27kwCO3Hw6k9ndJqVRB\nSQQcL8wBoEzrhT+ZqdkAiQJPgREkYjoqmYQZYwibS7r0MLJ9iMu35zYJS+0jVwMP\n6+1JBBWbyA+nvtApE7Ffm+TyQx1jANBLbZKFoFsLL1SYHJIdQLSdnXXTZMTaF772\nBeceOZQgtiMsbsfnNsRgx1pav1erNNFCAyyqRJ70083EJWPh9USt11zA/kRq9y8y\nshwY30oYA8+K/iFSp6KUovuAVIQTrXfsr7I5qUupudMh0TRS7UAjqYFqjtiPGd+Y\nQ4tChYXjAgMBAAECggEAHcqbYapifiN9+B97QqeFa8NkTCMonxXNjWqOLwAnktCt\nxpyNcP2ODlMCkRwiBwiyl+ByKP3+ibWXvNiMaN39XgVPb2o5YB5FUKJQGb454Xt0\nfHNugw/4/MCTHi6ywNm2qjKCXTX0NwzjpiMEL6kQw8qEKOI+nuCbJOTovFzEcOIr\nYv7EmAhpTxEuxyPfi35kB7fASIX/tcTIFYoX4Pw0gIQkxjEEsqlEF+BHSTjLhcNB\nJycofAs20Kz/dXOpuj0qH1IaKBm228pCqQCmujNcNEPchUxMQeto2TnG5GRqa9bP\nfzbsKzLpxf3DXsgrHmmb3Jo7xt+/FpyE5M2ctdvbwQKBgQD39a7geS1p9AOqbvke\nWvo8v2GzAS0z3M79hoQszOf4KBkKMw1vgMRZsnI6v99Hf0iNtUO0iDVFqL4OHdtO\n+UbNyQXoWEdkvVs6taKJfKGgW8QgUUuLhnn3+eMgKUz4wcbtG9D1eJLWjiORStth\ncQeWL1I531Rrhw0kg4fG9hLlAwKBgQDMSsrFR3KsZsiBtDaOUS6wX6czFA7uKgbV\nP9Cq9MVCfmvsksyAVoSBvhJPidpp7VK/w6O+TykJwKKTManDLzqcPfxNuD1FMCll\nV75lx/S/M57N/foMpXN29RLuCr4zzPO2sDhkvtQQkrZ4ua4j3isIrKb5DqcByotN\nvXeR4AjVoQKBgQCjfi8Me1niXq58FifUSBBvNZFpwgDYDWO97pAAKitZiLbZ7seR\nGcpdijefXRwPvHFOXpKB2r2lbJnEHROZguuYjE+E35BTcDdTAqhlFvRLE7bByFiT\natvJEc8cSZ8i9kH/3TNuZ04KgjYZes4j9a8W66S/2+2B6M5VoRRJr77NmQKBgDbC\niY3N9AgQWQijZMhLLIesbCX9526hp0k8HNPmXoXPW2CDjPuNtWENsNzPJ9OjAL5U\nU6zsjSSHFUz9T/L40u4Uk2/Fxe6o1T/MAEZKDem+jX/L513Cb6vgT12tVYSPGHjM\nzaD7od57ZRwBMZN9tu1RUkSKT+vj/ekts0JP2i5hAoGBAJo+q7BFZT6dkyaUZIAP\nIt9G7smdOpWWCN5WfF76b5NUsgukc36mLh+kr5gzHlBKbQ1kJv7JmdelVZvJXpMz\nbKlNIy0PjOATkCRjgwaT9QZfJn69st4zLSS20pdgMsfyazd5xRNAHzdGoEjunMv3\nKREdqdhmokbKapL8sAY1M6Au\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-htix6@cojo-74668.iam.gserviceaccount.com",
  "client_id": "100989243980321409767",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://accounts.google.com/o/oauth2/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-htix6%40cojo-74668.iam.gserviceaccount.com"
}


db_url = "https://sustained-flux-162207.firebaseio.com/"

class db_connect:

    def __init__(self):
        self.firekey = firekey
        self.db = db_url
        self.cred = credentials.Certificate(firekey)
        self.access = firebase_admin.initialize_app(self.cred, {
            'databaseURL': self.db
        })
