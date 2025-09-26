import sys

class PizzaAgent:
    def __init__(self):
        self.customer_name = None
        self.has_greeted = False

    def greet_customer(self):
        self.has_greeted = True
        return "Hi there! Welcome to Contoso Pizza! 🍕 I'm your friendly pizza assistant. What's your name?"

    def set_customer_name(self, name):
        self.customer_name = name
        return f"Nice to meet you, {name}! How can I help you with your pizza order today?"

    def handle_order(self, size, crust, toppings):
        if not self.customer_name:
            return "I need to know your name before I can take your order. What's your name?"

        if "pineapple" in toppings:
            return (
                f"Oh, pineapple on pizza? Bold choice, {self.customer_name}! 😏"
                f" Your {size} {crust} pizza with {', '.join(toppings)} is on its way!"
            )
        return (
            f"Got it, {self.customer_name}! Your {size} {crust} pizza with {', '.join(toppings)}"
            " will be ready soon!"
        )

    def deflect_unrelated_questions(self):
        return (
            "I'm here to help with pizza orders and Contoso Pizza info only. "
            "Let me know if you'd like to order a pizza! 🍕"
        )

    def respond(self, message):
        if not self.has_greeted:
            return self.greet_customer()

        if self.customer_name is None and "my name is" in message.lower():
            name = message.split("is")[-1].strip()
            return self.set_customer_name(name)

        if self.customer_name is None:
            return "I need to know your name before we proceed. What's your name?"

        if "order" in message.lower():
            # Example: "I want to order a large thin-crust pizza with pepperoni and mushrooms"
            parts = message.lower().split(" ")
            size = next((word for word in parts if word in ["small", "medium", "large"]), "medium")
            crust = next((word for word in parts if word in ["thin-crust", "thick-crust", "stuffed-crust"]), "regular")
            toppings = [word for word in parts if word not in ["small", "medium", "large", "thin-crust", "thick-crust", "stuffed-crust", "order", "pizza", "with"]]
            return self.handle_order(size, crust, toppings)

        return self.deflect_unrelated_questions()

# Example usage
if __name__ == "__main__":
    agent = PizzaAgent()
    print(agent.greet_customer())

    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() in ["exit", "quit"]:
                print("Goodbye! Have a great day! 🍕")
                break
            response = agent.respond(user_input)
            print(response)
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye! Have a great day! 🍕")
            sys.exit()