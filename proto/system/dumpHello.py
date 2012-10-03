import pprint, pickle

# Create data
string = "Hello world!"

# Open file for writing
file = open("files/hello.txt", "w")

# Dump content in default format
pickle.dump(string, file)

# Close the file
file.close()

