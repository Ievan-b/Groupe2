import xmlrpc.client
 
def connect(url, db, username, password):
   
    try:
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {})
        
        if uid:
            print('Authentification réussie. UID: {}'.format(uid))
            models = xmlrpc.client.ServerProxy('{}/xmlprc/2/objects'.format(url))
            return models,xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
        else:
            print("Connexion échouée : Authentification impossible")
            return None
    except Exception as e:
        print(f"Erreur de connexion : {e}")
        return None
 
 
url = 'http://172.21.0.3:8069'
db = 'demo'
username = 'papamalick214@gmail.com'
password = 'Malick2000'
 
odoo_models, odoo_connection = connect(url, db, username, password)
if odoo_connection and odoo_models:
    print("Connexion réussie à Odoo")

