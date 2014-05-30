# encoding: utf-8
'''
Created on 2014-4-16

@author: CL.lam
'''

import os
from sqlalchemy import Column
from sqlalchemy.orm import synonym
from sqlalchemy.types import Integer, Text

from tg import config

from rpac.model import DeclarativeBase, qry
from interface import SysMixin


__all__ = ['FileObject']


class FileObject( DeclarativeBase, SysMixin ):
    __tablename__ = 'common_file_object'

    id = Column( Integer, primary_key = True )
    file_name = Column( Text )
    _file_path = Column( "file_path", Text, nullable = False )
    url = Column( Text )

    def _get_file_path( self ):
        return os.path.join( config.get( "public_dir" ), self._file_path )

    def _set_file_path( self, value ):
        self._file_path = value

    file_path = synonym( '_file_path', descriptor = property( _get_file_path, _set_file_path ) )

    @property
    def url( self ): return '/%s' % self._file_path.replace( '\\', '/' )
