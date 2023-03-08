import time

with open("Level1.schema") as f:
    tabbed = f.read()

start = time.time()

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ "
replace = {}

list_depth = 0
out = ""
splitted = tabbed.split("\n")
cache = []

def startswith_any(string: str, start_alphabet: str) -> bool:
    for a in start_alphabet:
        if string.startswith(a): return True
    return False

for x in splitted:
    # Replacement dict
    if len(x) >= 3 and startswith_any(x, ALPHABET) and x[1] == "/":
        try: int(x[2])
        except: exit("Expected int n in schematic X/n")
        replace.update({x[0]: int(x[2])})

    if x == "-----":
        replace = {}

    # List generation
    if x == ",.....................":
        list_depth += 1
        cache.append([])

    elif x.startswith("."):
        x = x.strip(".")
        x = x + (" " * (21 - len(x)))
        for char in x:
            if char not in replace.keys(): exit("Unknown character found: " + str(char))
            cache[list_depth-1].append(replace[char])

for i in range(len(cache)):
    out +=  "{" + ",".join(str(x) for x in cache[i]) + "}->List " + str(i+1) + "\n"

end = time.time()

with open("Level1.list", "w") as f:
    f.write(out)

diff = end - start

print(str(diff) + "s")
print(str(len(out)) + "B")
if diff > 0: print(str(len(out)/1024/1024/diff) + "MB/s")
