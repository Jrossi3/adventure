import json

# Load the JSON data from the file
with open("adventure.json") as f:
    rooms = json.load(f)

# Start the player in the first room
current_room = rooms[0]
inventory = []
count = 1

# Main game loop
while True:
    if count:
        # Print the current room's name and description
        print("> " + current_room["name"])
        print(current_room["desc"])

        # Check for any items in the room and print them
        if "items" in current_room:
            print("Items:")
            for item in current_room["items"]:
                print("" + item)
        if inventory:
            print("Inventory:")
            for item in inventory:
                print("" + item)
        # Print the available exits for the current room
        print("Exits:")
        for exit_direction, room_index in current_room["exits"].items():
            print(f"{exit_direction}: {rooms[room_index]['name']}")
    
    # Ask the player which direction they want to go in
    direction = input("What would you like to do? ")
    if direction.lower() == "quit":
        print("Goodbye!")
        break
    elif direction.lower() == "look":
        count = 1
        continue
    elif direction.lower().startswith("get "):
        # Get the item name
        item_name = direction.lower().replace("get ", "")
        # Check if the item is in the room
        if "items" in current_room and item_name in current_room["items"]:
            # Add the item to the inventory and remove it from the room
            inventory.append(item_name)
            current_room["items"].remove(item_name)
            print(f"You pick up the {item_name}.")
            count = 0
            continue
        else:
            count = 0
            print("There's no " + direction.replace("get ", "") + " anywhere.")

    # Check if the chosen action is to show inventory
    elif direction.lower() == "inventory":
        if inventory:
            print("Inventory:")
            for item in inventory:
                print("" + item)
            count = 0
        else:
            count = 0
            print("Your inventory is empty.")
    elif direction.lower() == "go":
        count = 0
        print("Sorry, you need to 'go' somewhere.")
    # Check if the chosen direction is valid
    elif "go" in direction.lower():
        direction = direction.replace("go ", "")
        if direction in current_room["exits"]:
            # Move the player to the new room
            room_index = current_room["exits"][direction]
            current_room = rooms[room_index]
            count = 1
        else:
            count = 0
            print("You cant go that way")
    elif direction in current_room["exits"]:
        # Move the player to the new room
        room_index = current_room["exits"][direction]
        current_room = rooms[room_index]
        count = 1
    else:
        print("You can't go that way.")
        count = 0
