# import dependencies
import pandas as pd
import numpy as np
from plotly.io import write_image, write_html, write_json
import plotly.graph_objs as go
import panel as pn
import param 
from itertools import cycle
from io import StringIO
pn.extension('plotly')

# create chart studio class
# create chart studio class
class ChartStudio(param.Parameterized):
    
    # create param objects for all possible widgets in the app
    
    # import tab
    data_file = param.FileSelector(path='*.csv')
    use_layout_file = param.Boolean(default = False)
    layout_file = param.FileSelector(path='*.cslayout')

    # chart editor tab 
    
    # type tab widgets
    chart_type = param.ObjectSelector(default="Scatter", objects=["Scatter", "Bar"])
    bar_mode = param.ObjectSelector(default="group", objects=["group", "stack", "relative", "overlay"])
    scatter_mode = param.ObjectSelector(default = "lines+markers", objects = ["lines+markers","lines","markers"])
    
    # trace tab widgets
    
    trace_to_edit = param.ObjectSelector(default=None, objects=None)
    
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
    y_min = param.Number(default = 0)
    y_max = param.Number(default = 0)
    x_autorange = param.Boolean(default = True)
    x_min = param.Number(default = 0)
    x_max = param.Number(default = 0)
    y_grid_lines = param.Boolean(default = False)
    y_zeroline = param.Boolean(default = False)
    auto_x_tick_angle = param.Boolean(default = True)
    x_tick_angle = param.Number(default= 0)
    
    # legend tab widgets
    
    auto_position_legend = param.Boolean(default = True)
    legend_x = param.Number(default = 1)
    legend_y = param.Number(default = 1)
    
    # annotate tab widgets
    
    # text annotations widgets
    show_footnote = param.Boolean(default = False)
    footnote_text = param.String(default= '<i>Footnote:</i>')
    y_footnote = param.Number(default = -0.1)
    
    show_annotation_1 = param.Boolean(default = False)
    text_1 = param.String(default= 'Annotation 1')
    x_1 = param.Number(default = 0)
    y_1 = param.Number(default = 0)
    
    show_annotation_2 = param.Boolean(default = False)
    text_2 = param.String(default= 'Annotation 2')
    x_2 = param.Number(default = 0)
    y_2 = param.Number(default = 0)
    
    show_annotation_3 = param.Boolean(default = False)
    text_3 = param.String(default= 'Annotation 3')
    x_3 = param.Number(default = 0)
    y_3 = param.Number(default = 0)
    
    # shape annotation widgets
    
    show_shape_1 = param.Boolean(default = False)
    shape_1_type = param.ObjectSelector(default = "rect", objects = ["rect","circle","line"])
    shape_1_colour = param.Color(default='#0000ff')
    shape_1_opacity = param.Number(0.5, bounds=(0.0, 1.0))
    shape_1_line_style = param.ObjectSelector(default = "solid", objects = ["solid", "dot", "dash", "longdash", "dashdot", "longdashdot"])
    shape_1_line_width = param.Integer(default = 0)
    x_min_1 = param.Number(default = 0)
    x_max_1 = param.Number(default = 0)
    y_min_1 = param.Number(default = 0)
    y_max_1 = param.Number(default = 0)
    
    show_shape_2 = param.Boolean(default = False)
    shape_2_type = param.ObjectSelector(default = "rect", objects = ["rect","circle","line"])
    shape_2_colour = param.Color(default='#00ff00')
    shape_2_opacity = param.Number(0.5, bounds=(0.0, 1.0))
    shape_2_line_style = param.ObjectSelector(default = "solid", objects = ["solid", "dot", "dash", "longdash", "dashdot", "longdashdot"])
    shape_2_line_width = param.Integer(default = 0)
    x_min_2 = param.Number(default = 0)
    x_max_2 = param.Number(default = 0)
    y_min_2 = param.Number(default = 0)
    y_max_2 = param.Number(default = 0)
    
    show_shape_3 = param.Boolean(default = False)
    shape_3_type = param.ObjectSelector(default = "rect", objects = ["rect","circle","line"])
    shape_3_colour = param.Color(default='#ff0000')
    shape_3_opacity = param.Number(0.5, bounds=(0.0, 1.0))
    shape_3_line_style = param.ObjectSelector(default = "solid", objects = ["solid", "dot", "dash", "longdash", "dashdot", "longdashdot"])
    shape_3_line_width = param.Integer(default = 0)
    x_min_3 = param.Number(default = 0)
    x_max_3 = param.Number(default = 0)
    y_min_3 = param.Number(default = 0)
    y_max_3 = param.Number(default = 0)
    
    # export chart tab
    export_to_file = param.String(default= r"Figure_1", doc="Declare name for exported plot file")
    png = param.Boolean(default =False)
    svg = param.Boolean(default =False)
    pdf = param.Boolean(default =False)
    html = param.Boolean(default =False)
    json = param.Boolean(default =False)
    cslayout = param.Boolean(default =False)
    export = param.Action(lambda x: x.param.trigger('export'))
    
    data = None
    figure = None    
    update_plot = True
    
    #dataframe  = param.DataFrame(pd.util.testing.makeDataFrame().iloc[:3])
    
    @param.depends('data_file', watch=True) 
    def process_file(self):
        self.data = pd.read_csv(self.data_file)
        self.data_cols = list(self.data.columns)
        self.xdata = self.data_cols[0]
        self.x_title = self.xdata
        self.trace_names = self.data_cols[1:]
    
    # method for reading in data if using the customised filebrowser panel widget
    #@param.depends('data_file', watch=True) 
    #def process_file(self):    
    #    data = StringIO(str(self.data_file,'utf-8')) 
    #    self.data = pd.read_csv(data)
    #    self.data_cols = list(self.data.columns)
    #    self.xdata = self.data_cols[0]
    #    self.x_title = self.xdata
    #    self.trace_names = self.data_cols[1:]
    
    def show_data(self):
        return self.data
    
    @param.depends('layout_file','use_layout_file', watch=True) 
    def import_cslayout(self):
        if self.use_layout_file == True:
            self.update_plot = False
            read_layout = pd.read_csv(self.layout_file)
            for attribute in read_layout.Attribute.unique():
                if attribute == read_layout.Attribute.unique()[-1]:
                    self.update_plot = True
                dtype = read_layout[read_layout.Attribute == attribute].Type.values[0].replace("<class '",'').replace("'>",'')
                value = read_layout[read_layout.Attribute == attribute].Value.values[0]
                
                if dtype == 'int':
                    setattr(self, attribute, int(value))
                elif dtype == 'float':
                    setattr(self, attribute, float(value))
                elif dtype == 'bool':
                    if value == 'True':
                        setattr(self, attribute, True)
                    elif value == 'False':
                        setattr(self, attribute, False)
                elif dtype == 'str':
                    if str(value) == 'nan':
                        setattr(self, attribute, '')
                    else: 
                        setattr(self, attribute, value)    
        
    # function to export .cslayout file which contains param object names and values at time of export
    def export_cslayout(self):
        params = list(self.param.objects().keys())
        params_df = []
        # ignore name and export_plot params i.e. start at 1 and end at peniltimate param
        for i in range(len(params)):
            if params[i] not in ['name','data_file','use_layout_file','layout_file',
                                 'export_to_file','png','svg','pdf','html','json',
                                 'cslayout','export','trace_to_edit']:
                params_df.append([params[i], 
                                  getattr(self, list(self.param.objects().keys())[i]),
                                 type(getattr(self, list(self.param.objects().keys())[i]))
                                 ]) 
        # create dataframe and write out csv containing test layout parameters
        params_df = pd.DataFrame(params_df, columns = ['Attribute','Value','Type'])
        params_df.to_csv(f'{self.export_to_file}.cslayout', index = False)
        
    @param.depends('data_file', 'layout_file', 'use_layout_file',
                   'chart_type', 'bar_mode', 'scatter_mode',
                   'chart_background_colour', 'chart_background_opacity', 'chart_text_font', 'chart_text_size', 'chart_text_colour', 'chart_title',
                   'plot_width', 'plot_height', 'top_margin', 'bottom_margin', 'left_margin', 'right_margin',
                   'axes_colour', 'axes_thickness', 'x_title', 'y_title', 'y_autorange', 'y_min', 'y_max','x_autorange', 'x_min', 'x_max',
                   'y_grid_lines','y_zeroline',
                   'auto_x_tick_angle', 'x_tick_angle',
                   'auto_position_legend','legend_x','legend_y',
                   'show_footnote', 'footnote_text','y_footnote',
                   'show_annotation_1', 'text_1', 'x_1', 'y_1',
                   'show_annotation_2', 'text_2', 'x_2', 'y_2',
                   'show_annotation_3', 'text_3', 'x_3', 'y_3',
                   'show_shape_1', 'shape_1_type','shape_1_colour', 'shape_1_opacity', 'shape_1_line_style', 'shape_1_line_width', 'x_min_1', 'x_max_1', 'y_min_1', 'y_max_1',
                   'show_shape_2', 'shape_2_type','shape_2_colour', 'shape_2_opacity', 'shape_2_line_style', 'shape_2_line_width', 'x_min_2', 'x_max_2', 'y_min_2', 'y_max_2',
                   'show_shape_3', 'shape_3_type','shape_3_colour', 'shape_3_opacity', 'shape_3_line_style', 'shape_3_line_width', 'x_min_3', 'x_max_3', 'y_min_3', 'y_max_3'
                  ) # all plot widgets I think
    def plot(self):
        if self.update_plot == True:
            
            colours = cycle(['#3b064d','#8105d8','#ed0cef','#fe59d7'])
            
            # create traces
            data = []
            for i in range(0, len(self.trace_names)):

                colour = next(colours)

                if self.chart_type == 'Scatter':
                    data.append(go.Scatter(x = self.data[self.xdata],
                                           y = self.data[self.trace_names[i]],
                                           name = self.trace_names[i],
                                           mode = self.scatter_mode,
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
            
            self.param.trace_to_edit.objects = self.trace_names
            self.trace_to_edit = self.trace_names[0]
            
            # set values for items with both tickboxes and value boxes
            if self.y_autorange == True:
                ymin = None
                ymax = None
            else:
                ymin = self.y_min
                ymax = self.y_max
            if self.x_autorange == True:
                xmin = None
                xmax = None
            else:
                xmin = self.x_min
                xmax = self.x_max
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
            
            if self.show_footnote == True:
                annotations.append(dict(text = self.footnote_text,
                                        font = dict(family = self.chart_text_font,
                                                    size = self.chart_text_size - 2,
                                                    color = self.chart_text_colour
                                                   ),
                                        xanchor = 'right',
                                        yref = 'paper',
                                        xref = 'paper',
                                        x = 1.0,
                                        y = self.y_footnote,
                                        align = 'right',
                                        showarrow = False
                                       )
                                  )

            if self.show_annotation_1 == True:
                annotations.append(dict(text = self.text_1,
                                        font = dict(family = self.chart_text_font,
                                                    size = self.chart_text_size,
                                                    color = self.chart_text_colour
                                                   ),
                                        x = self.x_1,
                                        y = self.y_1,
                                        showarrow = False
                                       )
                                  )

            if self.show_annotation_2 == True:
                annotations.append(dict(text = self.text_2,
                                        font = dict(family = self.chart_text_font,
                                                    size = self.chart_text_size,
                                                    color = self.chart_text_colour
                                                   ),
                                        x = self.x_2,
                                        y = self.y_2,
                                        showarrow = False
                                       )
                                  )

            if self.show_annotation_3 == True:
                annotations.append(dict(text = self.text_3,
                                        font = dict(family = self.chart_text_font,
                                                    size = self.chart_text_size,
                                                    color = self.chart_text_colour
                                                   ),
                                        x = self.x_3,
                                        y = self.y_3,
                                        showarrow = False
                                       )
                                  )

            shapes = []

            if self.show_shape_1 == True:
                shapes.append(dict(type = self.shape_1_type,
                                  layer = 'below',
                                  x0 = self.x_min_1,
                                  x1 = self.x_max_1,
                                  y0 = self.y_min_1,
                                  y1 = self.y_max_1,
                                  opacity = self.shape_1_opacity,
                                  fillcolor = self.shape_1_colour,
                                  line = dict(color = self.shape_1_colour,
                                              width = self.shape_1_line_width,
                                              dash = self.shape_1_line_style)
                                  )
                             )

            if self.show_shape_2 == True:
                shapes.append(dict(type = self.shape_2_type,
                                  layer = 'below',
                                  x0 = self.x_min_2,
                                  x1 = self.x_max_2,
                                  y0 = self.y_min_2,
                                  y1 = self.y_max_2,
                                  line = dict(color = self.shape_2_colour,
                                              width = self.shape_2_line_width,
                                              dash = self.shape_2_line_style)
                                  )
                             )
                
            if self.show_shape_3 == True:
                shapes.append(dict(type = self.shape_3_type,
                                  layer = 'below',
                                  x0 = self.x_min_3,
                                  x1 = self.x_max_3,
                                  y0 = self.y_min_3,
                                  y1 = self.y_max_3,
                                  opacity = self.shape_3_opacity,
                                  fillcolor = self.shape_3_colour,
                                  line = dict(color = self.shape_3_colour,
                                              width = self.shape_3_line_width,
                                              dash = self.shape_3_line_style)
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
                                            range = [xmin, xmax],
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
    
    @param.depends('export', watch = True)
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
            if self.cslayout == True:
                self.export_cslayout()
                
# import custom styles
pn.extension(css_files=["styles.css"])
height = 600
# create instance of ChartStudio class
app = ChartStudio()

# Create tab for imprting data, call process_file method on start up to load first csv in list and create app.data
import_tab = pn.Column(pn.pane.HTML('''<h3>
                                            New chart:
                                        </h3> 
                                       <p>
                                           Please choose a .csv containing your data from the dropdown menu.<br>
                                       <b>Note:</b> This menu only shows .csv files present in the folder from which the chart studio was launched.
                                       </p>'''
                                   ),
                        app.param.data_file, 
                        #pn.Param(app.param['data_file'],widgets={'data_file2': pn.widgets.FileInput}), # testing fiel browser
                        pn.pane.HTML('''<h3>
                                            Import chart layout:
                                        </h3> 
                                       <p>
                                          Select 'Use layout file' and choose a .cslayout file from the dropdown menu.<br>
                                       <b>Note:</b> This menu only shows .cslayout files present in the folder from which the chart studio was launched.
                                       </p>'''
                                   ),
                       app.param.use_layout_file,
                       app.param.layout_file,
                       app.process_file,
                      css_classes=['widget-box'], height=height)

type_tab = pn.Column(app.param.chart_type,
                     app.param.bar_mode,
                     app.param.scatter_mode,
                     pn.pane.HTML('<p><b>Note:</b> "Bar mode" only for "Bar" chart type. "Scatter mode" only for "Scatter" chart type.</p>'),
                     css_classes=['widget-box'], height = height - 30
                    )

trace_tab = pn.Column(app.param.trace_to_edit,
                      pn.pane.HTML('<b>TBC</b>'),
                     css_classes=['widget-box'], height = height - 30
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
                        app.param.right_margin,
                        css_classes=['widget-box'], height=height - 2*30
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
                     app.param.x_autorange,
                     app.param.x_min,
                     app.param.x_max,
                     pn.pane.HTML('<b>Other:</b>'),
                     app.param.y_grid_lines,
                     app.param.y_zeroline,
                     app.param.auto_x_tick_angle,
                     app.param.x_tick_angle,
                     css_classes=['widget-box'], height=height- 2*30
                    )

leg_tab = pn.Column(app.param.auto_position_legend,
                   app.param.legend_x,
                   app.param.legend_y,
                   css_classes=['widget-box'], height=height- 2*30)
    
style_tab = pn.Tabs(('General', general_tab),
                   ('Axes', axes_tab),
                   ('Legend', leg_tab))

text_tab = pn.Column(pn.pane.HTML('<b>Footnote:</b>'),
                     app.param.show_footnote,
                     app.param.footnote_text,
                     app.param.y_footnote,
                     pn.pane.HTML('<b>Annotation 1:</b>'),
                     app.param.show_annotation_1,
                     app.param.text_1,
                     app.param.x_1,
                     app.param.y_1,
                     pn.pane.HTML('<b>Annotation 2:</b>'),
                     app.param.show_annotation_2,
                     app.param.text_2,
                     app.param.x_2,
                     app.param.y_2,
                     pn.pane.HTML('<b>Annotation 3:</b>'),
                     app.param.show_annotation_3,
                     app.param.text_3,
                     app.param.x_3,
                     app.param.y_3,
                     css_classes=['widget-box'], height=height- 2*30
                    )

shapes_tab = pn.Column(pn.pane.HTML('<b>Shape 1:</b>'),
                       app.param.show_shape_1,
                       app.param.shape_1_type,
                      app.param.shape_1_colour,
                      app.param.shape_1_opacity,
                      app.param.shape_1_line_style,
                      app.param.shape_1_line_width,
                       app.param.x_min_1,
                       app.param.x_max_1,
                       app.param.y_min_1,
                       app.param.y_max_1,
                       pn.pane.HTML('<b>Shape 2:</b>'),
                       app.param.show_shape_2,
                       app.param.shape_2_type,
                      app.param.shape_2_colour,
                      app.param.shape_2_opacity,
                      app.param.shape_2_line_style,
                      app.param.shape_2_line_width,
                      app.param.x_min_2,
                       app.param.x_max_2,
                       app.param.y_min_2,
                       app.param.y_max_2,
                       pn.pane.HTML('<b>Shape 3:</b>'),
                       app.param.show_shape_3,
                       app.param.shape_3_type,
                      app.param.shape_3_colour,
                      app.param.shape_3_opacity,
                      app.param.shape_3_line_style,
                      app.param.shape_3_line_width,
                      app.param.x_min_3,
                       app.param.x_max_3,
                       app.param.y_min_3,
                       app.param.y_max_3,
                       css_classes=['widget-box'], height=height- 2*30
                      )
                       
anno_tab = pn.Tabs(('Text', text_tab),
                  ('Shapes', shapes_tab)) 

editor_tab = pn.Tabs(('Type', type_tab),
                     ('Traces', trace_tab),
                     ('Style', style_tab),
                    ('Annotate', anno_tab))

# create chart export tab
export_tab= pn.Column(app.param.export_to_file,
                      pn.pane.HTML('<p>Select formats to create in export:</p>'),
                      app.param.png,
                      app.param.svg,
                      app.param.pdf,
                      app.param.html,
                      app.param.json,
                      pn.pane.HTML('<p>Select to export chart layout:</p>'),
                      app.param.cslayout,
                      app.param.export,
                      pn.pane.HTML("<b>Exporting may take a few minutes when first used in session. Please be patient and check the destination folder."),
                      css_classes=['widget-box'], height=height
                     )

widgets = pn.Tabs(('Import data', import_tab),
                     ('Chart editor', editor_tab),
                     ('Export chart', export_tab), background = '#F5F5F5'
                 )

table = pn.Column(app.show_data,
                  #app.param.dataframe,
                  css_classes=['data-table'], height=height, width = 650)

display = pn.Tabs(('Chart view', app.plot),
                 ('Data view', table)
                 )

panes = pn.Row(widgets, display)

studio = pn.Column(pn.Row(pn.pane.PNG('logo_pyviz.png', width = 70, height = 70),
                          pn.pane.PNG('logo_panel.png', width = 70, height = 70),
                          pn.pane.PNG('logo_plotly.png', width = 70, height = 70),
                          pn.pane.HTML('<h1>Plotly Chart Studio<h1>')),
                   panes,
                   pn.pane.HTML('<p><b>Last updated:</b> 12 January 2020</p>'))

# set servable method to be called for command line and deployed to heroku
studio.servable()#.show()