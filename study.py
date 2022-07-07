# class UniqueChars(object):
#     def has_unique_chars(self, string):
#         if string == "None":
#             return False
#         return len(set(string)) == len(string)
#
# s = UniqueChars()
# while True:
#     st = input('输入')
#     print(s.has_unique_chars(st))

# num = 28
# str = f'(R{num}*S{num}+U{num}*V{num})*N{num}*L26'
# # s = '((R21*S21+U21*V21)*N21+R22*S22+U22*V22)*N22+(R23*S23+U23*V23)*N23)*L21)'
# print(str)

# l = [1, 2, 3]
# k = ['a', 's', 'd']
# print(dict(zip(l, k)))
# for k, v in dict(zip(l, k)).items():
#     print(v)
import random

print(round(random.random(), 1))
print(random.randrange(-1, 1))
print(range(-1, 2))


