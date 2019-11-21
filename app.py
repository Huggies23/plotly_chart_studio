# import dependencies
import pandas as pd
import numpy as np
from plotly.io import write_image, write_html, write_json
import plotly.graph_objs as go
import panel as pn
import param 
from itertools import cycle
pn.extension('plotly')

# create chart studio class
class ChartStudio(param.Parameterized):
    
    # create param objects for all possible widgets in the app
    
    # import tab
    data_file = param.FileSelector(path='*.csv')
    
    # chart editor tab 
    
    # type tab widgets
    chart_type = param.ObjectSelector(default="Scatter", objects=["Scatter", "Bar"])
    bar_mode = param.ObjectSelector(default="group", objects=["group", "stack", "relative", "overlay"])
    
    # style tab widgets
    
    # general tab widgets
    chart_background_colour = param.Color(default='#ffffff')
    chart_background_opacity = param.Number(0.5, bounds=(0.0, 1.0))
    chart_text_font = param.ObjectSelector(default="Arial", objects=["Arial", "Balto", "Courier New", "Droid Sans", "Droid Serif", 
                                                                     "Droid Sans Mono", "Gravitas One", "Old Standard TT", "Open Sans", 
                                                                     "Overpass", "PT Sans Narrow", "Raleway", "Times New Roman"])
    chart_text_size = param.Integer(default = 12)
    chart_text_colour = param.Color(default='#000000')
    chart_title = param.String(default= '')
    
    plot_width = param.Integer(default =650)
    plot_height = param.Integer(default = 450)
    top_margin = param.Integer(default = 20)
    bottom_margin = param.Integer(default = 80)
    left_margin = param.Integer(default = 80)
    right_margin = param.Integer(default = 80)
    
    # axes tab widgets
    
    axes_colour = param.Color(default='#000000')
    axes_thickness = param.Integer(default = 1)
    x_title = param.String(default= 'x_title')
    y_title = param.String(default= 'y_title')
    y_autorange = param.Boolean(default = True)
    y_min = param.Number(default = None)
    y_max = param.Number(default = None)
    y_grid_lines = param.Boolean(default = False)
    y_zeroline = param.Boolean(default = False)
    auto_x_tick_angle = param.Boolean(default = True)
    x_tick_angle = param.Number(default= None)
    
    # legend tab widgets
    
    auto_position_legend = param.Boolean(default = True)
    legend_x = param.Number(default = 1)
    legend_y = param.Number(default = 1)
    
    # annotate tab widgets
    
    # text annotations widgets
    annotation_1 = param.Boolean(default = False)
    text_1 = param.String(default= 'Annotation 1')
    x_1 = param.Number(default = None)
    y_1 = param.Number(default = None)
    
    annotation_2 = param.Boolean(default = False)
    text_2 = param.String(default= 'Annotation 2')
    x_2 = param.Number(default = None)
    y_2 = param.Number(default = None)
    
    annotation_3 = param.Boolean(default = False)
    text_3 = param.String(default= 'Annotation 3')
    x_3 = param.Number(default = None)
    y_3 = param.Number(default = None)
    
    # shape annotation widgets
    
    square_1 = param.Boolean(default = False)
    square_1_colour = param.Color(default='#0000ff')
    square_1_opacity = param.Number(0.5, bounds=(0.0, 1.0))
    x_min_1 = param.Number(default = None)
    x_max_1 = param.Number(default = None)
    y_min_1 = param.Number(default = None)
    y_max_1 = param.Number(default = None)
    
    square_2 = param.Boolean(default = False)
    square_2_colour = param.Color(default='#00ff00')
    square_2_opacity = param.Number(0.5, bounds=(0.0, 1.0))
    x_min_2 = param.Number(default = None)
    x_max_2 = param.Number(default = None)
    y_min_2 = param.Number(default = None)
    y_max_2 = param.Number(default = None)
    
    # export chart tab
    export_to_file = param.String(default= r"Figure_1", doc="Declare name for exported plot file")
    png = param.Boolean(False, doc="A sample Boolean parameter")
    svg = param.Boolean(False, doc="A sample Boolean parameter")
    pdf = param.Boolean(False, doc="A sample Boolean parameter")
    html = param.Boolean(False, doc="A sample Boolean parameter")
    json = param.Boolean(True, doc="A sample Boolean parameter")
    export_plot = param.Action(lambda x: x.param.trigger('export_plot'))
    
    data = None
    figure = None
    
    @param.depends('data_file', watch=True) 
    def process_file(self):
        self.data = pd.read_csv(self.data_file)
        self.data_cols = list(self.data.columns)
        self.xdata = self.data_cols[0]
        self.x_axis_title = self.xdata
        self.trace_names = self.data_cols[1:]
    
    def show_data(self):
        return self.data
    
    @param.depends('data_file',
                   'chart_type', 'bar_mode',
                   'chart_background_colour', 'chart_background_opacity', 'chart_text_font', 'chart_text_size', 'chart_text_colour', 'chart_title',
                   'plot_width', 'plot_height', 'top_margin', 'bottom_margin', 'left_margin', 'right_margin',
                   'axes_colour', 'axes_thickness', 'x_title', 'y_title', 'y_autorange', 'y_min', 'y_max','y_grid_lines','y_zeroline',
                   'auto_x_tick_angle', 'x_tick_angle',
                   'auto_position_legend','legend_x','legend_y',
                   'annotation_1', 'text_1', 'x_1', 'y_1',
                   'annotation_2', 'text_2', 'x_2', 'y_2',
                   'annotation_3', 'text_3', 'x_3', 'y_3',
                   'square_1', 'square_1_colour', 'square_1_opacity', 'x_min_1', 'x_max_1', 'y_min_1', 'y_max_1',
                   'square_2', 'square_2_colour', 'square_2_opacity', 'x_min_2', 'x_max_2', 'y_min_2', 'y_max_2',
                   watch = True) # all plot widgets I think
    def plot(self):
        colours = cycle(['#3b064d','#8105d8','#ed0cef','#fe59d7'])
        # create traces
        data = []
        for i in range(0, len(self.trace_names)):
            
            colour = next(colours)
            
            if self.chart_type == 'Scatter':
                data.append(go.Scatter(x = self.data[self.xdata],
                                       y = self.data[self.trace_names[i]],
                                       name = self.trace_names[i],
                                       mode = 'lines+markers',
                                       marker=dict(size=12,
                                                   color=colour,
                                                   opacity = 0.5
                                                  ),
                                       line = dict(color = colour,
                                                   width = 2
                                                  )
                                      )
                           )
                
            elif self.chart_type == 'Bar':
                data.append(go.Bar(x = self.data[self.xdata],
                                   y = self.data[self.trace_names[i]],
                                   name = self.trace_names[i],
                                   marker=dict(color=colour,
                                               opacity = 1.0,
                                               line = dict(width = 0)
                                                )
                                  )
                           )
            
        # set values for items with both tickboxes and value boxes
        if self.y_autorange == True:
            ymin = None
            ymax = None
        else:
            ymin = self.y_min
            ymax = self.y_max
        if self.auto_x_tick_angle == True:
            xtickangle = None
        else:
            xtickangle = self.x_tick_angle
        if self.auto_position_legend == True:
            legx = None
            legy = None
        else:
            legx = self.legend_x
            legy = self.legend_y
            
        # set background rgba
        hex = app.chart_background_colour.lstrip('#')
        rgb = tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))
        alpha = self.chart_background_opacity
        bg_rgba = f'rgba({rgb[0]},{rgb[1]},{rgb[2]},{alpha})'
        
        # create annotations and shapes
        annotations = []
        
        if self.annotation_1 == True:
            annotations.append(dict(text = self.text_1,
                                    font = dict(family = self.chart_text_font,
                                                size = self.chart_text_size,
                                                color = self.chart_text_colour
                                               ),
                                    x = self.x_1,
                                    y = self.y_1,
                                    #xref = 'paper',
                                    #yref = 'paper',
                                    showarrow = False
                                   )
                              )
        
        if self.annotation_2 == True:
            annotations.append(dict(text = self.text_2,
                                    font = dict(family = self.chart_text_font,
                                                size = self.chart_text_size,
                                                color = self.chart_text_colour
                                               ),
                                    x = self.x_2,
                                    y = self.y_2,
                                    #xref = 'paper',
                                    #yref = 'paper',
                                    showarrow = False
                                   )
                              )
            
        if self.annotation_3 == True:
            annotations.append(dict(text = self.text_3,
                                    font = dict(family = self.chart_text_font,
                                                size = self.chart_text_size,
                                                color = self.chart_text_colour
                                               ),
                                    x = self.x_3,
                                    y = self.y_3,
                                    #xref = 'paper',
                                    #yref = 'paper',
                                    showarrow = False
                                   )
                              )
            
        shapes = []
        
        if self.square_1 == True:
            shapes.append(dict(type = 'rect',
                              layer = 'below',
                              x0 = self.x_min_1,
                              x1 = self.x_max_1,
                              y0 = self.y_min_1,
                              y1 = self.y_max_1,
                              opacity = self.square_1_opacity,
                              fillcolor = self.square_1_colour,
                              line = dict(width = 0)
                              )
                         )
            
        if self.square_2 == True:
            shapes.append(dict(type = 'rect',
                              layer = 'below',
                              x0 = self.x_min_2,
                              x1 = self.x_max_2,
                              y0 = self.y_min_2,
                              y1 = self.y_max_2,
                              opacity = self.square_2_opacity,
                              fillcolor = self.square_2_colour,
                              line = dict(width = 0)
                              )
                         )
        # create layout
        
        layout = go.Layout(title = dict(text = '<b>'+self.chart_title+'</b>',
                                        font = dict(family = self.chart_text_font,
                                                    size = self.chart_text_size + 4,
                                                    color = self.chart_text_colour),
                                        x = 0.5
                                       ),
                           showlegend=True,
                           hovermode = 'x',
                           legend = dict(font = dict(family = self.chart_text_font,
                                                     size = self.chart_text_size,
                                                     color = self.chart_text_colour
                                                    ),
                                         x = legx,
                                         y = legy,
                                         bgcolor = 'rgba(0,0,0,0)'
                                        ),
                           margin = dict(t = self.top_margin,
                                         l = self.left_margin,
                                         b = self.bottom_margin,
                                         r = self.right_margin
                                        ),
                           width = self.plot_width,
                           height = self.plot_height,
                           font = dict(family = self.chart_text_font,
                                       size = self.chart_text_size,
                                       color = self.chart_text_colour
                                      ),
                           paper_bgcolor=bg_rgba,
                           plot_bgcolor='rgba(0,0,0,0)',
                           xaxis = dict(visible = True,
                                        color = self.axes_colour,
                                        title = dict(text = '<b>'+self.x_title+'</b>',
                                                     font = dict(family = self.chart_text_font,
                                                                 size = self.chart_text_size,
                                                                 color = self.chart_text_colour
                                                                )
                                                    ),
                                        #range = None,
                                        ticks = 'outside',
                                        ticklen = 5,
                                        tickwidth = self.axes_thickness,
                                        tickcolor = self.axes_colour,
                                        tickfont = dict(family = self.chart_text_font,
                                                        size = self.chart_text_size,
                                                        color = self.chart_text_colour
                                                       ),
                                        tickangle = xtickangle,
                                        showline = True,
                                        linecolor = self.axes_colour,
                                        linewidth = self.axes_thickness,
                                        showgrid = False,
                                        zeroline = False,
                                       ),
                           yaxis = dict(visible = True,
                                        color = self.axes_colour,
                                        title = dict(text = '<b>'+self.y_title+'</b>',
                                                     font = dict(family = self.chart_text_font,
                                                                 size = self.chart_text_size,
                                                                 color = self.chart_text_colour
                                                                )
                                                    ),
                                        range = [ymin,ymax],
                                        rangemode = 'tozero',
                                        ticks = 'outside',
                                        ticklen = 5,
                                        tickwidth = self.axes_thickness,
                                        tickcolor = self.axes_colour,
                                        tickfont = dict(family = self.chart_text_font,
                                                        size = self.chart_text_size,
                                                        color = self.chart_text_colour
                                                       ),
                                        showline = True,
                                        linecolor = self.axes_colour,
                                        linewidth = self.axes_thickness,
                                        showgrid = self.y_grid_lines,
                                        gridcolor = 'grey',
                                        zeroline = self.y_zeroline,
                                        zerolinecolor = 'grey',
                                        zerolinewidth = 1
                                       ),
                           barmode = self.bar_mode,
                           annotations = annotations,
                           shapes = shapes
                          )
        
        # create figure
        self.figure = go.Figure(data=data, layout = layout)
            
        return self.figure
    
    @param.depends('export_plot', watch = True)
    def export_plots(self):
        if self.figure != None:
            if self.png == True:
                self.figure.write_image(self.export_to_file + ".png", scale = 4)
            if self.svg == True:
                self.figure.write_image(self.export_to_file + ".svg")
            if self.pdf == True:
                self.figure.write_image(self.export_to_file + ".pdf")
            if self.json == True:
                self.figure.write_json(self.export_to_file + ".json")
            if self.html == True:
                self.figure.write_html(self.export_to_file + ".html")
                
