def shift_character(c, shift):
    if c.isalpha(): 
        base = ord('a') if c.islower() else ord('A')
       
        return chr((ord(c) - base + shift) % 26 + base)
    return c  

def encrypt_decrypt_string(s, operation_type):
    result = []
    for i, c in enumerate(s):
        position = i + 1  
        if operation_type == 1:  
            shifted_char = shift_character(c, position)
        else: 
            shifted_char = shift_character(c, -position)
        result.append(shifted_char)
    return ''.join(result)

user_input = input()
s, operation_type = user_input.rsplit(' ', 1)
operation_type = int(operation_type)
output = encrypt_decrypt_string(s, operation_type)
print(output)

