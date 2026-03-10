
from src.game import Game


def _line(char="─", width=60):
    print(char * width)


def _header(title):
    _line()
    print(f"  {title}")
    _line()


def _print(text):
    print(f"  {text}")


def _ask(prompt):
    return input(f"\n  > {prompt}: ").strip()


def show_scene(game):
    scene = game.which_scene_am_i_in()
    if scene is None:
        _print("You are nowhere.")
        return

    _header(scene.name)
    _print(scene.description)

    objects = scene.show_available_things()
    if objects:
        print()
        _print("Objects you can see:")
        for obj in objects:
            _print(f"• {obj.name}")

    chars = scene.get_characters()
    if chars:
        print()
        _print("People here:")
        for c in chars:
            _print(f"• {c.name} – {c.description}")


def _pretty_interaction_name(strategy_name):
    name = strategy_name.replace("Strategy", "")
    name = name.replace("LookAt", "Look at")
    name = name.replace("OpenIt", "Open")
    name = name.replace("MoveIt", "Move")
    name = name.replace("TurnItOn", "Turn on")
    name = name.replace("TurnItOff", "Turn off")
    name = name.replace("TasteIt", "Taste")
    name = name.replace("PickItUp", "Pick up")
    name = name.replace("DropIt", "Drop")
    return name


def interact_with_object(game):
    ctrl = game.create_interaction_controller()

    object_name = _ask("Which object do you want to interact with")
    obj = ctrl.pick_game_object(object_name)

    if obj is None:
        _print("That object is not here.")
        return

    interactions = ctrl.get_interaction_types()

    print()
    _print(f"What do you want to do with '{obj.name}'?")

    pretty_names = [_pretty_interaction_name(name) for name in interactions]
    for i, name in enumerate(pretty_names, 1):
        print(f"  [{i}] {name}")
    print("  [0] Cancel")

    choice = input("\n  > Your choice: ").strip()

    if choice == "0":
        return

    try:
        idx = int(choice) - 1
        if idx < 0 or idx >= len(interactions):
            _print("Invalid choice.")
            return
    except ValueError:
        _print("Invalid input.")
        return

    strategy_name = interactions[idx]
    ctrl.choose_interaction(strategy_name)

    if ctrl._selected_strategy and ctrl._selected_strategy.needs_options():
        options = _ask("Direction")
        ctrl.provide_options(options)

    print()
    result = ctrl.perform_interaction()
    _print(result)


def interact_with_character(game):
    scene = game.which_scene_am_i_in()
    chars = scene.get_characters()

    if not chars:
        _print("There is no one here.")
        return

    print()
    _print("Who do you want to talk to?")

    for i, c in enumerate(chars, 1):
        print(f"  [{i}] {c.name}")
    print("  [0] Cancel")

    choice = input("\n  > Your choice: ").strip()

    if choice == "0":
        return

    try:
        idx = int(choice) - 1
        if idx < 0 or idx >= len(chars):
            _print("Invalid choice.")
            return
    except ValueError:
        _print("Invalid input.")
        return

    char_name = chars[idx].name

    if not game.initiate_conversation(char_name):
        _print("Could not start conversation.")
        return

    _line()
    _print(f"You start talking to {char_name}")
    _print("(type 'accept' to take an item or 'bye' to leave)")
    _line()

    while game.character_ctrl.is_in_conversation:
        query = input("\n  You: ").strip()

        if not query:
            continue

        if query.lower() == "bye":
            game.end_conversation()
            print()
            _print(f"You end the conversation with {char_name}.")
            break

        if query.lower() == "accept":
            item = game.accept_game_object()
            if item:
                _print(f"{char_name} gives you: {item}")
            else:
                _print(f"{char_name} has nothing to give you.")
            continue

        response = game.send_query(query)
        print()
        _print(f"{char_name}: {response}")


def run(game):
    print()
    _line("═")
    print("  MEAN STREETS – Karlskrona")
    print("  A detective mystery")
    _line("═")
    print()
    _print("Your secretary just texted you:")
    _print("\"There's been a murder at Stortorget. Get there now.\"")
    print()
    input("  Press Enter to begin...")

    show_scene(game)

    while True:
        print()
        _line()
        stage = game.game_plot.get_current_stage()
        _print(f"Stage: {stage.description}")
        _line()
        print("  What do you want to do?")
        print("  [1] Interact with an object")
        print("  [2] Talk to someone")
        print("  [0] Quit")

        choice = input("\n  > Your choice: ").strip()

        if choice == "1":
            print()
            interact_with_object(game)
        elif choice == "2":
            print()
            interact_with_character(game)
        elif choice == "0":
            print()
            _print("Goodbye, detective.")
            break
        else:
            _print("Unknown command.")