# create instance of ChartStudio class
app = ChartStudio()

# Create tab for imprting data, call process_file method on start up to load first csv in list and create app.data
import_tab = pn.Column(app.param.data_file, app.process_file)

type_tab = pn.Column(app.param.chart_type,
                     app.param.bar_mode,
                     pn.pane.HTML('<p><b>Note:</b> "Bar mode" only for "Bar" chart type.</p>')
                    )

# create chart editor tabs
general_tab = pn.Column(pn.pane.HTML('<b>General:</b>'),
                        app.param.chart_background_colour,
                        app.param.chart_background_opacity,
                        app.param.chart_text_font,
                        app.param.chart_text_size,
                        app.param.chart_text_colour,
                        app.param.chart_title,                       
                        pn.pane.HTML('<b>Sizing:</b>'),
                        app.param.plot_width,
                        app.param.plot_height,
                        app.param.top_margin,
                        app.param.bottom_margin,
                        app.param.left_margin,
                        app.param.right_margin
                       )

axes_tab = pn.Column(pn.pane.HTML('<b>General:</b>'),
                     app.param.axes_colour,
                     app.param.axes_thickness,
                     pn.pane.HTML('<b>Text:</b>'),
                     app.param.x_title,
                     app.param.y_title,
                     pn.pane.HTML('<b>Range:</b>'),
                     app.param.y_autorange,
                     app.param.y_min,
                     app.param.y_max,
                     pn.pane.HTML('<b>Other:</b>'),
                     app.param.y_grid_lines,
                     app.param.y_zeroline,
                     app.param.auto_x_tick_angle,
                     app.param.x_tick_angle
                    )

