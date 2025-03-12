from database import create_database, insert_sample_data
from agent import agent, AgentDependencies


def main():
    # Initialize the database (runs once at startup)
    create_database()
    insert_sample_data()

    # Welcome message with instructions
    print("Welcome to the Construction Risk Management Assistant!")
    print("You can ask for risk predictions or log new incidents.")
    print("Type 'exit' or 'quit' to end the session.")
    print("\nSee example prompts in the documentation or try your own queries.")

    # Main interaction loop
    while True:
        user_input = input("\nEnter your query: ").strip()
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        # Process the user's query with the agent
        result = agent.run_sync(user_input, deps=AgentDependencies())

        # Display the response based on its type
        if result.data.response_type == "prediction":
            print("\nPredicted Risks:", result.data.predicted_risks or "No risks identified.")
            print("Suggestions:", result.data.suggestions or "No suggestions available.")
        elif result.data.response_type == "log":
            print("\n" + (result.data.log_message or "No confirmation message returned."))
        else:
            print("\nUnknown response type received.")


if __name__ == "__main__":
    main()