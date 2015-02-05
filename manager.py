#!/usr/bin/python

import sys

from oauth2client.client import OAuth2WebServerFlow
from oauth2client.client import AccessTokenRefreshError
from oauth2client.file import Storage
from oauth2client.tools import run
from httplib2 import Http
from apiclient.discovery import build
from apiclient.errors import HttpError


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


def rows_collection(service):
    try:
        collection = service.query()
    except AccessTokenRefreshError:
        print ("The credentials have been revoked or expired, "
               "please, re-run the application to re-authorize")

    return collection


def list_all_rowids(tableid, collection):
    column_name = "ROWID"
    sql = "SELECT {} FROM {}".format(column_name, tableid)
    request = collection.sqlGet(sql=sql)
    try:
        response = request.execute()
    except HttpError as detail:
        print "Handling run-time error:", detail
    else:
        if u'rows' not in response:
            raise ValueError("Inappropriate value for the 'tableId' key")
        rows = response.get(u'rows', [])
        rowids = [row[0] for row in rows]

    return rowids


def list_rowids(tableid, collection, page_token=None, max_results=None):
    column_name = "ROWID"
    limit = max_results if max_results else 5
    offset = (page_token - 1)*limit if page_token else 0
    sql = "SELECT {} FROM {} OFFSET {} LIMIT {}".format(column_name, tableid, offset, limit)
    request = collection.sqlGet(sql=sql)
    try:
        response = request.execute()
    except HttpError as detail:
        print "Handling run-time error:", detail
    else:
        if u'rows' not in response:
            raise ValueError("Inappropriate value for the 'tableId' key")
        rows = response.get(u'rows', [])
        rowids = [row[0] for row in rows]

    return rowids


def retrieve_record(tableid, collection, record):
    names = [name for name in record.iterkeys() if name != u'rowid']
    column_names = ", ".join(names)
    row_condition = "ROWID = '{}'".format(record[u'rowid'])
    sql = "SELECT {} FROM {} WHERE {}".format(column_names, tableid, row_condition)
    request = collection.sqlGet(sql=sql)
    try:
        response = request.execute()
    except HttpError as detail:
        print "Handling run-time error:", detail
    else:
        if u'rows' not in response:
            raise ValueError("Inappropriate value for the 'rowid' key")
        columns = response.get(u'columns', [])
        rows = response.get(u'rows', [])
        record.update(zip(columns, rows[0]))

    return record


def create_record(tableid, collection, record):
    fields = [field for field in record.iteritems() if field[0] != u'rowid']
    column_names = ", ".join([field[0] for field in fields])
    values = ", ".join([field[1] for field in fields])
    sql = "INSERT INTO {} ({}) VALUES ({})".format(tableid, column_names, values)
    request = collection.sql(sql=sql)
    try:
        response = request.execute()
    except HttpError as detail:
        print "Handling run-time error:", detail
    else:
        if u'columns' not in response:
            raise ValueError("Inappropriate values for the 'columnId' keys")
        columns = response.get(u'columns', [])
        rows = response.get(u'rows', [])
        record.update(zip(columns, rows[0]))

    return record


def modify_record(tableid, collection, record):
    fields = [field for field in record.iteritems() if field[0] != u'rowid']
    column_conditions = ", ".join([" = ".join(field) for field in fields])
    row_condition = "ROWID = '{}'".format(record[u'rowid'])
    sql = "UPDATE {} SET {} WHERE {}".format(tableid, column_conditions, row_condition)
    request = collection.sql(sql=sql)
    try:
        response = request.execute()
    except HttpError as detail:
        print "Handling run-time error:", detail
    else:
        columns = response.get(u'columns', [])
        rows = response.get(u'rows', [])
        record = dict(zip(columns, rows[0]))

    return record


def destroy_record(tableid, collection, record):
    row_condition = "ROWID = '{}'".format(record[u'rowid'])
    sql = "DELETE FROM {} WHERE {}".format(tableid, row_condition)
    request = collection.sql(sql=sql)
    try:
        response = request.execute()
    except HttpError as detail:
        print "Handling run-time error:", detail
    else:
        columns = response.get(u'columns', [])
        rows = response.get(u'rows', [])
        record = dict(zip(columns, rows[0]))

    return record


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

    # Rows
    collection = rows_collection(service)
    #rowids = list_all_rowids(tableid, collection)
    rowids = list_rowids(tableid, collection, page_token=1, max_results=10)
    print
    print "List of rowIds:"
    pprint.pprint(rowids)
    # One row ID happens to be the first.
    rowid = rowids[0]
    # Two column IDs happen to be "City" and "date".
    record = {u'rowid': rowid, u"City": u"", u"date": u""}
    print
    print "Selected Record (to retrieve):\n", record
    record = retrieve_record(tableid, collection, record)
    pprint.pprint(record)

    record = {u'rowid': u'', u"City": u"'Madrid'", u"date": u"20141023"}
    print
    print "Selected Record (to create):\n", record
    record = create_record(tableid, collection, record)
    pprint.pprint(record)
    record.update({u"date": u"20141115"})
    print
    print "Selected Record (to modify):\n", record
    result = modify_record(tableid, collection, record)
    pprint.pprint(result)
    print
    print "Selected Record (to destroy):\n", record
    result = destroy_record(tableid, collection, record)
    pprint.pprint(result)

    record = {u'rowid': u'', u"City": u"'Madrid'"}
    print
    print "Selected Record (to modify):\n", record
    result = modify_record(tableid, collection, record)
    pprint.pprint(result)

    print
    print "Selected Record (to destroy):\n", record
    result = destroy_record(tableid, collection, record)
    pprint.pprint(result)
