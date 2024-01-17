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
access = models.execute_kw(erp_db, user_id, erp_pwd,
                           'mrp.production', 'check_access_rights',
                           ['read'], {'raise_exception': False})
print(f"Manufacturing Order read access rights: {access}")

# Recherche de tous les IDs des ordres de fabrication
production_ids = models.execute_kw(erp_db, user_id, erp_pwd,
                                   'mrp.production', 'search',
                                   [[]])

if production_ids:
    print("Associations ID - Référence - Date prévue - Nom de l'article - Quantité produite - Quantité à produire - État des ordres de fabrication:")
    for production_id in production_ids:
        # Lecture des informations associées à l'ID
        production_info = models.execute_kw(erp_db, user_id, erp_pwd,
                                            'mrp.production', 'read',
                                            [production_id],
                                            {'fields': ['name', 'product_id', 'state', 'date_planned_start', 'qty_produced', 'product_qty']})
        if production_info:
            reference = production_info[0]['name']
            date_planned = production_info[0]['date_planned_start']
            product_name = production_info[0]['product_id'][1]  # Le nom de l'article est dans la position 1
            qty_produced = production_info[0]['qty_produced']
            qty_to_produce = production_info[0]['product_qty']
            state = production_info[0]['state']
            print(f"ID {production_id} - Référence: {reference} - Date prévue: {date_planned} - Nom de l'article: {product_name} - Quantité produite: {qty_produced} - Quantité à produire: {qty_to_produce} - État: {state}")
        else:
            print(f"ID {production_id} : Informations non trouvées.")
else:
    print("Aucun ordre de fabrication trouvé.")
