# -*- coding: utf-8 -*-
'''
Created on 2014-2-17
@author: CL.lam
'''
import os
import random
import traceback
import transaction
import shutil
import json
from datetime import datetime as dt
from tg import expose, redirect, flash, request, config, session
from tg.decorators import paginate
from repoze.what import authorize
from repoze.what.predicates import has_permission
from sqlalchemy.sql.expression import and_, desc

from rpac.lib.base import BaseController
from rpac.util.common import tabFocus, logError, serveFile, \
    ReportGenerationException, sendEmail
from rpac.model import qry, DBSession, OrderHeader, PrintShop, AddressBook, \
                        Product, COO, Care, Category, Fibers, GarmentPart, \
                        OrderDetail, Division, Brand, Size
from rpac.widgets.ordering import order_search_form, product_search_form
from rpac.util.excel_helper import AEOReport, getExcelVersion, AEOOrder
from rpac.constant import ACTIVE, ORDER_INPROCESS, ORDER_COMPLETE, ORDER_NEW, ORDER_CANCEL


__all__ = ['OrderingController', ]




DEFAULT_SENDER = 'r-pac-aeo-order-system@r-pac.com.hk'


class OrderingController( BaseController ):
    allow_only = authorize.not_anonymous()

    @expose( 'rpac.templates.ordering.index' )
    @paginate( "result", items_per_page = 20 )
    @tabFocus( tab_type = "main" )
    def index( self , **kw ):
        ws = [OrderHeader.active == 0]
        if kw.get( "no", False ) : ws.append( OrderHeader.no.op( "ilike" )( "%%%s%%" % kw["no"] ) )
        if kw.get( "customerpo", False ) : ws.append( OrderHeader.customerpo.op( "ilike" )( "%%%s%%" % kw["customerpo"] ) )
        if kw.get( "vendorpo", False ) : ws.append( OrderHeader.vendorpo.op( "ilike" )( "%%%s%%" % kw["vendorpo"] ) )
        if kw.get( "status", False ) : ws.append( OrderHeader.status == kw["status"] )
        if kw.get( "printShopId", False ) : ws.append( OrderHeader.printShopId == kw["printShopId"] )
        if kw.get( "create_time_from", False ) : ws.append( OrderHeader.createTime >= kw["create_time_from"] )
        if kw.get( "create_time_to", False ) : ws.append( OrderHeader.createTime <= kw["create_time_from"] )

        if kw.get( "divisionId", False ) : ws.extend( [OrderHeader.id == OrderDetail.headerId, OrderDetail.active == ACTIVE, OrderDetail.divisionId == kw['divisionId']] )
        if kw.get( "brandId", False ) : ws.extend( [OrderHeader.id == OrderDetail.headerId, OrderDetail.active == ACTIVE, OrderDetail.brandId == kw['brandId']] )
        if kw.get( "categoryId", False ) : ws.extend( [OrderHeader.id == OrderDetail.headerId, OrderDetail.active == ACTIVE, OrderDetail.categoryId == kw['categoryId']] )

        if not has_permission( "MAIN_ORDERING_CHECKING_ALL" ): ws.append( OrderHeader.createById == request.identity["user"].user_id )

        result = qry( OrderHeader ).filter( and_( *ws ) ).order_by( desc( OrderHeader.createTime ) ).all()
        ps = qry( PrintShop ).filter( and_( PrintShop.active == 0 ) ).order_by( PrintShop.name )

        is_admin = False
        for g in request.identity["user"].groups :
            if g.flag == 'ADMIN' :
                is_admin = True
                break

        return { "result" : result , "values" : kw, "widget" : order_search_form , "printshops" : ps , "is_admin" : is_admin}


    @expose()
    def export( self, **kw ):
        ws = [OrderHeader.active == 0]
        if kw.get( "no", False ) : ws.append( OrderHeader.no.op( "ilike" )( "%%%s%%" % kw["no"] ) )
        if kw.get( "customerpo", False ) : ws.append( OrderHeader.customerpo.op( "ilike" )( "%%%s%%" % kw["customerpo"] ) )
        if kw.get( "vendorpo", False ) : ws.append( OrderHeader.vendorpo.op( "ilike" )( "%%%s%%" % kw["vendorpo"] ) )
        if kw.get( "status", False ) : ws.append( OrderHeader.status == kw["status"] )
        if kw.get( "printShopId", False ) : ws.append( OrderHeader.printShopId == kw["printShopId"] )
        if kw.get( "create_time_from", False ) : ws.append( OrderHeader.createTime >= kw["create_time_from"] )
        if kw.get( "create_time_to", False ) : ws.append( OrderHeader.createTime <= kw["create_time_from"] )
        if kw.get( "divisionId", False ) : ws.extend( [OrderHeader.id == OrderDetail.headerId, OrderDetail.active == ACTIVE, OrderDetail.divisionId == kw['divisionId']] )
        if kw.get( "brandId", False ) : ws.extend( [OrderHeader.id == OrderDetail.headerId, OrderDetail.active == ACTIVE, OrderDetail.brandId == kw['brandId']] )
        if kw.get( "categoryId", False ) : ws.extend( [OrderHeader.id == OrderDetail.headerId, OrderDetail.active == ACTIVE, OrderDetail.categoryId == kw['categoryId']] )

        if not has_permission( "MAIN_ORDERING_CHECKING_ALL" ): ws.append( OrderHeader.createById == request.identity["user"].user_id )

        data = []
        for h in  qry( OrderHeader ).filter( and_( *ws ) ).order_by( desc( OrderHeader.createTime ) ):
            data.append( map( lambda v : unicode( v or '' ), [ h.no, h.customerpo, h.vendorpo, "\n".join( h.items.split( "|" ) ) if h.items else '', h.createTime.strftime( "%Y/%m/%d %H:%M" ),
                                      h.createBy, h.totalQty, h.printShop, h.showStatus(),
                                      h.completeDate.strftime( "%Y/%m/%d %H:%M" ) if h.completeDate else '',
                                      h.courier, h.trackingNumber,
                                     ] ) )
        try:
            v = getExcelVersion()
            if not v : raise ReportGenerationException()
            if v <= "2003" :  # version below 2003
                templatePath = os.path.join( config.get( "public_dir" ), "TEMPLATE", "AEO_REPORT_TEMPLATE.xls" )
            else :  # version above 2003
                templatePath = os.path.join( config.get( "public_dir" ), "TEMPLATE", "AEO_REPORT_TEMPLATE.xlsx" )

            tempFileName, realFileName = self._getReportFilePath( templatePath )
            sdexcel = AEOReport( templatePath = tempFileName, destinationPath = realFileName )
            sdexcel.inputData( data )
            sdexcel.outputData()
        except:
            traceback.print_exc()
            logError()
            if sdexcel:sdexcel.clearData()
            raise ReportGenerationException()
        else:
            return serveFile( realFileName )



    def _getReportFilePath( self, templatePath ):
        current = dt.now()
        dateStr = current.strftime( "%Y%m%d" )
        fileDir = os.path.join( config.get( "public_dir" ), "aeo", dateStr )
        if not os.path.exists( fileDir ): os.makedirs( fileDir )
        v = getExcelVersion()
        if not v : raise ReportGenerationException()
        if v <= "2003" :  # version below 2003
            tempFileName = os.path.join( fileDir, "%s_%s_%d.xls" % ( request.identity["user"].user_name,
                                                               current.strftime( "%Y%m%d%H%M%S" ), random.randint( 0, 1000 ) ) )
            realFileName = os.path.join( fileDir, "%s_%s.xls" % ( request.identity["user"].user_name, current.strftime( "%Y%m%d%H%M%S" ) ) )
        else:
            tempFileName = os.path.join( fileDir, "%s_%s_%d.xlsx" % ( request.identity["user"].user_name,
                                                               current.strftime( "%Y%m%d%H%M%S" ), random.randint( 0, 1000 ) ) )
            realFileName = os.path.join( fileDir, "%s_%s.xlsx" % ( request.identity["user"].user_name, current.strftime( "%Y%m%d%H%M%S" ) ) )
        shutil.copy( templatePath, tempFileName )
        return tempFileName, realFileName



    @expose( 'rpac.templates.ordering.detail' )
    @paginate( "result", items_per_page = 20 )
    @tabFocus( tab_type = "main" )
    def detail( self, **kw ):
        hid = kw.get( 'id', None )
        if not hid :
            flash( "No ID provides!", "warn" )
            return redirect( '/ordering/index' )

        try:
            obj = qry( OrderHeader ).filter( and_( OrderHeader.active == 0 , OrderHeader.id == hid ) ).one()
        except:
            flash( "The record does not exist!", "warn" )
            return redirect( '/ordering/index' )

        return {
                'obj' : obj ,
                }




    @expose( 'rpac.templates.ordering.placeorder' )
    @tabFocus( tab_type = "main" )
    def placeorder( self , **kw ):
        locations = qry( PrintShop ).filter( and_( PrintShop.active == 0 ) ).order_by( PrintShop.name )
        address = qry( AddressBook ).filter( and_( AddressBook.active == 0, AddressBook.createById == request.identity['user'].user_id ) ).order_by( AddressBook.createTime ).all()
        values = {}
        if len( address ) > 0 :
            for f in ['shipCompany', 'shipAttn', 'shipAddress', 'shipAddress2', 'shipAddress3',
                      'shipCity', 'shipState', 'shipZip', 'shipCountry', 'shipTel', 'shipFax', 'shipEmail', 'shipRemark',
                      'billCompany', 'billAttn', 'billAddress', 'billAddress2', 'billAddress3',
                      'billCity', 'billState', 'billZip', 'billCountry', 'billTel', 'billFax', 'billEmail', 'billRemark'] :
                values[f] = unicode( getattr( address[0], f ) or '' )

        products = []
        for p in session.get( 'items', [] ) :
            p['productobj'] = qry( Product ).get( p['id'] )
            products.append( p )

        return {'locations' : locations ,
                'products' : products, 'address' : address,
                'values' : values,
                'address' : address,
                }


    @expose()
    def saveorder( self, **kw ):
        try:
            addressFields = [
                              'shipCompany', 'shipAttn', 'shipAddress', 'shipAddress2', 'shipAddress3', 'shipCity', 'shipState', 'shipZip', 'shipCountry', 'shipTel', 'shipFax', 'shipEmail', 'shipRemark',
                              'billCompany', 'billAttn', 'billAddress', 'billAddress2', 'billAddress3', 'billCity', 'billState', 'billZip', 'billCountry', 'billTel', 'billFax', 'billEmail', 'billRemark',
                             ]
            fields = [ 'customerpo', 'vendorpo', 'printShopId', 'shipInstructions', 'style']
            params = {}
            for f in addressFields: params[f] = kw.get( f, None ) or None
            if kw.get( 'addressID', None ) == 'OTHER': DBSession.add( AddressBook( **params ) )
            for f in fields: params[f] = kw.get( f, None ) or None
            if params['printShopId'] : params['printShopCopy'] = unicode( qry( PrintShop ).get( params['printShopId'] ) )

            hdr = OrderHeader( **params )
            DBSession.add( hdr )
            qtys, itemCodes = [], []
            for item in session.get( 'items' , [] ):
                params = {
                          'header' : hdr, 'product' : item['productobj'],
                          'qty' : item['qty'] or None,
                          }
                for f in ['divisionId', 'brandId', 'categoryId', 'itemCode', 'logo', 'size', 'content', 'coo',
                          'care', 'productType', 'highPrice', 'lowPrice', 'thumb', 'image', 'type'] :
                    params[f] = getattr( item['productobj'], f, None )

                if item.get( 'values', None ) or None : params['optionContent'] = json.dumps( item.get( 'values', [] ) )
                if item.get( 'optionstext', None ) or None : params['optionText'] = json.dumps( item['optionstext'] )
