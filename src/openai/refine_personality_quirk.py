# System message
system_message_quirk = """
You are creating a personality profile where there is a primary, standout personality quirk. You will be provided 
with a generic quirk and need to come up with a specific version of that quirk to be referenced in the future.

The quirk you receive may be general or abstract, and your task is to make it more specific. For example:
- If the quirk mentions an animal sound, specify which animal makes that sound.
- If it mentions a time period or place, specify the exact time period or location.
- If the quirk does not need further clarification, you may return the provided quirk as-is.

The result should be in plain text format, reflecting the specified quirk as accurately and specifically as possible.
"""

# Generate quirk message
generate_quirk_message = """
You are creating a personality profile and need to refine a generic quirk into a specific version. Use the following 
generic quirk and make it specific based on the guidelines:

Generic Quirk: {generic_quirk}

Instructions:
1. If the quirk mentions an animal sound, specify the exact animal.
2. If it mentions a time period or place, specify the exact time period or location.
3. If the quirk is already specific or does not need further clarification, return the provided quirk as is.

Return the result in plain text format, reflecting the specific quirk accurately.
"""

# User message
user_message_quirk = """
Generic Quirk: {generic_quirk}
"""

# Combining everything into one Python file structure
def create_quirk_messages(generic_quirk):
    # User message passed with the generic quirk
    user_message_filled = f"""
    Generic Quirk: {generic_quirk}
    """
    
    return {
        'system_message_quirk': system_message_quirk,
        'generate_quirk_message': generate_quirk_message,
        'user_message_quirk': user_message_filled
    }

# Example use
if __name__ == "__main__":
    generic_quirk = "likes to make unusual animal sounds"

    quirk_messages = create_quirk_messages(generic_quirk)
    print(quirk_messages)