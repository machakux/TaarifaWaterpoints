from csv import DictReader
from datetime import datetime
from pprint import pprint

from flask.ext.script import Manager

from taarifa_api import add_document, delete_documents, get_schema
from taarifa_waterpoints import app
from taarifa_waterpoints.schemas import facility_schema, service_schema

manager = Manager(app)


def check(response, success=201):
    data, _, _, status = response
    if status == success:
        print " Succeeeded"
        return True
    else:
        print "Failed with status", status
        pprint(data)
        return False


@manager.option("resource", help="Resource to show the schema for")
def show_schema(resource):
    """Show the schema for a given resource."""
    pprint(get_schema(resource))


@manager.command
def list_routes():
    """List all routes defined for the application."""
    import urllib
    for rule in sorted(app.url_map.iter_rules(), key=lambda r: r.endpoint):
        methods = ','.join(rule.methods)
        print urllib.unquote("{:40s} {:40s} {}".format(rule.endpoint, methods,
                                                       rule))


@manager.command
def create_facility():
    """Create facility for waterpoints."""
    check(add_document('facilities', facility_schema))


@manager.command
def create_service():
    """Create service for waterpoints."""
    check(add_document('services', service_schema))


@manager.command
def delete_facilities():
    """Delete all facilities."""
    check(delete_documents('facilities'), 200)


@manager.command
def delete_services():
    """Delete all services."""
    check(delete_documents('services'), 200)


@manager.option("filename", help="CSV file to upload (required)")
@manager.option("--skip", type=int, default=0, help="Skip a number of records")
@manager.option("--limit", type=int, help="Only upload a number of records")
def upload_waterpoints(filename, skip=0, limit=None):
    """Upload waterpoints from a CSV file."""
    date_converter =  lambda s: datetime.strptime(s, '%Y-%m-%d')
    bool_converter = lambda s: s == "true"

    status_map = {
        "non functional": "not functional",
        "functional needs repair": "needs repair"
    }

    status_converter = lambda s: status_map.get(s.lower(), s.lower())

    convert = {
        'gid': int,
        'object_id': int,
        'valid_from': date_converter,
        'valid_to': date_converter,
        'amount_tsh': float,
        'breakdown_year': int,
        'date_recorded': date_converter,
        'gps_height': float,
        'latitude': float,
        'longitude': float,
        'num_private': int,
        'region_code': int,
        'district_code': int,
        'population': int,
        'public_meeting': bool_converter,
        'construction_year': int,
        'status_group': status_converter
    }

    facility_code = "wpf001"

    with open(filename) as f:
        reader = DictReader(f)
        for i in range(skip):
            reader.next()
        for i, d in enumerate(reader):
            print "Adding line", i + skip + 2

            try:
                d = dict((k, convert.get(k, str)(v)) for k, v in d.items() if v)
                d['facility_code'] = facility_code
                if not check(add_document('waterpoints', d)):
                    raise Exception()

            except Exception as e:
                print "Error adding waterpoint", e
                pprint(d)
                exit()

            if limit and i >= limit:
                break


@manager.option("status", help="Status (functional or non functional)")
@manager.option("wp", help="Waterpoint id")
def create_request(wp, status):
    """Create an example request reporting a broken waterpoint"""
    r = {"service_code": "wps001",
         "attribute": {"waterpoint_id": wp,
                       "status": status}}
    check(add_document("requests", r))


@manager.command
def delete_waterpoints():
    """Delete all existing waterpoints."""
    print delete_documents('waterpoints')

if __name__ == "__main__":
    manager.run()