leg_tab = pn.Column(app.param.auto_position_legend,
                   app.param.legend_x,
                   app.param.legend_y)
    
style_tab = pn.Tabs(('General', general_tab),
                   ('Axes', axes_tab),
                   ('Legend', leg_tab))

text_tab = pn.Column(app.param.annotation_1,
                     app.param.text_1,
                     app.param.x_1,
                     app.param.y_1,
                     app.param.annotation_2,
                     app.param.text_2,
                     app.param.x_2,
                     app.param.y_2,
                     app.param.annotation_3,
                     app.param.text_3,
                     app.param.x_3,
                     app.param.y_3,
                    )

shapes_tab = pn.Column(app.param.square_1,
                      app.param.square_1_colour,
                      app.param.square_1_opacity,
                      app.param.x_min_1,
                       app.param.x_max_1,
                       app.param.y_min_1,
                       app.param.y_max_1,
                       app.param.square_2,
                      app.param.square_2_colour,
                      app.param.square_2_opacity,
                      app.param.x_min_2,
                       app.param.x_max_2,
                       app.param.y_min_2,
                       app.param.y_max_2
                      )
                       
anno_tab = pn.Tabs(('Text', text_tab),
                  ('Shapes', shapes_tab)) 

editor_tab = pn.Tabs(('Type', type_tab),
                     ('Style', style_tab),
                    ('Annotate', anno_tab))

# create chart export tab
export_tab= pn.Column(app.param.export_to_file,
                      app.param.png,
                      app.param.svg,
                      app.param.pdf,
                      app.param.html,
                      app.param.json,
                      app.param.export_plot,
                      pn.pane.HTML("<b>Exporting may take a few minutes when first used in session. Please be patient and check the destination folder.")
                     )

widgets = pn.Tabs(('Import data', import_tab),
                     ('Chart editor', editor_tab),
                     ('Export chart', export_tab))

display = pn.Tabs(('Chart view', app.plot),
                 ('Data view', app.show_data)
                 )

studio = pn.Row(widgets, display)

pn.Column('# Plotly chart creator v. 0.1',
         studio).servable()