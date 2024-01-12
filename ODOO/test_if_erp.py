import xmlrpc.client
 
def connect(url, db, username, password):
   
    try:
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {})
        
        if uid:
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
 
    #model_name = 'res.partner'
    #partner_ids = odoo_connection.execute_kw(db, 2, password, model_name, 'search', [[]])
    #partners = odoo_connection.execute_kw(db, 2, password, model_name, 'read', [partner_ids])
 
    #for partner in partners:
        #print(partner)
 
def Company(models, db, uid, password, company_name):
    """
    Récupère l'identifiant d'une entreprise dans les modèles Odoo en fonction du nom de l'entreprise.
    
    Args:
    - models: L'objet ServerProxy pour accéder aux modèles Odoo
    - db: Nom de la base de données Odoo
    - uid: Identifiant de l'utilisateur Odoo
    - password: Mot de passe de l'utilisateur Odoo
    - company_name: Nom de l'entreprise
    
    Returns:
    - L'identifiant de l'entreprise (company_id) si trouvé, sinon None
    """
    try:
        company_id = models.execute_kw(db, uid, password,
                                       'res.company', 'search',
                                       [[('name', '=', company_name)]],
                                       {'limit': 1})
        if company_id:
            return company_id[0]  # Renvoie le premier élément trouvé
        else:
            print(f"Entreprise '{company_name}' non trouvée.")
            return None
    except Exception as e:
        print(f"Erreur lors de la recherche de l'entreprise : {e}")
        return None
 
# Utilisation de la fonction Company() pour récupérer l'identifiant d'une entreprise spécifique
url = 'http://172.21.0.3:8069'
db = 'demo'
username = 'papamalick214@gmail.com'
password = 'Malick2000'
company_name = 'Touch tech solution'
 
odoo_models, odoo_connection = connect(url, db, username, password)
if odoo_models and odoo_connection:
    print("Connexion réussie à Odoo")
    company_id = Company(odoo_connection, db, 2, password, company_name)
    if company_id:
        print(f"L'identifiant de '{company_name}' est : {company_id}")
