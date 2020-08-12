from azure.search.documents.indexes.models import ( 
    ComplexField, 
    CorsOptions, 
    SearchIndex, 
    ScoringProfile, 
    SearchFieldDataType, 
    SimpleField, 
    SearchableField 
)

name = "hotels"
fields = [
        SimpleField(name="HotelId", type=SearchFieldDataType.String, key=True),
        SearchableField(name="HotelName", type=SearchFieldDataType.String,analyzer_name='en.lucene'),
        SearchableField(name="Description", type=SearchFieldDataType.String,analyzer_name='en.lucene'),
        SimpleField(name="Rating", type=SearchFieldDataType.Double),
        SimpleField(name="Rooms", type=SearchFieldDataType.Int32),
        
    ]


index = SearchIndex(
    name=name,
    fields=fields,
)
