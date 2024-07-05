from typing import Dict, Any, List


def more_like_this_query(body: str, fields: List[str],
                         min_term_freq: int = 1, max_query_terms: int = 25) -> Dict[str, Any]:
    """
       Constructs a 'more_like_this' query for Elasticsearch.

       This function creates a query dictionary to find documents similar to the provided text
       in the specified fields. The 'more_like_this' query finds documents that are similar
       to the given text based on the term frequency and the maximum number of query terms.

       :param body: The text to find similar documents for.
       :type body: str
       :param fields: The list of fields to search in.
       :type fields: list
       :param min_term_freq: The minimum term frequency to consider terms for similarity.
       :type min_term_freq: int
       :param max_query_terms: The maximum number of query terms to use for the similarity search.
       :type max_query_terms: int
       :return: The query dictionary to be used with Elasticsearch.
       :rtype: dict
   """
    query: Dict[str, Any] = {
        "query": {
            "more_like_this": {
                "fields": fields,
                "like": body,
                "min_term_freq": min_term_freq,
                "max_query_terms": max_query_terms
            }
        }
    }
    return query
