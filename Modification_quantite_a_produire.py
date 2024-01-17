erp_ipaddr = "192.168.201.216"
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
# Vous pouvez retirer l'argument 'raise_exception' de la ligne suivante
access = models.execute_kw(erp_db, user_id, erp_pwd,
                           'mrp.production', 'check_access_rights',
                           ['read', 'write'], {})
print(f"Manufacturing Order read and write access rights: {access}")

def update_quantity_to_produce(production_id, new_quantity_to_produce):
    try:
        # Mise à jour de la quantité à produire de l'ordre de fabrication
        models.execute_kw(erp_db, user_id, erp_pwd,
                          'mrp.production', 'write',
                          [[production_id], {'product_qty': new_quantity_to_produce}])

        print(f"Quantité à produire de l'ordre de fabrication ID {production_id} mise à jour avec succès!")

        # Vérification de la nouvelle quantité à produire
        updated_production = models.execute_kw(erp_db, user_id, erp_pwd,
                                              'mrp.production', 'read',
                                              [[production_id]],
                                              {'fields': ['product_qty']})

        print(f"Nouvelle quantité à produire de l'ordre de fabrication ID {production_id} : {updated_production[0]['product_qty']}")
    except Exception as e:
        print(f"Erreur lors de la mise à jour de la quantité à produire : {e}")

# Exemple d'utilisation : Mettre à jour la quantité à produire pour l'ordre de fabrication avec l'ID 1
update_quantity_to_produce(3, 386)
