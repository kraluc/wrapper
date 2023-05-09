# Wrapper

## Introduction

This script generates a new list of commands that includes capturing the command itself, and a timestamp in addition to the desired output. This new list is displayed on the screen and saved to file so it can easily be uploaded to a switch and executed by copying it to running-config.

## Installation

+ No additional module required at this time

## High Level Solution

1. Read content of file containing show commands, (default "cli.txt")

    ```python
    with open(file="cli.txt", mode="r", encoding="UTF-8") as f_read:
        first_line = str(f_reader.readline().strip())
    ```

2. For each ```<show command>``` generate the associated commands and redirect them to bootflash:

    ```python
    echo "### <my show command>" >> $(SWITCHNAME)-logs.txt
    show clock >> $(SWITCHNAME)-logs.txt
    <my show command>  >> $(SWITCHNAME)-logs.txt
    ```

3. script outputs the result to screen for easy copy/paste and also save it to a file that can be uploaded to a switch and copied to running-config to generate the desired result.

+ first line should be an overwrite redirect
+ next lines should append to the file

```python
        my_stuff = '''
        this is an example
        '''
        with open(file="output.txt", mode="w", encoding="UTF-8") as f_write:
            f_write.write(my_stuff)
```
