import base64
import unittest
import builtins

def api_redirection(a, b):
    def _real_api_add(x, y):
        return x + y
    def _wrapper(x, y):
        return _real_api_add(x, y)
    return _wrapper(a, b)

def mixed_language_tiny_interpreter(bytecode):
    stack = []
    for instr in bytecode.split(';'):
        instr = instr.strip()
        if not instr:
            continue
        if instr.startswith("PUSH"):
            _, val = instr.split()
            stack.append(int(val))
        elif instr == "ADD":
            b = stack.pop()
            a = stack.pop()
            stack.append(a + b)
    return stack.pop() if stack else None

def base64_encoded_string(encoded_str):
    return base64.b64decode(encoded_str).decode()

def xor_string_encryption(s, key=42):
    return ''.join(chr(ord(c) ^ key) for c in s)

def control_flow_flattening(x):
    state = 0
    while True:
        if state == 0:
            if x > 0:
                state = 1
            else:
                state = 2
        elif state == 1:
            return x * 2
        elif state == 2:
            return -x

def dummy_code_insertion(x):
    dummy = 123
    return x + 1

def string_splitting_concatenation():
    part1 = "Hel"
    part2 = "lo"
    return part1 + part2

def function_reordering():
    def a():
        return 1
    def b():
        return 2
    return b() + a()

def opaque_predicates(x):
    if (x * x) % 2 == 0:
        return x * 3
    else:
        return x

def arithmetic_obfuscation(x):
    return ((x * 3 + 6) - 6) // 3

def encoding_decoding_layers(s):
    layer1 = base64.b64encode(s.encode())
    layer2 = base64.b64encode(layer1)
    return base64.b64decode(base64.b64decode(layer2)).decode()

def reflection_dynamic_calls():
    func = getattr(builtins, "len")
    return func([1, 2, 3])

class TestObfuscationTechniques(unittest.TestCase):
    def test_api_redirection(self):
        self.assertEqual(api_redirection(2, 3), 5)

    def test_mixed_language(self):
        self.assertEqual(mixed_language_tiny_interpreter("PUSH 2; PUSH 3; ADD;"), 5)

    def test_base64_encoded_string(self):
        self.assertEqual(base64_encoded_string("SGVsbG8="), "Hello")

    def test_xor_string_encryption(self):
        s = "Hello"
        encrypted = xor_string_encryption(s)
        decrypted = xor_string_encryption(encrypted)
        self.assertEqual(decrypted, s)

    def test_control_flow_flattening(self):
        self.assertEqual(control_flow_flattening(5), 10)
        self.assertEqual(control_flow_flattening(-3), 3)

    def test_dummy_code_insertion(self):
        self.assertEqual(dummy_code_insertion(4), 5)

    def test_string_splitting_concatenation(self):
        self.assertEqual(string_splitting_concatenation(), "Hello")

    def test_function_reordering(self):
        self.assertEqual(function_reordering(), 3)

    def test_opaque_predicates(self):
        self.assertEqual(opaque_predicates(2), 6)
        self.assertEqual(opaque_predicates(3), 3)

    def test_arithmetic_obfuscation(self):
        self.assertEqual(arithmetic_obfuscation(9), 9)

    def test_encoding_decoding_layers(self):
        self.assertEqual(encoding_decoding_layers("Hello"), "Hello")

    def test_reflection_dynamic_calls(self):
        self.assertEqual(reflection_dynamic_calls(), 3)

if _name_ == "_main_":
    unittest.main()