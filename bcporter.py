import re

CHAR_BACKSPACE = re.compile(".\b")    # Don't use a raw string here
ANY_BACKSPACES = re.compile("\b+")  # or here

COMMAND_OUTPUT_SEPARATOR = '-' * 100 + '\n'


def reset_file(file_path):
    with open(file_path, 'w') as shit:
        shit.write('')


def process_non_printable(s):
    pattern = '[^\b]\b'
    sub = ''
    flags = re.U

    patc = re.compile(pattern, flags)

    sold = ''
    while sold != s:
        sold = s
        #print("patc=>%s<    sold=>%s<   s=>%s<" % (patc,sold,s))
        s = patc.sub(sub, sold)
        #print help(patc.sub)

    return s


reset_file('processed_log')
reset_file('final_report')

with open('test_log') as log:
    for line in log.readlines():
        new_line = process_non_printable(line)
        with open('processed_log', 'a') as new_log:
            new_log.write(new_line)


def get_commands():
    commands = """show version
show runn"""

    return (command.strip() for command in commands.splitlines())


def get_command_output(command, prompt, log_name):
    recording_prompt = False

    command_outputs = []

    with open(log_name) as log:
        for line in log.readlines():
            # A command ends when a new prompt appears
            if line.startswith(prompt):
                recording_prompt = False

            # Test if this line is a command start
            if line.strip().lower().endswith(command.lower()):
                recording_prompt = True
                command_outputs.append([])

            if recording_prompt:
                command_outputs[-1].append(line)

    return command_outputs


prompt = 'Caj_MayorsaBrena#'
for command in get_commands():
    command_outputs = get_command_output(command, prompt, 'processed_log')

    index = 0
    if len(command_outputs) > 1:
        for i, output in enumerate(command_outputs):
            print(''.join(output))

            print('     ****************************************************END OF OUTPUT %i****************' % i)

        print("***************************************************************END OF OUTPUT FOR %s*************" % command)

        print("More than one %s output has been found" % command.upper())
        index = input('Choose the INDEX of the desired output: ')

        while index not in range(len(command_outputs)):
            print('Invalid index')
            index = input('Choose the INDEX of the desired output: ')

    with open('final_report', 'a') as final_report:
        for line in command_outputs[index]:
            final_report.write(line)

        final_report.write(COMMAND_OUTPUT_SEPARATOR)

print("*******************************FINISHED*****************************")
