import os
from flask import Flask, request, send_file
from flask_restful import reqparse, abort, Api, Resource
from flask_cors import CORS
from storage_module.features_dao import FeatureDao
from export_module.export_shp import ExportShp

SERVER_IP='0.0.0.0'
SERVER_DOMAIN='terrabrasilis.info'
SHP_PATH='/export'

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
api = Api(app)

class ExportShapefile(Resource):
     def get(self, input_table, output_file_name, filters):
        
        curpath = os.path.abspath(os.curdir) + SHP_PATH
        fd = FeatureDao()
        try:
            estimated_time = fd.getEstimatedTime()
            # using thread to exec this call
            ExportShp(curpath, input_table, output_file_name, filters)
        except Exception as error:
            return 404
    return {'estimated_time': estimated_time}, 200


api.add_resource(ExportShapefile, '/export/<input_table>/<output_file_name>/<filters>')


if __name__ == '__main__':
     app.run(host=SERVER_IP, port=5000, debug=True)