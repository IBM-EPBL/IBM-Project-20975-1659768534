import ibm_db

try:
    conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=ba99a9e6-d59e-4883-8fc0-d6a8c9f7a08f.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=31321;PROTOCOL=TCPIP;UID=zpk91239;PWD=kcAFB7vdtgiV994R;Security=SSL;SSLSecurityCertificate=DigiCertGlobalRootCA.crt", "", "")
    print("Connected to the database")
except:
    print("Error in connecting to the database: ", ibm_db.conn_errormsg())


def register(name, email,number, password):
    insert_sql = "INSERT INTO  ZPK91239.USER VALUES (?, ? ,?, ?)"
    prep_stmt = ibm_db.prepare(conn, insert_sql)
    ibm_db.bind_param(prep_stmt, 1, name)
    ibm_db.bind_param(prep_stmt, 2, email)
    ibm_db.bind_param(prep_stmt, 3, number)
    ibm_db.bind_param(prep_stmt, 4, password)
    ibm_db.execute(prep_stmt)


def login(name, password):
    select_sql = "SELECT * FROM  ZPK91239.USER WHERE USERNAME = ? AND PASSWORD = ?"
    prep_stmt = ibm_db.prepare(conn, select_sql)
    ibm_db.bind_param(prep_stmt, 1, name)
    ibm_db.bind_param(prep_stmt, 2, password)
    out = ibm_db.execute(prep_stmt)
    result_dict = ibm_db.fetch_assoc(prep_stmt)
    print(result_dict)
    return result_dict