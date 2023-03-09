import time

with open("beta-COOKING1.cas") as f:
    tabbed = f.read()

start = time.time()

out = ["'ProgramMode:RUN"]
splitted = tabbed.split("\n")
cache = []

for x in splitted:
    # Remove space prefixes
    while x.startswith(" "):
        x = x.removeprefix(" ")
    # Remove comments
    if x.startswith("#"): continue
    # Remove blank lines
    if x == "": continue

    cache.append(x)

splitted = cache
cache = []

# Remove comments
for x in splitted:
    if not x.startswith("#"):
        cache.append(x)

splitted = cache
cache = []

def fill_space(string, length = 2):
    string = str(string)
    return " " * (length - len(string)) + string
try:
    # Un-pretty-fie If-Else statements
    prev_line = ""
    for i in range(len(splitted)):
        x = splitted[i]
        if prev_line.startswith("Else") and prev_line != "Else":
            cache[i] = x
            prev_line = x
            continue

        if prev_line.startswith("If ") or prev_line.startswith("Then If "):
            x = "Then " + x
        elif prev_line.startswith("Else"):
            if prev_line != "Else": exit(f"Else not aligned correctly. (line {str(i-1)})")
            cache[-1] += " " + x
            x = splitted[i]
            prev_line = x
            continue

        cache.append(x)
        prev_line = x
except:
    print("Error")
    print(i)
    print(prev_line)
    print(x)

splitted = cache
cache = []

# Create output
out = out + splitted
out = "\n".join(x for x in out)

end = time.time()

with open("COOKING1.txt", "w") as f:
    f.write(out)

diff = end - start

print(str(diff) + "s")
print(str(len(out)) + "B")
if diff > 0: print(str(len(out)/1024/1024/diff) + "MB/s")
