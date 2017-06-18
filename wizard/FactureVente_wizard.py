# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime



class FactureVenteTemp(models.TransientModel):
    _name = "gctjara.factureventeregle"

    datereception = fields.Date(string='Date réception')
    datevaleur = fields.Date(string='Date valeur')
    dateoperation = fields.Date(string='Date opération')
    dateecheance = fields.Date(string='Date écheance')

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
            ('vs', 'A versé'),
            ('rp', 'Rapproché'),

        ]
    )
    montant_tranche = fields.Float(
        string='Montant',
        digits=(16, 3),
        default=0.0,
        store=True
    )
    numerochq = fields.Char(string='Numero')
    defalquer_facture = fields.Many2one(comodel_name='gctjara.defalquerfactureachat')

    @api.multi
    def Paiement(self):
        for facture_id in self.env.context.get('active_ids'):
            factures = self.env['gctjara.facturevente'].search([('id', '=', facture_id)])

            if (factures.etatreglement == u"Réglée"):
                raise ValidationError('La facture numéro  ' + str(factures.numero) + ' est déja réglée')
                return False

            record = self.env['gctjara.regvente'].create({
                'numero': self.env['ir.sequence'].next_by_code('gctjara.regvente.seq'),
                'date': fields.datetime.now(),
                'dateoperation': self.dateoperation,
                'datevaleur': self.datevaleur,
                'daterecption': self.dateecheance,
                'prixttc': factures.montantttc,
                'etatrapp': self.etatrapp,
                'modepayment': self.modepayment,
                'numerochq': self.numerochq,
                'facture_id': str(factures.id)

            })

            factures.write({'refregvente': [(4, record.id, False)], 'etatreglement': 'Réglée'})


        return True


class DefalquerFactureVente(models.TransientModel):
    _name = "gctjara.defalquerfacturevente"

    defalquer_facture = fields.One2many(
        comodel_name='gctjara.factureventeregle',
        inverse_name='defalquer_facture',

    )

    @api.multi
    def Defalquer_facture(self):
        for record_id in self.env.context.get('active_ids'):
            records = self.env['gctjara.facturevente'].search([('id', '=', record_id)])
            if (records.etatreglement == u"Réglée"):
                raise ValidationError('La facture numéro  ' + str(records.numero) + ' est déja réglée')
                return False

            total_montant = 0.0
            for rm in self.defalquer_facture:
                total_montant += rm.montant_tranche

            if (total_montant != records.montantttc):
                raise ValidationError(
                    'La somme des tranches ' + str(total_montant) + '  n\'est pas égale au montant de facture ' + str(
                        records.montantttc))
                return False

            list_reg = ()
            for rec in self.defalquer_facture:
                record = self.env['gctjara.regvente'].create({
                    'numero': self.env['ir.sequence'].next_by_code('gctjara.regvente.seq'),
                    'date': fields.datetime.now(),
                    'dateoperation': rec.dateoperation,
                    'datevaleur': rec.datevaleur,
                    'daterecption': rec.dateecheance,
                    'prixttc': rec.montant_tranche,
                    'etatrapp': rec.etatrapp,
                    'modepayment': rec.modepayment,
                    'numerochq': rec.numerochq,
                    'facture_id': str(records.id)
                })
                list_reg += (record.id,)
            records.write({'etatreglement': 'Réglée'})
            for reg in list_reg:
                records.write({'refregvente': [(4, reg, False)]})
        return True


class RegrouperFactureVente(models.TransientModel):
    _name = "gctjara.regrouperfacturevente"

    datereception = fields.Date(string='Date réception')
    datevaleur = fields.Date(string='Date valeur')
    dateoperation = fields.Date(string='Date opération')
    dateecheance = fields.Date(string='Date écheance')

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
            ('vs', 'A versé'),
            ('rp', 'Rapproché'),

        ]
    )
    montant_tranche = fields.Float(
        string='Montant',
        digits=(16, 3),
        default=0.0,
        store=True
    )
    numerochq = fields.Char(string='Numero')

    @api.multi
    def Paiement_Regroupee(self):
        somme_prixttc = 0.0
        list_fac = ()
        for facture_id in self.env.context.get('active_ids'):
            factures = self.env['gctjara.facturevente'].search([('id', '=', facture_id)])

            if (factures.etatreglement == u"Réglée"):
                raise ValidationError('La facture numéro  ' + str(factures.numero) + ' est déja réglée')
                return False
            somme_prixttc += factures.montantttc
            list_fac += (factures.id,)

        record = self.env['gctjara.regvente'].create({
            'numero': self.env['ir.sequence'].next_by_code('gctjara.regvente.seq'),
            'date': fields.datetime.now(),
            'dateoperation': self.dateoperation,
            'datevaleur': self.datevaleur,
            'daterecption': self.dateecheance,
            'prixttc': somme_prixttc,
            'etatrapp': self.etatrapp,
            'modepayment': self.modepayment,
            'numerochq': self.numerochq,

        })

        rec_reg = self.env['gctjara.regvente'].search([('id', '=', record.id)])
        for fac in list_fac:
            rec_reg.write({'facture_id': [(4, fac, False)]})

        for facture_id in self.env.context.get('active_ids'):
            factures = self.env['gctjara.facturevente'].search([('id', '=', facture_id)])
            factures.write({'refregvente': [(4, record.id, False)], 'etatreglement': 'Réglée'})
        return True
