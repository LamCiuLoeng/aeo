# -*- coding: utf-8 -*-
'''
Created on 2014-4-9

@author: CL.lam
'''
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Integer, Text, Numeric
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import synonym, relation
from interface import SysMixin
from rpac.model import DeclarativeBase


__all__ = ['Division', 'Brand', 'Category', 'Product', 'Fibers', 'GarmentPart', 'COO', 'Care', 'PrintShop', 'Size']


class Division( DeclarativeBase , SysMixin ):
    __tablename__ = 'master_division'

    id = Column( Integer, primary_key = True )
    name = Column( Text )

    @property
    def value( self ): return self.name

    def __unicode__( self ): return self.name
    def __str__( self ): return self.name


class Brand( DeclarativeBase , SysMixin ):
    __tablename__ = 'master_brand'

    id = Column( Integer, primary_key = True )
    name = Column( Text )

    @property
    def value( self ): return self.name

    def __unicode__( self ): return self.name
    def __str__( self ): return self.name


class Category( DeclarativeBase , SysMixin ):
    __tablename__ = 'master_category'

    id = Column( Integer, primary_key = True )
    name = Column( Text )

    @property
    def value( self ): return self.name

    def __unicode__( self ): return self.name
    def __str__( self ): return self.name


class ProductMixin( object ):

    @declared_attr
    def divisionId( clz ): return Column( "division_id", Integer, ForeignKey( 'master_division.id' ) )
    @declared_attr
    def division( clz ): return relation( Division )

    @declared_attr
    def brandId( clz ) : return Column( "brand_id", Integer, ForeignKey( 'master_brand.id' ) )
    @declared_attr
    def brand( clz ) : return relation( Brand )

    @declared_attr
    def categoryId( clz ) : return Column( "category_id", Integer, ForeignKey( 'master_category.id' ) )
    @declared_attr
    def category( clz ) : return relation( Category )

    itemCode = Column( "item_code", Text )
    productType = Column( "product_type", Text )
    logo = Column( Text )
    size = Column( Text )
    content = Column( Text )
    coo = Column( Text )
    care = Column( Text )
    highPrice = Column( "high_price", Numeric( 15, 2 ), default = None )
    lowPrice = Column( "low_price", Numeric( 15, 2 ), default = None )
    thumb = Column( Text )  # the thumb image's URL
    image = Column( Text )  # the product image's URL
    type = Column( Text )


class Product( DeclarativeBase , SysMixin , ProductMixin ):
    __tablename__ = 'master_product'

    id = Column( Integer, primary_key = True )

    def __unicode__( self ): return self.itemCode
    def __str__( self ): return self.itemCode


class Size( DeclarativeBase, SysMixin ):
    __tablename__ = 'master_size'

    id = Column( Integer, primary_key = True )

#     @declared_attr
#     def brandId( clz ) : return Column( "brand_id", Integer, ForeignKey( 'master_brand.id' ) )
#     @declared_attr
#     def brand( clz ) : return relation( Brand )


    brandId = Column( "brand_id", Integer, ForeignKey( 'master_brand.id' ) )
    brand = relation( Brand )

#     @declared_attr
#     def categoryId( clz ) : return Column( "category_id", Integer, ForeignKey( 'master_category.id' ) )
#     @declared_attr
#     def category( clz ) : return relation( Category )


    categoryId = Column( "category_id", Integer, ForeignKey( 'master_category.id' ) )
    category = relation( Category )

    us_size = Column( Text )
    ca_size = Column( Text )
    mx_size = Column( Text )
    uk_size = Column( Text )
    cn_size = Column( Text )

    def __unicode__( self ): return self.us_size
    def __str__( self ): return self.us_size


class TranslateMixin( object ):
    english = Column( Text )
    french_canadian = Column( Text )
    spanish_mx = Column( Text )
    spanish_latin = Column( Text )
    russian = Column( Text )
    french = Column( Text )
    arabic = Column( Text )
    japanese = Column( Text )
    hebrew = Column( Text )
    turkish = Column( Text )
    polish = Column( Text )
    chinese_simple = Column( Text )
    bahasa = Column( Text )
    german = Column( Text )
    dutch = Column( Text )
    hindi = Column( Text )

    @property
    def value( self ): return self.english

    def __unicode__( self ): return self.english
    def __str__( self ): return self.english

    def getAllTranslation( self ):
        return "/".join( [getattr( self, attr, '' ) or '' for attr in ['english', 'french_canadian', 'spanish_mx',
                                                                       'spanish_latin', 'russian', 'french', 'arabic',
                                                                       'japanese', 'hebrew', 'turkish', 'polish', 'chinese_simple',
                                                                       'bahasa', 'german', 'dutch', 'hindi']] )


class Fibers( DeclarativeBase , SysMixin , TranslateMixin ):
    __tablename__ = 'master_fibers'

    id = Column( Integer, primary_key = True )



class GarmentPart( DeclarativeBase , SysMixin, TranslateMixin ):
    __tablename__ = 'master_garment_part'

    id = Column( Integer, primary_key = True )


class COO( DeclarativeBase , SysMixin, TranslateMixin ):
    __tablename__ = 'master_coo'

    id = Column( Integer, primary_key = True )



class Care( DeclarativeBase , SysMixin, TranslateMixin ):
    __tablename__ = 'master_care'

    id = Column( Integer, primary_key = True )
    category = Column( Text )  # BLEACH,DRY,DRYCLEAN,IRON,SPECIALCARE,WASH

    def showType( self ):
        return {'WASH' : "Wash", 'BLEACH': "Bleach", 'DRY':"Dry", 'IRON':"Iron", 'DRYCLEAN':"Dry Clean", 'SPECIALCARE':"Special Care"}.get( self.category, '' )


class PrintShop( DeclarativeBase , SysMixin ):
    __tablename__ = 'master_print_shop'

    id = Column( Integer, primary_key = True )
    name = Column( Text )
    _email = Column( "email", Text )


    def __unicode__( self ): return self.name
    def __str__( self ): return self.name


    def _getEmail( self ):
        if not self._email : return []
        return self._email.split( ";" )

    def _setEmail( self, s ): self._email = s

    @declared_attr
    def email( self ): return synonym( '_email', descriptor = property( self._getEmail, self._setEmail ) )
