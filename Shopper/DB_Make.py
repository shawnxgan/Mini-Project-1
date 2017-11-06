import hashlib
import os

def fileToString(fileName):
    try:
        fp = open(fileName, 'r')
        fileContents = fp.read()
        fp.close()
        return fileContents
    except IOError as e:
        print('"?" is an invalid file.', fileName)
        print(e)

def loadSchema(conn, cur, fileName):
    schema = fileToString(os.path.join(os.path.dirname(__file__), fileName))
    if schema:
        cur.executescript(schema)
        conn.commit()
    else:
        exit

def encrypt(password):
    password = password.encode('utf-8')
    alg = hashlib.sha256()
    alg.update(password)
    
    return alg.hexdigest()