# from src.game import Game


# def _line(char="─", width=60):
#     print(char * width)


# def _header(title):
#     _line()
#     print(f"  {title}")
#     _line()


# def _print(text):
#     print(f"  {text}")


# def _ask(prompt):
#     return input(f"\n  > {prompt}: ").strip()


# def show_scene(game):
#     scene = game.which_scene_am_i_in()
#     if scene is None:
#         _print("You are nowhere.")
#         return

#     _header(f" {scene.name}")
#     _print(scene.description)

#     objects = scene.show_available_things()
#     if objects:
#         print()
#         _print("Objects you can see:")
#         for obj in objects:
#             _print(f"  • {obj.name}")
#     else:
#         print()
#         _print("There are no objects here.")

#     chars = scene.get_characters()
#     if chars:
#         print()
#         _print("People here:")
#         for c in chars:
#             _print(f"  • {c.name} – {c.description}")


# def _pretty_interaction_name(strategy_name):
#     name = strategy_name.replace("Strategy", "")
#     name = name.replace("LookAt", "Look at")
#     name = name.replace("OpenIt", "Open")
#     name = name.replace("MoveIt", "Move")
#     name = name.replace("TurnItOn", "Turn on")
#     name = name.replace("TurnItOff", "Turn off")
#     name = name.replace("TasteIt", "Taste")
#     name = name.replace("PickItUp", "Pick up")
#     name = name.replace("DropIt", "Drop")
#     return name


# def interact_with_object(game):
#     ctrl = game.create_interaction_controller()

#     object_name = _ask("Which object do you want to interact with")
#     obj = ctrl.pick_game_object(object_name)

#     if obj is None:
#         _print(f"'{object_name}' is not here.")
#         return

#     interactions = ctrl.get_interaction_types()
#     if not interactions:
#         _print(f"You can't do anything with {obj.name}.")
#         return

#     print()
#     _print(f"What do you want to do with '{obj.name}'?")
#     names = [_pretty_interaction_name(name) for name in interactions]

#     for i, name in enumerate(names, 1):
#         print(f"  [{i}] {name}")
#     print("  [0] Cancel")

#     choice = input("\n  > Your choice: ").strip()

#     if choice == "0":
#         ctrl.cancel_interaction()
#         _print("Cancelled.")
#         return

#     try:
#         idx = int(choice) - 1
#         if idx < 0 or idx >= len(interactions):
#             _print("Invalid choice.")
#             ctrl.cancel_interaction()
#             return
#     except ValueError:
#         _print("Invalid input.")
#         ctrl.cancel_interaction()
#         return

#     strat_name = interactions[idx]
#     ctrl.choose_interaction(strat_name)

#     if ctrl._selected_strategy and ctrl._selected_strategy.needs_options():
#         opts = _ask("Additional input needed (e.g. direction)")
#         ctrl.provide_options(opts)

#     print()
#     result = ctrl.perform_interaction()
#     _print(result)


# def interact_with_character(game):
#     scene = game.which_scene_am_i_in()
#     if scene is None:
#         _print("You are not in a scene.")
#         return

#     chars = scene.get_characters()
#     if not chars:
#         _print("There is no one here to talk to.")
#         return

#     print()
#     _print("Who do you want to talk to?")
#     for i, c in enumerate(chars, 1):
#         print(f"  [{i}] {c.name} – {c.description}")
#     print("  [0] Cancel")

#     choice = input("\n  > Your choice: ").strip()
#     if choice == "0":
#         return

#     try:
#         idx = int(choice) - 1
#         if idx < 0 or idx >= len(chars):
#             _print("Invalid choice.")
#             return
#     except ValueError:
#         _print("Invalid input.")
#         return

#     char_name = chars[idx].name

#     ok = game.initiate_conversation(char_name)
#     if not ok:
#         _print(f"{char_name} is not available to talk right now.")
#         return

#     _line()
#     _print(f"You start talking to {char_name}.")
#     _print("(Type your message, 'accept' to take an offered item, or 'bye' to end.)")
#     _line()

#     while game.character_ctrl.is_in_conversation:
#         query = input("\n  You: ").strip()

#         if not query:
#             continue

#         if query.lower() in ("bye", "goodbye", "leave"):
#             game.end_conversation()
#             print()
#             _print(f"You end the conversation with {char_name}.")
#             break

#         if query.lower() == "accept":
#             item = game.accept_game_object()
#             if item:
#                 _print(f"{char_name} gives you: {item}. It is now in your inventory.")
#             else:
#                 _print(f"{char_name} has nothing to give you.")
#             continue

#         resp = game.send_query(query)
#         print()
#         _print(f"{char_name}: {resp}")


# def show_inventory(game):
#     _header(" Inventory")
#     inv = game.inventory

