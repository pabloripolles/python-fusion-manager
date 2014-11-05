# FusionManager

Simple utility to manage Google Fusion Tables from Python

<!-- MarkdownTOC -->

- [Google Fusion Tables API](#google-fusion-tables-api)
	- [Getting Started](#getting-started)
		- [Introduction](#introduction)
		- [Before you start](#before-you-start)
			- [Get a Google account](#get-a-google-account)
			- [Learn about identifying your application and authorizing requests](#learn-about-identifying-your-application-and-authorizing-requests)
	- [Using the API](#using-the-api)
		- [Introduction](#introduction-1)
			- [Identifying your application and authorizing requests](#identifying-your-application-and-authorizing-requests)
				- [About authorization protocols](#about-authorization-protocols)
				- [Authorizing requests with OAuth 2.0](#authorizing-requests-with-oauth-20)
			- [Table access permissions](#table-access-permissions)
	- [References](#references)
- [Install](#install)

<!-- /MarkdownTOC -->

## Google Fusion Tables API

### Getting Started

For more information, see [https://developers.google.com/fusiontables/docs/v1/getting_started](https://developers.google.com/fusiontables/docs/v1/getting_started).

#### Introduction

[Google Fusion Tables](http://www.google.com/fusiontables) is a web application used for sharing, visualizing, and publishing tabular data.  You can upload your own CSV, KML, ODS, XLS, or Google Spreadsheet data to a Fusion Tables table.  Once your data is in Fusion Tables, you can collaborate on it with others in real time, publish it for Google Search, create map and chart visualizations for private use or for embedding on websites, filter it according to specific criteria, and update the data behind your visualizations or filters at any time.

The Fusion Tables API allows you to use HTTP requests to programmatically to perform these tasks, which are also available in the Fusion Tables web application:

*   create and delete tables
*   read and modify table metadata such as table and column names and column types
*   insert, update, and delete the rows in a table
*   create, update, and delete settings for certain visualizations
*   query the rows in a table

Table structure, metadata, and visualization settings are represented as JSON data structures accessible through RESTful HTTP requests.  Row data is handled using a subset of SQL statements sent as HTTP requests, and can be retrieved in either CSV or JSON formats.

#### Before you start

We're assuming you're familiar with web programming concepts and web data formats.

##### Get a Google account

Make sure that you have a Google account set up.  We recommend that you use a separate Google account for development and testing purposes to protect yourself from accidental data loss.  If you already have a test account, then you're all set; you can visit the Google Fusion Tables user interface to set up, edit, or view your test data.

##### Learn about identifying your application and authorizing requests

Every time your application sends a request to the Fusion Tables API it needs to be identified.  When your application requests private data or resources, the request must be authorized by an authenticated user who has access to that data.  When your application requests data or resources from a public or unlisted table, the request doesn't need to be authorized, but it does need to be accompanied by an API key.

### Using the API

For more information, see [https://developers.google.com/fusiontables/docs/v1/using](https://developers.google.com/fusiontables/docs/v1/using).

#### Introduction

[Google Fusion Tables](http://www.google.com/fusiontables) is data management web application in the cloud for storing and visualizing your data.

##### Identifying your application and authorizing requests

Every request your application sends to the Fusion Tables API needs to identify your application to Google.  There are two ways to identify your application: using an OAuth 2.0 token (which also authorizes the request) and/or using the application's API key.  Here's how to determine which of those options to use:

*   If the request requires authorization (such as a request for an individual's private data), then the application must provide an OAuth 2.0 token with the request.  The application may also provide the API key, but it doesn't have to.
*   If the request doesn't require authorization (such as a request for public data), then the application must provide either the API key or an OAuth 2.0 token, or both—whatever option is most convenient for you.

###### About authorization protocols

We'll be using OAuth 2.0 to authorize requests.  To find your application's API credentials:

1.  Go to the [Google Developers Console](https://console.developers.google.com/project).
2.  Select a project.
3.  In the sidebar on the left, select **APIs & auth**.  In the list of APIs, make sure the status is **ON** for the Fusion Tables API.
4.  In the sidebar on the left, select **Credentials**.
5.  The API supports two types of credentials but we will be using **OAuth 2.0**: Your application must send an OAuth 2.0 token with any request that accesses private user data.  Your application sends a client ID and, possibly, a client secret to obtain a token.  You can generate OAuth 2.0 credentials for web applications, service accounts, or installed applications.

###### Authorizing requests with OAuth 2.0

Requests to the Fusion Tables API for non-public user data must be authorized by an authenticated user.

The details of the authorization process, or "flow," for OAuth 2.0 vary, but in general the following process applies:

1.  When you create your application, you register it using the [Google Developers Console](https://console.developers.google.com/project).  Google then provides information you'll need later, such as a client ID and a client secret.
2.  Activate the Fusion Tables API in the Google Developers Console.
3.  When your application needs access to user data, it asks Google for a particular **scope** of access.
4.  Google displays a **consent screen** to the user, asking them to authorize your application to request some of their data.
5.  If the user approves, then Google gives your application a short-lived **access token**.
6.  Your application requests user data, attaching the access token to the request.
7.  If Google determines that your request and the token are valid, it returns the requested data.

##### Table access permissions

The default settings for a new table is to be private and exportable.  Owners and editors can control access to a table in these ways:

*   **Private**.

    Only the owner and editors have access to your table. Visualizations embedded in other websites and Google Earth network links cannot authenticate to Fusion Tables when they call for data, so the table must be Public or Unlisted for these features to work.

    To change: In the [Docs List API](https://developers.google.com/google-apps/documents-list/#managing_sharing_permissions_of_resources_via_access_control_lists_acls), change ACLs to allow "default" type, which makes the table publicly shared with all users.  In the web application, click the Share button and select Public in the Sharing settings dialog box.
*   **Public**.
    
    No authentication required for read-only HTTP GET access, provided the table is exportable. 
    
    To change: In the [Docs List API](https://developers.google.com/google-apps/documents-list/#managing_sharing_permissions_of_resources_via_access_control_lists_acls), change ACLs to limit access by user role or type.  In the web application, click the Share button and select Private in the Sharing settings dialog box.
*   **Unlisted**.
    
    No authentication required for read-only HTTP GET access, provided the table is exportable.  Embedded visualizations and Google Earth network links have access, but your table is not included in Fusion Tables public search and it is not suggested to search engines for indexing although they may discover the URL through links you create online.
    
    To change: in the web application, click the Share button and deselect the "Anyone with the link" radio button in the Sharing settings dialog box to make the table completely private or completely public.  You cannot make this change in the API.
*   **Exportable**.
    
    Anyone can download the table data and authentication is not required for read-only HTTP GET access. 
    
    To change: In the Fusion Tables API, change the table property to be "isExportable = false."  In the web application, choose Edit > Modify Table Info and deselect "exportable" checkbox.  A table that is public or unlisted but that is not exportable allows read-only access but does not allow data downloading.

### References

*   [https://developers.google.com/fusiontables/docs/v1/reference/](https://developers.google.com/fusiontables/docs/v1/reference/)
*   [https://developers.google.com/fusiontables/docs/v1/sql-reference](https://developers.google.com/fusiontables/docs/v1/sql-reference)

## Install

Please, take a look at `INSTALL.md`.



