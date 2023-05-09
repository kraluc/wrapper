# Wrapper

## Introduction

This script generates a new list of commands that includes capturing the command itself, and a timestamp in addition to the desired output. This new list is displayed on the screen and saved to file so it can easily be uploaded to a switch and executed by copying it to running-config.

## Release history

+ 0.0.1 Initial release

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

## Getting Started

2 Jupyter notebooks are provided for training:

+ [wrapper.ipynb](./wrapper.ipynb) includes the overall structure (solution removed)
+ [wrapper_solution.ipynb](./wrapper_solution.ipynb) includes a proposed solution

a Python executable with logging and argparse example

+ [wrapper.py](./wrapper.py)

## Usage

```python
usage: wrapper [-h] [--debug] [--input [INPUT]] [--mode {w,a}] [--output [OUTPUT]]

wrap commands read from file

optional arguments:
  -h, --help            show this help message and exit
  --debug, -d           enable debug
  --input [INPUT], -i [INPUT]
                        file containing show commands (Default: 'cli.txt').
  --mode {w,a}, -m {w,a}
                        'a'ppend or over'w'rite logs to 'wrapper.log'. Default: 'w'
  --output [OUTPUT], -o [OUTPUT]
                        save output to file. (Default: 'wrapped_cli.txt')
```

### Running the script with defaults and debug enabled

```python
❯ ./wrapper.py -d

executing wrapper.py as a module...

        overwrite existing logfile(s)
        '/Users/vricci/Documents/Development/PYTHON/wrapper/wrapper.log'

commands read from clis.txt:
=============================

show version
show module
show logg log

wrapped commands:
=================

echo "### show version" >> $(SWITCHNAME)-debugs.txt
show clock >> $(SWITCHNAME)-debugs.txt
show version >> $(SWITCHNAME)-debugs.txt

echo "### show module" >> $(SWITCHNAME)-debugs.txt
show clock >> $(SWITCHNAME)-debugs.txt
show module >> $(SWITCHNAME)-debugs.txt

echo "### show logg log" >> $(SWITCHNAME)-debugs.txt
show clock >> $(SWITCHNAME)-debugs.txt
show logg log >> $(SWITCHNAME)-debugs.txt



wrapped commands saved to 'wrapped_clis.txt'
```

associated logfile ```wrapper.log```

```python
2023-05-09 16:09:20,633 - INFO     - wrapper.py     :<module>                       --------- BEGIN wrapper.py -------
2023-05-09 16:09:20,633 - DEBUG    - wrapper.py     :commands_from_file             opened 'clis.txt' for reading
2023-05-09 16:09:20,634 - INFO     - wrapper.py     :commands_from_file             read command(s): ['show version', 'show module', 'show logg log']
2023-05-09 16:09:20,634 - DEBUG    - wrapper.py     :wite_commands_to_file          opened 'wrapped_clis.txt' for writing
2023-05-09 16:09:20,634 - INFO     - wrapper.py     :wite_commands_to_file          command(s) written to: 'wrapped_clis.txt'
2023-05-09 16:09:20,634 - INFO     - wrapper.py     :<module>
```

### Customize input files and/or output files

+ create a new input file

```python
❯ tee my_clis.txt << EOF
heredoc> show accounting log
heredoc> show logging logfile
heredoc> show module
heredoc> show interface brief
heredoc> show system uptime
heredoc> show module internal exceptionlog
heredoc> EOF
```

+ Run the wrapper on the new input file

```python
❯ ./wrapper.py -d -i ./my_clis.txt -o debug_commands.txt

executing wrapper.py as a module...

        overwrite existing logfile(s)
        '/Users/vricci/Documents/Development/PYTHON/wrapper/wrapper.log'

commands read from ./my_clis.txt:
==================================

show accounting log
show logging logfile
show module
show interface brief
show system uptime
show module internal exceptionlog

wrapped commands:
=================

echo "### show accounting log" >> $(SWITCHNAME)-debugs.txt
show clock >> $(SWITCHNAME)-debugs.txt
show accounting log >> $(SWITCHNAME)-debugs.txt

echo "### show logging logfile" >> $(SWITCHNAME)-debugs.txt
show clock >> $(SWITCHNAME)-debugs.txt
show logging logfile >> $(SWITCHNAME)-debugs.txt

echo "### show module" >> $(SWITCHNAME)-debugs.txt
show clock >> $(SWITCHNAME)-debugs.txt
show module >> $(SWITCHNAME)-debugs.txt

echo "### show interface brief" >> $(SWITCHNAME)-debugs.txt
show clock >> $(SWITCHNAME)-debugs.txt
show interface brief >> $(SWITCHNAME)-debugs.txt

echo "### show system uptime" >> $(SWITCHNAME)-debugs.txt
show clock >> $(SWITCHNAME)-debugs.txt
show system uptime >> $(SWITCHNAME)-debugs.txt

echo "### show module internal exceptionlog" >> $(SWITCHNAME)-debugs.txt
show clock >> $(SWITCHNAME)-debugs.txt
show module internal exceptionlog >> $(SWITCHNAME)-debugs.txt



wrapped commands saved to 'debug_commands.txt'
```

associated syslogs:

```python
2023-05-09 16:12:25,373 - INFO     - wrapper.py     :<module>                       --------- BEGIN wrapper.py -------
2023-05-09 16:12:25,373 - DEBUG    - wrapper.py     :commands_from_file             opened './my_clis.txt' for reading
2023-05-09 16:12:25,374 - INFO     - wrapper.py     :commands_from_file             read command(s): ['show accounting log', 'show logging logfile', 'show module', 'show interface brief', 'show system uptime', 'show module internal exceptionlog']
2023-05-09 16:12:25,374 - DEBUG    - wrapper.py     :wite_commands_to_file          opened 'debug_commands.txt' for writing
2023-05-09 16:12:25,374 - INFO     - wrapper.py     :wite_commands_to_file          command(s) written to: 'debug_commands.txt'
2023-05-09 16:12:25,374 - INFO     - wrapper.py     :<module>
```
