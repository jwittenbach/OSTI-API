import requests
import math
import datetime as dt

ROWS_PER_QUERY = 20

def get_citation_URL(dict_list):
    '''
    Takes a list of dicts in which at least one dict is {'rel': 'citation', 'href': URL} and returns the URL. 

    Intended to be used in pd.Series.apply(). If none of the dicts in the list 
    is of the form {'rel': 'citation', 'href': URL},
    returns None.
    
    Parameters
    ----------
    dict_list: list of dicts in which at least one dict is {'rel': 'citation', 
                'href': URL}
    
    Outputs
    -------
    url: str. citation URL AKA landing page for a record on OSTI.gov
    '''
    
    #does {'rel': 'citation'} exist in the list?
    for e in dict_list:
        if e['rel'] == 'citation':
            return e['href']
        else: return None


def query_API(url = "https://www.osti.gov/api/v1/records", 
              params = {'sort': 'publication_date desc', 'sponsor_org': '"EE-4S"'},
             print_status = False, start_date = '01/01/1980',
             end_date = dt.date.today().strftime('%m/%d/%Y')):
    '''
    Queries the OSTI.gov API for records.
    
    Parameters
    ----------
    url: str. Full URL that should be prepended to the query to get it started
    
    params: dict. Keys should be parameter field names as dictated by the API docs,
                values should be what they're being set to/queried for
    
    print_status: bool. If set to True, will print a message to stdout that 
                    tells you if the query was successful, how many results it returned,
                    etc.

    start_date: str of format 'MM/DD/YYYY'. Indicates how far back you want 
        to pull records. 

    end_date: str of format 'MM/DD/YYYY'. Indicates how recent you want records
        to be. Defaults to today's date.
                
    Returns
    -------
    (r.json(), results_count): tuple of the form (list of dicts, int). 
        The JSON can be used in pd.DataFrame.from_dict() to create
        a DataFrame for just the page of records generated. results_count
        provides an integer count of all results that can be used to modify
        the query to capture all results instead of just the first 20 (default)
    '''
    
    params['publication_date_start'] = start_date
    params['publication_date_end'] = end_date
    
    r = requests.get(url, params=params)

    query_date = r.headers["Date"]
    results_count = int(r.headers['X-Total-Count'])
    #page_count = math.ceil(results_count/ROWS_PER_QUERY)

    if print_status:
        print(f"Query was successful: {r.status_code == requests.codes.ok}")
        print(f"\nQuery made on {query_date} returned {results_count} hits")
        print(f"\nURL used was {r.url}")
    
    return r.json(), results_count
