import time

with open("alpha-COOKING1.cas") as f:
    tabbed = f.read()

start = time.time()

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ "
ALLOWED_VARIABLE_NAMES = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

variable_stats = {"numeric": 0, "string": 0, "list": 0}
variables = {}
out_variables = {}

out = ["'ProgramMode:RUN"]
splitted = tabbed.split("\n")
cache = []

def fill_space(string, length = 2):
    string = str(string)
    return " " * (length - len(string)) + string

for x in splitted:
    # Remove space pre- and suffixes
    while x.startswith(" "): x = x.removeprefix(" ")
    while x.endswith(" "): x = x.removesuffix(" ")

    # Remove comments
    is_string = False
    for i in range(len(x)):
        if x[i] == "\"": is_string = not is_string
        if x[i] == "#" and not is_string:
            x = x[:i]
            break

    # Remove blank lines
    if x == "": continue

    is_string = False
    word = ""
    WORD_TO_FIND = "->"
    for i in range(len(x)-1):
        if x[i] == "\"": is_string = not is_string
        word += x[i]
        wfi = word.find(WORD_TO_FIND)
        if wfi > 0 and not is_string:
            #content, variable = x[:wfi], x[wfi+len(WORD_TO_FIND):]
            #variable = variable.split(" ")[0]
            content, variable_temp = x[:wfi], x[wfi+len(WORD_TO_FIND):]
            variable = ""
            for char in variable_temp:
                if char == " ": break
                variable += char

            if variable.endswith("]"): break
            if variable not in variables: variables.update({variable: content})
            break

    cache.append(x)

splitted = cache
cache = []

#print(splitted)

for variable in variables:
    content = variables[variable]
    if content.startswith("{"): # List (TODO: cap this because the calc doesnt have unlimited lists)
        variable_stats["list"] += 1
        out_variables.update({"List " + str(variable_stats["list"]): content})

    elif content.startswith("\"") or content.startswith("\'"): # Str (TODO: same here)
        variable_stats["string"] += 1
        out_variables.update({"Str " + str(variable_stats["string"]): content})

    else: # Numeric (already capped with ALLOWED_VARIABLE_NAMES)
        if variable_stats["numeric"] == len(ALLOWED_VARIABLE_NAMES): exit("Too much variables used. Limit: 26.")
        out_variables.update({ALLOWED_VARIABLE_NAMES[variable_stats["numeric"]]: content})

        variable_stats["numeric"] += 1

print(variables)
print()
print(out_variables)
print()

# Replace variable names with ALLOWED_VARIABLE_NAMES / Lists / Strings (casio friendly)
#for x in splitted:
"""
    is_string = False
    line = ""
    for word in x.split(" "):
        if word == "\"": is_string = not is_string
        if is_string: continue
        print(word)
        if word in list(variables.keys()):
            var_index = list(variables.keys()).index(word)
            out_variable = list(out_variables.keys())[var_index]

            print("Replacing " + word + " with " + out_variable)

            word = out_variable

        line += word + " "

    cache.append(line)
"""
for x in splitted:
    for WORD_TO_FIND in ["->", "="]:
        is_string = False
        word = ""
        #WORD_TO_FIND = "->"
        for i in range(len(x)-1): # gotta change this to not "->" but all words in the line and then replace everything that is a variable with its dum name (casio friendly)
            if x[i] == "\"": is_string = not is_string
            word += x[i]
            wfi = word.find(WORD_TO_FIND)
            if wfi > 0 and not is_string:
                content, variable_temp = x[:wfi], x[wfi+len(WORD_TO_FIND):]
                variable = ""
                for char in variable_temp:
                    if char == " ": break
                    variable += char

                if variable.endswith("]"): break # gotta implement this tho

                var_index = list(variables.keys()).index(variable)
                out_variable = list(out_variables.keys())[var_index]

                print(variable + " wird zu " + out_variable)

                all_after_var = x[wfi+len(WORD_TO_FIND)+len(variable):]

                x = content + "->" + out_variable + all_after_var

                break

    cache.append(x)

splitted = cache
cache = []

print(splitted)
print()

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
