import hashlib

def fileToString(fileName):
    try:
        fp = open(fileName, 'r')
        fileContents = fp.read()
        fp.close()
        return fileContents
    except IOError:
        print('"?" is an invalid file.', fileName)

def loadSchema(conn, cur, fileName):
    schema = fileToString(fileName)
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