#                 params['layoutValue'] = json.dumps( self._setLayoutValue( item.get( 'values', [] ) ) )
                DBSession.add( OrderDetail( **params ) )
                qtys.append( item['qty'] )
                itemCodes.append( item['productobj'].itemCode )
            DBSession.flush()
            hdr.totalQty = sum( map( int, qtys ) )
            hdr.items = "|".join( itemCodes )
        except:
            transaction.doom()
            traceback.print_exc()
            flash( 'Error occur on the server side!', "warn" )
            return redirect( '/ordering/placeorder' )
        else:
            try:
                del session['items']
                session.save()
            except:
                pass
            return redirect( '/ordering/afterSaveOrder?id=%s' % hdr.id )




    def _genExcel( self, hdr ):
        v = getExcelVersion()
        if not v : raise ReportGenerationException()
        if v <= "2003" :  # version below 2003
            templatePath = os.path.join( config.get( "public_dir" ), "TEMPLATE", "AEO_DETAIL_TEMPLATE.xls" )
        else :  # version above 2003
            templatePath = os.path.join( config.get( "public_dir" ), "TEMPLATE", "AEO_DETAIL_TEMPLATE.xlsx" )

        current = dt.now()
        dateStr = current.strftime( "%Y%m%d" )
        fileDir = os.path.join( config.get( "public_dir" ), "excel", dateStr )
        if not os.path.exists( fileDir ): os.makedirs( fileDir )

        if v <= "2003" :  # version below 2003
            tempFileName = os.path.join( fileDir, "%s_%s_%d.xls" % ( request.identity["user"].user_name,
                                                               current.strftime( "%Y%m%d%H%M%S" ), random.randint( 0, 1000 ) ) )
            realFileName = os.path.join( fileDir, "%s_%s.xls" % ( request.identity["user"].user_name, current.strftime( "%Y%m%d%H%M%S" ) ) )
        else:
            tempFileName = os.path.join( fileDir, "%s_%s_%d.xlsx" % ( request.identity["user"].user_name,
                                                               current.strftime( "%Y%m%d%H%M%S" ), random.randint( 0, 1000 ) ) )
            realFileName = os.path.join( fileDir, "%s_%s.xlsx" % ( hdr.no, current.strftime( "%Y%m%d%H%M%S" ) ) )

        shutil.copy( templatePath, tempFileName )

        data = { 'createTime' : hdr.createTime.strftime( "%Y-%m-%d %H:%M" ) }
        for f in [ 'no', 'shipCompany', 'shipAttn', 'shipAddress', 'shipAddress2', 'shipAddress3',
                   'shipCity', 'shipState', 'shipZip', 'shipCountry', 'shipTel', 'shipFax',
                   'shipEmail', 'shipRemark',
                   'billCompany', 'billAttn', 'billAddress', 'billAddress2', 'billAddress3',
                   'billCity', 'billState', 'billZip', 'billCountry', 'billTel', 'billFax',
                   'billEmail', 'billRemark',
                   'customerpo', 'vendorpo', 'printShopCopy', 'shipInstructions', 'style' ]:
            data[f] = unicode( getattr( hdr, f ) or '' )

        data['details'] = [map( lambda v : unicode( v or '' ), [d.itemCode, d.division, d.brand, d.category, d.substrate, d.width,
                                                             '\n'.join( json.loads( d.optionText ) ) if d.optionText else '', d.qty,
                                                             ] ) for d in hdr.dtls]
        try:
            sdexcel = AEOOrder( templatePath = tempFileName, destinationPath = realFileName )
            sdexcel.inputData( data )
            sdexcel.outputData()
            return realFileName
        except Exception, e:
            traceback.print_exc()
            raise e


    @expose()
    def getexcel( self, **kw ):
        hid = kw.get( 'id', None )
        if not hid :
            flash( "No ID provided!" )
            return redirect( '/index' )

        hdr = DBSession.query( OrderHeader ).get( hid )
        xls = self._genExcel( hdr )
        return serveFile( unicode( xls ) )


    @expose()
    def afterSaveOrder( self, **kw ):
        _id = kw.get( 'id', None ) or None
        if not _id:
            flash( "No ID provided !", "warn" )
            return redirect( '/index' )

        try:
            hdr = qry( OrderHeader ).get( _id )
            #=======================================================================
            # generate excel
            #=======================================================================
            xls = self._genExcel( hdr )
            #=======================================================================
            # generate PDF
            #=======================================================================
            details = [( d.id, d.itemCode ) for d in hdr.dtls]
            pdf = gen_pdf( hdr.no, details )
            files1 = [pdf]
            files2 = [pdf, xls, ]

            #=======================================================================
            # send email to user
            #=======================================================================
            subject = "[AEO] Order(%s) is placed" % hdr.no
            content = [
                       "Dear User:",
                       "Order(%s) is placed, please check the below link to check the detail." % hdr.no,
                       "%s/ordering/detail?id=%s" % ( config.get( 'website_url', '' ), hdr.id ),
                       "Thanks.", "",
                       "*" * 80,
                       "This e-mail is sent by the r-pac American Eagle Outfitters ordering system automatically.",
                       "Please don't reply this e-mail directly!",
                       "*" * 80,
                       ]
            self._toVendor( hdr, subject, content, files1 )
            #=======================================================================
            # send email to print shop
            #=======================================================================
            self._toPrintshop( hdr, subject, content, files2 )
            flash( "Save the order successfully!", "ok" )
        except:
            traceback.print_exc()
            flash( "The service is not available now ,please try again later.", 'warn' )
            return redirect( '/ordering/index' )
        else:
            return redirect( '/ordering/detail?id=%s' % hdr.id )


    @expose()
    def cancelOrder( self, **kw ):
        _id = kw.get( "id", None ) or None
        if not _id :
            flash( "No ID provided!" )
            return redirect( '/ordering/index' )

        hdr = qry( OrderHeader ).get( _id )
        hdr.status = ORDER_CANCEL
        subject = "[AEO] Order(%s) is cancelled" % hdr.no
        content = [
                   "Dear User:",
                   "Order(%s) is cancelled." % hdr.no,
                   "Thanks.", "",
                   "*" * 80,
                   "This e-mail is sent by the r-pac American Eagle Outfitters ordering system automatically.",
                   "Please don't reply this e-mail directly!",
                   "*" * 80,
                   ]
        #=======================================================================
        # send email to user
        #=======================================================================
        self._toVendor( hdr, subject, content )
        #=======================================================================
        # send email to print shop
        #=======================================================================
        self._toPrintshop( hdr, subject, content )
        flash( "Cancel the order successfully!" )
        return redirect( '/ordering/index' )



    @expose( "json" )
    def ajaxOrderInfo( self, **kw ):
        hid = kw.get( 'id', None )
        if not hid : return {'flag' : 1 , 'msg' : 'No ID provided!'}
        try:
            data = []
            for d in qry( OrderDetail ).filter( and_( OrderDetail.active == 0, OrderDetail.headerId == hid ) ).order_by( OrderDetail.id ):
                data.append( {'id' : d.id, 'code' : d.itemCode , 'qty' : d.qty} )
            return {'flag' : 0, 'data' : data}
        except:
            traceback.print_exc()
            return {'flag' : 1 , 'msg' : 'Error occur on the server side!'}



    @expose( 'rpac.templates.ordering.manage_address' )
    @paginate( "result", items_per_page = 20 )
    @tabFocus( tab_type = "ship" )
    def manageAddress( self, **kw ):
        result = DBSession.query( AddressBook ).filter( and_( AddressBook.active == 0, AddressBook.createById == request.identity['user'].user_id ) ).order_by( desc( AddressBook.createTime ) )
        return {'result' : result}



    @expose( 'rpac.templates.ordering.edit_address' )
    @tabFocus( tab_type = "ship" )
    def editAddress( self, **kw ):
        _id = kw.get( 'id', None )
        if not _id :
            flash( 'No id provided!' , "warn" )
            return redirect( '/index' )

        obj = DBSession.query( AddressBook ).get( _id )
        values = {'id' : obj.id}
        for f in ['shipCompany', 'shipAttn', 'shipAddress', 'shipAddress2', 'shipAddress3',
                  'shipCity', 'shipState', 'shipZip', 'shipCountry', 'shipTel', 'shipFax', 'shipEmail', 'shipRemark',
                  'billCompany', 'billAttn', 'billAddress', 'billAddress2', 'billAddress3',
                  'billCity', 'billState', 'billZip', 'billCountry', 'billTel', 'billFax', 'billEmail', 'billRemark'] :
            values[f] = unicode( getattr( obj, f ) or '' )
        return {'values' : values}


    @expose()
    def saveAddress( self, **kw ):
        _id = kw.get( 'id', None )
        if not _id :
            flash( 'No id provided!', 'warn' )
            return redirect( '/ordering/manageAddress' )

        fields = ['shipCompany', 'shipAttn', 'shipAddress', 'shipAddress2', 'shipAddress3',
                  'shipCity', 'shipState', 'shipZip', 'shipCountry', 'shipTel', 'shipFax', 'shipEmail', 'shipRemark',
                  'billCompany', 'billAttn', 'billAddress', 'billAddress2', 'billAddress3',
                  'billCity', 'billState', 'billZip', 'billCountry', 'billTel', 'billFax', 'billEmail', 'billRemark']

        try:
            obj = DBSession.query( AddressBook ).get( _id )
            for f in fields : setattr( obj, f, kw.get( f, None ) or None )
            flash( 'Save the record successfully!', 'ok' )
        except:
            traceback.print_exc()
            flash( "The service is not available now ,please try again later.", 'warn' )
        return redirect( '/ordering/manageAddress' )


    @expose()
    def delAddress( self, **kw ):
        oid = kw.get( 'id', None )
        if not oid :
            flash( 'No id provided!', 'warn' )
            return redirect( '/ordering/manageAddress' )

        obj = DBSession.query( AddressBook ).get( oid )
        if not obj :
            flash( 'The record does not exist!', 'warn' )
            return redirect( '/ordering/manageAddress' )

        obj.active = 1
        flash( 'Update the record successfully!', 'ok' )
        return redirect( '/ordering/manageAddress' )



    @expose( 'json' )
    def ajaxAddress( self, **kw ):
        aid = kw.get( 'addressID', None )
        if not aid : return {'code' : 1 , 'msg' : 'No ID provided!'}

        obj = qry( AddressBook ).get( aid )
        if not obj : return {'code' : 1 , 'msg' : 'The record does not exist!'}

        result = {'code' : 0}
        for f in ["shipCompany", "shipAttn", "shipAddress", "shipAddress2", "shipAddress3", "shipCity", "shipState",
                  "shipZip", "shipCountry", "shipTel", "shipFax", "shipEmail", "shipRemark",
                  "billCompany", "billAttn", "billAddress", "billAddress2", "billAddress3", "billCity", "billState",
                  "billZip", "billCountry", "billTel", "billFax", "billEmail", "billRemark", ] :
            result[f] = unicode( getattr( obj, f ) or '' )
        return result



    @expose( 'json' )
    def ajaxChangeStatus( self, **kw ):
        _id, status = kw.get( 'id', None ) or None , kw.get( 'status', None ) or None
        if not _id or not status:
            return {'flag' : 1 , 'msg' : 'No enough parameter(s) provided!'}

        if status not in map( unicode, [ORDER_INPROCESS, ORDER_COMPLETE, ] ):
            return {'flag' : 1 , 'msg' : 'No such operation!'}

        try:
            hdr = qry( OrderHeader ).get( _id )

            if status == unicode( ORDER_INPROCESS ):
                so = kw.get( 'so', None ) or None
                if not so : return {'flag' : 1 , 'msg' : 'No enough parameter(s) provided!'}
                if hdr.status != ORDER_NEW:
                    return {'flag' : 1 , 'msg' : 'The record is not in NEW status!'}
                hdr.so, hdr.status = so, ORDER_INPROCESS
            elif status == unicode( ORDER_COMPLETE ):
                if hdr.status != ORDER_INPROCESS:
                    return {'flag' : 1 , 'msg' : 'The record is not in process status!'}
                hdr.status, hdr.completeDate = ORDER_COMPLETE, dt.now()
                hdr.courier, hdr.trackingNumber = kw.get( 'courier', None ) or None , kw.get( 'trackingNumber', None ) or None
