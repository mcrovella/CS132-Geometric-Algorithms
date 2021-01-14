import os
import glob
import re

# configuration
course = 'cs132'
session = 's21'

# config file location
config_file_location = 'https://www.cs.bu.edu/faculty/crovella/diagramar'

# figure file location
figure_file_location = 'https://www.cs.bu.edu/faculty/crovella/{}-figures'.format(course)

# get all figure names 
figure_files = glob.glob('Fig*.json')
#
# the pattern that figure names should follow
name_pattern = r'Fig(\d+).(\d+).json'

figs = []
for figname in figure_files:
    match = re.search(name_pattern, figname)
    if match:
        figs.append([match.group(1, 2), (int(match.group(1)), int(match.group(2)))])
    else:
        'unparseable figure name: {}'.format(figname)

# handle figures in proper order
high_order = len(figs)
figs_in_order = sorted(figs, key = lambda x: x[1][0]*high_order + x[1][1])

lesson_ints = list(set([x[1][0] for x in figs_in_order]))
lesson_ints_in_order = sorted(lesson_ints)

# format strings needed to create lesson file in JSON
lesson_file_header = '{\n  "LessonPointers": [\n'
lesson_entry_pattern =  '  {{"Name" : "Lecture {}", "URL" : "{}/config-' + course + '-' + session + '-L{:02d}.json"}}'
lesson_file_footer = '  ]\n}'

# create lesson file
with open('config-{}-{}.json'.format(course, session), 'w') as fp:
    fp.write(lesson_file_header)
    first_item = True
    for lesson in lesson_ints_in_order:
        if not first_item:
            fp.write(',\n')
        else:
            first_item = False
        fp.write(lesson_entry_pattern.format(lesson,
                                                 config_file_location, lesson))
    fp.write('\n' + lesson_file_footer)
                 
lesson_header = '{\n  "FigurePointers": [\n'
lesson_pattern =  '  {{"Name" : "Figure {}.{}", "URL" : "{}/Fig{}.{}.json"}}'
lesson_footer = '  ]\n}'

# create each lesson
for lesson in lesson_ints_in_order:
    first_item = True
    with open('config-{}-{}-L{:02}.json'.format(course, session, lesson), 'w') as fp:
        fp.write(lesson_header)
        lesson_figs = [f for f in figs_in_order if f[1][0] == lesson]
        for lesson_fig in lesson_figs:
            if not first_item:
                fp.write(',\n')
            else:
                first_item = False
            # example lesson fig: [('01', '9'), (1, 9)]]
            fp.write(lesson_pattern.format(lesson_fig[1][0],
                            lesson_fig[1][1], figure_file_location,
                            lesson_fig[0][0], lesson_fig[0][1]))
        fp.write('\n' + lesson_footer)
                
