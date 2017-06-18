# -*- coding: utf-8 -*-

from odoo import models, fields, api

class MouvementStock(models.Model):

    _name = 'gctjara.mvtstock'
    
    _rec_name = 'numero'
    
    numero = fields.Char(
        string='Numero mvt',
        default=lambda self: self.env['ir.sequence'].next_by_code('gctjara.mvtstock.seq'))
    
    date = fields.Date(
        string='Date de Mvt' ,
        default=fields.datetime.now() 
        )
    
    quantite = fields.Integer(
        string='Quantité'
        )
    
    produit = fields.Many2one(
        string='Produits',
          comodel_name='gctjara.produitemballee'
        )
    type=fields.Char(
        string='Type')
    
    bonentree_id=fields.Many2one(
        string='Réf bon d\'entrée',
        comodel_name='gctjara.bonentree'
        )
    bonlivraison_id=fields.Many2one(
        string='Réf bon de livraison',
        comodel_name='gctjara.bonlivraison'
        )
