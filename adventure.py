import json
import sys
if len(sys.argv) != 2:
    print("Usage: python3 adventure.py [map filename]")

map_filename = sys.argv[1]

# Load the JSON data from the file
with open(map_filename) as f:
    rooms = json.load(f)

# Start the player in the first room
current_room = rooms[0]
inventory = []
count = 1
test = 0
exitStr = "Exits:"
itemList = ""
directionList = ["north", "east", "south", "west"]
quitHelp = 1

# Main game loop
while quitHelp:
    try:
        while True:
            if count:
                # Print the current room's name and description
                print("> " + current_room["name"] + "\n")
                print(current_room["desc"] + "\n")

                # Check for any items in the room and print them
                if "items" in current_room:
                    if len(current_room["items"]) != 0:
                        for item in current_room["items"]:
                            itemList = itemList + " " + item
                        print("Items:" + itemList + "\n")
                        itemList = ""
                # Print the available exits for the current room
                if test:
                    print("Exits:")
                    for exit_direction, room_index in current_room["exits"].items():
                        print(f"{exit_direction}: {rooms[room_index]['name']}\n")
                else:
                    exitStr = "Exits:"
                    for exit_direction, room_index in current_room["exits"].items():
                        exitStr = exitStr + " " + exit_direction
                    print(exitStr + "\n")
                    
            # Ask the player which direction they want to go in
            direction = input("What would you like to do? ")
            direction = direction.lower()
            if direction.lstrip() == "quit":
                print("Goodbye!")
                quitHelp = 0
                break
            elif direction.lstrip().startswith("drop"):
                if direction.lstrip().replace("drop ", "") in inventory:
                    inventory.remove(direction.replace("drop ", ""))
                    count = 0
                    if "items" in current_room:
                        current_room["items"].append(item_name)
                        print("You drop the " + direction.replace("drop ", "") + ".")
                        continue
                    else:
                        current_room["items"] = []
                        current_room["items"].append(item_name)
                        print("You drop the " + direction.replace("drop ", "") + ".")
                        continue
                elif len(direction.lstrip().replace("drop", "")) < 2:
                    print("Please designate an item to be removed")
                    count = 0
                else:
                    print("Item cannot be removed")
                    count = 0
            elif direction.lstrip() == "show exits" and test:
                count = 0
                print("Exits are already showing")
                continue
            elif direction.lstrip() == "show exits":
                count = 1
                test = 1
                continue
            elif direction.lstrip() == "remove exits" and test != 1:
                count = 0
                print("Exits are not showing")
                continue
            elif direction.lstrip() == "remove exits":
                count = 1
                test = 0
                continue
            elif direction.lstrip() == "look":
                count = 1
                continue
            elif direction.lstrip().startswith("get"):
                if len(direction.lstrip().replace("get", "")) < 2:
                    print("Sorry, you need to 'get' something.")
                    count = 0
                    continue
                # Get the item name
                item_name = direction.lower().replace("get ", "")
                # Check if the item is in the room
                if "items" in current_room and item_name in current_room["items"]:
                    # Add the item to the inventory and remove it from the room
                    inventory.append(item_name)
                    itemList = itemList.replace(" " + item_name, "")
                    current_room["items"].remove(item_name)
                    print(f"You pick up the {item_name}.")
                    count = 0
                    continue
                else:
                    count = 0
                    print("There's no " + direction.replace("get ", "") + " anywhere.")
                    continue
            # Check if the chosen action is to show inventory
            elif direction.lstrip() == "inventory":
                if inventory:
                    print("Inventory:")
                    for item in inventory:
                        print("  " + item)
                    count = 0
                else:
                    count = 0
                    print("You're not carrying anything.")
            elif direction.lstrip().startswith("go"):
                direction = direction.replace("go", "").strip()
                if len(direction) == 0:
                    print("Sorry, you need to 'go' somewhere.")
                    count = 0
                    continue
            # Check if the chosen direction is valid
                elif direction in current_room["exits"]:
                    # Move the player to the new room
                    room_index = current_room["exits"][direction]
                    current_room = rooms[room_index]
                    count = 1
                    print("You go " + direction + ".\n")
                    continue
                else:
                    count = 0
                    print("There's no way to go " + direction + ".")
                    continue   
            elif direction.lstrip() in current_room["exits"]:
                # Move the player to the new room
                room_index = current_room["exits"][direction]
                current_room = rooms[room_index]
                count = 1
                print("You go " + direction + ".\n")
            elif direction.lstrip() in directionList:
                print("There's no way to go " + direction + ".")
                count = 0
            elif direction.strip() == "help":
                print("You can run the following commands:")
                print("  go ...")
                print("  get ...")
                print("  inventory")
                print("  look")
                print("  quit")
                print("  help")
                print("  show exits")
                print("  remove exits")
                print("  drop ...")
                count = 0
            else:
                print("Please enter a valid direction or command like 'get'")
                count = 0
    except EOFError as e:
        print("\nUse 'quit' to exit.")
        count = 0
        continue
