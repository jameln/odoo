# -*- coding: utf-8 -*-
{
    'name': "GC-TJARA",

    'summary': """
    Dans le cadre de PFE de Mr JAMEL NEFZI :
         Solution pour la gestion de l'activité commerciale d'une entreprise (PME)

""",

    'description': """
        Application Gestion commercial T-JARA pour les PME 
    """,

    'author': "Khidma",
    'website': "http://khidma.tn",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    # Uncategorized
    'category': 'sales',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail', 'report', 'board','web'],

    # always loaded
    'data': [
        'views/template.xml',
        'views/BonEntree.xml',
        'views/BonLivraison.xml',
        'views/Client.xml',
        'views/Fournisseur.xml',
        'views/CommandeClient.xml',
        'views/CommandeFournisseur.xml',
        'views/FactureAchat.xml',
        'views/FactureVente.xml',
        'views/ReglementAchat.xml',
        'views/ReglementVente.xml',
        'views/Produits.xml',
        'views/Emballages.xml',
        'views/ProduitEmballee.xml',
        'views/MouvementStock.xml',
        'security/acces_rules.xml',
        'views/dashboard.xml',
        'views/sequence.xml',
        'report/report_factureachat_template.xml',
        'report/report_cmdfournisseur_template.xml',
        'report/report_facturevente_template.xml',
        'report/report_cmdclient_template.xml',
        'report/report_bonlivraison_template.xml',
        'wizard/FactureAchat_wizard.xml',
        'wizard/FactureVente_wizard.xml',
        'views/menu.xml',
               
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    
    'application': True,
    'css' : ['static/src/css/*.css']
}
