# Pluggable search provider interface.
# Default is a no-op/stub that returns no results. Replace with real provider.

def web_search(query: str, max_results: int = 5):
    # TODO: integrate Tavily / Serper / Bing etc.
    # Return structure: [{"title":"", "url":"", "snippet":""}, ...]
    return []
