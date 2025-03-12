import os
from database import create_database, insert_sample_data, get_training_data
from agent import agent, AgentDependencies
from ml_model import RiskPredictor

def main():
    create_database()
    insert_sample_data()

    ml_model = RiskPredictor()
    pkl_path = 'risk_model.pkl'
    if os.path.exists(pkl_path):
        print("Loading pre-trained model from", pkl_path)
        ml_model.load(pkl_path)
    else:
        print("No pre-trained model found. Training with database data...")
        data = get_training_data()
        if data:
            descriptions, labels = zip(*data)
            ml_model.train(descriptions, labels)
            ml_model.save(pkl_path)
            print(f"Model trained and saved as {pkl_path}")
        else:
            print("No training data available. Starting with an untrained model.")

    deps = AgentDependencies(ml_model=ml_model)

    print("Welcome to the Construction Risk Management Assistant!")
    print("Type 'exit' or 'quit' to end the session.")
    while True:
        user_input = input("\nEnter your query: ").strip()
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        result = agent.run_sync(user_input, deps=deps)
        if result.data.response_type == "prediction":
            print("\nPredicted Risks:", result.data.predicted_risks or "No risks predicted.")
            print("Suggestions:", result.data.suggestions or "No suggestions available.")
        elif result.data.response_type == "log":
            print("\n" + (result.data.log_message or "No confirmation message returned."))
        else:
            print("\nUnknown response type received.")

if __name__ == "__main__":
    main()