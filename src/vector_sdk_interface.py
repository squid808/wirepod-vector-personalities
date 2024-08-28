import anki_vector

def main():
    args = anki_vector.util.parse_command_args()

    with anki_vector.Robot(args.serial) as robot:
        robot.behavior.say_text("This hasn't been implemented yet. Whoops.")