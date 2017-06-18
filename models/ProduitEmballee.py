# -*- coding: utf-8 -*-

from odoo import models, fields, api

class LigneProduitEmballage(models.Model):
    _name = 'gctjara.produitemballee'
    
    _rec_name = 'name'
       
    _sql_constraints = [
        ('produitemballée', 'unique (emballage_id , produit_id )', 'Cette emballage est déja crée')
    ] 
    
    name = fields.Char(string='Nom' , compute='_compute_name')
    
    @api.depends('produit_id', 'emballage_id')
    def _compute_name(self):
        for r in self:
            if(isinstance(r.produit_id.name , unicode)) and isinstance(r.emballage_id.name,unicode)and isinstance(r.emballage_id.unite,unicode):
                r.name= r.produit_id.name + " "+ (r.emballage_id.name).strip()+" "+r.emballage_id.unite
               
   
    @api.one     
    @api.depends('produit_id','emballage_id')
    def _prix_unit(self):
         for r in self:
            r.prixunit=r.produit_id.prixunit*r.emballage_id.poids
    @api.one       
    @api.depends('produit_id','emballage_id')
    def _prix_vente(self):
         for r in self:
            r.prixvente=r.produit_id.prixvente*r.emballage_id.poids
            print("r.produit_id.prixvente ****>>" +str(r.produit_id.prixvente))
            print("r.emballage_id.poids ****>>" +str(r.emballage_id.poids))
            print(" r.prixvente ****>>" +str( r.prixvente))
     
     

    
    quantitestocke=fields.Integer(
        string ='Stock',
        default=0.0,
        digits=(16, 3)
        )
     
    produit_id = fields.Many2one(
          string='Produit',
          required=True,
          index=True,
          comodel_name='gctjara.produits',
          ondelete='set null'
      )
    
    prixunit= fields.Float(
#         related='produit_id.prixunit,emballage_id.poids',
        string='Prix unitaire',
#         default='_prix_unit',
        compute='_prix_unit',
        store=True,
        digits=(16, 3)
    )
    prixvente= fields.Float(
#         related='produit_id.prixvente,emballage_id.poids',
        string='Prix de vente',
#           default='_prix_vente',
        compute='_prix_vente',
        store=True,
        digits=(16, 3)
    )
    emballage_id = fields.Many2one(
         comodel_name='gctjara.emballage',
         string='Emballage',
     )
    
    lignecmd_id = fields.One2many(
        string='Commandes Achats',
        comodel_name='gctjara.lignecmdachat',
        inverse_name='embalageproduit_id'
                        )  
    
    lignecmdvente_id = fields.One2many(
        string='Commandes Ventes',
        comodel_name='gctjara.lignecmdvente',
        inverse_name='embalageproduit_id'
                        )  
  
