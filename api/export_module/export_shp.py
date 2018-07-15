import os, errno
import zlib, zipfile
from subprocess import call
from storage_module.features_dao import FeatureDao

class ExportShp():

   #constructor
    def __init__(self, path, input_table, output_file_name, default_schema="public", filters=None):
        self.path = path
        self.table = "{}.{}".format( default_schema, input_table )
        self.shp_name = output_file_name
        self.filters = filters
        
        if not os.path.exists(path):
            os.mkdir(path)
        
        if self.__export():
            self.__zipShapefile()

    def __zipShapefile(self):
        
        zip_file = "{}/{}.zip".format( self.path, self.shp_name )

        with zipfile(zip_file, 'w', zipfile.ZIP_DEFLATED, True, 9) as shpzip:
            files = ['shp', 'shx', 'dbf', 'prj']
            for f in files:
                shpzip.write("{}/{}.{}".format( self.path, self.shp_name, f ))

    def __export(self):
        if self.filters:
            self.filters = "WHERE {}".format(self.filters)
        
        columns = self.__getTableColumns(self.table)
        fd = FeatureDao()
        pg = fd.getServerParams()
        status = None
        output_file_name = "{}/{}.shp".format( self.path, self.shp_name )

        pgsql2shp = "pgsql2shp -f {}".format( output_file_name )
        pgsql2shp = "{} -h {} -u {} -p {} -P {} {}".format( pgsql2shp, pg["host"], pg["user"], pg["port"], pg["password"], pg["database"] )
        pgsql2shp = "{} \"SELECT {} FROM {} {}\"".format( pgsql2shp, columns, self.table, self.filters )
        try:
            status = call(pgsql2shp)
        except OSError as error:
            raise error
        
        if status not is None:
            return True


    def __getTableColumns(self):
        fd = FeatureDao()
        return fd.getTableColumns()



