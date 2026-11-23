import ollama

SYSTEM_PROMT= """
You are Docker Expert, you can explain things in 1-2 lines max . You don't overthink , hallucinate or keep reasoning in loop 
, you Reason and Act accordingly .

These are the things you do :
1) You tell about errors(what went wrong , what might be not written , etc)
2) You tell about root cause (What was the cause likely)
3) You tell about fix or solution in short 
"""
while True:
    user_input = input("Enter your message:\n")
    if user_input == "exit":
        break

    response = ollama.chat(
        model="llama3.2",
        messages=[
            {
                'role': 'system',
                'content': SYSTEM_PROMT
            },

            {
            'role': 'user',
            'content': user_input,
        }]
    )

    print(response['message']['content'])