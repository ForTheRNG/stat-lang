TARGET_EXEC := interpreter

BUILD_DIR := ./obj
TESTS_DIR := ./tests
SRC_DIRS := ./src

OTHER_FLAGS := -std=c++17 -Wall -m64 -Isrc

# Find all the C and C++ files we want to compile
# Note the single quotes around the * expressions. The shell will incorrectly expand these otherwise, but we want to send the * directly to the find command.
SRCS := $(shell find $(SRC_DIRS) -name '*.cpp' -or -name '*.c' -or -name '*.s')

# Prepends BUILD_DIR and appends .o to every src file
# As an example, ./your_dir/hello.cpp turns into ./build/./your_dir/hello.cpp.o
OBJS := $(SRCS:%=$(BUILD_DIR)/%.o)

# String substitution (suffix version without %).
# As an example, ./build/hello.cpp.o turns into ./build/hello.cpp.d
DEPS := $(OBJS:.o=.d)

# Every folder in ./src will need to be passed to GCC so that it can find header files
INC_DIRS := $(shell find $(SRC_DIRS) -type d)
# Add a prefix to INC_DIRS. So moduleA would become -ImoduleA. GCC understands this -I flag
INC_FLAGS := $(addprefix -I,$(INC_DIRS))

TEST_SRCS := $(shell find $(TESTS_DIR) -name '*.cpp' -or -name '*.c')
TESTS := $(TEST_SRCS:%/test.cpp=%)
TEST_EXES := $(TESTS:%=%.exe)

# The -MMD and -MP flags together generate Makefiles for us!
# These files will have .d instead of .o as the output.
CPPFLAGS := $(INC_FLAGS) -MMD -MP

# The final build step.
$(BUILD_DIR)/$(TARGET_EXEC): $(OBJS)
	@ echo -ne '\n'
	@ $(CXX) $(OBJS) -o $@ $(LDFLAGS) $(OTHER_FLAGS)

# Build step for C source
$(BUILD_DIR)/%.c.o: %.c
	@ mkdir -p $(dir $@)
	@ echo '$<'
	@ $(CC) $(CPPFLAGS) $(CFLAGS) -c $< -o $@
	@ echo -ne '\n'

# Build step for C++ source
$(BUILD_DIR)/%.cpp.o: %.cpp
	@ mkdir -p $(dir $@)
	@ echo '$<'
	@ $(CXX) $(CPPFLAGS) $(CXXFLAGS) -c $< -o $@ $(OTHER_FLAGS)
	@ echo -ne '\n'

$(TESTS_DIR)/%.exe: $(TESTS_DIR)/%/test.cpp
	@ $(CXX) $(CXXFLAGS) $(LDFLAGS) -Wno-exceptions -o $@ $< $(OTHER_FLAGS)

.PHONY: tests clean
clean:
	rm -r $(BUILD_DIR)
	rm tests/*.exe

tests: $(TEST_EXES)
	@ echo $(TESTS)
	@ for folder in $(TESTS); do echo ''; cd $$folder; ../../$$folder.exe; cd ../..; done

# Include the .d makefiles. The - at the front suppresses the errors of missing
# Makefiles. Initially, all the .d files will be missing, and we don't want those
# errors to show up.
-include $(DEPS)