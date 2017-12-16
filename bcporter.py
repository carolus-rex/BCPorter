import re

from PIL import Image, ImageFont, ImageDraw

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
    with open("show_commands.txt") as show_commands_file:
        commands = [(command.strip(), False) for command in show_commands_file.readlines()]

    with open("atp_commands.txt") as atp_commands_file:
        commands.extend((command.strip(), True) for command in atp_commands_file.readlines())

    return commands


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


FOREGROUND = (255, 255, 255)
WIDTH = 375
HEIGHT = 50


def lines_to_png(lines, file_name):
    font_path = 'C:\\Windows\\fonts\\lucon.ttf'
    font = ImageFont.truetype(font_path, 14, encoding='unic')
    (width, height) = font.getsize('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890,._-?¡¿')

    lines_height = height * len(lines)

    x = Image.new("RGBA", (1000, lines_height), (0, 0, 0))

    draw = ImageDraw.Draw(x)

    for index, line in enumerate(lines):
        draw.text((0, index * height), line, font=font, fill=FOREGROUND)

    x.show()
    x.save('%s.png' % file_name)


prompt = 'Caj_MayorsaBrena#'

for command, is_atp in get_commands():
    command_outputs = get_command_output(command, prompt, 'processed_log')

    index = 0
    if len(command_outputs) > 1:
        for i, output in enumerate(command_outputs):
            print(''.join(output))

            print('     ****************************************************END OF OUTPUT %i****************' % i)

        print("***************************************************************END OF OUTPUT FOR %s*************" % command)

        print("More than one %s output has been found" % command.upper())
        index = input('Choose the INDEX of the desired output: ')
        try:
            index = int(index)
        except:
            pass

        while index not in range(len(command_outputs)):
            print('Invalid index')
            index = input('Choose the INDEX of the desired output: ')
            try:
                index = int(index)
            except:
                continue

    if is_atp:
        data = list(command_outputs[index])
        data.append(prompt)

        lines_to_png(data, command)
    else:
        with open('final_report', 'a') as final_report:
            for line in command_outputs[index]:
                final_report.write(line)

            final_report.write(COMMAND_OUTPUT_SEPARATOR)

print("*******************************FINISHED*****************************")
