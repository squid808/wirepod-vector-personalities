# Vector Personalities
I have been piecing together the components to allow us to create more rich and flexible personalities for the vectors. This is as of yet incomplete, and needs to be refined a lot.

## MVP
The MVP goal is to allow this project to capture the unhandled system messages, throw those to the prompt generation against a personality, and update intents to then have future responses of the same intent to draw from the same generated list, saving on cloud IO and allowing more offline personality.

## TODO
- chain calls together
  - accept custom text to main
    - if no personality, prompt to create one. if no, pass through to OpenAI. if yes:
      - generate personality
      - call openAI to refine quirk
  - check for existing personality intent responses
  - if not
    - from main call response generator
    - chain OpenAI commands
    - save responses
  - if so, use intent to query response from file
    - if usage of file exceeds threshold, refresh/add more
- pass through and do not save factual information requests
- installer script, including ability to add in custom OpenAI key
- unit tests (teehee)

## Wish List
- update / migrate scripts
- tracking of recent responses to allow user to tell Vector to not use that one again
- tracking of recent milestones to influence?
- creating self-starting features to run at random
  - look for face, ask questions, follow up on things
- tracking of user responses, with OpenAI, to influence and align the personality of the vector (with a toggle to disable)
- daily updates to the personality questions most used
- voice commands to list, reassign and create personalities
- conversational options vs just one-off responses
- Github Pages demo
- adding in AI controlled behaviors in tandem with response, based on the response tone/intent
- other custom commands - refined setting of eye color, verbal triggering of behaviors, muting