# -*- coding: utf-8 -*-

from odoo import fields , models, api


class Emballage(models.Model):
     _name = 'gctjara.emballage'
     
     _rec_name= 'name'
     
     name = fields.Char(string='Nom' ,default="Produit" ,compute='_compute_name',required=True)
         
       
     type = fields.Char('Type d\'emballage', default=' ',required=True)
     
     poids = fields.Integer(string='Poids unitaire', placeholder="0",required=True)
     
     produitemballee_id = fields.One2many(
        comodel_name='gctjara.produitemballee',
        string='Produits',
        inverse_name='emballage_id'
    )
     unite=fields.Selection(
        string='Unité',
        default='',
        selection=[
            ('KG', 'KG'),
            ('L', 'L'),
            ('Piece', 'Pièce'),
            ('M', 'M'),
        
        ],
        required=True
    )
     @api.depends('type', 'poids')
     def _compute_name(self):
        for r in self:
            r.name= r.type + " "+ str(r.poids)
        
       
