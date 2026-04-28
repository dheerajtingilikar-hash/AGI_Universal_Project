from ddgs import DDGS

class ResearchBridge:
    def __init__(self):
        self.ddgs = DDGS()
        self.cache = {}

    def search(self, query, max_results=5):
        query = query.lower().strip()

        if query in self.cache:
            return self.cache[query]

        try:
            results = self.ddgs.text(query, max_results=max_results)

            data = []
            for r in results:
                data.append({
                    "title": r.get("title"),
                    "url": r.get("href"),
                    "snippet": r.get("body")
                })

            self.cache[query] = data
            return data

        except Exception as e:
            return [{"error": str(e)}]

    def format(self, query):
        data = self.search(query)

        if not data or "error" in data[0]:
            return "No research results."

        return "\n".join(
            f"- {d['title']}\n  {d['snippet']}\n  {d['url']}\n"
            for d in data
        )