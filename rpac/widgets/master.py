# -*- coding: utf-8 -*-
'''
Created on 2014-3-5
@author: CL.lam
'''
from sqlalchemy.sql.expression import and_
from rpac.widgets.components import RPACForm, RPACText, RPACCalendarPicker, \
    RPACSelect, RPACHidden
from rpac.model import Product, DBSession, qry, Brand, Division, Category


__all__ = ['master_search_form1', 'master_search_form2', ]


class MasterSearchForm1( RPACForm ):
    fields = [
              RPACText( "name", label_text = "Name" ),
              RPACCalendarPicker( "create_time_from", label_text = "Create Date(from)" ),
              RPACCalendarPicker( "create_time_to", label_text = "Create Date(to)" ),
              RPACHidden( 't' ),
              ]

master_search_form1 = MasterSearchForm1()



class MasterSearchForm2( RPACForm ):
    fields = [
              RPACText( "english", label_text = "English Term" ),
              RPACCalendarPicker( "create_time_from", label_text = "Create Date(from)" ),
              RPACCalendarPicker( "create_time_to", label_text = "Create Date(to)" ),
              RPACHidden( 't' ),
              ]

master_search_form2 = MasterSearchForm2()



class MasterSearchForm3( RPACForm ):
    fields = [
              RPACText( "english", label_text = "English Term" ),
              RPACCalendarPicker( "create_time_from", label_text = "Create Date(from)" ),
              RPACCalendarPicker( "create_time_to", label_text = "Create Date(to)" ),
              RPACSelect( "category", label_text = "Category", options = [( "", "" ), ( 'WASH', "Wash" ), ( 'BLEACH', "Bleach" ),
                                                                     ( 'DRY', "Dry" ), ( 'IRON', "Iron" ),
                                                                     ( 'DRYCLEAN', "Dry Clean" ), ( 'SPECIALCARE', "Special Care" ),
                                                                     ] ),
              RPACHidden( 't' ),
              ]

master_search_form3 = MasterSearchForm3()


def getOptions(clz):
    def func():
        return [("",""),]+[(unicode(b.id),unicode(b)) for b in qry(clz).order_by(clz.name).all()]
    return func


class MasterSearchForm4( RPACForm ):
    fields = [
              RPACText( "itemCode", label_text = "Item Code" ),
              RPACSelect( "brand", label_text = "Brand", options = getOptions(Brand)),
              RPACSelect( "division", label_text = "Division", options = getOptions(Division)),
              RPACSelect( "category", label_text = "Category", options = getOptions(Category)),
              RPACCalendarPicker( "create_time_from", label_text = "Create Date(from)" ),
              RPACCalendarPicker( "create_time_to", label_text = "Create Date(to)" ),
              RPACHidden( 't' ),
              ]

master_search_form4 = MasterSearchForm4()


class MasterSearchForm5( RPACForm ):
    fields = [
              RPACSelect( "brand", label_text = "Brand", options = getOptions(Brand)),
              RPACSelect( "category", label_text = "Category", options = getOptions(Category)),
              RPACText( "us_size", label_text = "US Size" ),
              RPACCalendarPicker( "create_time_from", label_text = "Create Date(from)" ),
              RPACCalendarPicker( "create_time_to", label_text = "Create Date(to)" ),
              RPACHidden( 't' ),
              ]

master_search_form5 = MasterSearchForm5()
