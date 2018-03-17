import firebase_admin
from firebase_admin import credentials
from firebase_admin import db



firekey = {
  "type": "service_account",
  "project_id": "sustained-flux-162207",
  "private_key_id": "dfc3b1c710d54446d14849ca117b9b097c325e14",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCqBIj4yS9vE5SC\n6i3q1QROdGO2tCefccZ/6Kcp2L7Hj/6jQGeJyklLtJpNTIoM+PGttIZzG13geJPm\nqlJq3dFA/bapNj4zpXB11RxfmuPfqTS3TuSxFVYiJVieO6xOFqVTmy8xjarrfIaM\ne9g1N/jrkhgK6W2rAkVTnnupFTRzN6K0dL7MG9EHcfV+GQQceVy3g4/TMT5thHN3\nWJviyaMou42Elm0LhixpeHc/Z4SZwaheMzca/ftOVEMuyi+esp/F9vVpAy2D1Uyk\nqmz1FzycNRz7Jo9OVUIG0wprIlVJrQkgPUJUciYSu1pgNeSUQynlfoz6sayR3dHo\nWM2imjppAgMBAAECggEAVC8TrXBcwtjEoAAZhV49mCVMXGKe/fWlrp8B6pgOex0D\nHk2dFt6pZUmDX8QG1T6M2JB7RFKoLKY3wa7TSWQVIWOfRvD7YrJH2aiQuIwmyg/r\n8NopJb/lWtn4I71zZ2USLrA38Ybuu1R5AOWvnEZfRDGeIwULTvI8ZpeiLoo34tY6\nNJGF5aFAiPvpLQlp5MTrghGMJYFGTKKsNWXQ7u4+Z1zyCDgbxLPQZSSUJVjc7dgX\nIvLSPdGPI9PPxs0LV8LhzDCaOiSzFpjasUngG2W7Ye9Xjw6jJxpVUyViiCsg1X+H\nhMEqyqPpE58QGbTXi8F20KVmp16mLkBJMJbezlhl0wKBgQDaIkmMfuYl3pU/1JEa\n7vGUvb+mIeu4g1Ny3sWmYe++xTBFthaIYwIk5jasjrHJpOBoOm3f1CHQyR4CtLQq\nzveTZZ+dprf7nAZXLxF/h3vyuBpTpFKzSVASpYpQmI+/s4VwH5XStTRocGYCLzV3\n9v7n2sXlPPXjnMY731CVujTjBwKBgQDHh/+DAxqNkf6YZQnWmRPsCTwskQu+/fMR\nR9GZN3FzqLUj2PmYkCRoIP8ct1IcTOyaVm0S9BtMMvpeu+mofR2s5l7/6uoZme3l\nnwaNj0MXj+6Mn2yKUeLgbHoR3Ni/nys6+t21JhXQKTmpFBnaLtpcOXIfL3hMdXob\niGsTVDtrDwKBgQDL4NwparoljwKkZEMzjz1QroEf//hXvrcSWFEYD9WK0rcpkOVC\nmHd6kYlsgvp845OzF1l2qMjqYe+gy9DRahxQMd2b9iVkEBKFDkMmlTUuSRCiOKXr\nWIx0wTCj39QLcvk3MO5RwHe5XcSaKhGpjLv3bK0mc3HHSdKmRzUEnMOtpQKBgCae\nxzEHj8MpJ/s9S0szM+zy2KfTp09ffgWxPfuHBLmbRPxcSetisvlIsbhQL1908DLr\nWY9amlIEZ/ugKZjIJs9Jg8fLI2azKZ3RSwZpXVYZMNYdIXggY2aG+JWuhnGIkGiJ\nGBKw/XXeFOAKGPrnKLLDF7i7inBaKLldjUQfgKS3AoGAcPbiPV94koL1miHAdepL\nCNlmOR0DQfCZ6BSFm8SNZ+IOWxQg1bzMsuCxLY7qDXWWpJ5KbmhSbi1+hHE5+gvf\nUCVKsyUY7P/wXNUinNB+IsC9dVtySgrTDonXIrJ4K1kvtFjq0F3jmRDpfnp7VEjX\naklATv//yKAVrfomAwb4M1I=\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-s1cgi@sustained-flux-162207.iam.gserviceaccount.com",
  "client_id": "104485391492248334419",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://accounts.google.com/o/oauth2/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-s1cgi%40sustained-flux-162207.iam.gserviceaccount.com"
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
