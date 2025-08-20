from odoo import models, fields

class BukuLog(models.Model):
    _name = 'logbooks.bukulog'
    _description = 'Log Peminjaman dan Pengembalian Buku'
    _rec_name = 'buku_id'

    buku_id = fields.Many2one('books.buku', string='Buku', ondelete='restrict')
    member_id = fields.Many2one('people.member', string='Member', ondelete='restrict')
    peminjaman_id = fields.Many2one('borrow.peminjaman', string='Peminjaman', ondelete='restrict')
    pengembalian_id = fields.Many2one('giveback.pengembalian', string='Pengembalian', ondelete='restrict')
