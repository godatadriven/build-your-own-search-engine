from pathlib import Path
import json
from dataclasses import dataclass
from dataclasses_json import dataclass_json

@dataclass_json
@dataclass(order=True, frozen=True)
class Article:
    """The data model for processed articles
    """
    id: str
    timestamp: str
    source: str
    title: str
    body: str

source_articles = Path(__file__).resolve().parent.parent.parent / 'data' / 'aylien_covid_news_data.jsonl'
destination_articles = Path(__file__).resolve().parent.parent.parent / 'data' / 'aylien_covid_news_data_sample.jsonl'



with open(source_articles,'r') as source_file:
    with open(destination_articles, 'w') as destination_file:
        for i in range(5000):
            line = source_file.readline()
            json_line = json.loads(line)
            id = str(json_line.get('id'))
            timestamp = json_line.get('published_at')
            source = json_line.get('source').get('domain')
            title = json_line.get('title')
            body = json_line.get('body')

            mini_article = Article(id=id, timestamp=timestamp, source=source, title=title, body=body)
            destination_file.write(mini_article.to_json()+'\n')

    
    
