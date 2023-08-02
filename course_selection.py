from nicegui import ui
import time

# This is a table test

columns = [
    {'name': 'id', 'label': "Course #", 'field': 'id', 'required': True, 'sortable': True},
    {'name': 'course_name', 'label': 'Course Name', 'field': 'name', 'required': True, 'sortable': True, 'align': 'left'},
    {'name': 'req', 'label': "Prerequisites", 'field': 'req', 'required': True, 'align': 'left'}
]
rows = [
    {'id': 0, 'name': 'intro to marvel movies', 'req': 'brain, humor'},
    {'id': 1, 'name': 'memes history'},
    {'id': 2, 'name': 'intro to programming of meme machines'},
    {'id': 30752, 'name': 'Operating Systems', 'req': 'Discrete Mathematics'}
]

with ui.table(title='Course List', columns=columns, rows=rows, selection='multiple', pagination=10).classes('w-96').style('margin: auto; width: 75%; max-width: 1280px') as table:
    with table.add_slot('top-right'):
        with ui.input(placeholder='Search').props('type=search').bind_value(table, 'filter').add_slot('append'):
            ui.icon('search')
    with table.add_slot('bottom-row'):
        with table.row():
            with table.cell():
                ui.button(on_click=lambda: (
                    table.add_rows({'id': time.time(), 'name': new_name.value, 'req': new_req.value}),
                    new_name.set_value(None),
                    new_req.set_value(None),
                ), icon='add').props('flat fab-mini')
            with table.cell().style('width: 0px'):
                new_id = ui.input('id')
            with table.cell():
                new_name = ui.input('Name')
            with table.cell():
                new_req = ui.number('req')

ui.label().bind_text_from(table, 'selected', lambda val: f'Current selection: {val}')
ui.button('Remove', on_click=lambda: table.remove_rows(*table.selected)) \
    .bind_visibility_from(table, 'selected', backward=lambda val: bool(val))

ui.run()




