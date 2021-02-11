def initialize_analytics_api(credentials):
    """Initializes an Analytics Reporting API V4 service object.

    Returns:
        An authorized Analytics Reporting API V4 service object.
    """
    from googleapiclient.discovery import build
    
    # Build the service object.
    analytics = build('analyticsreporting', 'v4', credentials=credentials)

    return analytics

def get_report(analytics, view_id, start_date, end_date, metrics, dimensions):
    """Queries the Analytics Reporting API V4.
    
    Args:
        analytics: An authorized Analytics Reporting API V4 service object.
    Returns:
        The Analytics Reporting API V4 response.
    """
    metrics_list = []
    for metric in metrics:
        metrics_list.append({'expression': metric})

    dimensions_list = []
    for dimension in dimensions:
        dimensions_list.append({'name': dimension})

    return analytics.reports().batchGet(
        body={
            'reportRequests': [{
                'viewId': view_id,
                'samplingLevel': 'LARGE',
                #'pageToken': '50',
                'pageSize': 100000,
                'includeEmptyRows': True,
                'hideTotals': True,
                'hideValueRanges': True,
                'dateRanges': [{'startDate': start_date, 'endDate': end_date}],
                'metrics': metrics_list,
                'dimensions': dimensions_list
                }]
        }
    ).execute()

def list_response(response):
    """Parses and prints the Analytics Reporting API V4 response.
    
    Args:
        response: An Analytics Reporting API V4 response.
    """
    for report in response.get('reports', []):
        columnHeader = report.get('columnHeader', {})
        dimensionHeaders = columnHeader.get('dimensions', [])
        metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])
        rows = report.get('data', {}).get('rows', [])

        data_output = []
        for row in rows:
            dimensions = row.get('dimensions', [])
            dateRangeValues = row.get('metrics', [])

            item = {}
            for dimensionheader, dimension in zip(dimensionHeaders, dimensions):
                item.update({dimensionheader: dimension})

            for values in dateRangeValues:
                for metricHeader, value in zip(metricHeaders, values.get('values')):
                    item.update({metricHeader.get('name'): value})
            
            data_output.append(item)
        
        return data_output