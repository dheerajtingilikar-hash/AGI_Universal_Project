import json

def route_intent(user_query: str) -> str:
    subjects = {
        "python": "python_logic",
        "sql": "database_expert",
        "php": "web_dev_expert",
        "math": "math_expert"
    }

    query_lower = user_query.lower()

    for key, subject in subjects.items():
        if key in query_lower:
            return subject

    return "general_knowledge"


# optional test
if __name__ == "__main__":
    print(route_intent("how to use python loop"))