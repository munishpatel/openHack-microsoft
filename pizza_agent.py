import sys
import json
import os
import re

class PizzaAgent:
    def __init__(self):
        self.customer_name = None
        self.store = None
        self.stores = self.load_store_data()

    def load_store_data(self):
        store_data = []
        knowledge_path = os.path.join(os.path.dirname(__file__), "knowledge")
        for file_name in os.listdir(knowledge_path):
            if file_name.endswith(".md"):
                with open(os.path.join(knowledge_path, file_name), "r", encoding="utf-8") as file:
                    content = file.read()
                    store_info = self.parse_store_markdown(content)
                    if store_info:
                        store_data.append(store_info)
        return store_data

    def parse_store_markdown(self, content):
        name_match = re.search(r"# 📍 (.+)", content)
        address_match = re.search(r"\*\*Address:\*\* (.+)", content)
        hours_match = re.search(r"\*\*Opening Hours:\*\*\s+(.+)", content)
        contact_match = re.search(r"\*\*Contact:\*\* (.+)", content)

        if name_match and address_match and hours_match and contact_match:
            return {
                "name": name_match.group(1),
                "address": address_match.group(1),
                "hours": hours_match.group(1),
                "contact": contact_match.group(1),
            }
        return None

    def greet_customer(self):
        return "Hi there! Welcome to Contoso Pizza! 🍕 What's your name?"

    def set_customer_name(self, name):
        self.customer_name = name
        return f"Nice to meet you, {name}! How can I help you with your pizza order today?"

    def list_stores(self):
        store_list = "\n".join([f"- {store['name']} at {store['address']} (Hours: {store['hours']})" for store in self.stores])
        return f"Here are our Contoso Pizza locations:\n{store_list}"

    def set_store(self, store_name):
        store_name = store_name.lower()
        for store in self.stores:
            if store_name in store['name'].lower() or store_name in store['address'].lower():
                self.store = store
                return f"Got it! We'll place your order at {store['name']} located at {store['address']}!"
        # Suggest available stores if no match is found
        suggestions = ", ".join([store['name'] for store in self.stores])
        return (
            f"Sorry, I couldn't find that store. Here are some options: {suggestions}. "
            "Please choose one of these locations."
        )

    def handle_order(self, size, crust, toppings):
        if not self.store:
            return "Please let me know which store you'd like to order from first."

        if "pineapple" in toppings:
            return (
                f"Oh, pineapple on pizza? Bold choice, {self.customer_name}! 😏"
                f" Your {size} {crust} pizza with {', '.join(toppings)} is on its way from {self.store['name']}!"
            )
        return (
            f"Got it, {self.customer_name}! Your {size} {crust} pizza with {', '.join(toppings)}"
            f" will be ready soon at {self.store['name']}!"
        )

    def deflect_unrelated_questions(self):
        return (
            "I'm here to help with pizza orders and Contoso Pizza info only. "
            "Let me know if you'd like to order a pizza! 🍕"
        )

    def respond(self, message):
        if self.customer_name is None:
            if "my name is" in message.lower():
                name = message.split("is")[-1].strip()
                return self.set_customer_name(name)
            return self.greet_customer()

        if "locations" in message.lower() or "stores" in message.lower():
            return self.list_stores()

        if "order" in message.lower():
            parts = message.lower().split(" ")
            size = next((word for word in parts if word in ["small", "medium", "large"]), "medium")
            crust = next((word for word in parts if word in ["thin-crust", "thick-crust", "stuffed-crust"]), "regular")
            toppings = [word for word in parts if word not in ["small", "medium", "large", "thin-crust", "thick-crust", "stuffed-crust", "order", "pizza", "with"]]
            return self.handle_order(size, crust, toppings)

        if "store" in message.lower():
            store_name = message.split("store")[-1].strip()
            return self.set_store(store_name)

        return self.deflect_unrelated_questions()

# Example usage
if __name__ == "__main__":
    agent = PizzaAgent()
    print("Welcome to Contoso Pizza! Type 'exit' to end the chat.")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Goodbye! Have a great day! 🍕")
            break
        response = agent.respond(user_input)
        print(f"Agent: {response}")