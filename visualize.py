from bokeh.plotting import figure, output_file, show
from bokeh.layouts import column
from bokeh.models import Band, ColumnDataSource

#Produce graphs representing the ideal functions.
#Inputs to the function : ideal functions as a list 
#output is in  html format 
#Generate a customized chart that includes a scatter plot for the training function and a line plot for the ideal function.
#Inputs : training function, ideal function, deviation sqaured)
def generate_chart(ideal_funcs, output_filename):
    
    ideal_funcs.sort(key=lambda id_fnc: id_fnc.tr_func.name, reverse=False)
    chart_data = []
    for id_fnc in ideal_funcs:
        #p = create_custom_chart(line_func=id_fnc, scatter_func=id_fnc.tr_func, deviation_sqaured=id_fnc.error)
        
        scatter_dataframe = id_fnc.tr_func.dataframe
        line_dataframe = id_fnc.dataframe
        
        scatter_name = id_fnc.tr_func.name  
        line_name = id_fnc.name

        deviation_sqaured = round(id_fnc.error, 2)
        p = figure(title="Training Model {} vs Ideal Function {}.  deviation_sqaured = {}".format(scatter_name, line_name, deviation_sqaured),
                   x_axis_label='x', y_axis_label='y')
        p.scatter(scatter_dataframe["x"], scatter_dataframe["y"], fill_color="green", legend_label="Training_function")
        p.line(line_dataframe["x"], line_dataframe["y"], legend_label="Ideal_function", line_width=2)
        
        chart_data.append(p)
    output_file("{}.html".format(output_filename))
    show(column(*chart_data))

#Visualize all points that have a corresponding classification

def plot_matched_points(points_data, output_filename):
    
    plot_charts = []
    for index, i in enumerate(points_data):
        if i["category"] is not None:
            plot = classify_plot(i["pnt"], i["category"])
            plot_charts.append(plot)
    output_file("{}.html".format(output_filename))
    show(column(*plot_charts))


#Plot the classification function along with a data point overlay, and visualize the threshold
def classify_plot(pnt, id_fnc):

    if id_fnc is not None:
        classify_df = id_fnc.dataframe

        point_str = "({},{})".format(pnt["x"], round(pnt["y"], 2))
        title = "Point {} with Classification: {}".format(point_str, id_fnc.name)

        p = figure(title=title, x_axis_label='x', y_axis_label='y')

        # Draw the classification function
        p.line(classify_df["x"], classify_df["y"],
                legend_label="Classification Function", line_width=2, line_color='black')

        # generates a plot that visualizes the classification function, the threshold range, and a test point for an ideal function provided
        criterion = id_fnc.threshold
        classify_df['upper'] = classify_df['y'] + criterion
        classify_df['lower'] = classify_df['y'] - criterion

        source = ColumnDataSource(classify_df.reset_index())

        band = Band(base='x', lower='lower', upper='upper', source=source, level='underlay',
                    fill_alpha=0.5, line_width=2, line_color='green', fill_color="yellow")

        p.add_layout(band)

        # Draw the point
        p.scatter([pnt["x"]], [round(pnt["y"], 4)], fill_color="yellow", legend_label="Test Point", size=7)

        return p
