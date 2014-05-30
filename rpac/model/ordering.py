# -*- coding: utf-8 -*-
'''
Created on 2014-4-9

@author: CL.lam
'''

from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import DateTime, Integer, Text, Numeric
from sqlalchemy.orm import relation, synonym, backref
from sqlalchemy.ext.declarative import declared_attr

from rpac.model import DeclarativeBase
from interface import SysMixin, nextVal
from master import PrintShop, ProductMixin, Product, Division
from rpac.constant import ORDER_COMPLETE, ORDER_NEW, ORDER_INPROCESS, \
    ORDER_CANCEL


__all__ = ['OrderHeader', 'OrderDetail', 'AddressBook']



class OrderHeader( DeclarativeBase , SysMixin ):
    __tablename__ = 'ordering_order_header'

    id = Column( Integer, primary_key = True )
    no = Column( "no", Text )

    shipCompany = Column( "ship_company", Text, default = None )
    shipAttn = Column( "ship_attn", Text, default = None )
    shipAddress = Column( "ship_address", Text, default = None )
    shipAddress2 = Column( "ship_address2", Text, default = None )
    shipAddress3 = Column( "ship_address3", Text, default = None )
    shipCity = Column( "ship_city", Text, default = None )
    shipState = Column( "ship_state", Text, default = None )
    shipZip = Column( "ship_zip", Text, default = None )
    shipCountry = Column( "ship_country", Text, default = None )
    shipTel = Column( "ship_tel", Text, default = None )
    shipFax = Column( "ship_fax", Text, default = None )
    shipEmail = Column( "ship_email", Text, default = None )
    shipRemark = Column( "ship_remark", Text, default = None )
    shipInstructions = Column( "ship_instructions", Text )

    billCompany = Column( "bill_company", Text, default = None )
    billAttn = Column( "bill_attn", Text, default = None )
    billAddress = Column( "bill_address", Text, default = None )
    billAddress2 = Column( "bill_address2", Text, default = None )
    billAddress3 = Column( "bill_ddress3", Text, default = None )
    billCity = Column( "bill_city", Text, default = None )
    billState = Column( "bill_state", Text, default = None )
    billZip = Column( "bill_zip", Text, default = None )
    billCountry = Column( "bill_country", Text, default = None )
    billTel = Column( "bill_tel", Text, default = None )
    billFax = Column( "bill_fax", Text, default = None )
    billEmail = Column( "bill_email", Text, default = None )
    billRemark = Column( "bill_remark", Text, default = None )

    customerpo = Column( "customerpo", Text )
    vendorpo = Column( "vendorpo", Text )
    style = Column( "style", Text )
    printShopId = Column( "printshop_id", Integer, ForeignKey( 'master_print_shop.id' ) )
    printShop = relation( PrintShop, primaryjoin = PrintShop.id == printShopId )
    printShopCopy = Column( "printshop_copy", Text, default = None )

    items = Column( "items", Text )
    so = Column( Text )
    completeDate = Column( 'complete_date', DateTime )
    totalQty = Column( "total_qty" , Text )
#     shipQty = Column( "ship_qty", Text )
    courier = Column( "courier", Text )
    trackingNumber = Column( "tracking_number", Text )
    status = Column( "status", Integer, default = ORDER_NEW )

    def __unicode__( self ): return self.no
    def __str__( self ): return self.no

    def __init__( self, *args, **kwargs ):
        super( self.__class__, self ).__init__( *args, **kwargs )
        seq = nextVal( 'ordering_header_seq' )
        self.no = 'AEOPO%.9d' % seq

    def showStatus( self ):
        return {
                ORDER_NEW : 'New', ORDER_INPROCESS : 'In Process' , ORDER_COMPLETE : 'Completed',
                ORDER_CANCEL : 'Cancelled',
                }.get( self.status, '' )



class OrderDetail( DeclarativeBase , SysMixin, ProductMixin ):
    __tablename__ = 'ordering_order_detail'

    id = Column( Integer, primary_key = True )

    headerId = Column( "header_id", Integer, ForeignKey( 'ordering_order_header.id' ) )
    header = relation( OrderHeader, backref = backref( "dtls", order_by = id ), primaryjoin = "and_(OrderHeader.id == OrderDetail.headerId,OrderDetail.active == 0)" )

    productId = Column( "product_id", Integer, ForeignKey( 'master_product.id' ) )
    product = relation( Product, primaryjoin = Product.id == productId )

    optionContent = Column( "option_content", Text )
    optionText = Column( "option_text", Text )

    qty = Column( Integer, default = 0 )
    shipQty = Column( "ship_qty", Text )

    layoutValue = Column( "layout_value", Text )



class AddressBook( DeclarativeBase, SysMixin ):
    __tablename__ = 'ordering_address_book'

    id = Column( Integer, primary_key = True )
    shipCompany = Column( "ship_company", Text, default = None )
    shipAttn = Column( "ship_attn", Text, default = None )
    shipAddress = Column( "ship_address", Text, default = None )
    shipAddress2 = Column( "ship_address2", Text, default = None )
    shipAddress3 = Column( "ship_address3", Text, default = None )
    shipCity = Column( "ship_city", Text, default = None )
    shipState = Column( "ship_state", Text, default = None )
    shipZip = Column( "ship_zip", Text, default = None )
    shipCountry = Column( "ship_country", Text, default = None )
    shipTel = Column( "ship_tel", Text, default = None )
    shipFax = Column( "ship_fax", Text, default = None )
    shipEmail = Column( "ship_email", Text, default = None )
    shipRemark = Column( "ship_remark", Text, default = None )

    billCompany = Column( "bill_company", Text, default = None )
    billAttn = Column( "bill_attn", Text, default = None )
    billAddress = Column( "bill_address", Text, default = None )
    billAddress2 = Column( "bill_address2", Text, default = None )
    billAddress3 = Column( "bill_ddress3", Text, default = None )
    billCity = Column( "bill_city", Text, default = None )
    billState = Column( "bill_state", Text, default = None )
    billZip = Column( "bill_zip", Text, default = None )
    billCountry = Column( "bill_country", Text, default = None )
    billTel = Column( "bill_tel", Text, default = None )
    billFax = Column( "bill_fax", Text, default = None )
    billEmail = Column( "bill_email", Text, default = None )
    billRemark = Column( "bill_remark", Text, default = None )

