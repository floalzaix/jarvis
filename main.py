#
#   Imports
#

# Perso

from llm import infer

#
#   Script
#

def main():
    while True:
        user_input = input("> ")

        if user_input:
            stream = infer(
                user_input,
            )

            for chunk in stream:
                print(chunk.message.content, end="", flush=True)

            print("\n")
            

if __name__ == "__main__":
    main()