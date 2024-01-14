erp_ipaddr = "172.20.10.7"
erp_port = "8069"
erp_url = f'http://{erp_ipaddr}:{erp_port}'
print("Connexion ODOO")
print(f"@URL={erp_url}")

import xmlrpc.client

common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(erp_url))
version = common.version()
print(f"Odoo version={version}")

erp_db = "Touch_db"
erp_user = "admin"
erp_pwd = "1234"
user_id = common.authenticate(erp_db, erp_user, erp_pwd, {})
print(f"Odoo authentification:{user_id}")

models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(erp_url))
access = models.execute_kw(erp_db, user_id, erp_pwd,
'mrp.production', 'check_access_rights',
['write'], {'raise_exception': False})
print(f"Manufactoring Order write access rights : {access}")

# ... (votre code existant)

# ID de l'article que vous souhaitez mettre à jour
product_id = 14 # Remplacez ceci par l'ID de votre article

# Nouvelle quantité pour l'artcle
new_quantity = 15 # Remplacez ceci par la nouvelle quantité

# Recherche de l'article dans Odoo
article = models.execute_kw(erp_db, user_id, erp_pwd,
                            'stock.quant', 'read',
                            [[product_id]],
                            {'fields': ['quantity']})

print(f"Ancienne quantité de l'article : {article[0]['quantity']}")

# Mise à jour de la quantité de l'article
models.execute_kw(erp_db, user_id, erp_pwd,
                  'stock.quant', 'write',
                  [[product_id], {'quantity': new_quantity}])

print("Quantité de l'article mise à jour avec succès!")

# Vérification de la nouvelle quantité
updated_article = models.execute_kw(erp_db, user_id, erp_pwd,
                                    'stock.quant', 'read',
                                    [[product_id]],
                                    {'fields': ['quantity']})

print(f"Nouvelle quantité de l'article : {updated_article[0]['quantity']}")