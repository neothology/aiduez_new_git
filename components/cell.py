import ipywidgets as widgets
from IPython.display import display
import ipyvuetify as v

class AppCell:
    " AIan App Cell.. "
    def __init__(self, output, cfgCell, context):
        self.output = output
        self.config = cfgCell
        self.context = context

    def onEvent(self, idEvent):
        self.context.setLastEvent(idEvent)
        #events = self.config['events'] if 'events' in self.config.keys() else {}
        events = self.context.config['events'] if 'events' in self.context.config.keys() else {}
        actions = events[idEvent] if idEvent in events.keys() else []
        # with self.output:
        #     display(actions)
        #    display(f'onEvent: event-{idEvent}, actions-{str(actions)}')
        for action in actions:
            actionCode = action['action'] if 'action' in action.keys() else 'none'
            cellTarget = self.context.getCellOf(action['target-cell'])
            args = action['args'] if 'args' in action.keys() else []
            if cellTarget is None: 
                continue
            cellTarget.handleAction(actionCode, args)


    def replayLastEvent(self):
        eventLast = self.context.getLastEvent()
        self.output.clear_output()
        #with self.output:
        #    display(f'replaying last event {eventLast}')
        if eventLast is not None:
            self.onEvent(eventLast)
        else:
            self.draw()

    def replayLastEvent_except_CTX(self):
        eventCurrent = self.context.currEvent
        if eventCurrent is not None:
            instance = self.context.getCellOf(eventCurrent)
            instance.output.clear_output()
            instance.draw()

    ## event handlers..
    def onButtonPressed(self, btn):
        self.onEvent(btn.event)
            
    def handleAction(self, actionCode, args):
        if actionCode in ['clear-cell']:
            self.output.clear_output()
        elif actionCode in ['apply-form'] and len(args)>0:
            for formName in args:
                form = self.context.getCellOf(formName) 
                with self.output:  
                    display(form.output)
                    form.output.clear_output()
                    form.draw()

    def make_buttons_list(self,button_spec_list,layout,disabled=False,style=None,class_name=None):
        buttons_list=[]
        for button_spec in button_spec_list:
            button = v.Btn(color = "primary", children = [button_spec[0]])
            # button = widgets.Button(description=button_spec[0],layout=layout,disabled =disabled)
            if style is not None:
                button.style = style
            button.event = button_spec[1]
            if class_name is not None:
                button.add_class(class_name)
            button.on_click(self.onButtonPressed)
            buttons_list.append(button)
        return buttons_list

    def make_buttons_list_v(self,button_spec_list,layout,disabled=False):
        buttons_list=[]
        for button_spec in button_spec_list:
            button = v.Btn(color = "primary", children = [button_spec[0]])
            # button = widgets.Button(description=button_spec[0],layout=layout,disabled =disabled)
            button.event = button_spec[1]
            button.on_click(self.onButtonPressed)
            buttons_list.append(button)
        return buttons_list
