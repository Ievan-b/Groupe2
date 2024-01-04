import xmlrpc.client
import tkinter
import tkinter as tk
from tkinter import ttk  # Importer le module ttk pour des styles améliorés

erp_ipaddr = "192.168.0.17"
erp_port = "9999"
erp_url = f'http://{erp_ipaddr}:{erp_port}'
print("Connexion ODOO")
print(f"@URL={erp_url}")
try:
    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(erp_url))
    version = common.version()
    print(f"Odoo version={version['server_serie']}")
except ConnectionRefusedError:
    print("Odoo Server not found or connection rejected")
else:
    erp_db = "vitre"
    erp_user = "inter"
    erp_pwd = "inter"