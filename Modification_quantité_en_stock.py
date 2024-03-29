import xmlrpc.client

def get_product_name_by_id(product_id, models, erp_db, user_id, erp_pwd):
    # Récupérer le nom de l'article en fonction de l'ID
    product_name = models.execute_kw(erp_db, user_id, erp_pwd,
                                     'stock.quant', 'read',
                                     [[product_id]],
                                     {'fields': ['display_name']})
    return product_name[0]['display_name'] if product_name else None

def update_stock_quantity(product_id, new_quantity):
    erp_ipaddr = "192.168.201.216"
    erp_port = "8069"
    erp_url = f'http://{erp_ipaddr}:{erp_port}'
    print("Connexion ODOO")
    print(f"@URL={erp_url}")

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
    print(f"Manufacturing Order write access rights : {access}")

    # Récupérer le nom de l'article
    product_name = get_product_name_by_id(product_id, models, erp_db, user_id, erp_pwd)
    
    if product_name:
        # Vérification de l'article dans Odoo avant la modification
        article_before_update = models.execute_kw(erp_db, user_id, erp_pwd,
                                                  'stock.quant', 'read',
                                                  [[product_id]],
                                                  {'fields': ['quantity']})
        print(f"Ancienne quantité de l'article {product_name} (ID={product_id}): {article_before_update[0]['quantity']}")

        # Mise à jour de la quantité de l'article
        models.execute_kw(erp_db, user_id, erp_pwd,
                          'stock.quant', 'write',
                          [[product_id], {'quantity': new_quantity}])

        print(f"Quantité de l'article {product_name} (ID={product_id}) mise à jour avec succès!")

        # Vérification de la nouvelle quantité
        article_after_update = models.execute_kw(erp_db, user_id, erp_pwd,
                                                 'stock.quant', 'read',
                                                 [[product_id]],
                                                 {'fields': ['quantity']})
        print(f"Nouvelle quantité de l'article {product_name} (ID={product_id}): {article_after_update[0]['quantity']}")
    else:
        print(f"L'article avec l'ID={product_id} n'a pas été trouvé.")

# Exemple d'utilisation de la fonction avec un product_id et une nouvelle quantité
product_id_to_update = 41
new_quantity_to_update = 181
update_stock_quantity(product_id_to_update, new_quantity_to_update)
