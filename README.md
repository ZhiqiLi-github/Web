# Web-Search Engine
- language: python

## TODO

- [ ] Define Data Structure
- [ ] wildcard search
- [ ] phrase search
- [x] bool search

## Usage

```
git clone ...
cd $WEBHOME/src 
python console.py
```


## Data Structure

### SearchEngine

```python
class SearchEngine:
    def __init__(self) -> None:
        self.state = 0 # 0 for bool, 1 for wildcard search, 2 for phrase search
        self.mode = {
            "bool" : 0,
            "wildcard": 1,
            "phrase": 2,
        }
        self.command = {
            "switch": self.switch
        }
        self.inverted_index = Index.ReadII()
        self.term_dict = None
        self.doc_dict  = None
        self.search_method = [
            bool_search,
            wildcard_search,
            phrase_search
        ]
        pass

```
    
`state` for current search mode, `mode` for all the search modes

| keys           | Description                                                              |
| -------------- | ------------------------------------------------------------------------ |
| state          | current search mode                                                      |
| mode           | all search modes, 0 for bool, 1 for wildcard search, 2 for phrase search |
| command        | supporting commands, `switch`, detail in Table methods                   |
| inverted_index | as name shows                                                            |
| term_dict      | as name shows                                                            |
| doc            | as name shows                                                            |
| search_method  | function list for  search                                                |

| methods     | description                           |
| ----------- | ------------------------------------- |
| search      | search according to current state     |
| switch      | switch current search mode to another |
| interpreter | analysis the string that user inputs  |



