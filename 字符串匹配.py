def shift_character(c, shift):
    if c.isalpha():  # 检查是否为字母
        base = ord('a') if c.islower() else ord('A')
        # 使用模运算处理循环
        return chr((ord(c) - base + shift) % 26 + base)
    return c  # 非字母字符保持不变

def encrypt_decrypt_string(s, operation_type):
    result = []
    for i, c in enumerate(s):
        position = i + 1  # 位置从1开始计数
        if operation_type == 1:  # 加密
            shifted_char = shift_character(c, position)
        else:  # 解密
            shifted_char = shift_character(c, -position)
        result.append(shifted_char)
    return ''.join(result)

try:
    user_input = input("请输入字符串和操作类型（如 'HelloWorld 1'）: ")
    s, operation_type = user_input.rsplit(' ', 1)
    operation_type = int(operation_type)
    
    if operation_type not in [0, 1]:
        raise ValueError("操作类型必须为0或1。")
    
    output = encrypt_decrypt_string(s, operation_type)
    print(output)

except ValueError as ve:
    print(f"输入错误: {ve}")
except Exception as e:
    print(f"发生了一个错误: {e}")