#                 self._sendEmailToVendor( hdr )
#                 self._sendEmailToPrintshop( hdr )
        except:

            traceback.print_exc()
            return {'flag' : 1, 'msg' : 'Error occur on the sever side !'}
        return {'flag' : 0}



    def _sendEmailToVendor( self, hdr ):
        subject = "[AEO] Order(%s) is completed" % hdr.no
        content = [
                   "Dear User:",
                   "Order(%s) is completed, please check the below link to check the detail." % hdr.no,
                   "%s/ordering/detail?id=%s" % ( config.get( 'website_url', '' ), hdr.id ),
                   "Thanks.", "",
                   "*" * 80,
                   "This e-mail is sent by the r-pac American Eagle Outfitters ordering system automatically.",
                   "Please don't reply this e-mail directly!",
                   "*" * 80,
                   ]
        self._toVendor( hdr, subject, content )


    def _sendEmailToPrintshop( self, hdr ):
        subject = "[AEO] Order(%s) is completed" % hdr.no
        content = [
                   "Dear User:",
                   "Order(%s) is completed, please check the below link to check the detail." % hdr.no,
                   "%s/ordering/detail?id=%s" % ( config.get( 'website_url', '' ), hdr.id ),
                   "Thanks.", "",
                   "*" * 80,
                   "This e-mail is sent by the r-pac American Eagle Outfitters ordering system automatically.",
                   "Please don't reply this e-mail directly!",
                   "*" * 80,
                   ]
        self._toPrintshop( hdr, subject, content )


    def _toVendor( self, hdr , subject, content, files = [] ):
        defaultsendto = config.get( "default_email_sendto", "" ).split( ";" )
        if hdr.createBy.email_address:  to = hdr.createBy.email_address.split( ";" )
        else: to = []
        sendto = defaultsendto + to
        cc = config.get( "default_email_cc", "" ).split( ";" )
        if config.get( "sendout_email", None ) != 'F': sendEmail( DEFAULT_SENDER, sendto, subject, '\n'.join( content ), cc, files )


    def _toPrintshop( self, hdr, subject, content, files = [] ):
        defaultsendto = config.get( "default_email_sendto", "" ).split( ";" )
        if hdr.printShopId and hdr.printShop.email: to = hdr.printShop.email
        else: to = []
        sendto = defaultsendto + to
        cc = config.get( "default_email_cc", "" ).split( ";" )
        if config.get( "sendout_email", None ) != 'F': sendEmail( DEFAULT_SENDER, sendto, subject, '\n'.join( content ), cc, files )



    def _filterAndSorted( self, prefix, kw ):
        return sorted( filter( lambda ( k, v ): k.startswith( prefix ), kw.iteritems() ), cmp = lambda x, y:cmp( x[0], y[0] ) )


    #===========================================================================
    # new function  for phase 2
    #===========================================================================
    @expose( 'rpac.templates.ordering.listItems' )
    @paginate( "result", items_per_page = 20 )
    @tabFocus( tab_type = "main" )
    def listItems( self, **kw ):
        ws = [Product.active == ACTIVE]
        if kw.get( "itemCode", None ) : ws.append( Product.itemCode.op( "ilike" )( "%%%s%%" % kw['itemCode'] ) )
        if kw.get( "divisionId", None ) : ws.append( Product.divisionId == kw['divisionId'] )
        if kw.get( "brandId", None ) : ws.append( Product.brandId == kw['brandId'] )
        if kw.get( "categoryId", None ) : ws.append( Product.categoryId == kw['categoryId'] )
        products = qry( Product ).filter( and_( *ws ) ).order_by( Product.itemCode )
        return {'result' : products, 'values' : kw, "widget" : product_search_form }


    def _getProductInfo( self, obj ):
        options = {}
        product = {'id' : obj.id , 'type' : obj.type}
        _m = lambda t : [{ 'key' : o.id, 'value' : unicode( o ) } for o in qry( Care ).filter( and_( Care.active == ACTIVE, Care.category == t ) ).order_by( Care.english )]
        if obj.type == 'GUARANTEECARD':
            options['content'] = {
                                  'name' : 'content' ,
                                  'fabrics' : [{'key' : f.id, 'value' : unicode( f )} for f in  qry( Fibers ).filter( and_( Fibers.active == ACTIVE ) ).order_by( Fibers.english )],
                                  'parts' : [{'key' : p.id , 'value' : unicode( p )} for p in qry( GarmentPart ).filter( and_( GarmentPart.active == ACTIVE ) ).order_by( GarmentPart.english )],
                                  }
            options['coo'] = {
                                'name' : 'COO',
                                'values' : [{'key' : o.id, 'value' : unicode( o )} for o in qry( COO ).filter( and_( COO.active == ACTIVE ) ).order_by( COO.english )]
                                }
            options['care'] = { 'name' : 'Care Instruction', 'values' : {}}
            for k in ['BLEACH', 'DRY', 'DRYCLEAN', 'IRON', 'SPECIALCARE', 'WASH'] : options['care']['values'][k] = _m( k )
        else:
            if obj.logo == 'YES' : pass
            if obj.size == 'YES' :
                ss = []
                for s in qry( Size ).filter( and_( Size.active == 0, Size.brandId == obj.brandId, Size.categoryId == obj.categoryId ) ).order_by( Size.us_size ):
                    ss.append( {'key' : s.id, 'value' : unicode( s )} )
                options['size'] = {
                                   'name' : 'size' ,
                                   'values' : ss
                                   }
            if obj.content == 'YES' :
                options['content'] = {
                                      'name' : 'content' ,
                                      'fabrics' : [{'key' : f.id, 'value' : unicode( f )} for f in  qry( Fibers ).filter( and_( Fibers.active == ACTIVE ) ).order_by( Fibers.english )],
                                      'parts' : [{'key' : p.id , 'value' : unicode( p )} for p in qry( GarmentPart ).filter( and_( GarmentPart.active == ACTIVE ) ).order_by( GarmentPart.english )],
                                      }
            if obj.coo == 'YES' :
                options['coo'] = {
                                'name' : 'COO',
                                'values' : [{'key' : o.id, 'value' : unicode( o )} for o in qry( COO ).filter( and_( COO.active == ACTIVE ) ).order_by( COO.english )]
                                }
            if obj.care == 'YES' :
                options['care'] = { 'name' : 'Care Instruction', 'values' : {}}
                for k in ['BLEACH', 'DRY', 'DRYCLEAN', 'IRON', 'SPECIALCARE', 'WASH'] : options['care']['values'][k] = _m( k )
        return product, options


    @expose( 'json' )
    def ajaxProductInfo( self, **kw ):
        _id = kw.get( 'id', None ) or None
        if not _id: return {'flag' : 1 , 'msg' : 'No ID provided!'}

        try:
            obj = qry( Product ).get( _id )
            product, options = self._getProductInfo( obj )
            return {'flag' : 0 , 'product' : product, 'options' : options}
        except:
            traceback.print_exc()
            return {'flag' : 1, 'msg' : 'Error occur on the sever side !'}


    '''
    def _formatKW( self, kw ):
        values, optionstext = [], []
        for k, v in self._filterAndSorted( "option_", kw ):
            val, text = v.split( "|" )
            values.append( { 'key' : k, 'value' : val, 'text' : text } )
            if k.startswith( 'option_a_' ) :  # SELECT OR TEXT
                oid = k.split( "_" )[2]
                option = qry( Option ).get( oid )
                if option.master in ['CO', 'Care']:
                    clz = getattr( DBModel, option.master )
                    obj = qry( clz ).get( val )
                    if obj.english.upper() == 'NONE':
                        optionstext.append( "%s : %s" % ( option.name, '' ) )
                    elif option.language and 'S' not in option.language.split( "|" ):  # this option just need the english
                        optionstext.append( "%s : %s" % ( option.name, obj.english ) )
                    else:
                        optionstext.append( "%s : [English]%s [Spanish]%s" % ( option.name, obj.english, obj.spanish or '' ) )
                else:
                    optionstext.append( "%s : %s" % ( option.name, text ) )
            elif k.startswith( 'option_as_' ) :  # SELECT + TEXT
                oid = k.split( "_" )[2]
                option = qry( Option ).get( oid )
                obj = qry( Fibers ).get( val )
                e = obj.english if obj.english.upper() != 'NONE' else ''
                s = obj.spanish if obj.english.upper() != 'NONE' else ''

                k2 = k.replace( '_as_', '_at_' )
                v2 = kw.get( k2, '' ) or ''
                if option.language and 'S' not in option.language.split( "|" ):  # this option just need the english
                    optionstext.append( "%s : %s - %s" % ( option.name, e, v2.split( '|' )[0] ) )
                else:
                    optionstext.append( "%s : [English]%s [Spanish]%s [Percentage]%s" % ( option.name, e, s or '', v2.split( '|' )[0] ) )
        return values, optionstext
    '''

    def _formatKW( self, kw, obj ):
        values, optionstext = [], []

        _v = lambda v : v.split( "|" )

        def _g( ps ):
            for prefix in ps:
                for ( pk, pv ) in self._filterAndSorted( prefix, kw ) :
                    if not pv : continue
                    val , txt = _v( pv )
                    values.append( {"key" : pk, "value" : val, "text" : txt} )

        def _o( name, label ):
            v = kw.get( name, None ) or None
            if v:
                val, txt = _v( v )
                values.append( {"key" : name, "value" : val, "text" :txt} )
                optionstext.append( "%s : %s" % ( label, txt ) )

        def _handleContent():
            parts = self._filterAndSorted( "option_part_", kw )
            onlys = self._filterAndSorted( "option_only_", kw )
            for ( pk, pcol ), ( ok, onlycol ) in zip( parts, onlys ):
                if not pcol or not onlycol : continue
                partval, parttxt = _v( pcol )
                onlyval, onlytxt = _v( onlycol )

                values.append( {"key" : pk, "value" : partval, "text" : parttxt} )
                values.append( {"key" : ok, "value" : onlyval, "text" : onlytxt} )

                pobj = qry( GarmentPart ).get( partval )
                otxt = "[Garment Part : %s][%s]" % ( _v( pobj.getAllTranslation() ), _v( onlycol )[-1] )
                _id = pk.split( "_" )[-1]
                contents = self._filterAndSorted( "option_content_%s_" % _id, kw )
                pers = self._filterAndSorted( "option_percentage_%s_" % _id, kw )
                for ( contentkey, contentcol ), ( perkey, percol ) in zip( contents, pers ):
                    if not contentcol or not percol : continue
                    contentval, contenttxt = _v( contentcol )
                    perval, pertxt = _v( percol )
                    cobj = qry( Fibers ).get( contentval )
                    otxt += '[Content : %s - %s%%]' % ( cobj.getAllTranslation(), pertxt )

                    values.append( {"key" : contentkey, "value" : contentval, "text" : contenttxt} )
                    values.append( {"key" : perkey, "value" : perval, "text" : pertxt} )
                optionstext.append( otxt )

        def _handleCare():
            for( f1, f2 ) in [( 'WASH', 'Wash' ), ( 'BLEACH', 'Bleach' ), ( 'DRY', 'Dry' ),
                                  ( 'IRON', 'Iron' ), ( 'DRYCLEAN', 'Dry Clean' ), ( 'SPECIALCARE', "Special Care" )]:
                for k, v in self._filterAndSorted( "option_%s" % f1, kw ):
                    if not v : continue
                    cid, ctxt = _v( v )
                    c = qry( Care ).get( cid )
                    values.append( {"key" :k, "value" : cid, "text" : ctxt} )
                    optionstext.append( "Care Instruction - %s : %s" % ( f2, c.getAllTranslation() ) )


        if obj.type == 'GUARANTEECARD':  # it's a Guarant Eecard
            for n, l in [( 'option_ProductStandardName', 'Product Standard Name' ), ( 'option_ChinaSize', 'China Size' ),
                         ( 'option_ProductStandard', 'Product Standard' ), ( 'option_QualityGrade', 'Quality Grade' ),
                         ( 'option_SafetyStandard', 'Safety Standard' ), ( 'option_QualifiedCertificate', 'Qualified Certificate' ),
                         ( 'option_ChinaAddress', 'China Address' ), ( 'option_coo', 'Country of Origin' ),
                        ]: _o( n, l )
            _handleCare()
            _handleContent()
        else:  # it's normal card
            if obj.logo == 'YES' :
                pass
            if obj.size == 'YES' :
                ss = self._filterAndSorted( 'option_size_', kw )
                qs = self._filterAndSorted( 'option_qty_', kw )
                for ( sk, sv ), ( qk, qv ) in zip( ss, qs ):
                    if not sv or not qv : continue
                    svv, svt = _v( sv )
                    qvv, qvt = _v( qv )
                    values.append( {"key" : sk, "value" : svv, "text" :svt} )
                    values.append( {"key" : qk, "value" : qvv, "text" :qvt} )
                    optionstext.append( 'Size : %s , Qty : %s' % ( svt, qvt ) )
            else: _o( [( 'option_qty', 'Qty' ), ] )
            if obj.content == 'YES' : _handleContent()
            if obj.coo == 'YES' : _o( "option_coo", 'Country of Origin' )
            if obj.care == 'YES' : _handleCare()
        return values, optionstext


    @expose( 'json' )
    def ajaxAddtoCart( self, **kw ):
        _id = kw.get( 'id', None ) or None
        if not _id : return {'flag' : 1 , 'msg' : 'No ID provided!'}

        try:
            items = session.get( 'items', [] )
            tmp = {
                   '_k' : "%s%s" % ( dt.now().strftime( "%Y%m%d%H%M%S" ), random.randint( 100, 10000 ) ) ,
                   'id' : _id,
                   }
            qs = []
            for qk, qv in self._filterAndSorted( "option_qty", kw ):
                if not qv : continue
                q, _ = qv.split( "|" )
                if not q.isdigit() : continue
                qs.append( int( q ) )
            tmp['qty'] = sum( qs ) if qs else 0

            p = qry( Product ).get( _id )
            tmp['values'], tmp['optionstext'] = self._formatKW( kw, p )
            items.append( tmp )
            session['items'] = items
            session.save()
            return {'flag' : 0 , 'total' : len( session['items'] )}
        except:
            traceback.print_exc()
            return {'flag' : 1, 'msg':'Error occur on the sever side!'}


    @expose( 'json' )
    def ajaxSavetoCart( self, **kw ):
        _k = kw.get( "_k", None )
        if not _k : return {'flag' : 1 , 'msg' : 'No ID provided!'}

        try:
            items = session.get( 'items', [] )
            for index, item in enumerate( items ):
                if item['_k'] != _k : continue
                p = qry( Product ).get( item['id'] )
                item['values'], item['optionstext'] = self._formatKW( kw , p )
                qs = []
                for qk, qv in self._filterAndSorted( "option_qty", kw ):
                    if not qv : continue
                    q, _ = qv.split( "|" )
                    if not q.isdigit() : continue
                    qs.append( int( q ) )
                item['qty'] = sum( qs ) if qs else 0
                items[index] = item
                session['items'] = items
                session.save()
                return {'flag' : 0 , 'optionstext' : item['optionstext'], }
        except:
            traceback.print_exc()
            return {'flag' : 1 , 'msg' : 'Error occur on the sever side!'}
        return {'flag' : 1 , 'msg' : 'No such item!'}



    @expose( 'json' )
    def ajaxRemoveItem( self, **kw ):
        _k = kw.get( "_k", None )
        if not _k : return {'flag' : 1 , 'msg' : 'No ID provided!'}

        try:
            session['items'] = filter( lambda item : item['_k'] != _k, session.get( 'items', [] ) )
            session.save()
            return {'flag' : 0 }
        except:
            traceback.print_exc()
            return {'flag' : 1, 'msg':'Error occur on the sever side!'}


    @expose( 'json' )
    def ajaxEditItem( self, **kw ):
        _k = kw.get( '_k', None ) or None
        if not _k: return {'flag' : 1 , 'msg' : 'No ID provided!'}
        try:
            for s in session.get( 'items', [] ):
                if s['_k'] != _k : continue
                obj = qry( Product ).get( s['id'] )
                product, options = self._getProductInfo( obj )
                product['qty'] = s.get( 'qty', '' )
                print "*-" * 10
                print s.get( 'values', [] )
                print "^-" * 10

                return {'flag' : 0 , 'product' : product, 'options' : options , 'values' : s.get( 'values', [] ) }
        except:
            traceback.print_exc()
            return {'flag' : 1, 'msg' : 'Error occur on the sever side !'}
        return {'flag' : 1 , 'msg' : 'No such item!'}


    @expose()
    def removeall( self, **kw ):
        try:
            del session['items']
            session.save()
        except:
            pass
        return redirect( '/ordering/listItems' )



    def _setLayoutValue( self , values ):
        layout = {}
        '''
        for v in values :
            gs = v['key'].split( "_" )
            f, oid = gs[1], gs[2]
            if f == 'at' : continue  # it's percentage ,will add in the fibers
            option = qry( Option ).get( oid )

            if option.layoutKey in ['TRACKING', 'DESC', 'SKU', 'PRICE', 'NAME', 'SIZE', 'SKU', 'WPL']:
                lv = v['value']
            elif option.layoutKey in ['DOT', ]:
                d = qry( DotPantone ).get( v['value'] )
                lv = {'value' : v['text'] , 'css' : d.css}
            elif option.layoutKey in ['DATECODE', 'CATEGORY', ]:
                lv = v['text']
            elif option.layoutKey in ['CO', 'WASH', 'BLEACH', 'IRON', 'DRY', 'DRYCLEAN', 'SPECIALCARE']:
                if option.layoutKey == 'CO':
                    k = qry( CO ).get( v['value'] )
                else:
                    k = qry( Care ).get( v['value'] )
                if k.english.upper() == 'NONE':
                    lv = {'english' : '', 'spanish' : ''}
                else:
                    lv = {'english' : k.english, 'spanish' : k.spanish}
            elif option.layoutKey in ['FIBERS', ]:
                k = qry( Fibers ).get( v['value'] )
                if k.english.upper() == 'NONE':
                    lv = {'english' : '', 'spanish' : ''}
                else:
                    lv = {'english' : k.english, 'spanish' : k.spanish}

                pkey = v['key'].replace( "_as_", "_at_" )
                for tmp in values :
                    if tmp['key'] == pkey :
                        lv['percent'] = tmp['value']
                        break;
            if option.layoutKey not in layout:
                layout[option.layoutKey] = {'values' : [lv]}
            else:
                layout[option.layoutKey]['values'].append( lv )
            '''
        return layout



