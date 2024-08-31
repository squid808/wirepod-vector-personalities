import anki_vector

def main():
    args = anki_vector.util.parse_command_args()

    with anki_vector.Robot(args.serial) as robot:
        robot.behavior.say_text("This hasn't been implemented yet. Whoops.")
        
        
def say_text(bot_serial, text):
    try:
        with anki_vector.Robot(bot_serial) as robot:
            robot.behavior.say_text(text)
    except:
        print("Robot: " + text)