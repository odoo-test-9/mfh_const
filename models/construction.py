# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
# res_company.py

from openerp.osv import fields, osv
from openerp.tools.translate import _

#class const_mo(osv.osv):
class const_product_template(osv.osv):
    _inherit = 'product.template'
    def _get_total_mo(self, cr, uid, ids, fields, arg, context=None):
      res = {}
      suma = 0
      for line in self.browse(cr, uid, ids, context=context):
        for line2 in line.mo_cant:
          suma += line2.price * line2.cant

      res[line.id] = suma
      # id y Valor
      return res


    _columns = {
       'mat_cant': fields.one2many('lsmat', 'product_tmpl_id', 'mat_cant'),
       'mo_cant': fields.one2many('lsmo', 'product_tmpl_id', 'mo_cant'),
       'eq_cant': fields.one2many('lsequipo', 'product_tmpl_id', 'eq_cant'),
       'total_mo': fields.function(_get_total_mo, string='Total MO'),
       # Hererdar el Precio Total y Hacerlo dependeciente 
    }



class const_mat(osv.osv):
    _name = 'lsmat'
    _columns = {
       'name' : fields.char('Materiales'),
       'product_id' : fields.many2one ('product.product', 'Producto'),
       'product_tmpl_id' : fields.many2one ('product.template', 'Plantilla'),
       'cant' : fields.float('Cantidad'), 
    }


class const_mo(osv.osv):
    _name = 'lsmo'
    _columns = {
       'name' : fields.char('Mano de Obra'),
       'product_id' : fields.many2one ('product.product', 'Producto'),
       'product_tmpl_id' : fields.many2one ('product.template', 'Plantilla'),
       'cant' : fields.float('Cantidad'),
       'price' : fields.float('Precio'),
    }
    def onchange_mo(self, cr, uid, ids, vproduct_id, vcant, context=None):
        print '=============',vproduct_id
        print '=============',vcant
        res = {}
        product_obj = self.pool.get('product.product')
        product_brw = product_obj.browse(cr, uid, vproduct_id, context)
        precio = product_brw.product_tmpl_id.list_price * vcant
        res['value'] = { 'price': precio }
        print '****',res
        return res



class const_eq(osv.osv):
    _name = 'lsequipo'
    _columns = {
       'name' : fields.char('Equipo'),
       'product_id' : fields.many2one ('product.product', 'Producto'),
       'product_tmpl_id' : fields.many2one ('product.template', 'Plantilla'),
       'cant' : fields.float('Cantidad'),
    }
