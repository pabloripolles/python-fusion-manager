#!/usr/bin/python

import sys

from oauth2client.client import OAuth2WebServerFlow
from oauth2client.client import AccessTokenRefreshError
from oauth2client.file import Storage
from oauth2client.tools import run
from httplib2 import Http
from apiclient.discovery import build


client_id = sys.argv[1]
client_secret = sys.argv[2]
scope = 'https://www.googleapis.com/auth/fusiontables'

flow = OAuth2WebServerFlow(client_id, client_secret, scope)


def authorized_http(flow):
    storage = Storage('credentials.dat')

    credentials = storage.get()
    if credentials is None or credentials.invalid:
        credentials = run(flow, storage)

    http = Http()
    http = credentials.authorize(http)

    return http


def fusiontables_service(http):
    service = build('fusiontables', 'v1', http=http)

    return service


def tables_collection(service):
    try:
        collection = service.table()
    except AccessTokenRefreshError:
        print ("The credentials have been revoked or expired, "
               "please, re-run the application to re-authorize")

    return collection


def list_all_tables(collection):
    tables = list()
    request = collection.list()
    while request != None:
        response = request.execute()
        items = response.get(u'items', [])
        tables.extend(items)
        request = collection.list_next(request, response)

    return tables


def list_tables(collection, page_token=None, max_results=None):
    request = collection.list(pageToken=page_token, maxResults=max_results)
    response = request.execute()
    tables = response.get(u'items', [])

    return tables


def retrieve_table(collection, tableid):
    request = collection.get(tableId=tableid)
    response = request.execute()

    return response


def columns_collection(service):
    try:
        collection = service.column()
    except AccessTokenRefreshError:
        print ("The credentials have been revoked or expired, "
               "please, re-run the application to re-authorize")

    return collection


def list_all_columns(tableid, collection):
    columns = list()
    request = collection.list(tableId=tableid)
    while request != None:
        response = request.execute()
        items = response.get(u'items', [])
        columns.extend(items)
        request = collection.list_next(request, response)

    return columns


def list_columns(tableid, collection, page_token=None, max_results=None):
    request = collection.list(tableId=tableid, pageToken=page_token, maxResults=max_results)
    response = request.execute()
    columns = response.get(u'items', [])

    return columns


def retrieve_column(tableid, collection, columnid):
    request = collection.get(tableId=tableid, columnId=columnid)
    response = request.execute()

    return response


if __name__ == '__main__':
    import pprint
    import json

    http = authorized_http(flow)
    service = fusiontables_service(http)

    # Tables
    collection = tables_collection(service)
    tables = list_all_tables(collection)
    name_to_tablesid = {table[u'name']: table[u'tableId'] for table in tables}
    print
    print "Mapping of names -> tableIds:"
    for (name, tableid) in name_to_tablesid.iteritems():
        print "name: {}, tableId: {}".format(name, tableid)
    # One table happens to be named: "procesed_New_Lost"
    tableid = name_to_tablesid["procesed_New_Lost"]
    print
    print "Selected Table Id:", tableid
    table = retrieve_table(collection, tableid)
    print json.dumps(table, sort_keys=True, indent=4)

    # Columns
    collection = columns_collection(service)
    columns = list_all_columns(tableid, collection)
    name_to_columnid = {column[u'name']: column[u'columnId'] for column in columns}
    print
    print "Mapping of names -> columnIds:"
    for (name, columnid) in name_to_columnid.iteritems():
        print "name: {}, columnId: {}".format(name, columnid)
    # One column happens to be named: "City"
    columnid = name_to_columnid[u"City"]
    print
    print "Selected Column Id:", columnid
    column = retrieve_column(tableid, collection, columnid)
    print json.dumps(column, sort_keys=True, indent=4)
