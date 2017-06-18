# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Fournisseur(models.Model):
     _name = 'gctjara.fournisseur'
     
     _rec_name = 'name'
     
     _inherit='mail.thread'
     
     name = fields.Char('Nom', required=True)
     
     matriculefiscal = fields.Char('Matricule fiscale', required=True)
     
     company_name = fields.Char('Company Name')
     
     image = fields.Binary("Image",
                           attachment=True,
                           help="This field holds the image used as avatar for this contact, limited to 1024x1024px",
                           )
     
     email = fields.Char('Email')
     
     phone = fields.Char('Telephone')
     
     fax = fields.Char('Fax')
     
     mobile = fields.Char('Portable')
     
     adresse = fields.Char('Adresse')
     
     street = fields.Char()
    
     zip = fields.Char(change_default=True)
     
     city = fields.Char()
     
     active = fields.Boolean(default=True)

     # Agree = fields.Boolean(string='Fournisseur Agréé' ,default=False)

     state = fields.Selection(string="Etat", required=True, selection=[
         ('Agree', 'Agrée'),
         ('NonAgree', 'Non Agrée')
     ], default='NonAgree')
     state_bool = fields.Boolean(compute="_state_bool")

     @api.one
     def toggle_state(self):
         if self.state == 'Agree':
             self.state = 'NonAgree'
         else:
             self.state = 'Agree'
         return True

     @api.depends("state")
     def _state_bool(self):
         for v in self:
             v.state_bool = (v.state != 'NonAgree')

      
     commande_id = fields.One2many(
       string="Commande",
       ondelete='restrict',
       comodel_name='gctjara.cmdfournisseur',
       inverse_name='fournisseur_id',
       )
       
     facture_id = fields.One2many(
       string="Factures",
       ondelete='restrict',
       comodel_name='gctjara.factureachat',
       inverse_name='fournisseur_id',
       )
       
#      produit_id = fields.Many2one(
#        string='Prosuits',
#        comodel_name='gctjara.produits'
#       )
#    
     nature_relation = fields.Selection(
    string='Nature de la relation',
    default='',
    selection=[
        ('fr', 'Fournisseur'),
        ('cn', 'Concurent'),
        ('ag', 'Agence'),

    ]
)
     relation = fields.Selection(
    string='Relation fournisseur',
    default='',
    selection=[
        ('exclusif', 'Régulier exclusif'),
        ('potentiel', 'Potentiel'),
        ('regulier', 'Régulier'),
        ('occacionnel', 'Occacionnel'),
        ('Pas', 'Pas de relation actuel')
    ]
)
     type_de_relation = fields.Selection(
    string='Type de relation',
    default='',
    selection=[
        ('Intense', 'Intense'),
        ('Confiante', 'Confiante'),
        ('Inexistante', 'Inexistante'),
        ('Réserve', 'Réservée'),
        ('Negative', 'Negative'),
        ('Limite', 'Limitée')
    ]
)
     necessite_fournisseur = fields.Selection(
    string='Neccessite fournisseur',
    default='',
    selection=[
        ('Intense', 'Prioritaire'),
        ('Confiante', 'Contact interessant'),
        ('Inexistante', 'Structuration Engagée'),
        ('Réserve', 'Compangnes périodiques'),
        ('Negative', 'Non categorisé')

    ]
)

