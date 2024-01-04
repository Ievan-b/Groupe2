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
 
 
url = 'http://192.168.201.216:8069'
db = 'Touch_db'
username = 'admin'
password = '1234'
 

 
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
url = 'http://192.168.201.216:8069'
db = 'Touch_db'
username = 'admin'
password = '1234'
company_name = 'Touch Tech Solution'
 
odoo_models, odoo_connection = connect(url, db, username, password)
if odoo_models and odoo_connection:
    print("Connexion réussie à Odoo")
    company_id = Company(odoo_connection, db, 2, password, company_name)
    if company_id:
        print(f"L'identifiant de '{company_name}' est : {company_id}")


        ##################################################################################
def find_product_id(models, db, uid, password, product_name):
    try:
        product_ids = models.execute_kw(
            db, uid, password,
            'product.product', 'search',
            [[('name', '=', product_name)]],
            {'limit': 1}
        )
        if product_ids:
            return product_ids[0]  # Renvoie le premier élément trouvé
        else:
            print(f"Article '{product_name}' non trouvé.")
            return None
    except Exception as e:
        print(f"Erreur lors de la recherche de l'article : {e}")
        return None

# Utilisation de la fonction pour trouver l'identifiant d'un article spécifique
product_name = 'Souris gameur'  # Remplacez ceci par le nom de votre article
product_id = find_product_id(odoo_connection, db, 2, password, product_name)
if product_id:
    print(f"L'identifiant de '{product_name}' est : {product_id}")


    #############################################
   
######################################################################
def get_article_name(models, db, uid, password, article_code):
    """
    Récupère le nom d'un article dans les modèles Odoo en fonction du code de l'article.
    
    Args:
    - models: L'objet ServerProxy pour accéder aux modèles Odoo
    - db: Nom de la base de données Odoo
    - uid: Identifiant de l'utilisateur Odoo
    - password: Mot de passe de l'utilisateur Odoo
    - article_code: Code de l'article
    
    Returns:
    - Le nom de l'article si trouvé, sinon None
    """
    try:
        article_ids = models.execute_kw(db, uid, password,
                                        'product.template', 'search',
                                        [[('default_code', '=', article_code)]],
                                        {'limit': 1})
        if article_ids:
            article_data = models.execute_kw(db, uid, password,
                                             'product.template', 'read',
                                             [article_ids], {'fields': ['name']})
            if article_data:
                return article_data[0]['name']
            else:
                print(f"Article avec le code '{article_code}' trouvé mais impossible de récupérer le nom.")
                return None
        else:
            print(f"Article avec le code '{article_code}' non trouvé.")
            return None
    except Exception as e:
        print(f"Erreur lors de la recherche de l'article : {e}")
        return None

# Utilisation de la fonction get_article_name() pour récupérer le nom d'un article spécifique
article_code = '80001'

odoo_models, odoo_connection = connect(url, db, username, password)
if odoo_models and odoo_connection:
    print("Connexion réussie à Odoo")
    article_name = get_article_name(odoo_connection, db, 2, password, article_code)
    if article_name:
        print(f"Le nom de l'article avec le code '{article_code}' est : {article_name}")


        ################################################
def get_article_info(models, db, uid, password, article_name):
    """
    Récupère le code et le prix d'un article dans les modèles Odoo en fonction du nom de l'article.
    
    Args:
    - models: L'objet ServerProxy pour accéder aux modèles Odoo
    - db: Nom de la base de données Odoo
    - uid: Identifiant de l'utilisateur Odoo
    - password: Mot de passe de l'utilisateur Odoo
    - article_name: Nom de l'article
    
    Returns:
    - Un dictionnaire contenant le code et le prix de l'article si trouvé, sinon None
    """
    try:
        product_id = find_product_id(models, db, uid, password, article_name)
        if product_id:
            article_data = models.execute_kw(db, uid, password,
                                             'product.product', 'read',
                                             [product_id], {'fields': ['default_code', 'list_price']})
            if article_data:
                return {
                    'code': article_data[0]['default_code'],
                    'price': article_data[0]['list_price']
                }
            else:
                print(f"Article '{article_name}' trouvé mais impossible de récupérer les informations.")
                return None
        else:
            print(f"Article '{article_name}' non trouvé.")
            return None
    except Exception as e:
        print(f"Erreur lors de la recherche de l'article : {e}")
        return None

# Utilisation de la fonction get_article_info() pour récupérer le code et le prix d'un article spécifique
article_name_to_find = 'Clavier Corsaire RGB'
article_info = get_article_info(odoo_connection, db, 2, password, article_name_to_find)
if article_info:
    print(f"Informations sur l'article '{article_name_to_find}':")
    print(f"Code: {article_info['code']}")
    print(f"Prix: {article_info['price']}")








