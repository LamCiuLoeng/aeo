# -*- coding: utf-8 -*-
'''
Created on 2014-3-5
@author: CL.lam
'''
from cgi import FieldStorage

from tg import flash, redirect, expose
from tg.decorators import paginate
from repoze.what import authorize
from sqlalchemy.sql.expression import and_, desc


from rpac.lib.base import BaseController
from rpac.util.common import tabFocus, sysUpload, generate_thumbnail
from rpac.model import qry, Care, COO, Fibers, Division, Brand, Category, DBSession, GarmentPart, Product, Size
from rpac.widgets.master import master_search_form1, master_search_form2, \
    master_search_form3, master_search_form4, master_search_form5
from rpac.constant import INACTIVE, ACTIVE
from rpac.model import FileObject

__all__ = ['MasterController', ]


class MasterController( BaseController ):
    allow_only = authorize.not_anonymous()

    @expose( 'rpac.templates.master.index' )
    @paginate( "result", items_per_page = 20 )
    @tabFocus( tab_type = "master" )
    def index( self , **kw ):
        t = kw.get( 't', None )
        vs = self._check( t )
        dbclz = vs['dbclz']
        search_form = vs['search_form']
        label = vs['label']
        ws = []
        if search_form == master_search_form1:
            if kw.get( "name", False ) : ws.append( dbclz.name.op( "ilike" )( "%%%s%%" % kw["name"] ) )
        elif search_form == master_search_form2 or search_form == master_search_form3:
            if kw.get( "english", False ) : ws.append( dbclz.english.op( "ilike" )( "%%%s%%" % kw["english"] ) )
            if search_form == master_search_form3:
                if kw.get( "category", False ) : ws.append( dbclz.category == kw['category'] )
        elif search_form == master_search_form4:
            if kw.get( "brand", False ) : ws.append( dbclz.brandId == kw["brand"] )
            if kw.get( "division", False ) : ws.append( dbclz.divisionId == kw["division"] )
            if kw.get( "category", False ) : ws.append( dbclz.categoryId == kw["category"] )
            if kw.get( "itemCode", False ) : ws.append( dbclz.itemCode.op( "ilike" )( "%%%s%%" % kw["itemCode"] ) )
        elif search_form == master_search_form5:
            if kw.get( "brand", False ) : ws.append( dbclz.brandId == kw["brand"] )
            if kw.get( "category", False ) : ws.append( dbclz.categoryId == kw["category"] )
            if kw.get( "us_size", False ) : ws.append( dbclz.us_size.op( "ilike" )( "%%%s%%" % kw["us_size"] ) )
        if kw.get( "create_time_from", False ) : ws.append( dbclz.createTime >= kw["create_time_from"] )
        if kw.get( "create_time_to", False ) : ws.append( dbclz.createTime <= kw["create_time_to"] )
        ws.append( dbclz.active == ACTIVE )

        result = qry( dbclz ).filter( and_( *ws ) ).order_by( desc( dbclz.createTime ) ).all()
        return { "result" : result , "values" : kw, "widget" : search_form, 'label' : label}


    @expose( 'rpac.templates.master.add' )
    @tabFocus( tab_type = "master" )
    def add( self, **kw ):
        t = kw.get( 't', None )
        vs = self._check( t )
        data = {'t' : t , 'label' : vs['label']}
        if t in [ 'Product', 'Size' ]:
            cats = qry(Category.id, Category.name).order_by(Category.name)
            data['cats'] = cats
            brands = qry(Brand.id, Brand.name).order_by(Brand.name)
            data['brands'] = brands
            divisions = qry(Division.id, Division.name).order_by(Division.name)
            data['divisions'] = divisions
        return data


    @expose()
    def save_new( self, **kw ):
        t = kw.get( 't', None )
        vs = self._check( t )
        dbclz = vs['dbclz']
        if t in ['Division', 'Category', 'Brand', ]:
            name = kw.get( 'name', None ) or None
            if not name:
                flash( "The value could not be blank!", "warn" )
                return redirect( '/master/add?t=%s' % t )
            DBSession.add( dbclz( name = name ) )
            flash( 'Save the new recored successfully!', "ok" )

        elif t in ['Fibers', 'COO', 'GarmentPart', ]:
            params = {}
            for f in ['english', 'french_canadian', 'spanish_mx', 'spanish_latin', 'russian',
                      'french', 'arabic', 'japanese', 'hebrew', 'turkish', 'polish', 'chinese_simple',
                      'bahasa', 'german', 'dutch', 'hindi'] : params[f] = kw.get( f, None ) or None
            if not params['english'] :
                flash( 'The English value could not be blank!', "warn" )
                return redirect( 'master/add?t=%s' % t )
            DBSession.add( dbclz( **params ) )
            flash( 'Save the new recored successfully!', "ok" )

        elif t in ['Care', ]:
            params = {}
            for f in ['english', 'french_canadian', 'spanish_mx', 'spanish_latin', 'russian',
                      'french', 'arabic', 'japanese', 'hebrew', 'turkish', 'polish', 'chinese_simple',
                      'bahasa', 'german', 'dutch', 'hindi', 'category'] : params[f] = kw.get( f, None ) or None
            for f in [''] : params[f] = kw.get( f, None ) or None
            if not params['english'] or not params['category'] :
                flash( 'The English value could not be blank!', "warn" )
                return redirect( 'master/add?t=%s' % t )
            DBSession.add( dbclz( **params ) )
            flash( 'Save the new recored successfully!', "ok" )
        elif t in ['Product']:
            del kw['t']
            itemCode = kw.get('itemCode')
            width = kw.get('width')
            substrate = kw.get('substrate')
            if not itemCode or not width or not substrate:
                flash("Can't be empty!", 'warn')
                return redirect( '/master/add?t=%s' % t )
            c = qry(Product).filter_by(itemCode=itemCode).count()
            if c:
                flash("ItemCode exist!", 'warn')
                return redirect( '/master/add?t=%s' % t )
            image = kw['image']
            # if image not in ['', None]:
            if isinstance(image, FieldStorage):
                img_info = sysUpload(image, folder='files')
                img = qry(FileObject).get(img_info[1][0])
                kw['image'] = img.url
                thumb = generate_thumbnail(img)
                kw['thumb'] = thumb.url
            obj = dbclz(**kw)
            DBSession.add(obj)
            flash('Success!', 'ok')
        elif t in ['Size']:
            del kw['t']
            obj = dbclz(**kw)
            DBSession.add(obj)
            flash('Success!', 'ok')
        return redirect( '/master/add?t=%s' % t )
        return redirect( '/master/index?t=%s' % t )

    @expose( 'rpac.templates.master.edit' )
    @tabFocus( tab_type = "master" )
    def edit( self, **kw ):
        t = kw.get( 't', None )
        vs = self._check( t )
        _id = kw.get( 'id', None )
        dbclz = vs['dbclz']
        obj = qry( dbclz ).get( _id )
        result = {'t' : t, 'obj' : obj , 'label' : vs['label']}
        if t in [ 'Product', 'Size' ]:
            data = {}
            categorys = qry(Category.id, Category.name).order_by(Category.name)
            data['categorys'] = categorys
            brands = qry(Brand.id, Brand.name).order_by(Brand.name)
            data['brands'] = brands
            divisions = qry(Division.id, Division.name).order_by(Division.name)
            data['divisions'] = divisions
            result['data'] = data
        return result


    @expose()
    def save_edit( self, **kw ):
        t = kw.get( 't', None )
        vs = self._check( t )
        _id = kw.get( 'id', None )
        dbclz = vs['dbclz']
        obj = qry( dbclz ).get( _id )

        if t in ['Division', 'Category', 'Brand', ]:
            name = kw.get( 'name', None ) or None
            if not name:
                flash( "The value could not be blank!", "warn" )
                return redirect( '/master/edit?id=%s&t=%s' % ( obj.id, t ) )
            obj.name = name

        elif t in ['Fibers', 'COO', ]:
            params = {}
            for f in ['english', 'french_canadian', 'spanish_mx', 'spanish_latin', 'russian',
                      'french', 'arabic', 'japanese', 'hebrew', 'turkish', 'polish', 'chinese_simple',
                      'bahasa', 'german', 'dutch', 'hindi'] : params[f] = kw.get( f, None ) or None
            if not params['english'] :
                flash( 'The English value could not be blank!', "warn" )
                return redirect( 'master/edit?t=%s' % t )
            for k, v in params.items() : setattr( obj, k, v )
        elif t in ['Care', ]:
            params = {}
            for f in ['english', 'french_canadian', 'spanish_mx', 'spanish_latin', 'russian',
                      'french', 'arabic', 'japanese', 'hebrew', 'turkish', 'polish', 'chinese_simple',
                      'bahasa', 'german', 'dutch', 'hindi', 'category'] : params[f] = kw.get( f, None ) or None
            if not params['english'] or not params['category']:
                flash( 'The English value could not be blank!', "warn" )
                return redirect( 'master/edit?t=%s' % t )
            for k, v in params.items() : setattr( obj, k, v )
        elif t in ['Product', ]:
            itemCode = kw.get('itemCode')
            width = kw.get('width')
            substrate = kw.get('substrate')
            if not itemCode or not width or not substrate:
                flash("Can't be empty!", 'warn')
                return redirect( '/master/edit?t=%s&id=%s' % (t, obj.id) )
            c = qry(Product).filter_by(itemCode=itemCode).count() and itemCode != obj.itemCode
            if c:
                flash("ItemCode exist!", 'warn')
                return redirect( '/master/edit?t=%s&id=%s' % (t, obj.id) )
            del kw['t']
            image = kw['image']
            if isinstance(image, FieldStorage):
                img_info = sysUpload(image, folder='files')
                img = qry(FileObject).get(img_info[1][0])
                kw['image'] = img.url
                thumb = generate_thumbnail(img)
                kw['thumb'] = thumb.url
            for k, v in kw.items(): setattr(obj, k, v)
        elif t in ['Size', ]:
            for k, v in kw.items(): setattr(obj, k, v)
        flash( 'Update the record successfully!', "ok" )
        return redirect( '/master/index?t=%s' % t )


    @expose()
    def delete( self, **kw ):
        t = kw.get( 't', None )
        vs = self._check( t )
        _id = kw.get( 'id', None )
        dbclz = vs['dbclz']
        obj = qry( dbclz ).get( _id )
        obj.active = INACTIVE
        flash( 'Delete the record successfully!', 'ok' )
        return redirect( '/master/index?t=%s' % t )


    def _check( self, t ):
        if t not in ['Division', 'Brand', 'Category', 'Product', 'Fibers', 'GarmentPart', 'COO', 'Care', 'Size']:
            flash( "No such acton!", "warn" )
            return redirect( '/index' )

        if t == 'Care': dbclz, search_form, label = Care, master_search_form3, 'Care Instruction'
        if t == 'GarmentPart': dbclz, search_form, label = GarmentPart, master_search_form2, 'Garment Parts'
        elif t == 'COO': dbclz, search_form, label = COO, master_search_form2, 'Country Of Origin'
        elif t == 'Fibers': dbclz, search_form, label = Fibers, master_search_form1, 'Fabrics'
        elif t == 'Division': dbclz, search_form, label = Division, master_search_form1, 'Division'
        elif t == 'Brand': dbclz, search_form, label = Brand, master_search_form1, 'Brand'
        elif t == 'Category': dbclz, search_form, label = Category, master_search_form1, 'Category'
        elif t == 'Product': dbclz, search_form, label = Product, master_search_form4, 'Product'
        elif t == 'Size': dbclz, search_form, label = Size, master_search_form5, 'Size'

        return {'dbclz' : dbclz, 'search_form' : search_form, 'label' : label }


