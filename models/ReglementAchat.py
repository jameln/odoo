# -*- coding: utf-8 -*-

from odoo import models, fields, api
import dateutil.parser

from datetime import datetime
class ReglementAchat(models.Model):

    _name = 'gctjara.regachat'
    
    _rec_name = 'numero'

    _inherit = 'mail.thread'
    
    _order = "dateecheance desc"
    
    numero = fields.Char(
        string='Numero règlement',
        required=True,
        default=lambda self: self.env['ir.sequence'].next_by_code('gctjara.regachat.seq')
                         )
    
    date = fields.Date(string='Date règlement',
                      required=True,
                      default=fields.datetime.now(),
                      help='La date de création de la facture'
                      )
    
    datevaleur = fields.Date(
        string='Date valeur',
        default=fields.datetime.now(),
                            )
    
    dateoperation = fields.Date(
        string='Date d\'opération',
        default=fields.datetime.now(),
                            )
    dateecheance = fields.Date(
        string='Date d\'écheance',
        default=fields.datetime.now(),
                            )
    duration = fields.Integer(
        string='Durée de raprrochement',
        compute='_get_duration'
    )

    @api.depends('date', 'datevaleur')
    def _get_duration(self):
        for r in self:
            start_date = fields.Datetime.from_string(r.date)
            end_date = fields.Datetime.from_string(r.datevaleur)
            r.duration = (end_date - start_date).days

    

   
    prixttc = fields.Float(
        string='Prix TTC',
        
        digits=(16, 3)
    )

    facture_id = fields.Many2many(
        string='Réf. facture',
        comodel_name='gctjara.factureachat'
    )
  
            

    modepayment = fields.Selection(
        string='Mode de payment',
        default='',
        selection=[
            ('ch', 'Chèque'),
            ('es', 'Espèce'),
            ('vr', 'Virement'),
            ('tr', 'Traite'),
            ('pr', 'Prélevement')
        ]
    )
    etatrapp = fields.Selection(
        string='Etat de rapprochement',
        default='',
        selection=[
            ('cd', 'A céditer'),
            ('db', 'A débiter'),
            ('vs', 'A versé'),
            ('rp', 'Rapproché'),
        
        ]
    )

    def Rapproche(self):
        self.write({'etatrapp': 'rp'})
        return True

    numerochq = fields.Char(string='Numero')

    
    description = fields.Text(
        string='Description',
       
    )
    upload_file = fields.Binary(string='Upload File')
    
    file_name = fields.Char(string='File Name')

    def _cron_check_reglement_achat_date(self):


        regachat_ids = self.search([])

        about = 'regachat'
        for reg_id in regachat_ids:
            notification = False
            name = u""
            description = u""
            reg = self.browse(reg_id.id)

            date_now = dateutil.parser.parse(fields.datetime.now()).date() # datetime.strptime(reg.date, '%Y-%m-%d %H:%M:%S')
            datech_reg = dateutil.parser.parse(reg.dateecheance).date() #datetime.strptime(reg.dateecheance, '%Y-%m-%d %H:%M:%S')

            # date_now = fields.Datetime.from_string(fields.datetime.now())
            # datech_reg= fields.Datetime.from_string(reg.dateecheance)
            print " dddd***************************ddddd**************"
            print ( date_now.days)
            if date_now.days == datech_reg.days :
                print "date egale"
                # name = reg_id.numero
                # description = u"jour de paiement le règelment"+str(reg_id.id)
                # notification_level = u"info"

            elif (date_now - datech_reg).days == -1:
                print "date inf"
                # name = reg_id.numero
                # description = u"il reste un jour pour le paiement du   règelment"+str(reg_id.id)
                # notification_level = u"warning"
            else :
                print " else "

            # self.env['gctjara.notification'].create({
            #         'name': name,
            #         'description': description,
            #         'notification_level': notification_level,
            #         'about': about,
            #         'notification_date': fields.datetime.today(),
            #         'regachat_id': reg_id.id
            #     })

        return True