#     if inv.is_empty():
#         _print("Your inventory is empty.")
#         return

#     _print("Items in your inventory:")
#     for obj in inv.show_available_things():
#         _print(f"  • {obj.name} – {obj.description}")

#     print()
#     choice = input("  Interact with an item? (enter name or press Enter to skip): ").strip()
#     if choice:
#         curr_scene = game.which_scene_am_i_in()
#         game._world_service.set_active_scene(inv)
#         interact_with_object(game)
#         game._world_service.set_active_scene(curr_scene)


# def navigate(game):
#     all_scenes = game.get_all_scenes()
#     curr = game.which_scene_am_i_in()

#     _print("Available locations:")
#     for i, scene in enumerate(all_scenes, 1):
#         marker = " ← you are here" if scene == curr else ""
#         print(f"  [{i}] {scene.name}{marker}")
#     print("  [0] Stay here")

#     choice = input("\n  > Your choice: ").strip()
#     if choice == "0":
#         return

#     try:
#         idx = int(choice) - 1
#         if 0 <= idx < len(all_scenes):
#             target = all_scenes[idx]
#             game.go_to_scene(target.name)
#             print()
#             show_scene(game)
#         else:
#             _print("Invalid choice.")
#     except ValueError:
#         _print("Invalid input.")


# def run(game):
#     print()
#     _line("═")
#     print("  MEAN STREETS – Karlskrona")
#     print("  A detective mystery")
#     _line("═")
#     print()
#     _print("Your secretary just texted you:")
#     _print('"There\'s been a murder at Stortorget. Get there now."')
#     print()
#     input("  Press Enter to begin...")

#     show_scene(game)

#     while True:
#         print()
#         _line()
#         stage = game.game_plot.get_current_stage()
#         _print(f"Stage: {stage.description}")
#         _line()
#         print("  What do you want to do?")
#         print("  [1] Interact with an object")
#         print("  [2] Talk to someone")
#         print("  [3] Check inventory")
#         print("  [4] Travel to another location")
#         print("  [5] Look around (re-show scene)")
#         print("  [0] Quit")

#         choice = input("\n  > Your choice: ").strip()

#         if choice == "1":
#             print()
#             interact_with_object(game)
#         elif choice == "2":
#             print()
#             interact_with_character(game)
#         elif choice == "3":
#             print()
#             show_inventory(game)
#         elif choice == "4":
#             print()
#             navigate(game)
#         elif choice == "5":
#             print()
#             show_scene(game)
#         elif choice == "0":
#             print()
#             _print("Goodbye, detective.")
#             break
#         else:
#             _print("Unknown command.")

# from src.game import Game


# def _line(char="─", width=60):
#     print(char * width)

# def _header(title):
#     _line()
#     print(f"  {title}")
#     _line()

# def _print(text):
#     print(f"  {text}")

# def _ask(prompt):
#     return input(f"\n  > {prompt}: ").strip()


# def show_scene(game):
#     scene = game.which_scene_am_i_in()
#     if scene is None:
#         _print("You are nowhere.")
#         return

#     _header(f" {scene.name}")
#     _print(scene.description)

#     objects = scene.show_available_things()
#     if objects:
#         print()
#         _print("Objects you can see:")
#         for obj in objects:
#             _print(f"  • {obj.name}")
#     else:
#         print()
#         _print("There are no objects here.")

#     chars = scene.get_characters()
#     if chars:
#         print()
#         _print("People here:")
#         for c in chars:
#             _print(f"  • {c.name} – {c.description}")


# def interact_with_object(game):
#     ctrl = game.interaction_ctrl

#     object_name = _ask("Which object do you want to interact with")
#     obj = ctrl.pick_game_object(object_name)

#     if obj is None:
#         _print(f"'{object_name}' is not here.")
#         return

#     interactions = ctrl.get_interaction_types()
#     if not interactions:
#         _print(f"You can't do anything with {obj.name}.")
#         return

#     print()
#     _print(f"What do you want to do with '{obj.name}'?")
#     names = [s.__class__.__name__.replace("Strategy", "") for s in interactions]
#     for i, name in enumerate(names, 1):
#         print(f"  [{i}] {name}")
#     print(f"  [0] Cancel")

#     choice = input("\n  > Your choice: ").strip()

#     if choice == "0":
#         ctrl.cancel_interaction()
#         _print("Cancelled.")
#         return

#     try:
#         idx = int(choice) - 1
#         if idx < 0 or idx >= len(interactions):
#             _print("Invalid choice.")
#             ctrl.cancel_interaction()
#             return
#     except ValueError:
#         _print("Invalid input.")
#         ctrl.cancel_interaction()
#         return

#     strat_name = interactions[idx].__class__.__name__
#     ctrl.choose_interaction(strat_name)

