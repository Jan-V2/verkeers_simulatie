zuiden = [
    0, 0, 0, 0, 0, 0, 0.70866, 0.234241, -34.1418,
    0, 0, 0, 0, 0, 0, 0.47698, 0.536443, -30.6595,
    0, 0, 0, 0, 0, 0, 0.61923, 0.7199, -27.8472,
    0, 0, 0, 0, 0, 0, 0.77939, 0.711112, -16.5046,
    0, 0, 0, 0, 0, 0, 0.70094, 0.349773, -15.124,
]


noorden = [
    0, 0, 0, 0, 0, 0, 0.70094, 0.349773, -15.124,
    0, 0, 0, 0, 0, 0, 0.77939, 0.711112, -16.5046,
    0, 0, 0, 0, 0, 0, 0.61923, 0.7199, -27.8472,
    0, 0, 0, 0, 0, 0, 0.47698, 0.536443, -30.6595,
    0, 0, 0, 0, 0, 0, 0.70866, 0.234241, -34.1418,
]

row_len = 9
rows = int(len(zuiden) / row_len)
start_offset = 6

naar_zuiden = True

translation = -5

if naar_zuiden:
    for i in range(rows):
        zuiden[i * row_len + start_offset] += translation
    print(zuiden)
else:
    for i in range(rows):
        noorden[i * row_len + start_offset] += translation
    print(noorden)
