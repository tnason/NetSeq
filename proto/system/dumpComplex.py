import pprint, pickle, random
import time

# Initialize clock
start = time.clock()

'''Compute the number of seconds (floating point) that have passed since
last call)'''
def time_passed():
    global start
    end = time.clock()
    time_passed = end - start
    start = end
    return time_passed

'''Main procedures'''
def main():
    # Create data
    data = []

    # Prepare RNG
    random.seed(0)

    # Add bunch of random numbers to data
    for num in range(0, 1000000):
        new_int = random.randint(0, 1000000)
        data.append(new_int)

    print "Data created in " + str(time_passed()) + " seconds"

    # Open file for writing
    file = open("files/hello.txt", "w")

    # Dump content in default format
    pickle.dump(data, file)

    print "Data dumped in " + str(time_passed()) + " seconds"

    # Close the file
    file.close()

    print "File closed in " + str(time_passed()) + " seconds"

if __name__=="__main__":
    # Run the main function
    main()

