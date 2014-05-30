# -*- coding: utf-8 -*-
'''
Created on 2014-2-17
@author: CL.lam
'''
from sqlalchemy.sql.expression import and_
from rpac.widgets.components import RPACForm, RPACText, RPACCalendarPicker, \
    RPACSelect
from rpac.model import qry, PrintShop, Division, Brand, Category

from rpac.constant import ORDER_NEW, ORDER_INPROCESS, ORDER_COMPLETE, ORDER_CANCEL



__all__ = ['product_search_form', 'order_search_form', ]


def _getMaster( clz, orderByColumn = "name" ):
    def _f():
        return [( "", "" ), ] + [( unicode( p.id ), unicode( p ) ) for p in qry( clz ).filter( and_( clz.active == 0 ) ).order_by( getattr( clz, orderByColumn ) ).all()]
    return _f


# def getPrintShop():
#     return [( "", "" ), ] + [( unicode( p.id ), unicode( p ) ) for p in qry( PrintShop ).filter( and_( PrintShop.active == 0 ) ).order_by( PrintShop.name ).all()]

class ProductSearchForm( RPACForm ):
    fields = [
              RPACText( "itemCode", label_text = "Item Code" ),
              RPACSelect( "divisionId", label_text = "Division", options = _getMaster( Division ) ),
              RPACSelect( "brandId", label_text = "Brand", options = _getMaster( Brand ) ),
              RPACSelect( "categoryId", label_text = "Category", options = _getMaster( Category ) ),
              ]

product_search_form = ProductSearchForm()



class OrderSearchForm( RPACForm ):
    fields = [
              RPACText( "no", label_text = "Job No" ),
              RPACText( "customerpo", label_text = "AEO PO#" ),
              RPACText( "vendorpo", label_text = "Vendor PO" ),
              RPACCalendarPicker( "create_time_from", label_text = "Create Date(from)" ),
              RPACCalendarPicker( "create_time_to", label_text = "Create Date(to)" ),
              RPACSelect( "status", label_text = "Status", options = [( "", "" ), ( str( ORDER_NEW ), "New" ),
                                                                     ( str( ORDER_INPROCESS ), "In Process" ),
                                                                     ( str( ORDER_COMPLETE ), "Completed" ),
                                                                     ( str( ORDER_CANCEL ), "Canelled" ),
                                                                     ] ),

              RPACSelect( "printShopId", label_text = "r-pac production location", options = _getMaster( PrintShop ) ),
              RPACSelect( "divisionId", label_text = "Division", options = _getMaster( Division ) ),
              RPACSelect( "brandId", label_text = "Brand", options = _getMaster( Brand ) ),
              RPACSelect( "categoryId", label_text = "Category", options = _getMaster( Category ) ),
              ]

order_search_form = OrderSearchForm()
