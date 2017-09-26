# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class LigneCommandeAchat(models.Model):
    _name = 'gctjara.lignecmdachat'
    
    _rec_name = 'name'
    
    
    name =fields.Char(
        string='Nom:',
        compute='_compute_name'
                      )
    
    @api.depends('embalageproduit_id')
    def _compute_name(self):
        for r in self:
            if(isinstance(r.embalageproduit_id.name , unicode)) :
                r.name= r.embalageproduit_id.name 
   
    quantite = fields.Integer(
        string='Quantite',
        required=True,
          )
      
    @api.depends('quantite','embalageproduit_id')
    def compute_qte_tot(self):
        for r in self:
          r.quantitetot= r.quantite* r.embalageproduit_id.emballage_id.poids
                
    quantitetot = fields.Float(
        string='Qte total',
        compute='compute_qte_tot',
        required=True,
          )
    
    tva = fields.Float(
        string='TVA (%)',
        default='6',
        digits=(16, 1),
    )
    remise = fields.Float(
        string='Remise (%)',
        default='0.0',
        digits=(16,1),

    )
    @api.depends('embalageproduit_id')
    def _prix_unit(self):
         for r in self:
            r.prixunit=r.embalageproduit_id.prixunit
            
    prixunit= fields.Float(
        related='embalageproduit_id.prixunit',
        string='Prix unitaire',
        compute='_prix_unit',
        store=True
    )
    
    commande_id = fields.Many2one(
         required=True,
         index=True,
         comodel_name='gctjara.cmdfournisseur',
          
     )
    embalageproduit_id = fields.Many2one(
         comodel_name='gctjara.produitemballee',
         string='Produits'
     )


    @api.multi
    @api.constrains("remise","quantite")
    def verif_remise(self):
        for pe in self:
            tauxremise = float(pe.remise) / 100
            if tauxremise < 0 or tauxremise > 1:
                raise ValidationError("Le remise doit être un entier superieure a zéro et inferieure a 100")
            qte = float(pe.quantite) 
            if qte <= 0 :
                raise ValidationError("La quantité doit être un entier superieure à zéro ")

    @api.multi
    @api.depends("quantite" , "embalageproduit_id","tva","remise")
    def prixtot(self):
        for pe in self:
            remise= float(pe.remise)/100
            tauxtva=float(pe.tva)/100
            prixht=pe.quantite * pe.embalageproduit_id.prixunit #*pe.embalageproduit_id.emballage_id.poids
            pe.prix_ht=prixht
            prix_remise=prixht*(1-remise)
            pe.prix_total =(prixht*(1-remise))*(1+tauxtva)
            
    prix_total = fields.Float(
        string='Prix Tot',
        compute="prixtot",
        digits=(16, 3),
        store=True
    )
    prix_ht = fields.Float(
        string='Prix HT',
        compute="prixtot",
        digits=(16, 3),
        store=True
    )
    reffact=fields.Char()

    def is_empty(any_structure):
        if any_structure:
           print('Structure is not empty.')
           return  True
        else:
            print('Structure is empty.')
            return False
         

  