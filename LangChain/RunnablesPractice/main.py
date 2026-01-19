from query import Query
from model import Model

if __name__ == "__main__":
    print("\n\n--- Runnables Practice 🤖 ---\n")
    query = Query()
    user_topic = query.request_topic()
    model = Model()
    res = model.generate_content(user_topic)
    if res:
        user_rating = query.request_feedback()
        feedback_response = model.process_feedback(user_rating)
    else:
        print("❌ Content generation failed.")