from odoo import models, fields, api
class Pengembalian(models.Model):
    _name = 'giveback.pengembalian'
    _description = 'Data Pengembalian Buku'
    
    name = fields.Char(string="No. Pengembalian", required=True, readonly=True, default='New')
    hitung_buku_ids = fields.Many2many('logbooks.bukulog', string='Buku Dikembalikan')
    tanggal_kembali_sekarang = fields.Date(string='Tanggal Pengembalian', default=fields.Date.context_today)
    peminjaman_id = fields.Many2one('borrow.peminjaman', string='Peminjaman', required=True)
    pengembalian_buku_ids = fields.Many2many('borrow.peminjaman', string='Buku Dikembalikan')
    tanggal_pinjam = fields.Date(related='peminjaman_id.tanggal_pinjam', store=True)
    tanggal_kembali = fields.Date(related='peminjaman_id.tanggal_kembali', store=True)
    member_id = fields.Many2one(related='peminjaman_id.member_id', store=True)
    no_member = fields.Char(related='peminjaman_id.no_member', store=True)
    denda = fields.Integer(string='Total Denda', compute='_compute_denda', store=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('dikembalikan', 'Dikembalikan')],
        string='Status Pengembalian', default='draft'
    )

    @api.depends('tanggal_kembali', 'tanggal_kembali_sekarang', 'pengembalian_buku_ids')
    def _compute_denda(self):
        for record in self:
            denda = 0
            if record.tanggal_kembali and record.tanggal_kembali_sekarang:
                selisih = (record.tanggal_kembali_sekarang - record.tanggal_kembali).days
                if selisih > 0:
                    denda = len(record.pengembalian_buku_ids) * selisih * 1000
            record.denda = denda
  
    def action_kembalikan(self):
        for buku in self.hitung_buku_ids:
            if buku.jumlah <= 0:
                raise ValueError("Buku tidak tersedia untuk dikembalikan")
            else:
                buku.jumlah += 1
        self.state = 'dikembalikan'
        self.peminjaman_id.state = 'dikembalikan'
  
    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('giveback.pengembalian') or 'New'

        return super(Pengembalian, self).create(vals)

  
        
    # def action_kembalikan(self):
    #     for record in self.pengembalian_buku_ids:
    #         if record.jumlah <= 0:
    #             raise ValueError("Buku tidak tersedia untuk dikembalikan")
    #         else:
    #             record.jumlah += 1
    #     self.state = 'dikembalikan'
    #     self.peminjaman_id.state = 'dikembalikan'    