#     if ctrl._selected_strategy and ctrl._selected_strategy.needs_more_info():
#         opts = _ask("Additional input needed (e.g. direction)")
#         ctrl.provide_options(opts)

#     print()
#     result = ctrl.perform_interaction()
#     _print(result)


# def interact_with_character(game):
#     scene = game.which_scene_am_i_in()
#     if scene is None:
#         _print("You are not in a scene.")
#         return

#     chars = scene.get_characters()
#     if not chars:
#         _print("There is no one here to talk to.")
#         return

#     print()
#     _print("Who do you want to talk to?")
#     for i, c in enumerate(chars, 1):
#         print(f"  [{i}] {c.name} – {c.description}")
#     print(f"  [0] Cancel")

#     choice = input("\n  > Your choice: ").strip()
#     if choice == "0":
#         return

#     try:
#         idx = int(choice) - 1
#         if idx < 0 or idx >= len(chars):
#             _print("Invalid choice.")
#             return
#     except ValueError:
#         _print("Invalid input.")
#         return

#     charName = chars[idx].name

#     ok = game.initiate_conversation(charName)
#     if not ok:
#         _print(f"{charName} is not available to talk right now.")
#         return

#     _line()
#     _print(f"You start talking to {charName}.")
#     _print("(Type your message, 'accept' to take an offered item, or 'bye' to end.)")
#     _line()

#     while game.character_ctrl.is_in_conversation:
#         query = input("\n  You: ").strip()

#         if not query:
#             continue

#         if query.lower() in ("bye", "goodbye", "leave"):
#             game.end_conversation()
#             print()
#             _print(f"You end the conversation with {charName}.")
#             break

#         if query.lower() == "accept":
#             item = game.accept_game_object()
#             if item:
#                 _print(f"{charName} gives you: {item}. It is now in your inventory.")
#             else:
#                 _print(f"{charName} has nothing to give you.")
#             continue

#         resp = game.send_query(query)
#         print()
#         _print(f"{charName}: {resp}")


# def show_inventory(game):
#     _header(" Inventory")
#     inv = game.inventory

#     if inv.is_empty():
#         _print("Your inventory is empty.")
#         return

#     _print("Items in your inventory:")
#     for obj in inv.show_available_things():
#         _print(f"  • {obj.name} – {obj.description}")

#     print()
#     choice = input("  Interact with an item? (enter name or press Enter to skip): ").strip()
#     if choice:
#         curr_scene = game.which_scene_am_i_in()
#         game._world_service.set_active_scene(inv)
#         interact_with_object(game)
#         game._world_service.set_active_scene(curr_scene)


# def navigate(game):
#     all_scenes = game.get_all_scenes()
#     curr = game.which_scene_am_i_in()

#     _print("Available locations:")
#     for i, scene in enumerate(all_scenes, 1):
#         marker = " ← you are here" if scene == curr else ""
#         print(f"  [{i}] {scene.name}{marker}")
#     print("  [0] Stay here")

#     choice = input("\n  > Your choice: ").strip()
#     if choice == "0":
#         return

#     try:
#         idx = int(choice) - 1
#         if 0 <= idx < len(all_scenes):
#             target = all_scenes[idx]
#             game.go_to_scene(target.name)
#             print()
#             show_scene(game)
#         else:
#             _print("Invalid choice.")
#     except ValueError:
#         _print("Invalid input.")


# def run(game):
#     print()
#     _line("═")
#     print("  MEAN STREETS – Karlskrona")
#     print("  A detective mystery")
#     _line("═")
#     print()
#     _print("Your secretary just texted you:")
#     _print('"There\'s been a murder at Stortorget. Get there now."')
#     print()
#     input("  Press Enter to begin...")

#     show_scene(game)

#     while True:
#         print()
#         _line()
#         stage = game.game_plot.get_current_stage()
#         _print(f"Stage: {stage.description}")
#         _line()
#         print("  What do you want to do?")
#         print("  [1] Interact with an object")
#         print("  [2] Talk to someone")
#         print("  [3] Check inventory")
#         print("  [4] Travel to another location")
#         print("  [5] Look around (re-show scene)")
#         print("  [0] Quit")

#         choice = input("\n  > Your choice: ").strip()

#         if choice == "1":
#             print()
#             interact_with_object(game)
#         elif choice == "2":
#             print()
#             interact_with_character(game)
#         elif choice == "3":
#             print()
#             show_inventory(game)
#         elif choice == "4":
#             print()
#             navigate(game)
#         elif choice == "5":
#             print()
#             show_scene(game)
#         elif choice == "0":
#             print()
#             _print("Goodbye, detective.")
#             break
#         else:
#             _print("Unknown command.")
