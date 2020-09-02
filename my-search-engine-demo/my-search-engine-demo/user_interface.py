import os

import pandas as pd
from azure.core.credentials import AzureKeyCredential

import requests
from PIL import Image
import base64
import streamlit as st

def paginator(label, items, items_per_page=10, on_sidebar=True):
    """Lets the user paginate a set of items.
    Parameters
    ----------
    label : str
        The label to display over the pagination widget.
    items : Iterator[Any]
        The items to display in the paginator.
    items_per_page: int
        The number of items to display per page.
    on_sidebar: bool
        Whether to display the paginator widget on the sidebar.
        
    Returns
    -------
    Iterator[Tuple[int, Any]]
        An iterator over *only the items on that page*, including
        the item's index.
    Example
    -------
    This shows how to display a few pages of fruit.
    >>> fruit_list = [
    ...     'Kiwifruit', 'Honeydew', 'Cherry', 'Honeyberry', 'Pear',
    ...     'Apple', 'Nectarine', 'Soursop', 'Pineapple', 'Satsuma',
    ...     'Fig', 'Huckleberry', 'Coconut', 'Plantain', 'Jujube',
    ...     'Guava', 'Clementine', 'Grape', 'Tayberry', 'Salak',
    ...     'Raspberry', 'Loquat', 'Nance', 'Peach', 'Akee'
    ... ]
    ...
    ... for i, fruit in paginator("Select a fruit page", fruit_list):
    ...     st.write('%s. **%s**' % (i, fruit))
    """

    # Figure out where to display the paginator
    if on_sidebar:
        location = st.sidebar.empty()
    else:
        location = st.empty()

    # Display a pagination selectbox in the specified location.
    items = list(items)
    n_pages = len(items)
    n_pages = (len(items) - 1) // items_per_page + 1
    page_format_func = lambda i: f"Results {i*10} to {i*10 +10 -1}"
    page_number = location.selectbox(label, range(n_pages), format_func=page_format_func)

    # Iterate over the items in the page to let the user display them.
    min_index = page_number * items_per_page
    max_index = min_index + items_per_page
    import itertools
    return itertools.islice(enumerate(items), min_index, max_index)

def get_table_download_link(data:pd.DataFrame, search_text):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    camelcase = '_'.join(search_text.split())
    csv = data.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a download="{camelcase}.csv" href="data:file/csv;base64,{b64}">Download all results</a>'
    return href


#Title
# st.title("Covid-19 search engine")
st.markdown("<h1 style='text-align: center; '>Covid-19 search engine</h1>", unsafe_allow_html=True)
#Logo
logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'facemask.jpg')
robeco_logo = Image.open(logo_path)
st.image(robeco_logo,use_column_width=True)

#Search bar
search_query = st.text_input(
    "Search for Covid-19 here", value="", max_chars=None, key=None, type="default"
)


#Search API
index_name = "covid-19-index"
endpoint = os.environ["ACS_ENDPOINT"]
credential = os.environ["ACS_API_KEY"]
headers = {
            "Content-Type": "application/json",
            "api-key": credential,
        }
search_url = f"{endpoint}/indexes/{index_name}/docs/search?api-version=2020-06-30"

search_body = {
    "count": True,
    "search": search_query,
    "searchFields": "title",
    "searchMode": "all",
    "select": "title, body",
    "top": 100,
}





if search_query == "":
    pass
else:
    response = requests.post(
    search_url, headers=headers, json=search_body
    ).json()

    results_df = pd.DataFrame(response.get("value"))
    results_df = results_df.reset_index(drop=False)
    results_df["nr_results"] = response.get("@odata.count")
    results_df["search_query"] = search_query


    #Write 10 results
    st.write(f'Search results ({response.get("@odata.count")}):')
    # for i, record in paginator(f"Select a results (capped at 100/{response.get('@odata.count')})", list(results_df['title'])):
    #     st.write('%s. **%s**' % (i, record))
    record_list = []
    _ = [record_list.append({'title':record["title"],'body':record["body"]}) for record in response.get('value')]

    for i, record in paginator(f"Select a results (capped at 100/{response.get('@odata.count')})", record_list):
        st.write('%s. **%s**' % (i, record['title']))
        st.write('%s' % (record['body']))

    #Download all results to CSV
    st.sidebar.markdown(get_table_download_link(results_df, search_query), unsafe_allow_html=True)




