# -*- coding: utf-8 -*-

from odoo import models, fields, api

class BonEntree(models.Model):
    
    _name = 'gctjara.bonentree'
    
    _rec_name='numero'
     
    numero = fields.Char(
        string='Numéro',
        default=lambda self: self.env['ir.sequence'].next_by_code('gctjara.bonentree.seq'))
     
    date = fields.Date(
         string='Date bon d\'entrée',
         required=True,
         default=fields.datetime.now(),
         help='La date de  bon de livraison'
        )

    commande_id = fields.Many2one(
        string='Commande',
        # required=True,
        index=True,
        comodel_name='gctjara.cmdfournisseur',

    )

    fournisseur_id = fields.Many2one(
        string="Fournisseur",
        ondelete='restrict',
        comodel_name='gctjara.fournisseur'
    )
      
    state = fields.Selection(
        string='Etat',
        default='nr',
        selection=[
            ('nr', 'non reçu'),
            ('rc', 'reçu'),
            ('lv', 'livrée'),
           
        ]
    )
    lignebonentree_id = fields.One2many(
        string='Produits',
        comodel_name='gctjara.lignebonentree',
        inverse_name='bonentree_id',
        store=True
    )
    @api.multi 
    def action_draft(self):
        self.state = 'nr'
    @api.multi 
    def cmd_livree(self):
        self.write({'state': 'lv'})
        return True

    @api.multi  
    def creat_mvtstock(self):
        self.write({'state': 'rc'})
        for recmvt in self.lignebonentree_id :

            sequencesmvt =   self.env['ir.sequence'].next_by_code('gctjara.mvtstock.seq')
            self.env['gctjara.mvtstock'].create({
                  'numero' :  sequencesmvt,
                  'date': fields.datetime.now().strftime('%m/%d/%Y %H:%M'),
                  'quantite':recmvt.quantite,
                  'produit':recmvt.embalageproduit_id.id,
                  'bonentree_id': self.id,
                  'type':'Entrée'

                })

            qteprod = int(recmvt.embalageproduit_id.quantitestocke) + int(recmvt.quantite)
            product = self.env['gctjara.produitemballee']
            product_id = recmvt.embalageproduit_id.id
            package_product = product.browse(product_id)
            package_product.quantitestocke = qteprod

            # self.maj_produits()
        return True
    
    def getProductID(self):
        if self.produit: 
            return {
                'name' : 'Produit',
                'res_model':'gctjara.produitemballee',
                'res_id':self.produit.id,
                'view_type':'form',
                'view_mode':'form',
                'type':'ir.actions.act_window'
                
                }
    
    
    @api.multi 
    def maj_produits(self):
        qteprod= int(self.produit.quantitestocke) + int(self.quantite)
    
        product = self.env['gctjara.produitemballee']
        product_id = self.produit.id
        package_product = product.browse(product_id)
        package_product.quantitestocke = qteprod
       
        return True
    
    
    